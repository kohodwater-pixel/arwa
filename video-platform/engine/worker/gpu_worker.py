#!/usr/bin/env python3
"""GPU worker agent. Standard library only, so it never conflicts with a model's own dependencies.

It connects OUT to the engine (no inbound port needed), registers what it can run, then loops:
claim a job → build the model's documented command → run it in that model's environment →
upload the video → report. A heartbeat keeps the job lease alive and carries cancellation back.

    ENGINE_WORKER_TOKEN=... python3 gpu_worker.py --config worker.json
    python3 gpu_worker.py --config worker.json --dry-run     # print the commands, run nothing
"""
import argparse, json, os, subprocess, sys, tempfile, threading, time, urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runners import RUNNERS, RunnerError  # noqa: E402


class Engine:
    def __init__(self, url, token):
        self.url, self.token, self.worker_id = url.rstrip("/"), token, None

    def call(self, method, path, body=None, raw=None, headers=None, timeout=60):
        h = {"authorization": f"Bearer {self.token}", **(headers or {})}
        if self.worker_id:
            h["x-worker-id"] = self.worker_id
        data = raw
        if body is not None:
            data, h["content-type"] = json.dumps(body).encode(), "application/json"
        req = urllib.request.Request(self.url + path, data=data, method=method, headers=h)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read()

    def json(self, method, path, body=None):
        status, data = self.call(method, path, body)
        return status, (json.loads(data) if data else None)

    def download(self, path, dest):
        req = urllib.request.Request(self.url + path, headers={"authorization": f"Bearer {self.token}", "x-worker-id": self.worker_id})
        with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
            while chunk := r.read(1 << 20):
                f.write(chunk)

    def upload(self, path, file, headers):
        size = os.path.getsize(file)
        with open(file, "rb") as f:  # a file object with content-length is streamed, not read into memory
            return self.call("PUT", path, raw=f, headers={"content-type": "video/mp4", "content-length": str(size), **headers}, timeout=1800)


def gpu_info():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=10).stdout.strip().splitlines()
        name, mem = [x.strip() for x in out[0].split(",")]
        return name, round(float(mem) / 1024, 1)
    except Exception:
        return None, None


def run_job(engine, job, cfg, work):
    model_cfg = cfg["models"][job["model"]]
    runner = RUNNERS["mock" if cfg.get("mock") else model_cfg.get("runner", job["model"])]
    out = os.path.join(work, f"{job['id']}.mp4")
    image = lora = None
    if job.get("hasImage"):
        image = os.path.join(work, f"{job['id']}.img")
        engine.download(f"/v1/worker/jobs/{job['id']}/image", image)
    if job.get("lora"):
        lora = os.path.join(cfg.get("lora_cache", work), f"{job['lora']['sha256']}.safetensors")
        if not os.path.exists(lora):  # cached by content hash: a version is downloaded once per worker
            engine.download(f"/v1/worker/loras/{job['lora']['sha256']}", lora + ".part")
            os.replace(lora + ".part", lora)
    cmd = runner.build(job["spec"], model_cfg, out, image_path=image, lora_path=None if cfg.get("mock") else lora)
    started = time.time()
    proc = subprocess.Popen(cmd["argv"], cwd=cmd["cwd"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    tail, canceled = [], threading.Event()

    def heartbeat():
        while proc.poll() is None:
            try:
                _, r = engine.json("POST", f"/v1/worker/jobs/{job['id']}/progress", {"stage": "generating"})
                if r and r.get("cancel"):
                    canceled.set(); proc.terminate()
            except Exception:
                pass
            time.sleep(20)

    threading.Thread(target=heartbeat, daemon=True).start()
    for line in proc.stdout:
        tail.append(line.rstrip()); del tail[:-40]
    code = proc.wait()
    if canceled.is_set():
        return
    if code != 0 or not os.path.exists(out) or os.path.getsize(out) < 1000:
        text = "\n".join(tail)[-900:]
        raise RunnerError(f"model command exited {code}: {text}", retryable="out of memory" not in text.lower())
    engine.upload(f"/v1/worker/jobs/{job['id']}/result", out, {"x-gpu-seconds": f"{time.time() - started:.1f}", "x-mock": "1" if cfg.get("mock") else "0"})
    for f in (out, image):
        if f and os.path.exists(f):
            os.remove(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--dry-run", action="store_true", help="print the command each configured model would run and exit")
    ap.add_argument("--once", action="store_true", help="exit when the queue is empty (for tests)")
    args = ap.parse_args()
    cfg = json.load(open(args.config))
    if args.dry_run:
        sample = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_specs.json")))
        for mid, mcfg in cfg["models"].items():
            for spec in sample.get(mid, []):
                try:
                    cmd = RUNNERS[mcfg.get("runner", mid)].build(spec, mcfg, "/work/out.mp4", image_path="/work/in.jpg" if spec["task"] == "i2v" else None)
                    print(f"# {mid} {spec['task']} (cwd {cmd['cwd']})\n" + " ".join(a if " " not in a else repr(a) for a in cmd["argv"]) + "\n")
                except RunnerError as e:
                    print(f"# {mid}: cannot build command: {e}\n")
        return
    token = os.environ.get("ENGINE_WORKER_TOKEN")
    if not token:
        sys.exit("ENGINE_WORKER_TOKEN is not set")
    engine = Engine(cfg["engine_url"], token)
    name, vram = gpu_info()
    if not name and not cfg.get("mock"):
        sys.exit("no NVIDIA GPU found (nvidia-smi failed). Set \"mock\": true only to test the plumbing.")
    work = cfg.get("work_dir") or tempfile.mkdtemp(prefix="engine-worker-")
    os.makedirs(work, exist_ok=True)
    def register():
        engine.worker_id = None
        _, reg = engine.json("POST", "/v1/worker/register", {"name": cfg["name"], "gpu": name or "none (mock)", "vramGb": vram, "region": cfg.get("region", ""), "mock": bool(cfg.get("mock")),
                                                               "models": [{"id": k, "variants": v.get("variants")} for k, v in cfg["models"].items()]})
        engine.worker_id = reg["workerId"]
        print(json.dumps({"event": "registered", **reg, "gpu": name, "vramGb": vram}), flush=True)

    register()
    idle = 0
    while True:
        try:
            status, job = engine.json("POST", "/v1/worker/claim", {})
        except urllib.error.HTTPError as e:
            if e.code == 401:  # the engine no longer knows this worker (its database was reset): register again
                time.sleep(2); register(); continue
            print(json.dumps({"event": "engine_error", "status": e.code}), flush=True); time.sleep(10); continue
        except (urllib.error.URLError, OSError) as e:
            print(json.dumps({"event": "engine_unreachable", "error": str(e)}), flush=True); time.sleep(10); continue
        if status == 204 or not job:
            idle += 1
            if args.once and idle >= 3:
                return
            time.sleep(cfg.get("poll_seconds", 3)); continue
        idle = 0
        print(json.dumps({"event": "job", "id": job["id"], "model": job["model"], "variant": job["variant"]}), flush=True)
        try:
            run_job(engine, job, cfg, work)
        except RunnerError as e:
            engine.json("POST", f"/v1/worker/jobs/{job['id']}/fail", {"error": str(e), "retryable": e.retryable})
        except Exception as e:  # unexpected: report it and keep the worker alive
            engine.json("POST", f"/v1/worker/jobs/{job['id']}/fail", {"error": f"worker error: {e}", "retryable": True})


if __name__ == "__main__":
    main()
