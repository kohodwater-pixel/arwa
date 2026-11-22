#!/usr/bin/env python3
"""Checks on the FINAL MP4: QR decode at 1080 and 540 wide, QR size, seconds on screen, stills, contact sheet, ffprobe, loudness."""
import cv2, numpy as np, os, subprocess, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MP4 = f'{ROOT}/hippo_box-clip_9x16_ar_v02.mp4'
URL = 'https://otlobny.net/HIPPO-franchise-form-final/franchise/index.html'
FR = f'{ROOT}/_work/frames_v02'; os.makedirs(FR, exist_ok=True)
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
        cv2.imwrite(f'{ROOT}/_work/chk/v02_qr_{t:04.1f}s_{w}w.png', img)
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
stills = {'01_box-in-air_1.27s': 38, '02_impact_1.40s': 42, '03_walk-up_4.50s': 135, '04_join-A_6.93s': 208, '05_join-cut_7.03s': 211,
          '06_join-B_7.13s': 214, '07_card-first_8.07s': 242, '08_lid-opening_8.30s': 249, '09_first-hold_9.10s': 273, '10_hold-settled_10.50s': 315, '11_last_17.47s': len(frames)-1}
tiles = []
for name, i in stills.items():
    cv2.imwrite(f'{FR}/hippo_box-clip_frame_{name}.png', frames[i])
    t = cv2.resize(frames[i], (540, 960), interpolation=cv2.INTER_AREA); cv2.rectangle(t, (0,0), (540,44), (0,0,0), -1)
    cv2.putText(t, name, (8, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2); tiles.append(t)
tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(f'{FR}/hippo_box-clip_contact-sheet_v02.png', np.vstack([np.hstack(tiles[:6]), np.hstack(tiles[6:])]))
print('--- colours on the hold frame (frame 400, 13.33 s), median sRGB sampled from the final MP4 ---')
import importlib.util
spec = importlib.util.spec_from_file_location('r', os.path.join(os.path.dirname(os.path.abspath(__file__)), '03_render_video.py')); R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
n = 400; f = frames[n]; M = R.cam_matrix(n)
quad = cv2.transform(R.CARD_STILL[None], M)[0]
Hc = cv2.getPerspectiveTransform(np.float32([[0,0],[1200,0],[1200,3120],[0,3120]]), quad.astype(np.float32))
def region(x0, y0, x1, y1):
    m = np.zeros(f.shape[:2], np.uint8); p = cv2.perspectiveTransform(np.float32([[[x0,y0],[x1,y0],[x1,y1],[x0,y1]]]), Hc)[0]
    cv2.fillConvexPoly(m, p.astype(np.int32), 255); return m > 0
hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
def rep(name, mask, target=None):
    b, g, r = np.median(f[mask], axis=0); s = np.median(hsv[mask][:,1]) / 2.55
    print(f'{name}: #{int(r):02X}{int(g):02X}{int(b):02X}  (R {r:.0f} G {g:.0f} B {b:.0f}, HSV saturation {s:.0f} %, {int(mask.sum())} px)' + (f'   target {target}' if target else ''))
cardm = region(0, 0, 1200, 3120)
rep('card white (margin beside the proof lines)', region(40, 1560, 140, 1800), '#FFFFFF on the lid white')
rep('lime band (left margin of the band, no text)', region(25, 1000, 95, 1480), '#BBD032')
rep('lime band (right margin of the band)', region(1105, 1000, 1175, 1480), '#BBD032')
rep('logo lime (lime pixels of the hippo drawing)', region(400, 84, 800, 500) & (hsv[...,1] > 70) & (hsv[...,0] > 28) & (hsv[...,0] < 50), 'about #B3DB18 (client logo file)')
rep('pink strip', region(100, 3072, 1100, 3112), '#DA6FA2')
rep('pill black', region(300, 2830, 380, 2960), '#181717')
rep('lid white beside the card', region(1230, 600, 1260, 2400))
rep('generated box: lime tab', (~cardm) & (hsv[...,1] > 140) & (hsv[...,0] > 28) & (hsv[...,0] < 50))
rep('generated box: pink', (~cardm) & (hsv[...,1] > 140) & (hsv[...,0] > 150))
print('--- ffprobe ---')
print(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,profile,width,height,r_frame_rate,avg_frame_rate,pix_fmt,nb_frames,duration,sample_rate,channels,bit_rate:format=duration,size,bit_rate','-of','default=nw=1',MP4],capture_output=True,text=True).stdout)
print('--- loudness (ffmpeg ebur128, peak=true) ---')
r = subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',MP4,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
print(r[r.rfind('Summary:'):])
M = [(float(a), float(b)) for a, b in re.findall(r't:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+)', r)]
mx = max(M, key=lambda v: v[1]); thud = max([m for m in M if 1.3 < m[0] < 2.2], key=lambda v: v[1]); vo = max([m for m in M if m[0] > 8.0], key=lambda v: v[1])
print(f'loudest momentary (400 ms) loudness: {mx[1]} LUFS at {mx[0]:.1f} s; thud: {thud[1]} LUFS at {thud[0]:.1f} s; loudest during the VO: {vo[1]} LUFS at {vo[0]:.1f} s')
