#!/usr/bin/env python3
"""Checks on the FINAL MP4: QR decode at 1080 and 540 wide, QR size, seconds on screen, stills, contact sheet, ffprobe, loudness."""
import cv2, numpy as np, os, subprocess, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MP4 = f'{ROOT}/hippo_box-clip_9x16_ar_v01.mp4'
URL = 'https://otlobny.net/HIPPO-franchise-form-final/franchise/index.html'
FR = f'{ROOT}/_work/frames_v01'; os.makedirs(FR, exist_ok=True)
cap = cv2.VideoCapture(MP4); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
print('decoded frames:', len(frames), frames[0].shape)
det = cv2.QRCodeDetector()
def decode(img):
    try: txt, pts, _ = det.detectAndDecode(img)
    except cv2.error: return '', None
    return txt, pts
print('--- QR at three times in the hold, 1080 wide and 540 wide ---')
for t in (10.0, 13.0, 17.0):
    f = frames[int(round(t*30))]
    for w in (1080, 540):
        img = f if w == 1080 else cv2.resize(f, (540, 960), interpolation=cv2.INTER_AREA)
        cv2.imwrite(f'{ROOT}/_work/chk/qr_{t:04.1f}s_{w}w.png', img)
        txt, pts = decode(img)
        size = ''
        if pts is not None and txt:
            p = pts.reshape(4, 2); wq = (np.linalg.norm(p[1]-p[0]) + np.linalg.norm(p[2]-p[3])) / 2
            size = f'code width {wq:.0f} px = {100*wq/w:.1f} % of frame width (37 modules -> {wq/37:.2f} px/module); x {p[:,0].min():.0f}-{p[:,0].max():.0f}, y {p[:,1].min():.0f}-{p[:,1].max():.0f}'
        print(f't={t:>4}s {w:>4}w: {"EXACT MATCH" if txt == URL else "FAIL: " + repr(txt)}  {size}')
print('--- every frame: does the QR decode to the exact URL? ---')
ok_full = [decode(f)[0] == URL for f in frames]
ok_half = [decode(cv2.resize(f, (540, 960), interpolation=cv2.INTER_AREA))[0] == URL for f in frames]
for name, okv in (('1080w', ok_full), ('540w', ok_half)):
    idx = [i for i, v in enumerate(okv) if v]
    if idx:
        miss = [i for i in range(idx[0], len(frames)) if not okv[i]]
        print(f'{name}: first decodable frame {idx[0]} ({idx[0]/30:.2f} s), last {idx[-1]} ({idx[-1]/30:.2f} s), decodable frames {len(idx)} = {len(idx)/30:.2f} s; misses after first: {len(miss)} {miss[:20]}')
    else: print(name, 'never decodes')
stills = {'01_impact_1.40s': 42, '02_after-impact_1.57s': 47, '03_walk-up_4.50s': 135, '04_join-A_6.63s': 199, '05_join-B_6.73s': 202,
          '06_lid-opening_7.90s': 237, '07_first-hold_8.77s': 263, '08_hold-settled_10.00s': 300, '09_last_17.47s': len(frames)-1}
tiles = []
for name, i in stills.items():
    cv2.imwrite(f'{FR}/hippo_box-clip_frame_{name}.png', frames[i])
    t = cv2.resize(frames[i], (540, 960), interpolation=cv2.INTER_AREA); cv2.rectangle(t, (0,0), (540,44), (0,0,0), -1)
    cv2.putText(t, name, (8, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2); tiles.append(t)
tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(f'{FR}/hippo_box-clip_contact-sheet_v01.png', np.vstack([np.hstack(tiles[:5]), np.hstack(tiles[5:])]))
print('--- ffprobe ---')
print(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,profile,width,height,r_frame_rate,avg_frame_rate,pix_fmt,nb_frames,duration,sample_rate,channels,bit_rate:format=duration,size,bit_rate','-of','default=nw=1',MP4],capture_output=True,text=True).stdout)
print('--- loudness (ffmpeg ebur128, peak=true) ---')
r = subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',MP4,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(r[r.rfind('Summary:'):])
M = [(float(a), float(b)) for a, b in re.findall(r't:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)', r)]
mx = max(M, key=lambda v: v[1]); thud = max([m for m in M if 1.3 < m[0] < 2.0], key=lambda v: v[1])
print(f'loudest momentary (400 ms) loudness: {mx[1]} LUFS at {mx[0]:.1f} s; around the thud: {thud[1]} LUFS at {thud[0]:.1f} s')
