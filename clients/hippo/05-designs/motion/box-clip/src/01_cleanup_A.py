#!/usr/bin/env python3
"""Piece A clean-up: paint out car badges, wordmarks and plates in every frame.
Each car is tracked with a chained similarity transform (LK points inside the car box);
patches are ellipses defined on reference frame 60 (0-based index 59) and follow the car.
Out: _work/A_clean/NNN.png (720x1280), _work/A_clean_debug/ sheets with patch outlines.
Run: python3 src/01_cleanup_A.py   (from the box-clip folder)"""
import cv2, numpy as np, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f'{ROOT}/_work/gen/gen02_A_9x16_8s.mp4'
RAW = f'{ROOT}/_work/A_raw'; OUT = f'{ROOT}/_work/A_clean'; DBG = f'{ROOT}/_work/A_clean_debug'
for d in (RAW, OUT, DBG): os.makedirs(d, exist_ok=True)
if not os.path.exists(f'{RAW}/193.png'):
    subprocess.run(['ffmpeg','-v','error','-y','-i',SRC,f'{RAW}/%03d.png'],check=True)
N = 193
frames = [cv2.imread(f'{RAW}/{i:03d}.png') for i in range(1, N+1)]
REF = 59
# car boxes on the reference frame (x0,y0,x1,y1) and patches (cx,cy,rx,ry,mode)
CARS = {
 'sedan': dict(box=(0,360,170,480), patches=[
     (46,428,15,10,'inp'), (48,458,27,16,'inp'), (5,464,12,7,'inp'), (98,465,13,7,'inp')]),
 'small': dict(box=(225,360,440,480), patches=[
     (347,439,16,25,'inp'), (396,432,15,7,'inp'), (292,450,20,7,'inp'), (400,449,14,7,'inp'),
     (346,493,32,18,'inp')]),
 'suv': dict(box=(440,330,720,480), patches=[
     (654,451,17,14,'inp')]),
 # second reference for the small car (frame 172): perspective changes on the walk-up and the first track slides
 'small_late': dict(ref=171, box=(150,0,450,230), patches=[
     (311,52,19,31,'inp'), (389,41,17,8,'inp'), (235,74,24,8,'inp'), (392,72,16,8,'inp'), (313,140,42,25,'inp')]),
 # third reference (frame 184) for the plate during the fast tilt-down
 'small_end': dict(ref=183, box=(140,0,470,80), patches=[(307,6,44,26,'inp')]),
}
def track(box, REF):
    Ms = {REF: np.eye(3)}
    for direction in (1, -1):
        M = np.eye(3); i = REF
        while 0 <= i+direction < N:
            g0 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY); g1 = cv2.cvtColor(frames[i+direction], cv2.COLOR_BGR2GRAY)
            corners = np.array([[box[0],box[1],1],[box[2],box[1],1],[box[2],box[3],1],[box[0],box[3],1]],float) @ M.T
            mask = np.zeros(g0.shape, np.uint8); cv2.fillConvexPoly(mask, corners[:,:2].astype(np.int32), 255)
            p = cv2.goodFeaturesToTrack(g0, 200, 0.01, 4, mask=mask)
            if p is None or len(p) < 6:
                p = cv2.goodFeaturesToTrack(g0, 400, 0.01, 6)   # car nearly out of frame: follow the whole picture
            q, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p, None, winSize=(21,21), maxLevel=3)
            pb, st2, _ = cv2.calcOpticalFlowPyrLK(g1, g0, q, None, winSize=(21,21), maxLevel=3)
            ok = (st.ravel()==1) & (st2.ravel()==1) & (np.linalg.norm((p-pb).reshape(-1,2),axis=1) < 1.0)
            if ok.sum() < 6:
                p = cv2.goodFeaturesToTrack(g0, 400, 0.01, 6)
                q, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p, None, winSize=(31,31), maxLevel=4)
                ok = st.ravel()==1
            A, inl = cv2.estimateAffinePartial2D(p[ok], q[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
            if A is None: A = np.eye(3)[:2]
            M = np.vstack([A,[0,0,1]]) @ M
            i += direction; Ms[i] = M.copy()
    return Ms
tracks = {k: track(v['box'], v.get('ref', REF)) for k, v in CARS.items()}
def ellipse_params(M, cx, cy, rx, ry):
    c = M @ np.array([cx,cy,1.0]); s = np.sqrt(abs(np.linalg.det(M[:2,:2]))); ang = np.degrees(np.arctan2(M[1,0],M[0,0]))
    return (float(c[0]), float(c[1])), (rx*s, ry*s), ang
log = []
for i in range(N):
    f = frames[i]; out = f.copy(); dbg = f.copy()
    inp = np.zeros(f.shape[:2], np.uint8)
    for name, car in CARS.items():
        M = tracks[name].get(i)
        if name == 'small_late' and i < 140: continue
        if name == 'small_end' and i < 177: continue
        if M is None: log.append(f'frame {i+1}: no track for {name}'); continue
        for (cx,cy,rx,ry,mode) in car['patches']:
            c, ax, ang = ellipse_params(M, cx, cy, rx, ry)
            if c[1] < -60 or c[0] < -80 or c[0] > 800: continue
            cv2.ellipse(inp, (int(round(c[0])),int(round(c[1]))), (int(np.ceil(ax[0])),int(np.ceil(ax[1]))), ang, 0, 360, 255, -1)
            cv2.ellipse(dbg, (int(round(c[0])),int(round(c[1]))), (int(np.ceil(ax[0])),int(np.ceil(ax[1]))), ang, 0, 360, (0,255,0), 1)
    # never touch the falling box where it passes in front of a car
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    box = ((hsv[...,1] > 110) & (hsv[...,2] > 110) & ((hsv[...,0] > 140) | (hsv[...,0] < 6) | ((hsv[...,0] > 25) & (hsv[...,0] < 45)))).astype(np.uint8)*255
    box = cv2.morphologyEx(box, cv2.MORPH_OPEN, np.ones((5,5),np.uint8))
    boxd = cv2.dilate(box, np.ones((9,9),np.uint8))
    inp[boxd > 0] = 0
    if inp.any():
        filled = cv2.inpaint(f, inp, 4, cv2.INPAINT_TELEA)
        soft = cv2.GaussianBlur(filled, (0,0), 2.2)
        feather = cv2.GaussianBlur(cv2.dilate(inp, np.ones((5,5),np.uint8)).astype(np.float32)/255, (0,0), 1.5)[...,None]
        feather[boxd > 0] = 0
        out = (f*(1-feather) + soft*feather).round().astype(np.uint8)
    cv2.imwrite(f'{OUT}/{i+1:03d}.png', out); cv2.imwrite(f'{DBG}/{i+1:03d}.png', dbg)
print('\n'.join(log) if log else 'all cars tracked in all frames')
