# Slide Theme Preference — StarryPurple

**Chosen theme:** Theme A — Light Gray + Indigo Left Rail (`tmp/theme-a.html`)

## Design characteristics
- Background: cool light gray (`#f0f2f6`)
- Left rail: indigo (`#4f46e5`), 68px wide, shows slide number and vertical progress bar
- Cards: white with subtle border
- Accent: indigo, highlight tint `#eef2ff`
- Typography: Inter + Noto Sans SC, body at 1.45rem

## Math rendering
- KaTeX for inline and display math
- Delimiters: `$...$` for inline, `$$...$$` for display
- No raw subscript text like `N_act`; use proper $N_{\text{act}}$ notation
- Formula blocks: light neutral background (`#f8fafc`) with a subtle border — **not** colored/tinted

## Content style
- Hand-made graphs encouraged: timelines (for evolution/history), HTML tables (for comparisons), attention pattern grids, diagrams with CSS boxes and arrows
- Concrete examples or mini-annotations recommended alongside bullet descriptions (e.g. a side panel or inline callout with a specific number / model name)

## Git workflow notes
- `git push` to GitHub occasionally fails with `GnuTLS recv error (-110): The TLS connection was non-properly terminated.` — simply retry the push immediately; it succeeds on the next attempt.
