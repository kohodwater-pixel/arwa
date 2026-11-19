#!/usr/bin/env python3
"""Verification of the built MP4 (measured, not watched). Usage: python3 verify.py <film.mp4> <work-dir>
 - container: size, fps, frame count, duration, streams
 - audio onsets in the MP4 around 1.000 s and 29.600 s (first sample above -40 dBFS after each 80 ms mute)
 - extracts stills from the MP4 itself at the listed times into <work-dir>/mp4
 - visual hits: mean absolute change between the frame before each hit and the hit frame (a landing must show a jump)
 - QR: decoded with OpenCV from three frames of the MP4 at full and half size; pixel-static test on the rendered PNG frames"""
import json, os, subprocess, sys
import numpy as np, cv2
MP4, WORK = sys.argv[1], sys.argv[2]
OUT = os.path.join(WORK, 'mp4'); os.makedirs(OUT, exist_ok=True)
QR = 'https://otlobny.net/HIPPO-franchise-form-final/franchise/index.html'
fails = 0
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
p = json.loads(sh('ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=codec_name,codec_type,width,height,r_frame_rate,nb_read_frames,duration,pix_fmt,sample_rate,channels:format=duration', '-of', 'json', MP4))
for s in p['streams']: print('stream', {k: s[k] for k in s if k in ('codec_type', 'codec_name', 'width', 'height', 'r_frame_rate', 'nb_read_frames', 'duration', 'pix_fmt', 'sample_rate', 'channels')})
print('format duration', p['format']['duration'])
v = [s for s in p['streams'] if s['codec_type'] == 'video'][0]
ok = v['width'] == 1080 and v['height'] == 1920 and v['r_frame_rate'] == '30/1' and v['nb_read_frames'] == '1200' and len(p['streams']) == 2
print('container', 'OK' if ok else 'XX'); fails += 0 if ok else 1

raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', MP4, '-ac', '1', '-ar', '48000', '-f', 's16le', '-'], capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
print('audio samples', len(a), '= %.3f s' % (len(a) / 48000))
for name, lo, exp in (('hook', 0.95, 1.000), ('cta', 29.55, 29.600)):
    seg = np.abs(a[int(lo * 48000):int((lo + 0.3) * 48000)]); idx = np.argmax(seg > 10 ** (-40 / 20)); t = lo + idx / 48000
    ok = abs(t - exp) < 0.012; fails += 0 if ok else 1
    print('audio onset %-5s %.4f s (expected ~%.3f) %s' % (name, t, exp, 'OK' if ok else 'XX'))

cap = cv2.VideoCapture(MP4)
def frame(f):
    cap.set(cv2.CAP_PROP_POS_FRAMES, f); ok, im = cap.read(); assert ok, f; return im
HITS = {'hook 1.000': 30, 'tap1 3.138': 94, 'tap2 3.523': 106, 'tap3 3.907': 117, 'tap4 4.291': 129, 'squish 6.600': 198, 'proof1 7.200': 216, 'proof2 8.500': 255, 'proof3 9.800': 294,
        'heavy 12.500': 375, 'punch 12.86': 386, 'chip1 15.2': 456, 'chip2 16.0': 480, 'chip3 16.8': 504, 'chip4 17.6': 528, 'stack 18.3': 549, 'box 19.400': 582, 'athqal 21.81': 655,
        'cta 29.600': 888, 'end 33.300': 999, 'logo 38.2': 1146}
for name, f in HITS.items():
    b2, b1, h = frame(f - 2).astype(int), frame(f - 1).astype(int), frame(f).astype(int)
    before, jump = np.abs(b1 - b2).mean(), np.abs(h - b1).mean()
    cv2.imwrite(os.path.join(OUT, 'hit_%04d.jpg' % f), np.hstack([frame(f - 1), frame(f), frame(f + 2)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print('hit %-14s frame %4d  change into hit frame %.2f (frame before: %.2f)' % (name, f, jump, before))
for f in (26, 27, 28, 29):
    print('freeze 0.92-1.00: frame %d vs %d change %.3f' % (f, f + 1, np.abs(frame(f + 1).astype(int) - frame(f).astype(int)).mean()))
for f in (885, 886, 887):
    print('freeze 29.52-29.60: frame %d vs %d change %.3f' % (f, f + 1, np.abs(frame(f + 1).astype(int) - frame(f).astype(int)).mean()))

det = cv2.QRCodeDetector()
MENU = 'https://menu-hipoo-qr.vercel.app/'
TILES = {'form': (540, 1070, 1050, 1570, QR), 'menu': (50, 1100, 480, 1530, MENU)}     # crop x0, y0, x1, y1 around each tile
for t in (36.0, 38.4, 39.5):
    im = frame(round(t * 30))
    for name, (x0, y0, x1, y1, want) in TILES.items():
        crop = im[y0:y1, x0:x1]
        for label, img in (('full', crop), ('half', cv2.resize(crop, ((x1 - x0) // 2, (y1 - y0) // 2), interpolation=cv2.INTER_AREA))):
            s, _, _ = det.detectAndDecode(img); ok = s == want; fails += 0 if ok else 1
            print('QR %s from MP4 t=%.1f %s: %s %r' % (name, t, label, 'OK' if ok else 'XX', s))
fr = os.path.join(WORK, 'frames')
if os.path.isdir(fr):
    INNER = {'form': (600, 1124, 980, 1504), 'menu': (96, 1150, 424, 1478)}     # inside each tile, clear of its rounded corners (graphics drift behind the tiles)
    for name, (x0, y0, x1, y1) in INNER.items():
        ref = cv2.imread(os.path.join(fr, 'f_%05d.png' % 1065))[y0:y1, x0:x1]; worst = 0; first = None
        for f in range(1000, 1200):
            d = np.abs(cv2.imread(os.path.join(fr, 'f_%05d.png' % f))[y0:y1, x0:x1].astype(int) - ref.astype(int)).max()
            if d == 0 and first is None: first = f
            if d != 0: first = None
            if f >= 1065: worst = max(worst, d)
        ok = worst == 0; fails += 0 if ok else 1
        print('QR %s tile in the rendered PNG frames: identical from frame %s (%.3f s) to the end; max pixel difference 35.5 s -> end: %d %s' % (name, first, (first or 0) / 30, worst, 'OK' if ok else 'XX'))
print('failures:', fails); sys.exit(1 if fails else 0)
