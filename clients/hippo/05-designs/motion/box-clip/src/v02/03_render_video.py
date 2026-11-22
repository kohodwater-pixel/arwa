#!/usr/bin/env python3
"""v02 picture, 1080x1920, 30 fps.
  A   : gen03, cleaned; pre-fall interpolated at 100 %, fall + wobble as real frames, walk-up interpolated at 115 %;
        push-in over the last frames so the box is as wide in frame as piece B's box
  join: 7+7 frames of vertical whip blur with a 4-frame dissolve inside it and an exposure dip
  B   : gen02 B rotated 90 deg clockwise; graded towards A; soft cast shadow added left of the box;
        card tracked on the lid from the first frame the panel shows (source frame 39), hand matted over it
  hold: box and card from one still (B frame 70); the asphalt around them keeps playing (B frames 70-193, aligned, ping-pong)
Run: python3 src/v02/03_render_video.py            -> _work/video_v02_silent.mp4
     python3 src/v02/03_render_video.py 0 42 240   -> those output frames as PNG in _work/test/
"""
import cv2, numpy as np, os, subprocess, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W, H, FPS = 1080, 1920, 30
CARD = f'{ROOT}/card/hippo_box-clip_invitation-card_ar_v01.png'
B_RAW = f'{ROOT}/_work/B_raw'
os.makedirs(B_RAW, exist_ok=True)
if not os.path.exists(f'{B_RAW}/193.png'):
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{ROOT}/_work/gen/gen02_B_9x16_8s.mp4',f'{B_RAW}/%03d.png'],check=True)

# ---------------- timeline (output frames) ----------------
N_SEG1, RAW0, RAW1 = 34, 27, 44      # out 0..33 = seg1[k]; out 34..51 = source index 27..44 (0-based) as shot
N_A = 211                            # out 52..211 = seg2[k = n-51]  (source index 44 + 0.92 k)
IMPACT = 42                          # source index 35 (frame 36): first ground contact -> 1.40 s
B_F0, B_STILL, B_CARD0 = 9, 70, 39   # piece B source frames (1-based)
N_BLIVE = B_STILL - B_F0 + 1
HOLD0 = N_A + N_BLIVE                # 273 = 9.10 s
TOTAL = 525                          # 17.5 s
rng = np.random.default_rng(7)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3 - 2*x)

# ---------------- piece A ----------------
A_ANCHOR = (372.0, 675.0)            # box centre on the last A frame (source px)
def a_src(n):
    if n < N_SEG1:  return cv2.imread(f'{ROOT}/_work/A3_seg1/{n:03d}.png')
    if n <= 51:     return cv2.imread(f'{ROOT}/_work/A3_clean/{RAW0 + (n - N_SEG1) + 1:03d}.png')
    return cv2.imread(f'{ROOT}/_work/A3_seg2/{min(n - 51, 159):03d}.png')
def a_frame(n):
    f = a_src(n)
    s0 = 1.5 * 1.035
    z = 1 + 0.24 * sstep((n - (N_A - 20)) / 20.0) ** 1.5         # phone drops towards the box at the very end
    s = s0 * z
    ax, ay = A_ANCHOR
    ox = W/2 + (ax - 360) * s0; oy = H/2 + (ay - 640) * s0       # where the anchor sits before the push-in
    jolt = {0: 20, 1: -13, 2: 8, 3: -4, 4: 2}.get(n - IMPACT, 0)
    M = np.array([[s, 0, ox - s*ax], [0, s, oy - s*ay + jolt]], np.float32)
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

# ---------------- piece B: source frames, grade, shadow ----------------
def b_rot(f): return cv2.rotate(cv2.imread(f'{B_RAW}/{f:03d}.png'), cv2.ROTATE_90_CLOCKWISE)   # 1280 x 720
TINT = np.array([0.89, 0.925, 1.0], np.float32)                 # B,G,R on shadows/mids: B's grey asphalt -> A's warm asphalt
def grade_b(F):
    """F float32 BGR 0..255 (piece B, before the card goes on). White point up so the lid reads as sunlit paper,
    asphalt tinted to A, neon pink and lime pulled onto A's values."""
    x = np.clip(F / 255.0, 0, 1)
    y = x * (1 + 0.224 * x * x)
    w = 1 - np.clip(y, 0, 1) ** 1.5
    y = y * (TINT ** w)
    u8 = np.clip(F, 0, 255).astype(np.uint8); hsv = cv2.cvtColor(u8, cv2.COLOR_BGR2HSV)
    pink = ((hsv[...,1] > 168) & (hsv[...,2] > 110) & (hsv[...,0] > 150) & (hsv[...,0] < 179)).astype(np.float32)
    lime = ((hsv[...,1] > 110) & (hsv[...,0] > 28) & (hsv[...,0] < 48)).astype(np.float32)
    pink = cv2.GaussianBlur(pink, (0,0), 1.2)[..., None]; lime = cv2.GaussianBlur(lime, (0,0), 1.2)[..., None]
    y = y * (1 - pink) + y * np.array([0.93, 0.12, 0.98], np.float32) * pink      # (131,34,226)*grade -> about (130,2,235)
    y = y * (1 - lime) + y * np.array([0.10, 0.86, 0.85], np.float32) * lime      # -> about (3,217,187)
    return np.clip(y, 0, 1) * 255.0
