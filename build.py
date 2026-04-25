#!/usr/bin/env python3
"""
build.py  —  Assembles per-slide HTML fragments into dist/index.html.

Usage:
    python build.py

Steps:
  1. Read template.html
  2. Glob sections/**/*.html sorted by path
  3. Concatenate all slide <div> fragments
  4. Auto-inject slide counters (X / N) — any existing "N / M" counter span
     inside a numbered slide is replaced with the correct position.
  5. Replace <!-- SLIDES_PLACEHOLDER --> in template with the concatenation
  6. Write result to dist/index.html
  7. Print: "Built N slides (M numbered) → dist/index.html"
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.resolve()
TEMPLATE = ROOT / "template.html"
SECTIONS_DIR = ROOT / "sections"
DIST_DIR = ROOT / "dist"
OUTPUT = DIST_DIR / "index.html"

PLACEHOLDER = "<!-- SLIDES_PLACEHOLDER -->"

# Matches the counter span written by authors, e.g. "3 / 26"
COUNTER_RE = re.compile(
    r'(<span\s[^>]*\bfont-mono\b[^>]*>)\s*\d+\s*/\s*\d+\s*(</span>)'
)


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

    # 3. Read fragments, identify which carry a counter
    fragments: list[str] = []
    has_counter: list[bool] = []
    for path in section_files:
        content = path.read_text(encoding="utf-8").strip()
        fragments.append(content)
        has_counter.append(bool(COUNTER_RE.search(content)))

    total_numbered = sum(has_counter)

    # 4. Replace counters with auto-computed X / N
    counter = 0
    new_fragments: list[str] = []
    for frag, numbered in zip(fragments, has_counter):
        if numbered:
            counter += 1
            frag = COUNTER_RE.sub(
                lambda m, x=counter, n=total_numbered: f"{m.group(1)}{x} / {n}{m.group(2)}",
                frag,
            )
        new_fragments.append(frag)

    slides_html = "\n\n".join(new_fragments)

    # 5. Inject into template
    assembled = template_html.replace(PLACEHOLDER, slides_html, 1)

    # 6. Write output
    DIST_DIR.mkdir(exist_ok=True)
    OUTPUT.write_text(assembled, encoding="utf-8")

    # 7. Report
    n = len(section_files)
    print(f"Built {n} file{'s' if n != 1 else ''} ({total_numbered} numbered) → dist/index.html")


if __name__ == "__main__":
    main()
