#!/usr/bin/env python3
"""Copy an HTML file and everything it links to (CSS, fonts, images, scripts)
into one self-contained folder, rewriting the links to local paths.

Used when packaging editable sources for delivery, so a source opens correctly
outside the repository.

Usage: python3 scripts/collect_html.py <source.html> <output-dir>
"""
import hashlib, pathlib, re, shutil, sys

URL_IN_CSS = re.compile(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)')
ATTR = re.compile(r'\b(src|href)\s*=\s*(["\'])([^"\']+)\2')

def is_local(ref):
    return not re.match(r'^(?:[a-z][a-z0-9+.-]*:|//|#)', ref, re.I)

def main():
    src = pathlib.Path(sys.argv[1]).resolve()
    out = pathlib.Path(sys.argv[2]).resolve()
    assets = out / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    copied, missing = {}, []

    def take(ref, base):
        clean = ref.split("#")[0].split("?")[0]
        target = (base / clean).resolve()
        if not target.is_file():
            missing.append(ref); return None
        if target not in copied:
            name = target.name
            if (assets / name).exists() and (assets / name).read_bytes() != target.read_bytes():
                name = f"{target.stem}-{hashlib.sha1(str(target).encode()).hexdigest()[:6]}{target.suffix}"
            if target.suffix.lower() == ".css":
                css = URL_IN_CSS.sub(lambda m: fix_css(m, target.parent), target.read_text(encoding="utf-8"))
                (assets / name).write_text(css, encoding="utf-8")
            else:
                shutil.copy2(target, assets / name)
            copied[target] = name
        return copied[target]

    def fix_css(m, base):
        ref = m.group(1)
        if not is_local(ref) or ref.startswith("data:"): return m.group(0)
        name = take(ref, base)
        return f'url("{name}")' if name else m.group(0)   # CSS in assets/ -> sibling file

    def fix_inline_css(m):
        ref = m.group(1)
        if not is_local(ref) or ref.startswith("data:"): return m.group(0)
        name = take(ref, src.parent)
        return f'url("assets/{name}")' if name else m.group(0)

    def fix_attr(m):
        attr, q, ref = m.groups()
        if not is_local(ref) or ref.startswith(("data:", "mailto:", "tel:")): return m.group(0)
        name = take(ref, src.parent)
        return f'{attr}={q}assets/{name}{q}' if name else m.group(0)

    html = src.read_text(encoding="utf-8")
    html = ATTR.sub(fix_attr, html)
    html = URL_IN_CSS.sub(fix_inline_css, html)
    (out / src.name).write_text(html, encoding="utf-8")
    print(f"{src.name}: {len(copied)} linked files collected into {out}")
    if missing:
        print("  NOT FOUND:", ", ".join(sorted(set(missing)))); sys.exit(1)

if __name__ == "__main__":
    main()
