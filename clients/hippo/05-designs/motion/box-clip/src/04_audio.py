#!/usr/bin/env python3
"""Sound mix for the box clip. No generated sound is added here: the two clips' own audio is the ambience,
footsteps and cardboard; the impact thud is synthesised (sub sine burst + filtered noise + saturation);
VO take 1 is clean and full range. Car chirp: deliberately not built (see notes.md).
Out: _work/audio/mix_v01.wav (48 kHz stereo, -14 LUFS, <= -1.5 dBTP)."""
import numpy as np, scipy.io.wavfile as wf, scipy.signal as sg, subprocess, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AU = f'{ROOT}/_work/audio'; os.makedirs(AU, exist_ok=True)
SR = 48000
TOTAL = 17.5
A_T0 = 38 * 0.8 / 24          # piece A source time at output t=0 (1.2667 s)
JOIN = 201 / 30               # 6.70 s
B_T0 = 8 / 24                 # piece B source time at the join
B_LIVE = 62 / 30              # B plays 62 source frames in 62 output frames (125 %)
HOLD = JOIN + B_LIVE          # 8.767 s
IMPACT = 1.40
VO_AT = 7.90                  # card first visible at 7.87 s
rng = np.random.default_rng(11)
def dec(src, out, extra=()):
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,*extra,'-ar',str(SR),'-ac','1',out], check=True)
    sr, x = wf.read(out); return x.astype(np.float64) / 32768
def bp(x, lo, hi, order=2):
    sos = sg.butter(order, [lo, hi], 'bandpass', fs=SR, output='sos'); return sg.sosfilt(sos, x)
