#!/usr/bin/env python3
"""Renders the picture (no sound) of the box clip, 1080x1920, 30 fps.
  A  : cleaned + interpolated piece A, head trimmed so the impact is at 1.4 s
  join: vertical whip blur + 2-frame exposure dip
  B  : piece B rotated 90 deg clockwise (hand enters from the bottom), invitation card tracked on the lid
  hold: one still (B frame 70) with asphalt extended below, card pinned, synthetic handheld drift
Run: python3 src/03_render_video.py            -> _work/video_v01_silent.mp4
     python3 src/03_render_video.py 0 42 240   -> only these output frames, as PNG in _work/test/
"""
import cv2, numpy as np, os, subprocess, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
CARD = f'{ROOT}/card/hippo_box-clip_invitation-card_ar_v01.png'
B_SRC = f'{ROOT}/_work/gen/gen02_B_9x16_8s.mp4'
B_RAW = f'{ROOT}/_work/B_raw'
os.makedirs(B_RAW, exist_ok=True)
if not os.path.exists(f'{B_RAW}/193.png'):
    subprocess.run(['ffmpeg','-v','error','-y','-i',B_SRC,f'{B_RAW}/%03d.png'],check=True)

# ---------------- timeline (output frames) ----------------
A_K0 = 38                 # first A_30 frame used: impact (A_30 frame 80) lands on output frame 42 = 1.40 s
N_A = 201                 # output frames 0..200 are piece A (A_30 frames 38..238)
B_F0, B_STILL = 9, 70     # piece B source frames (1-based) used live: 9..70, one per output frame (125 % speed)
N_BLIVE = B_STILL - B_F0 + 1
HOLD0 = N_A + N_BLIVE     # first hold frame (263 = 8.77 s)
TOTAL = 525               # 17.5 s
IMPACT = 42
rng = np.random.default_rng(7)

# ---------------- piece A ----------------
def a_frame(n):
    k = n + A_K0
    if 73 <= k <= 80:    f = cv2.imread(f'{ROOT}/_work/A_clean/{k-16+1:03d}.png')   # the fall: real frames only, never interpolated
    elif k in (71, 72):  f = cv2.imread(f'{ROOT}/_work/A_clean/{56+1:03d}.png')
    else:                f = cv2.imread(f'{ROOT}/_work/A_30/{k:03d}.png')
    s = 1.5 * 1.035       # 3.5 % punch-in leaves room for the jolt
    jolt = {0: 20, 1: -13, 2: 8, 3: -4, 4: 2}.get(n - IMPACT, 0)
    M = np.array([[s, 0, W/2 - s*360], [0, s, H/2 - s*640 + jolt]], np.float32)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

# ---------------- piece B: frames, lid tracking ----------------
def b_rot(f): return cv2.rotate(cv2.imread(f'{B_RAW}/{f:03d}.png'), cv2.ROTATE_90_CLOCKWISE)   # 1280 x 720
HX = 704                  # hinge line (rotated frame), constant
def fit_env(t, v, sign, iters=6):
    t = np.asarray(t, float); v = np.asarray(v, float); keep = np.ones(len(t), bool); a = b = 0
    for _ in range(iters):
        if keep.sum() < 8: break
        a, b = np.polyfit(t[keep], v[keep], 1); r = (v - (a*t + b)) * sign
        keep = (r > -2.0) & (r < 6)
    return a, b
def detect_lid(f, fno):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    w = ((hsv[...,1] < 45) & (hsv[...,2] > 150)).astype(np.uint8); w[:, :HX+3] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(w)
    k = 1 + np.argmax(st[1:,4]); m = lab == k
    ys = np.arange(115, 400 if fno < 62 else 560)
    right = np.array([np.where(m[y])[0].max() if m[y].any() else 0 for y in ys]); ok = right > 0
    a, b = fit_env(ys[ok], right[ok], +1)                       # free edge  x = a*y + b
    xs = np.arange(HX+8, int(a*250 + b) - 8)
    top = np.array([np.where(m[:,x])[0].min() if m[:,x].any() else 9999 for x in xs])
    at, bt = fit_env(xs[top < 9999], top[top < 9999], -1)       # top edge   y = at*x + bt
    yt = (at*b + bt) / (1 - at*a); ft = [a*yt + b, yt]; ht = [HX, at*HX + bt]
    xb = np.arange(HX+5, HX+40)
    bot = np.array([np.where(m[:,x])[0].max() if m[:,x].any() else -1 for x in xb])
    hb_y = float(np.median(bot)) if (bot >= 0).all() and np.median(bot) < 713 else None
    return dict(ht=ht, ft=ft, a=a, hb_y=hb_y)
