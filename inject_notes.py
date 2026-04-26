"""Inject speech.md text into each slide's <aside class="notes"> element."""
import re
import glob

# ── 1. Parse speech.md ──────────────────────────────────────────────────────
with open("speech.md", encoding="utf-8") as f:
    raw = f.read()

slide_pattern = re.compile(
    r"### 【幻灯片 (\d+)[^】]*】[^\n]*\n(.*?)(?=### 【幻灯片|\Z)",
    re.DOTALL,
)

speech = {}
for m in slide_pattern.finditer(raw):
    num = int(m.group(1))
    text = m.group(2).strip()
    speech[num] = text

print(f"Parsed {len(speech)} speech sections")

# ── 2. Sorted slide file list ────────────────────────────────────────────────
html_files = sorted(glob.glob("sections/**/*.html", recursive=True))
print(f"Found {len(html_files)} HTML files")

# ── 3. Inject ────────────────────────────────────────────────────────────────
aside_re = re.compile(r'(<aside class="notes">)(.*?)(</aside>)', re.DOTALL)

for idx, fpath in enumerate(html_files):
    slide_num = idx + 1
    if slide_num not in speech:
        print(f"  [SKIP] slide {slide_num} ({fpath})")
        continue

    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    if '<aside class="notes">' not in content:
        print(f"  [WARN] slide {slide_num} ({fpath}) — no <aside>")
        continue

    new_speech = speech[slide_num]
    
    pattern = '\n' + '-' * 10 + '\n'

    def replacer(m, _text=new_speech):
        existing = m.group(2).strip()
        if pattern in existing:
            before = existing.split(pattern)[0].strip()
        else:
            before = existing
        return f'{m.group(1)}{before}{pattern}{_text}{m.group(3)}'

    updated = aside_re.sub(replacer, content)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(updated)

    print(f"  [OK]   slide {slide_num} → {fpath}")

print("Done.")
