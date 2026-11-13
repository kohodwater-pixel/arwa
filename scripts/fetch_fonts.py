#!/usr/bin/env python3
"""Download the agency's open-licence (SIL OFL) fonts into assets/fonts/.

Run once; the fonts are committed to the repo, so this is only needed to refresh them.
"""
import pathlib, subprocess, sys, urllib.parse

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
FONTS = {
    "ibmplexsansarabic": ["OFL.txt", "IBMPlexSansArabic-Light.ttf", "IBMPlexSansArabic-Regular.ttf",
                          "IBMPlexSansArabic-Medium.ttf", "IBMPlexSansArabic-SemiBold.ttf", "IBMPlexSansArabic-Bold.ttf"],
    "tajawal": ["OFL.txt", "Tajawal-Light.ttf", "Tajawal-Regular.ttf", "Tajawal-Medium.ttf",
                "Tajawal-Bold.ttf", "Tajawal-ExtraBold.ttf"],
    "cairo": ["OFL.txt", "Cairo[slnt,wght].ttf"],
    "notosansarabic": ["OFL.txt", "NotoSansArabic[wdth,wght].ttf"],
    "notokufiarabic": ["OFL.txt", "NotoKufiArabic[wght].ttf"],
    "amiri": ["OFL.txt", "Amiri-Regular.ttf", "Amiri-Bold.ttf"],
    "ibmplexsans": ["OFL.txt", "IBMPlexSans[wdth,wght].ttf"],
    "inter": ["OFL.txt", "Inter[opsz,wght].ttf"],
}
# Official static IBM Plex Sans (needed for print and for PPTX/PDF embedding by name)
STATIC_BASE = "https://raw.githubusercontent.com/IBM/plex/master/packages/plex-sans/fonts/complete/ttf"
STATIC = {"ibmplexsans-static": [f"IBMPlexSans-{w}.ttf" for w in ("Light", "Regular", "Medium", "SemiBold", "Bold")]}

root = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fonts"
failed = 0
for family, files in FONTS.items():
    (root / family).mkdir(parents=True, exist_ok=True)
    for name in files:
        dest = root / family / name
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        url = f"{BASE}/{family}/{urllib.parse.quote(name)}"
        r = subprocess.run(["curl", "-sfL", "--max-time", "90", url], capture_output=True)
        if r.returncode == 0 and len(r.stdout) > 1000:
            dest.write_bytes(r.stdout)
            print(f"ok   {family}/{name} ({len(r.stdout)//1024} KB)")
        else:
            failed += 1
            print(f"FAIL {family}/{name}")
for family, files in STATIC.items():
    (root / family).mkdir(parents=True, exist_ok=True)
    for name in files:
        dest = root / family / name
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        r = subprocess.run(["curl", "-sfL", "--max-time", "90", f"{STATIC_BASE}/{name}"], capture_output=True)
        if r.returncode == 0 and len(r.stdout) > 1000:
            dest.write_bytes(r.stdout); print(f"ok   {family}/{name}")
        else:
            failed += 1; print(f"FAIL {family}/{name}")
sys.exit(1 if failed else 0)