def track_lid():
    cache = f'{ROOT}/_work/lid_track.json'
    raw = {f: detect_lid(b_rot(f), f) for f in range(43, B_STILL+1)}
    fr = sorted(raw)
    # hinge-side length: measured where the lower corner is inside the frame, else bridged (lid is lifted towards the lens)
    L = np.array([np.nan if raw[f]['hb_y'] is None else raw[f]['hb_y'] - raw[f]['ht'][1] for f in fr])
    idx = np.arange(len(fr)); good = ~np.isnan(L)
    Lf = np.interp(idx, idx[good], L[good])
    bump = np.where(good, 0, 1.0); bump = np.convolve(np.pad(bump, 3, mode='edge'), np.ones(7)/7, 'valid')
    Lf = Lf + 45 * bump * (~good)                                # out-of-frame corner: at least past the frame edge
    quads = []
    for i, f in enumerate(fr):
        d = raw[f]; ht = np.array(d['ht']); ft = np.array(d['ft']); hb = np.array([HX, ht[1] + Lf[i]])
        u = np.array([d['a'], 1.0]); u /= np.linalg.norm(u)
        fb = ft + u * Lf[i] * 1.093                              # free side is 9.3 % longer than the hinge side in the final frame
        quads.append([ht, ft, fb, hb])
    Q = np.array(quads)                                          # (n,4,2)
    # last frames: lower free corner measured directly once the hand has left
    for i, f in enumerate(fr):
        if f >= 66:
            fimg = b_rot(f); hsv = cv2.cvtColor(fimg, cv2.COLOR_BGR2HSV)
            m = ((hsv[...,1] < 45) & (hsv[...,2] > 150)); m[:, :HX+3] = False
            xs = np.arange(int(Q[i,1,0]) - 60, int(Q[i,1,0]) - 8)
            bot = np.array([np.where(m[:,x])[0].max() for x in xs]); ab, bb = np.polyfit(xs, bot, 1)
            a = raw[f]['a']; bfree = Q[i,1,0] - a*Q[i,1,1]
            y = (ab*bfree + bb) / (1 - ab*a); Q[i,2] = [a*y + bfree, y]; Q[i,3] = [HX, ab*HX + bb]
    Qp = np.pad(Q, ((2,2),(0,0),(0,0)), mode='edge')
    Qm = np.array([np.median(Qp[i:i+3+2], axis=0) for i in range(len(fr))])   # 5-tap median
    Qp = np.pad(Qm, ((1,1),(0,0),(0,0)), mode='edge')
    Qs = 0.25*Qp[:-2] + 0.5*Qp[1:-1] + 0.25*Qp[2:]
    out = {f: Qs[i] for i, f in enumerate(fr)}
    json.dump({str(f): out[f].round(2).tolist() for f in fr}, open(cache, 'w'), indent=0)
    return out
LID = track_lid()
UNIT = np.array([[0,0],[1,0],[1,1],[0,1]], np.float32)
# card corners on the still (rotated-frame px): 2.6:1 card, 204 px wide, inside the lid panel (hinge x=704, fold x=916)
CARD_STILL = np.array([[708,120.8],[912,101.75],[912,650.75],[708,633.8]], np.float32)   # TL TR BR BL
H_still = cv2.getPerspectiveTransform(UNIT, LID[B_STILL].astype(np.float32))
CARD_UV = cv2.perspectiveTransform(CARD_STILL[None], np.linalg.inv(H_still))[0]
def card_quad(f):
    Hf = cv2.getPerspectiveTransform(UNIT, LID[f].astype(np.float32))
    return cv2.perspectiveTransform(CARD_UV[None], Hf)[0]

# ---------------- card artwork ----------------
card = cv2.imread(CARD).astype(np.float32) / 255.0             # 1200 x 3120
gray = card.mean(axis=2, keepdims=True)
card = gray + (card - gray) * 0.90                             # pull saturation to sit with the footage
card = 0.075 + 0.925 * card                                    # lift black to the footage's black level
fall = np.linspace(1.0, 0.96, card.shape[0], dtype=np.float32)[:, None, None]
card = card * fall * 1.025                                     # light fall-off; paper a touch brighter than the lid
CH, CW = card.shape[:2]
CARD_PX = np.array([[0,0],[CW,0],[CW,CH],[0,CH]], np.float32)

