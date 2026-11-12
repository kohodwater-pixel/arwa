#!/usr/bin/env bash
# Prepares a machine for Creative Agency OS production work.
# Idempotent and safe to re-run: installs the bundled fonts and the Python
# libraries used for Arabic shaping, PDF inspection and SVG rendering.
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FONT_DIR="${HOME}/.local/share/fonts/creative-agency-os"

mkdir -p "${FONT_DIR}"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --include='*/' --include='*.ttf' --include='*.otf' --exclude='*' "${ROOT}/assets/fonts/" "${FONT_DIR}/"
else
  cp -ru "${ROOT}/assets/fonts/." "${FONT_DIR}/"
fi
command -v fc-cache >/dev/null 2>&1 && fc-cache -f "${FONT_DIR}" >/dev/null 2>&1

if ! python3 -c "import arabic_reshaper, bidi, fontTools, pymupdf, cairosvg" >/dev/null 2>&1; then
  python3 -m pip install -q --disable-pip-version-check --root-user-action=ignore \
    arabic-reshaper python-bidi fonttools pymupdf cairosvg >/dev/null 2>&1 \
    || echo "creative-agency-os: could not install Python libraries (network?)"
fi

if command -v fc-list >/dev/null 2>&1; then
  n=$(fc-list :lang=ar family | grep -ciE 'plex sans arabic|tajawal|cairo|noto (sans|kufi) arabic|amiri')
  echo "creative-agency-os: setup done, ${n} Arabic font faces available"
fi
exit 0
