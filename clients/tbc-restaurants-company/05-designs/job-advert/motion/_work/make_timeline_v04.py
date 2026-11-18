"""Writes timeline.json for motion v04 (voice-over take 2) and derives the SFX
cue list from the animation keyframes, so a retime regenerates the cues.
Edit the numbers in SCENES below (or timeline.json directly) and re-run."""
import json, os
M = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFF = 0.15
# measured in take 2 with silencedetect (-35 dB, d=0.08) and a 20 ms energy scan; audio seconds
VO = [
    ("تحب التسويق وعندك حس إبداعي؟", 0.00, 2.29), ("هذي فرصتك!", 2.66, 3.65),
    ("مطلوب موظف أو موظفة تسويق وإدارة حسابات التواصل الاجتماعي", 3.99, 8.31),
    ("لشركة متخصصة في قطاع المطاعم", 8.58, 10.85),
    ("خبرة لا تقل عن ثلاث سنوات", 11.21, 13.10), ("وخبرة التصميم شرط أساسي", 13.32, 15.29),
    ("والراتب مجزي", 15.65, 16.81),
    ("أرسل سيرتك الذاتية وسابقة أعمالك على الإيميل اللي قدامك", 17.15, 20.85), ("وننتظرك!", 21.17, 22.05),
]
T = {
    "_note": "The ONE place to retime the film. All values are seconds. Scene 'start' values are film times; everything inside a scene is an offset from that scene's start ('end' is informational). v04 is timed to voice-over take 2, placed at audio_offset in the film; 'voice' lists each phrase's measured film time. The 'sfx' list is DERIVED from the keyframes by _work/make_timeline_v04.py: re-run it after changing any time. Word offsets inside the headline phrase come from the short dips found inside that phrase (at -28/-24 dB) and are less certain than the phrase starts.",
    "fps": 30, "duration": 23.5, "audio_offset": OFF,
    "voice_file": "audio/tbc-restaurants-company_job-advert_voiceover-take2_ar_v02.mp3",
    "voice": [{"text": t, "start": round(a + OFF, 2), "end": round(b + OFF, 2)} for t, a, b in VO],
    "scenes": {
        "hook": {"start": 0.0, "end": 4.0, "cues": {"swipes": [0.8, 1.42, 2.08], "fire": [0.62, 1.2, 1.82], "kicker": 2.6, "pop": 2.7}},
        "headline": {"start": 4.0, "end": 8.5, "words": [0.45, 1.6, 2.12, 2.6, 3.22, 3.7]},
        "sector": {"start": 8.5, "end": 11.05, "line": 0.1},
        "require": {"start": 11.05, "end": 16.9, "items": [0.28, 2.3, 4.45]},
        "apply": {"start": 16.9, "end": 23.5, "sentence": 0.45, "email": 1.55},
    },
}
S = T["scenes"]
h, hl, sc, rq, ap = (S[k]["start"] for k in ("hook", "headline", "sector", "require", "apply"))
# (keyframe film time, lead in seconds, file, peak target dBFS, what it marks)
PEAK = {"sfx_whoosh.mp3": -7.5, "sfx_swipe.mp3": -1.7, "sfx_pop.mp3": -1.5, "sfx_stamp.mp3": -1.5, "sfx_chime.mp3": -5.7}  # measured file peaks
cues = [
    (h + 0.0, 0.0, "sfx_whoosh.mp3", -23, "phone entrance starts"),
    (h + S["hook"]["cues"]["swipes"][0], 0.0, "sfx_swipe.mp3", -17, "feed swipe 1 starts"),
    (h + S["hook"]["cues"]["swipes"][1], 0.0, "sfx_swipe.mp3", -17, "feed swipe 2 starts"),
    (h + S["hook"]["cues"]["swipes"][2], 0.0, "sfx_swipe.mp3", -17, "feed swipe 3 starts"),
    (h + S["hook"]["cues"]["pop"], 0.02, "sfx_pop.mp3", -11, "burger pop-out starts (kicker is mid-pop)"),
    (hl, 0.22, "sfx_whoosh.mp3", -18, "scene change: hook to headline"),
    (sc, 0.14, "sfx_whoosh.mp3", -18, "scene change: headline to sector"),
    (rq, 0.10, "sfx_whoosh.mp3", -19, "scene change: sector to requirements"),
    (rq + S["require"]["items"][0], 0.03, "sfx_pop.mp3", -13, "item 1 appears («خبرة لا تقل عن 3 سنوات»)"),
    (rq + S["require"]["items"][1], 0.0, "sfx_pop.mp3", -13, "item 2 appears (design card)"),
    (rq + S["require"]["items"][2] + 0.19, 0.0, "sfx_stamp.mp3", -10, "salary badge lands (stamp reaches size)"),
    (ap, 0.02, "sfx_whoosh.mp3", -18, "scene change: end card builds"),
    (ap + S["apply"]["email"], 0.0, "sfx_chime.mp3", -14, "email pill starts to rise (settles 0.5 s later)"),
]
T["sfx"] = [{"t": round(max(0, k - lead), 3), "file": "audio/sfx/" + f, "gain_db": round(peak - PEAK[f], 1), "peak_dbfs": peak,
             "keyframe": round(k, 3), "marks": why} for k, lead, f, peak, why in cues]
json.dump(T, open(os.path.join(M, "timeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote timeline.json:", len(T["sfx"]), "sfx cues; last cue at", T["sfx"][-1]["t"])