def composite_card(F, quad_out, occ=None, opacity=1.0):
    """F: float32 BGR frame (any size); quad_out: card corners in F's pixels; occ: 0..1 map of 'this is bare lid' (hand = 0)."""
    h, w = F.shape[:2]
    Hc = cv2.getPerspectiveTransform(CARD_PX, quad_out.astype(np.float32))
    # shrink the card to about the target size first, so the warp does not alias the QR
    tw = np.linalg.norm(quad_out[1] - quad_out[0]); sc = min(1.0, max(0.05, 1.15 * tw / CW))
    small = cv2.resize(card, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
    Hs = Hc @ np.diag([1/sc, 1/sc, 1.0])
    cw = cv2.warpPerspective(small, Hs, (w, h), flags=cv2.INTER_LINEAR, borderValue=(1,1,1))
    cov = cv2.warpPerspective(np.ones(small.shape[:2], np.float32), Hs, (w, h), flags=cv2.INTER_LINEAR)
    px = tw / 480.0                                            # blur and shadow sizes scale with the card
    cw = cv2.GaussianBlur(cw, (0,0), 0.6 * px)
    sh = cv2.GaussianBlur(cov, (0,0), 2.2 * px)
    Ms = np.float32([[1,0,2.0*px],[0,1,2.5*px]])
    sh = cv2.warpAffine(sh, Ms, (w, h)) * (1 - cov)            # contact shadow, lower right, outside the card only
    a = cov * opacity
    if occ is not None: a = a * occ; sh = sh * occ
    out = F * (1 - 0.16 * sh[..., None] * opacity)
    out = out * (1 - a[..., None]) + (out * cw) * a[..., None]
    return out

# ---------------- grade, grain ----------------
GAM = 1 - 0.8 * (1 - np.array([0.709, 0.781, 0.799], np.float32))    # B,G,R: 80 % of the way from B's asphalt to A's
def grade_b(F):                                                # F float32 0..255
    x = np.clip(F / 255.0, 0, 1) ** GAM
    g = x.mean(axis=2, keepdims=True)
    return (g + (x - g) * 0.88) * 255.0
def grain(F, sigma=2.0):
    n = rng.normal(0, sigma, (H//2, W//2)).astype(np.float32)
    n = cv2.resize(n, (W, H), interpolation=cv2.INTER_LINEAR) * 0.7 + rng.normal(0, sigma*0.6, (H, W)).astype(np.float32)
    return F + n[..., None]
def unsharp(F, amount=0.5, sigma=1.4):
    return F + amount * (F - cv2.GaussianBlur(F, (0,0), sigma))

# ---------------- virtual camera for B ----------------
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3 - 2*x)
def shake(t, amp):                                             # smooth handheld wobble, output px
    x = amp * (0.62*np.sin(2*np.pi*0.93*t + 0.4) + 0.38*np.sin(2*np.pi*0.41*t + 2.1))
    y = amp * (0.60*np.sin(2*np.pi*1.07*t + 1.3) + 0.40*np.sin(2*np.pi*0.33*t + 0.2))
    r = 0.26*np.sin(2*np.pi*0.52*t + 0.9) + 0.04*np.sin(2*np.pi*1.3*t)
    return x, y, r
S_LIVE, S_HOLD = 2.75, 480.0/204.0
CY_HOLD = (120.8 + 633.8)/2 + ((H/2) - (150 + 1248/2)) / S_HOLD   # card top lands at y = 150 in the frame
def cam(n):
    """returns scale, centre (src px), and shake (px, px, deg) for B output frame n"""
    t = n / FPS
    if n < HOLD0:
        f = B_F0 + (n - N_A)
        cx = 605 + (790 - 605) * sstep((f - 29) / 17.0) + 20 * sstep((f - 52) / 18.0)
        sx, sy, r = shake(t, 9.0)
        return S_LIVE, cx, 360.0, sx, sy * 0.6, r * 0.5
    e = sstep((n - HOLD0) / 30.0)                              # 1 s settle: phone lifts and centres on the card
    s = S_LIVE + (S_HOLD - S_LIVE) * e
    amp = 9.0 + (5.0 - 9.0) * e
    sx, sy, r = shake(t, amp)
    return s, 810.0, 360.0 + (CY_HOLD - 360.0) * e, sx, sy * (0.6 + 0.4*e), r * (0.5 + 0.5*e)
def cam_matrix(n, ss=1):
    s, cx, cy, sx, sy, r = cam(n)
    M = cv2.getRotationMatrix2D((cx, cy), r, s)                # rotate+scale about the window centre (src px)
    M[0,2] += W/2 - cx + sx; M[1,2] += H/2 - cy + sy
    return M * ss

# ---------------- the still for the hold ----------------
EXT = 190
def build_still():
    f = b_rot(B_STILL).astype(np.float32)
    canvas = np.zeros((720 + EXT, 1280, 3), np.float32); canvas[:720] = f
    # real asphalt from the part of this same frame that is cropped away (left of the box), turned 90 deg
    donor = cv2.rotate(f[:, 0:440], cv2.ROTATE_90_COUNTERCLOCKWISE)          # 440 high x 720 wide
    donor = np.hstack([donor, donor[:, ::-1]])[:, :1280]                    # widen by mirroring; only x 560..1060 is ever seen
    donor = np.roll(donor, 470, axis=1)
    ov = 46
    strip = donor[40:40 + EXT + ov]
    # match low-frequency tone to the rows it joins
    ref = cv2.GaussianBlur(f[720-60:720], (0,0), 25).mean(axis=0, keepdims=True)
    cur = cv2.GaussianBlur(strip, (0,0), 25)
    strip = strip - cur + ref
    canvas[720:] = strip[ov:]
    ramp = np.linspace(0, 1, ov, dtype=np.float32)[:, None, None]
    canvas[720-ov:720] = f[720-ov:720] * (1 - ramp) + strip[:ov] * ramp
    # keep the box itself untouched where the blend zone crosses it (box ends above y=690)
    return np.clip(canvas, 0, 255)
STILL = build_still()
SS = 2
def still_with_card():
    big = cv2.resize(STILL, None, fx=S_HOLD*SS, fy=S_HOLD*SS, interpolation=cv2.INTER_LANCZOS4)
    big = unsharp(np.clip(big, 0, 255), 0.5, 1.4*SS)
    return composite_card(big, CARD_STILL * S_HOLD * SS)
_hold_cache = {}
def hold_frame(n):
    if 'img' not in _hold_cache: _hold_cache['img'] = still_with_card()
    M = cam_matrix(n)                                          # src px -> out px
    k = 1.0 / (S_HOLD * SS)
    M2 = M.copy(); M2[:, :2] *= k                              # hi-res still px -> out px
    out = cv2.warpAffine(_hold_cache['img'], M2, (W, H), flags=cv2.INTER_AREA if False else cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return out
def live_frame(n):
    f = B_F0 + (n - N_A)
    src = b_rot(f).astype(np.float32)
    M = cam_matrix(n)
    F = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    F = unsharp(np.clip(F, 0, 255), 0.5, 1.6)
    if f >= 43:
        hsv = cv2.cvtColor(src.astype(np.uint8), cv2.COLOR_BGR2HSV)
        occ = ((hsv[...,1] < 60) & (hsv[...,2] > 95)).astype(np.float32)
        occ = cv2.erode(occ, np.ones((3,3), np.uint8))
        occ = cv2.GaussianBlur(occ, (0,0), 1.0)
        occ = cv2.warpAffine(occ, M, (W, H), flags=cv2.INTER_LINEAR)
        q = card_quad(f)
        q_out = cv2.transform(q[None], M)[0]
        F = composite_card(F, q_out, occ, opacity={43: 0.45}.get(f, 1.0))
    return F

# ---------------- join ----------------
def vblur(F, length):
    if length < 2: return F
    k = np.zeros((int(length), 1), np.float32); k[:] = 1.0 / int(length)
    return cv2.filter2D(F, -1, k, borderType=cv2.BORDER_REFLECT)
def vshift(F, dy):
    M = np.float32([[1,0,0],[0,1,dy]]); return cv2.warpAffine(F, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
A_BLUR = {N_A-5: 14, N_A-4: 40, N_A-3: 90, N_A-2: 170, N_A-1: 260}
B_BLUR = {N_A: (300, 520, 0.72), N_A+1: (190, 300, 0.86), N_A+2: (100, 150, 1.0), N_A+3: (45, 60, 1.0), N_A+4: (16, 18, 1.0), N_A+5: (5, 4, 1.0)}

def frame(n):
    if n < N_A:
        F = a_frame(n).astype(np.float32)
        if n in A_BLUR: F = vblur(F, A_BLUR[n])
        if n == N_A-1: F = F * 0.86
    else:
        F = live_frame(n) if n < HOLD0 else hold_frame(n)
        F = grade_b(F)
        if n in B_BLUR:
            L, dy, g = B_BLUR[n]; F = vblur(vshift(F, dy), L) * g
    return np.clip(grain(F), 0, 255).astype(np.uint8)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        os.makedirs(f'{ROOT}/_work/test', exist_ok=True)
        for a in sys.argv[1:]:
            cv2.imwrite(f'{ROOT}/_work/test/{int(a):04d}.png', frame(int(a)))
        sys.exit()
    out = f'{ROOT}/_work/video_v01_silent.mp4'
    p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','13','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709', out], stdin=subprocess.PIPE)
    for n in range(TOTAL):
        p.stdin.write(frame(n).tobytes())
        if n % 50 == 0: print('frame', n, flush=True)
    p.stdin.close(); p.wait(); print('wrote', out)