SH_X0, SH_X1, SH_Y0, SH_Y1 = 318, 486, 92, 688                   # cast shadow left of the box (rotated-frame px), like A's
def add_shadow(src, ext=0):
    """Darken the asphalt left of the box. src: uint8/float BGR rotated B frame (or extended canvas)."""
    h, w = src.shape[:2]
    m = np.zeros((h, w), np.float32); m[SH_Y0:SH_Y1, SH_X0:SH_X1] = 1.0
    m = cv2.GaussianBlur(m, (0,0), 3.0)
    u8 = np.clip(src, 0, 255).astype(np.uint8); hsv = cv2.cvtColor(u8, cv2.COLOR_BGR2HSV)
    asphalt = ((hsv[...,1] < 75) & (hsv[...,2] < 150)).astype(np.float32)
    asphalt = cv2.GaussianBlur(cv2.erode(asphalt, np.ones((3,3), np.uint8)), (0,0), 1.2)
    k = 1 - 0.50 * m * asphalt
    return src.astype(np.float32) * k[..., None]

# ---------------- lid tracking ----------------
HX = 704
def fit_env(t, v, sign, iters=6):
    t = np.asarray(t, float); v = np.asarray(v, float); keep = np.ones(len(t), bool); a = b = 0
    for _ in range(iters):
        if keep.sum() < 8: break
        a, b = np.polyfit(t[keep], v[keep], 1); r = (v - (a*t + b)) * sign
        keep = (r > -2.0) & (r < 6)
    return a, b
def white_right_of_hinge(f):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    w = ((hsv[...,1] < 45) & (hsv[...,2] > 150)).astype(np.uint8); w[:, :HX+3] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(w)
    if n < 2: return None, hsv
    k = 1 + np.argmax(st[1:,4])
    return (lab == k) if st[k,4] > 600 else None, hsv
def detect_lid(f, fno):
    m, hsv = white_right_of_hinge(f)
    if m is None: return None
    ys = np.arange(125, 320 if fno < 46 else (400 if fno < 62 else 560))
    right = np.array([np.where(m[y])[0].max() if m[y].any() else 0 for y in ys]); ok = right > HX + 6
    if ok.sum() < 40 or np.median(right[ok]) - HX < 80: return None   # a sliver: not measurable, extrapolated instead
    if fno < 47:                                                  # early frames: nothing hides the edge above the thumb; plain robust fit
        yy = ys[ok].astype(float); rr = right[ok].astype(float); keep = np.ones(len(yy), bool)
        for _ in range(4):
            a, b = np.polyfit(yy[keep], rr[keep], 1); keep = np.abs(rr - (a*yy + b)) < 2.5
        b -= 1.5                                                  # stay just inside the antialiased edge
    else:
        a, b = fit_env(ys[ok], right[ok], +1)
    xs = np.arange(HX+6, max(HX+14, int(a*250 + b) - 6))
    top = np.array([np.where(m[:,x])[0].min() if m[:,x].any() else 9999 for x in xs])
    if (top < 9999).sum() < 8: return None
    at, bt = fit_env(xs[top < 9999], top[top < 9999], -1)
    yt = (at*b + bt) / (1 - at*a); ft = [a*yt + b, yt]; ht = [HX, at*HX + bt]
    xb = np.arange(HX+5, HX+40)
    bot = np.array([np.where(m[:,x])[0].max() if m[:,x].any() else -1 for x in xb])
    hb_y = float(np.median(bot)) if (bot >= 0).all() and np.median(bot) < 713 else None
    # is the tuck flap still folded (seen pink, just right of the free edge) or already lying white in the lid's plane?
    pk = 0
    for y in range(150, 300, 10):
        xe = int(a*y + b); seg = hsv[y, xe+3:xe+16]
        pk += int(((seg[:,1] > 110) & ((seg[:,0] > 150) | (seg[:,0] < 4))).mean() > 0.5)
    return dict(ht=ht, ft=ft, a=a, hb_y=hb_y, flap_pink=pk >= 8)
