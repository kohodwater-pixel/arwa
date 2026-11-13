#!/usr/bin/env python3
"""Copy an HTML file and everything it links to (CSS, fonts, images, scripts)
into one self-contained folder, rewriting the links to local paths.

Used when packaging editable sources for delivery, so a source opens correctly
outside the repository.

After copying, the page is opened in Chromium: font files that the page declares
but never loads are removed together with their @font-face rules, licence texts
(OFL.txt) found beside a collected font are copied in, and an empty assets
folder is removed. The script fails if anything fails to load.

Usage: python3 scripts/collect_html.py <source.html> <output-dir>
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys

URL_IN_CSS = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')
ATTR = re.compile(r'\b(src|href)\s*=\s*(["\'])([^"\']+)\2')

def is_local(ref):
    return not re.match(r'^(?:[a-z][a-z0-9+.-]*:|//|#)', ref, re.I)

def main():
    src = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve()
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    copied, missing = {}, []

    def take(ref, base):
        clean = ref.split("#")[0].split("?")[0]
        target = (base / clean).resolve()
        if not target.is_file():
            missing.append(ref); return None
        if target not in copied:
            name = target.name
            if (assets / name).exists() and (assets / name).read_bytes() != target.read_bytes():
                name = f"{target.stem}-{hashlib.sha1(str(target).encode()).hexdigest()[:6]}{target.suffix}"
            if target.suffix.lower() == ".css":
                css = URL_IN_CSS.sub(lambda m: fix_css(m, target.parent), target.read_text(encoding="utf-8"))
                (assets / name).write_text(css, encoding="utf-8")
            else:
                shutil.copy2(target, assets / name)
            copied[target] = name
        return copied[target]

    def fix_css(m, base):
        ref = m.group(1)
        if not is_local(ref) or ref.startswith("data:"): return m.group(0)
        name = take(ref, base)
        return f'url("{name}")' if name else m.group(0)   # CSS in assets/ -> sibling file

    def fix_inline_css(m):
        ref = m.group(1)
        if not is_local(ref) or ref.startswith("data:"): return m.group(0)
        name = take(ref, src.parent)
        return f'url("assets/{name}")' if name else m.group(0)

    def fix_attr(m):
        attr, q, ref = m.groups()
        if not is_local(ref) or ref.startswith(("data:", "mailto:", "tel:")): return m.group(0)
        name = take(ref, src.parent)
        return f'{attr}={q}assets/{name}{q}' if name else m.group(0)

    html = src.read_text(encoding="utf-8")
    html = ATTR.sub(fix_attr, html)
    html = URL_IN_CSS.sub(fix_inline_css, html)
    dest = out / src.name
    dest.write_text(html, encoding="utf-8")

    # Licence texts that sit beside collected fonts
    for target in list(copied):
        if target.suffix.lower() in (".ttf", ".otf", ".woff", ".woff2"):
            lic = target.parent / "OFL.txt"
            if lic.is_file():
                shutil.copy2(lic, assets / f"OFL_{target.parent.name}.txt")

    # Open the copy and see what it really loads
    probe = """
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage(); const req = [], bad = [];
  p.on('request', r => req.push(r.url())); p.on('requestfailed', r => bad.push(r.url()));
  await p.goto('file://' + process.argv[2]); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  console.log(JSON.stringify({ req, bad })); await b.close(); })();
"""
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".cjs", delete=False) as t:
        t.write(probe)
    r = subprocess.run(["node", t.name, str(dest)], capture_output=True, text=True)
    pathlib.Path(t.name).unlink(missing_ok=True)
    pruned = []
    if r.returncode == 0 and r.stdout.strip():
        seen = json.loads(r.stdout.strip().splitlines()[-1])
        loaded = {pathlib.Path(u.split("?")[0]).name.replace("%5B", "[").replace("%5D", "]").replace("%2C", ",") for u in seen["req"]}
        for f in sorted(assets.iterdir()):
            if f.suffix.lower() in (".ttf", ".otf", ".woff", ".woff2") and f.name not in loaded:
                f.unlink(); pruned.append(f.name)
        if pruned:
            block = re.compile(r"@font-face\s*\{[^}]*\}", re.S)
            def drop(m): return "" if any(n in m.group(0) for n in pruned) else m.group(0)
            for f in [dest] + [a for a in assets.iterdir() if a.suffix.lower() == ".css"]:
                f.write_text(block.sub(drop, f.read_text(encoding="utf-8")), encoding="utf-8")
        if seen["bad"]:
            print("  FAILED TO LOAD:", ", ".join(seen["bad"])); sys.exit(1)
    else:
        print("  note: could not open the copy in Chromium; unused files were not pruned:", r.stderr.strip().splitlines()[-1:] )
    # Licence texts only for font families that are still present
    have_fonts = any(a.suffix.lower() in (".ttf", ".otf", ".woff", ".woff2") for a in assets.iterdir())
    if not have_fonts:
        for a in assets.glob("OFL_*.txt"): a.unlink()
    if not any(assets.iterdir()):
        assets.rmdir()
    print(f"{src.name}: collected into {out} ({len(copied) - len(pruned)} linked files kept, {len(pruned)} unused fonts removed)")
    if missing:
        print("  NOT FOUND:", ", ".join(sorted(set(missing)))); sys.exit(1)

if __name__ == "__main__":
    main()
