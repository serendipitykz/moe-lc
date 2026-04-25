#!/usr/bin/env python3
"""
build.py  —  Assembles per-slide HTML fragments into dist/index.html.

Usage:
    python build.py

Steps:
  1. Read template.html
  2. Glob sections/*.html sorted by filename
  3. Concatenate all slide <div> fragments
  4. Replace <!-- SLIDES_PLACEHOLDER --> in template with the concatenation
  5. Write result to dist/index.html
  6. Print: "Built N slides → dist/index.html"
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).parent.resolve()
TEMPLATE = ROOT / "template.html"
SECTIONS_DIR = ROOT / "sections"
DIST_DIR = ROOT / "dist"
OUTPUT = DIST_DIR / "index.html"

PLACEHOLDER = "<!-- SLIDES_PLACEHOLDER -->"


def main() -> None:
    # 1. Read the template
    if not TEMPLATE.exists():
        sys.exit(f"Error: {TEMPLATE} not found.")
    template_html = TEMPLATE.read_text(encoding="utf-8")

    if PLACEHOLDER not in template_html:
        sys.exit(f"Error: placeholder '{PLACEHOLDER}' not found in template.html.")

    # 2. Glob and sort section files across subdirs (sections/NN-name/NN_slug.html)
    section_files = sorted(SECTIONS_DIR.rglob("*.html"))
    if not section_files:
        sys.exit(f"Error: no .html files found under {SECTIONS_DIR}.")

    # 3. Concatenate fragments
    fragments: list[str] = []
    for path in section_files:
        content = path.read_text(encoding="utf-8").strip()
        fragments.append(content)

    slides_html = "\n\n".join(fragments)

    # 4. Inject into template
    assembled = template_html.replace(PLACEHOLDER, slides_html, 1)

    # 5. Write output
    DIST_DIR.mkdir(exist_ok=True)
    OUTPUT.write_text(assembled, encoding="utf-8")

    # 6. Report
    n = len(section_files)
    print(f"Built {n} slide{'s' if n != 1 else ''} → dist/index.html")


if __name__ == "__main__":
    main()