K_STILL = 0.80                                                    # panel width / (panel + flap) on the still
def track_lid():
    raw = {f: detect_lid(b_rot(f), f) for f in range(B_CARD0, B_STILL+1)}
    fr = sorted(raw); first_ok = min(f for f in fr if raw[f] is not None)
    L = np.array([np.nan if (raw[f] is None or raw[f]['hb_y'] is None) else raw[f]['hb_y'] - raw[f]['ht'][1] for f in fr])
    idx = np.arange(len(fr)); good = ~np.isnan(L)
    Lf = np.interp(idx, idx[good], L[good])
    bump = np.convolve(np.pad((~good).astype(float), 3, mode='edge'), np.ones(7)/7, 'valid')
    Lf = Lf + 45 * bump * (~good)
    quads = []; kk = []
    for i, f in enumerate(fr):
        d = raw[f]
        if d is None: quads.append(None); kk.append(1.0); continue
        ht = np.array(d['ht']); ft = np.array(d['ft']); hb = np.array([HX, ht[1] + Lf[i]])
        u = np.array([d['a'], 1.0]); u /= np.linalg.norm(u)
        fb = ft + u * Lf[i] * (0.97 + 0.123 * sstep((f - 45) / 9.0))   # free side grows to 9.3 % longer than the hinge side as the lid lands
        quads.append([ht, ft, fb, hb]); kk.append(1.0 if d['flap_pink'] else K_STILL)
    # frames before the first detection: the panel is a sliver; extrapolate the free edge back linearly
    i0 = fr.index(first_ok)
    for i in range(i0 - 1, -1, -1):
        q1 = np.array(quads[i+1]); q2 = np.array(quads[i+2]); q = q1 + (q1 - q2)
        q[:, 0] = np.maximum(q[:, 0], HX); q[0, 0] = HX; q[3, 0] = HX
        q[1, 0] = max(q[1, 0], HX + 6); q[2, 0] = max(q[2, 0], HX + 6)
        quads[i] = list(q); kk[i] = 1.0
    Q = np.array(quads, float)
    for i, f in enumerate(fr):                                    # last frames: lower free corner measured directly
        if f >= 66:
            m, _ = white_right_of_hinge(b_rot(f))
            xs = np.arange(int(Q[i,1,0]) - 60, int(Q[i,1,0]) - 8)
            bot = np.array([np.where(m[:,x])[0].max() for x in xs]); ab, bb = np.polyfit(xs, bot, 1)
            a = raw[f]['a']; bfree = Q[i,1,0] - a*Q[i,1,1]
            y = (ab*bfree + bb) / (1 - ab*a); Q[i,2] = [a*y + bfree, y]; Q[i,3] = [HX, ab*HX + bb]
    Qp = np.pad(Q, ((2,2),(0,0),(0,0)), mode='edge')
    Qm = np.array([np.median(Qp[i:i+5], axis=0) for i in range(len(fr))])
    Qm[:9] = Q[:9]                                                # the first frames move fast: no median there
    Qp = np.pad(Qm, ((1,1),(0,0),(0,0)), mode='edge')
    Qs = 0.25*Qp[:-2] + 0.5*Qp[1:-1] + 0.25*Qp[2:]; Qs[:7] = Qm[:7]
    kk = np.array(kk); kk[-8:] = K_STILL
    kp = np.pad(kk, 2, mode='edge'); ks = np.convolve(kp, np.ones(5)/5, 'valid')
    out = {}
    for i, f in enumerate(fr):
        q = Qs[i].copy(); sc = ks[i] / K_STILL                    # put the quad's free side where panel+flap would end
        q[1] = q[0] + (q[1] - q[0]) * sc; q[2] = q[3] + (q[2] - q[3]) * sc
        out[f] = q
    json.dump({str(f): dict(quad=out[f].round(2).tolist(), panel_share=float(ks[i]), detected=raw[f] is not None) for i, f in enumerate(fr)},
              open(f'{ROOT}/_work/lid_track_v02.json', 'w'), indent=0)
    return out
