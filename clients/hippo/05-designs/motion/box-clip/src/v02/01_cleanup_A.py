#!/usr/bin/env python3
"""v02 piece A (gen03): the one car is far away and side-on; its grille/badge area is repainted flat
(inpainted from the surrounding bodywork, no blur patch). Tracked with a chained similarity transform.
Out: _work/A3_clean/NNN.png, debug outlines in _work/A3_clean_debug/."""
import cv2, numpy as np, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = f'{ROOT}/_work/gen/gen03_A_9x16_8s.mp4'
RAW = f'{ROOT}/_work/A3_raw'; OUT = f'{ROOT}/_work/A3_clean'; DBG = f'{ROOT}/_work/A3_clean_debug'
for d in (RAW, OUT, DBG): os.makedirs(d, exist_ok=True)
if not os.path.exists(f'{RAW}/193.png'):
    subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,f'{RAW}/%03d.png'],check=True)
N = 193
frames = [cv2.imread(f'{RAW}/{i:03d}.png') for i in range(1, N+1)]
REF = 0
BOX = (425, 115, 700, 260)                 # the white car on frame 1
PATCHES = [(646, 211, 15, 6.5, 'body'),     # grille + badge on the nose (cx, cy, rx, ry, what surrounds it)
           (578, 47, 8, 19, 'wall')]        # small sign with pseudo-lettering on the wall
def track(BOX):
    Ms = {REF: np.eye(3)}; M = np.eye(3)
    for i in range(REF, N-1):
        g0 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(frames[i+1], cv2.COLOR_BGR2GRAY)
        c = np.array([[BOX[0],BOX[1],1],[BOX[2],BOX[1],1],[BOX[2],BOX[3],1],[BOX[0],BOX[3],1]],float) @ M.T
        mask = np.zeros(g0.shape, np.uint8); cv2.fillConvexPoly(mask, c[:,:2].astype(np.int32), 255)
        p = cv2.goodFeaturesToTrack(g0, 200, 0.01, 4, mask=mask)
        if p is None or len(p) < 8: p = cv2.goodFeaturesToTrack(g0, 400, 0.01, 6)
        q, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p, None, winSize=(21,21), maxLevel=3)
        ok = st.ravel() == 1
        A, _ = cv2.estimateAffinePartial2D(p[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
        if A is None: A = np.eye(3)[:2]
        M = np.vstack([A,[0,0,1]]) @ M; Ms[i+1] = M.copy()
    return Ms
Ms_car = track(BOX); Ms_sign = track((555, 15, 605, 80))      # the sign is on the wall, behind the car: own track
for i in range(N):
    f = frames[i]; out = f.copy(); dbg = f.copy()
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    box = ((hsv[...,1] > 120) & (hsv[...,2] > 110) & ((hsv[...,0] > 140) | (hsv[...,0] < 6) | ((hsv[...,0] > 25) & (hsv[...,0] < 45)))).astype(np.uint8)
    boxd = cv2.dilate(box, np.ones((9,9), np.uint8)) > 0          # the falling box may pass in front: never touch pink/lime
    outf = f.astype(np.float32)
    for cx, cy, rx, ry, kind in PATCHES:
        M = Ms_sign[i] if kind == 'wall' else Ms_car[i]
        s = np.sqrt(abs(np.linalg.det(M[:2,:2]))); ang = np.degrees(np.arctan2(M[1,0], M[0,0]))
        c = M @ np.array([cx, cy, 1.0])
        if c[1] < -40 or c[0] > 780: continue
        ax = (int(np.ceil(rx*s)), int(np.ceil(ry*s))); ctr = (int(round(c[0])), int(round(c[1])))
        m = np.zeros(f.shape[:2], np.uint8); cv2.ellipse(m, ctr, ax, ang, 0, 360, 255, -1)
        ring = np.zeros_like(m); cv2.ellipse(ring, ctr, (ax[0]+5, ax[1]+5), ang, 0, 360, 255, -1); ring[m > 0] = 0
        px = f[ring > 0].astype(np.float32)
        if len(px) < 10: continue
        if kind == 'body':                                       # flat repaint in the bodywork colour (bright half of the surround)
            lum = px.mean(axis=1); px = px[lum >= np.percentile(lum, 60)]
        col = np.median(px, axis=0)
        m[boxd] = 0
        a = cv2.GaussianBlur(m.astype(np.float32)/255, (0,0), 1.0)[..., None]
        outf = outf*(1-a) + col*a
        cv2.ellipse(dbg, ctr, ax, ang, 0, 360, (0,255,0), 1)
    out = outf.round().astype(np.uint8)
    cv2.imwrite(f'{OUT}/{i+1:03d}.png', out); cv2.imwrite(f'{DBG}/{i+1:03d}.png', dbg)
print('done')