def lp(x, f, order=2): return sg.sosfilt(sg.butter(order, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sg.sosfilt(sg.butter(order, f, 'highpass', fs=SR, output='sos'), x)
def db(v): return 10 ** (v / 20)
N = int(TOTAL * SR); T = np.arange(N) / SR
def place(track, x, at, gain=1.0):
    i = int(round(at * SR)); j = min(N, i + len(x)); track[i:j] += x[:j - i] * gain
def fade(x, fin=0.0, fout=0.0):
    x = x.copy(); a = int(fin * SR); b = int(fout * SR)
    if a: x[:a] *= np.linspace(0, 1, a)
    if b: x[-b:] *= np.linspace(1, 0, b)
    return x

a = dec(f'{ROOT}/_work/gen/gen02_A_9x16_8s.mp4', f'{AU}/A_mono.wav')
b = dec(f'{ROOT}/_work/gen/gen02_B_9x16_8s.mp4', f'{AU}/B_mono.wav')
b_fast = dec(f'{ROOT}/_work/gen/gen02_B_9x16_8s.mp4', f'{AU}/B_live_125.wav', ('-ss', f'{B_T0:.4f}', '-t', f'{B_LIVE*1.25 + 0.25:.4f}', '-af', 'atempo=1.25'))
vo = dec(f'{ROOT}/audio/hippo_box-clip_vo-take1_ar_v01.mp3', f'{AU}/vo1.wav')

# ---- bed: the clips' own sound ----
bed = np.zeros(N)
a_seg = a[int(A_T0 * SR):].copy()
# the clip's own after-ring 0.25-0.75 s after its impact is tonal (about 220 Hz) and was not auditioned: pulled down 6 dB
t_a = np.arange(len(a_seg)) / SR
dip = np.interp(t_a, [IMPACT + 0.20, IMPACT + 0.28, IMPACT + 0.75, IMPACT + 0.9], [1, db(-6), db(-6), 1])
a_seg = a_seg * dip
a_seg = a_seg[:int((JOIN + 0.12) * SR)]
place(bed, fade(a_seg, 0.03, 0.2), 0.0)
place(bed, fade(b_fast[:int((B_LIVE + 0.15) * SR)], 0.15, 0.15), JOIN - 0.05)
# hold ambience: the steady part of B (3.0-7.9 s), looped with 0.6 s crossfades
amb = b[int(3.0 * SR):int(7.9 * SR)]
xf = int(0.6 * SR); pos = HOLD - 0.1; first = True
while pos < TOTAL:
    seg = fade(amb, 0.15 if first else 0.6, 0.6); place(bed, seg, pos); pos += len(amb) / SR - 0.6; first = False
bed = bp(bed, 150, 9000)                                   # phone-mic chain: band-limit, mono
# light compression
env = np.sqrt(lp(bed ** 2, 12) .clip(1e-12)); thr = db(-30)
bed = bed * np.where(env > thr, (env / thr) ** (-0.33), 1.0)

# ---- thud ----
n = int(0.75 * SR); t = np.arange(n) / SR
f = 46 + 34 * np.exp(-t / 0.035)
sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.17) * np.minimum(1, t / 0.004)
sub *= np.minimum(1, (0.75 - t) / 0.1)
body = lp(rng.normal(0, 1, n), 240, 4) * np.exp(-t / 0.12); body /= np.abs(body).max()
smack = bp(rng.normal(0, 1, n), 260, 2300) * np.exp(-t / 0.016); smack /= np.abs(smack).max()
grit = hp(rng.normal(0, 1, n), 2500) * (rng.random(n) > 0.9985) ; grit = lp(grit, 7000) * ((t > 0.06) & (t < 0.45)) * np.exp(-t / 0.2)
grit = sg.lfilter([1], [1, -0.97], grit) ; grit = hp(grit, 1800); grit /= (np.abs(grit).max() + 1e-9)
raw = bp(1.0 * body + 0.5 * smack + 0.8 * sub, 150, 9000)      # what a phone mic would pass
raw /= np.sqrt((raw[:int(0.1*SR)] ** 2).mean())
drive = 0.25 + 5.0 * np.exp(-t / 0.13)                       # overloaded for roughly the first 100 ms, then it lets go
phone = np.tanh(drive * raw) * np.exp(-t / 0.3) + 0.04 * grit
phone /= np.abs(phone).max()
thud_phone = np.zeros(N); place(thud_phone, phone, IMPACT, db(-8.5))
thud_sub = np.zeros(N); place(thud_sub, lp(sub, 120, 2), IMPACT, db(-13))     # clean, full range

# ---- handling rumble over the join ----
m = int(0.5 * SR); tt = np.arange(m) / SR
rum = bp(rng.normal(0, 1, m), 150, 420) * np.exp(-((tt - 0.2) / 0.11) ** 2); rum /= np.abs(rum).max()
handling = np.zeros(N); place(handling, rum, JOIN - 0.22, db(-13))

# ---- gains over time ----
bed_gain = np.full(N, db(14.0))
agc = np.interp(T, [0, IMPACT - 0.12, IMPACT - 0.07, IMPACT + 0.25, IMPACT + 0.8, TOTAL], [1, 1, db(-12), db(-9), 1, 1])   # mic AGC ducks after the hit
duck = np.interp(T, [0, VO_AT - 0.25, VO_AT + 0.05, TOTAL], [1, 1, db(-4), db(-4)])                              # ambience 4 dB under the voice
bed_t = bed * bed_gain * agc * duck
bed_t = db(-14) * np.tanh(bed_t / db(-14))            # footsteps and cardboard never poke above the voice
out_fade = np.interp(T, [0, 0.04, TOTAL - 0.25, TOTAL], [0, 1, 1, 0])

# VO: gentle 3:1 compression above -30 dBFS so the limiter has little left to do; otherwise untouched (no EQ, no reverb)
e = np.abs(vo); att = np.exp(-1/(0.001*SR)); rel_ = np.exp(-1/(0.08*SR)); envv = np.empty_like(e); c = 0.0
for i in range(len(e)):
    c = att*c + (1-att)*e[i] if e[i] > c else rel_*c + (1-rel_)*e[i]
    envv[i] = c
thr_v = db(-30); vo_c = vo * np.where(envv > thr_v, (envv/thr_v) ** (1/3.0 - 1), 1.0)
vo_t = np.zeros(N); place(vo_t, fade(vo_c, 0.01, 0.03), VO_AT)
def limiter(x, ceil):
    look = int(0.004 * SR)
    pk = np.abs(x); pk = np.maximum.reduce([np.roll(pk, -k) for k in range(0, look + 1, 8)])
    g = np.minimum(1.0, ceil / np.maximum(pk, 1e-9))
    # instant attack (already looked ahead), 90 ms release
    rel = np.exp(-1 / (0.09 * SR)); out = np.empty_like(g); c = 1.0
    for i in range(len(g)):
        c = g[i] if g[i] < c else 1 - (1 - c) * rel
        if c > g[i]: c = g[i]
        out[i] = c
    out = np.minimum(out, sg.lfilter(np.ones(look) / look, [1], np.concatenate([out[look:], np.ones(look)])) + 1e-3)
    return x * np.minimum(out, g)
def measure(path):
    r = subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',path,'-af','ebur128=peak=true','-f','null','-'], capture_output=True, text=True).stderr
    tail = r[r.rfind('Summary:'):]
    return float(re.search(r'I:\s+(-?[\d.]+) LUFS', tail).group(1)), float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', tail).group(1))
vo_gain = db(16.0); master = 1.0
for it in range(14):
    mix = (bed_t + thud_phone + handling) * 1.0 + thud_sub + vo_t * vo_gain
    mix = limiter(mix * master * out_fade, db(-2.0))
    st = np.stack([mix, mix], 1)
    wf.write(f'{AU}/mix_v01.wav', SR, (np.clip(st, -1, 1) * 32767).astype(np.int16))
    I, TP = measure(f'{AU}/mix_v01.wav')
    print(f'pass {it}: master {20*np.log10(master):+.2f} dB -> I {I} LUFS, true peak {TP} dBFS')
    if abs(I + 14.0) <= 0.15: break
    master *= db((-14.0 - I) * 1.3)
# report peaks per element after master
lim_in = (bed_t + thud_phone + handling + thud_sub + vo_t * vo_gain) * master
print('samples over the limiter ceiling: %.2f %% ; max over %.1f dB' % (100*(np.abs(lim_in) > db(-2.0)).mean(), 20*np.log10(np.abs(lim_in).max()/db(-2.0))))
for name, x in (('thud', (thud_phone + thud_sub) * master), ('vo', vo_t * vo_gain * master), ('bed', bed_t * master)):
    print(name, 'peak %.1f dBFS' % (20 * np.log10(np.abs(x).max() + 1e-9)))
print('VO start %.2f end %.2f; tail after VO %.2f s' % (VO_AT, VO_AT + len(vo) / SR, TOTAL - VO_AT - len(vo) / SR))

w = int(0.1*SR); r = np.array([np.sqrt((mix[i:i+w]**2).mean()) for i in range(0, N-w, w//2)]); tt = np.arange(len(r))*0.05
print('loudest 100 ms window: %.1f dBFS at %.2f s; loudest during VO: %.1f dBFS; bed before impact about %.1f dBFS; bed in hold tail %.1f dBFS' % (
    20*np.log10(r.max()), tt[r.argmax()], 20*np.log10(r[tt > VO_AT].max()), 20*np.log10(np.median(r[tt < 1.2])), 20*np.log10(np.median(r[tt > 15.8]))))