LID = track_lid()
UNIT = np.array([[0,0],[1,0],[1,1],[0,1]], np.float32)
CARD_STILL = np.array([[708,120.8],[912,101.75],[912,650.75],[708,633.8]], np.float32)   # TL TR BR BL on the still
H_still = cv2.getPerspectiveTransform(UNIT, LID[B_STILL].astype(np.float32))
CARD_UV = cv2.perspectiveTransform(CARD_STILL[None], np.linalg.inv(H_still))[0]
def card_quad(f):
    Hf = cv2.getPerspectiveTransform(UNIT, LID[f].astype(np.float32))
    return cv2.perspectiveTransform(CARD_UV[None], Hf)[0]

# ---------------- card artwork: only white point and black level are matched; hue and saturation stay ----------------
card = cv2.imread(CARD).astype(np.float32) / 255.0
card = 0.045 + 0.955 * card                                       # black level of the footage
fall = np.linspace(1.0, 0.975, card.shape[0], dtype=np.float32)[:, None, None]
card = card * fall
CH, CW = card.shape[:2]
CARD_PX = np.array([[0,0],[CW,0],[CW,CH],[0,CH]], np.float32)
def composite_card(F, quad_out, occ=None):
    """F: graded float32 frame; card colour = artwork x local lid white (so shading, paper texture and shadows carry through)."""
    h, w = F.shape[:2]
    Hc = cv2.getPerspectiveTransform(CARD_PX, quad_out.astype(np.float32))
    tw = np.linalg.norm(quad_out[1] - quad_out[0]); sc = min(1.0, max(0.03, 1.15 * tw / CW))
    small = cv2.resize(card, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
    Hs = Hc @ np.diag([1/sc, 1/sc, 1.0])
    cw = cv2.warpPerspective(small, Hs, (w, h), flags=cv2.INTER_LINEAR, borderValue=(1,1,1))
    cov = cv2.warpPerspective(np.ones(small.shape[:2], np.float32), Hs, (w, h), flags=cv2.INTER_LINEAR)
    px = max(0.3, tw / 525.0)
    cw = cv2.GaussianBlur(cw, (0,0), 0.55 * px)
    sh = cv2.GaussianBlur(cov, (0,0), 2.2 * px)
    sh = cv2.warpAffine(sh, np.float32([[1,0,2.0*px],[0,1,2.5*px]]), (w, h)) * (1 - cov)
    a = cov
    if occ is not None: a = a * occ; sh = sh * occ
    # local lid white: the frame itself, neutralised (its luminance, on the lid's median colour), a touch brighter = paper on card
    sel = (a > 0.9)
    if sel.sum() > 50:
        wref = np.median(F[sel], axis=0)
        lum = F.mean(axis=2) / max(1.0, wref.mean())
        lid = np.clip(lum, 0.5, 1.06)[..., None] * (wref * 1.025)
    else:
        lid = F
    out = F * (1 - 0.15 * sh[..., None])
    out = out * (1 - a[..., None]) + (lid * cw) * a[..., None]
    return out
def lid_matte(src):
    """1 where the bare white lid is visible, 0 on the hand and on anything else (source-resolution, rotated frame)."""
    u8 = np.clip(src, 0, 255).astype(np.uint8); hsv = cv2.cvtColor(u8, cv2.COLOR_BGR2HSV)
    hue, S, V = hsv[...,0], hsv[...,1], hsv[...,2]
    skin = (((hue < 24) | (hue > 166)) & (S >= 38) & (S < 215) & (V > 70)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19,19)))   # nail and highlights
    n, lab, st, _ = cv2.connectedComponentsWithStats(skin)
    hand = np.zeros_like(skin)
    for k in range(1, n):
        if st[k,4] > 900: hand[lab == k] = 1                      # the hand is one big blob; specks on the paper are not
    hand = cv2.dilate(hand, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    white = ((S < 30) & (V > 95)).astype(np.uint8)
    occ = (white & (1 - hand)).astype(np.float32)
    occ[:, :HX+2] = 0                                             # the card is on the lid only, never left of the hinge
    occ = cv2.erode(occ, np.ones((3,3), np.uint8))
    return cv2.GaussianBlur(occ, (0,0), 1.0)

def grain(F, sigma=2.0):
    n = rng.normal(0, sigma, (H//2, W//2)).astype(np.float32)
    n = cv2.resize(n, (W, H), interpolation=cv2.INTER_LINEAR) * 0.7 + rng.normal(0, sigma*0.6, (H, W)).astype(np.float32)
    return F + n[..., None]
def unsharp(F, amount=0.5, sigma=1.4): return F + amount * (F - cv2.GaussianBlur(F, (0,0), sigma))

# ---------------- virtual camera for B ----------------
def shake(t, amp):
    x = amp * (0.62*np.sin(2*np.pi*0.93*t + 0.4) + 0.38*np.sin(2*np.pi*0.41*t + 2.1))
    y = amp * (0.60*np.sin(2*np.pi*1.07*t + 1.3) + 0.40*np.sin(2*np.pi*0.33*t + 0.2))
    r = 0.26*np.sin(2*np.pi*0.52*t + 0.9) + 0.04*np.sin(2*np.pi*1.3*t)
    return x, y, r
S_LIVE, S_HOLD = 2.75, 525.0/204.0                               # card 525 px wide -> QR code 324 px = 30 % of the frame
CARD_TOP = 90
CY_HOLD = 120.8 + (H/2 - CARD_TOP) / S_HOLD
def cam(n):
    t = n / FPS
    if n < HOLD0:
        f = B_F0 + (n - N_A)
        cx = 590 + (790 - 590) * sstep((f - 27) / 16.0) + 20 * sstep((f - 52) / 18.0)
        e = sstep((n - N_A) / 8.0)                               # the whip ends: shake fades in
        sx, sy, r = shake(t, 9.0)
        return S_LIVE, cx, 360.0, sx*e, sy*0.6*e, r*0.5*e
    e = sstep((n - HOLD0) / 30.0)
    s = S_LIVE + (S_HOLD - S_LIVE) * e
    sx, sy, r = shake(t, 9.0 + (5.0 - 9.0) * e)
    return s, 810.0, 360.0 + (CY_HOLD - 360.0) * e, sx, sy * (0.6 + 0.4*e), r * (0.5 + 0.5*e)
def cam_matrix(n):
    s, cx, cy, sx, sy, r = cam(n)
    M = cv2.getRotationMatrix2D((cx, cy), r, s)
    M[0,2] += W/2 - cx + sx; M[1,2] += H/2 - cy + sy
    return M

# ---------------- hold: still box + card, live asphalt around it ----------------
EXT = 190
STILL = b_rot(B_STILL).astype(np.float32)
BOXMASK = np.zeros((720, 1280), np.float32); BOXMASK[30:712, 452:1004] = 1.0
BOXMASK = cv2.GaussianBlur(BOXMASK, (0,0), 7)[..., None]         # 1 = taken from the still
_sift = cv2.SIFT_create(3000); _amask = np.full((720, 1280), 255, np.uint8); _amask[40:720, 440:1010] = 0
_k0, _d0 = _sift.detectAndCompute(cv2.cvtColor(STILL.astype(np.uint8), cv2.COLOR_BGR2GRAY), _amask)
_live_cache = {}
def live_asphalt(f):
    """B frame f (>70) registered to the still by a homography found on the asphalt, tone-matched to the still."""
    if f == B_STILL: return STILL
    if f in _live_cache: return _live_cache[f]
    img = b_rot(f); k1, d1 = _sift.detectAndCompute(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), None)
    m = [a for a, b in cv2.BFMatcher().knnMatch(d1, _d0, k=2) if a.distance < 0.7 * b.distance]
    Hm, _ = cv2.findHomography(np.float32([k1[a.queryIdx].pt for a in m]), np.float32([_k0[a.trainIdx].pt for a in m]), cv2.RANSAC, 2.0)
    w = cv2.warpPerspective(img, Hm, (1280, 720), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    g = STILL[:, :430].reshape(-1, 3).mean(0) / w[:, :430].reshape(-1, 3).mean(0)
    w = w * g
    if len(_live_cache) > 4: _live_cache.clear()
    _live_cache[f] = w
    return w
def canvas_for(f):
    live = live_asphalt(f)
    fr = STILL * BOXMASK + live * (1 - BOXMASK)
    canvas = np.zeros((720 + EXT, 1280, 3), np.float32); canvas[:720] = fr
    donor = cv2.rotate(fr[:, 0:440], cv2.ROTATE_90_COUNTERCLOCKWISE)        # real asphalt from the cropped-away side
    donor = np.hstack([donor, donor[:, ::-1]])[:, :1280]; donor = np.roll(donor, 470, axis=1)
    ov = 46; strip = donor[40:40 + EXT + ov]
    ref = cv2.GaussianBlur(fr[720-60:720], (0,0), 25).mean(axis=0, keepdims=True)
    strip = strip - cv2.GaussianBlur(strip, (0,0), 25) + ref
    canvas[720:] = strip[ov:]
    ramp = np.linspace(0, 1, ov, dtype=np.float32)[:, None, None]
    canvas[720-ov:720] = fr[720-ov:720] * (1 - ramp) + strip[:ov] * ramp
    return np.clip(canvas, 0, 255)
PING = list(range(B_STILL, 194)) + list(range(192, B_STILL, -1))  # 70..193..71
def hold_frame(n):
    f = PING[(n - HOLD0) % len(PING)]
    M = cam_matrix(n)
    F = cv2.warpAffine(canvas_for(f), M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    F = grade_b(unsharp(np.clip(F, 0, 255), 0.5, 1.6))
    return composite_card(F, cv2.transform(CARD_STILL[None], M)[0])
def live_frame(n):
    f = B_F0 + (n - N_A)
    raw = b_rot(f)
    src = add_shadow(raw)
    M = cam_matrix(n)
    F = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    F = grade_b(unsharp(np.clip(F, 0, 255), 0.5, 1.6))
    if f >= B_CARD0:
        occ = cv2.warpAffine(lid_matte(raw), M, (W, H), flags=cv2.INTER_LINEAR)
        F = composite_card(F, cv2.transform(card_quad(f)[None], M)[0], occ)
    return F

# ---------------- join ----------------
def vblur(F, length, hsig=0):
    if length >= 2:
        k = np.full((int(length), 1), 1.0 / int(length), np.float32)
        F = cv2.filter2D(F, -1, k, borderType=cv2.BORDER_REFLECT)
    if hsig: F = cv2.GaussianBlur(F, (0,0), sigmaX=hsig, sigmaY=0.1)
    return F
def vshift(F, dy): return cv2.warpAffine(F, np.float32([[1,0,0],[0,1,dy]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
A_BL = [10, 26, 60, 130, 250, 420, 620]                          # last 7 A frames
B_BL = [(620, 420), (460, 260), (300, 140), (170, 70), (80, 30), (30, 10), (8, 3)]   # (blur length, downward offset) first 7 B frames
MIX = {N_A-2: 0.2, N_A-1: 0.42, N_A: 0.62, N_A+1: 0.82}          # share of B in the 4 frames around the cut
DIP = {N_A-2: 0.9, N_A-1: 0.74, N_A: 0.72, N_A+1: 0.88}
def a_blurred(n):
    nn = min(n, N_A-1); F = a_frame(nn).astype(np.float32); i = nn - (N_A - 7)
    L = A_BL[i] if i >= 0 else 0
    if n >= N_A: L = 700
    return vblur(vshift(F, -0.25*L), L, hsig=6 if L > 200 else 0)
def b_blurred(n):
    nn = max(n, N_A); F = live_frame(nn); i = nn - N_A
    L, dy = B_BL[i] if i < 7 else (0, 0)
    if n < N_A: L, dy = 700, 520
    return vblur(vshift(F, dy), L, hsig=6 if L > 200 else 0)
def frame(n):
    if n in MIX:
        F = a_blurred(n) * (1 - MIX[n]) + b_blurred(n) * MIX[n]
        F = F * DIP[n]
    elif n < N_A:
        F = a_blurred(n) if n >= N_A - 7 else a_frame(n).astype(np.float32)
    elif n < HOLD0:
        F = b_blurred(n) if n < N_A + 7 else live_frame(n)
    else:
        F = hold_frame(n)
    return np.clip(grain(F), 0, 255).astype(np.uint8)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        os.makedirs(f'{ROOT}/_work/test', exist_ok=True)
        for a in sys.argv[1:]: cv2.imwrite(f'{ROOT}/_work/test/v02_{int(a):04d}.png', frame(int(a)))
        sys.exit()
    out = f'{ROOT}/_work/video_v02_silent.mp4'
    p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','medium','-crf','13','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709', out], stdin=subprocess.PIPE)
    for n in range(TOTAL):
        p.stdin.write(frame(n).tobytes())
        if n % 50 == 0: print('frame', n, flush=True)
    p.stdin.close(); rc = p.wait(); print('ffmpeg exit', rc, 'wrote', out)
