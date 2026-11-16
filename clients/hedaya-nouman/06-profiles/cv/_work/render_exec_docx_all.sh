#!/usr/bin/env bash
# Three LibreOffice renders of the executive DOCX: fonts installed; fonts hidden (embedded fonts only);
# fonts hidden AND embedding stripped, with DejaVu Sans (a wider, taller face) substituted - a stress test.
set -euo pipefail
W=/home/user/arwa/clients/hedaya-nouman/06-profiles/cv/_work
S=${SCRATCH:-/tmp/claude-0/-home-user-arwa/f9b2b2de-370a-5464-a989-49bf939ab0bf/scratchpad}
bash "$W/render_exec_docx.sh"
rm -rf "$W/exec-docx-render-nofonts" "$W/exec-docx-render-fallback"; mkdir "$W/exec-docx-render-nofonts" "$W/exec-docx-render-fallback"
FONTCONFIG_FILE=$S/fonts.conf soffice -env:UserInstallation=file://$S/lo-profile --headless --convert-to pdf --outdir "$W/exec-docx-render-nofonts" "$W"/../*executive*_v04.docx >/dev/null 2>&1
FONTCONFIG_FILE=$S/fonts-wide.conf soffice -env:UserInstallation=file://$S/lo-profile2 --headless --convert-to pdf --outdir "$W/exec-docx-render-fallback" "$W"/exec-docx-noembed/*_v04.docx >/dev/null 2>&1
