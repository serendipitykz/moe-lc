# SII.md — MoE & Long Context Presentation

## Init Notes

**Date:** 2026-04-21  
**Branch:** `dev-claude-starry`  
**Author:** StarryPurple  

### What This Repo Is

A **pure-HTML slide deck** for the ACM Class 2026 Spring course *Large Language Models* (CS2916-01). The presentation covers **Mixture of Experts (MoE)** and **Long Context** techniques. Target duration: ~45 minutes. Primary language: Chinese with English technical terms.

This is **not** a software project — there is no build system, no package.json, no runtime dependencies. The deliverable is a static HTML presentation opened directly in a browser.

### Repo Layout

```
.
├── reference/           # The actual slide deck (production)
│   ├── index.html       # 21 slides, ~1007 lines
│   ├── style.css        # Theme A stylesheet, ~576 lines
│   ├── nav.js           # Keyboard/button navigation + progress bar
│   ├── MoeRef.pdf       # Reference paper (MoE)
│   └── LongContextRef.pdf  # Reference paper (Long Context)
├── preference/
│   └── starry.md        # Theme choice + design preferences (Theme A: Light Gray + Indigo)
├── tmp/                 # Theme prototypes (theme-a/b/c.html) — not used in production
├── CLAUDE.md            # Instructions for Claude Code (also applicable here)
├── README.md            # One-liner project description
└── .gitignore           # Ignores .codex/, .cursor/, .sii/, .claude/
```

### Slide Deck Structure (21 slides)

| #  | Topic |
|----|-------|
| 1  | Title |
| 2  | Agenda |
| 3  | Scaling Laws |
| 4  | Dense vs Sparse |
| 5  | MoE Core Mechanism |
| 6  | Load Balancing |
| 7  | Mixtral 8×7B |
| 8  | Section: Long Context |
| 9  | Why Attention Struggles |
| 10 | RoPE & Positional Encoding |
| 11 | Efficient Attention |
| 12 | Sparse Attention Techniques |
| 13 | Context Window Timeline |
| 14 | Section: MoE × Long Context |
| 15 | MoE × Long Context Challenges |
| 16 | DeepSeek-V2 Case Study |
| 17 | Section: Demo |
| 18 | Demo — Needle in a Haystack |
| 19 | Section: Critical Hypotheses |
| 20 | Critical Hypotheses |
| 21 | References |

> **Note:** Slide numbering in HTML comments has minor duplicates (two "13"s, two "16"s, two "18"s) — the actual rendered order is sequential 1–21.

### Design & Theme

- **Theme A** selected: Light gray background (`#f0f2f6`), indigo left rail (`#4f46e5`), white cards
- Fonts: Inter + Noto Sans SC
- Math: KaTeX with `$...$` (inline) and `$$...$$` (display)
- Navigation: arrow keys, spacebar, on-screen prev/next buttons, `N` key toggles speaker notes
- Speaker notes present on all slides (Chinese speech text)

### Key Conventions (from CLAUDE.md)

1. **Separate styles from content** — CSS in `style.css`, content in `index.html`
2. **Image attribution** — record source URLs alongside any downloaded images
3. **Never develop on `main`** — always work on feature branches
4. **Incremental generation** — produce a few slides at a time, pause for review
5. **Don't overload slides** — keep content density manageable

### AI Tool Configs

- `.codex/config.toml` — Codex configured with `gpt-4o`
- `.claude/` — Claude Code settings present
- `.cursor/` — Cursor IDE settings present
- The full AI interaction history is part of the course submission

### References (PDFs)

Two reference PDFs in `reference/`:
- `MoeRef.pdf` — MoE reference paper
- `LongContextRef.pdf` — Long Context reference paper

### Risks & Observations

1. **Slide comment numbering mismatch** — HTML comments show duplicate numbers (13, 16, 18); cosmetic only but could cause confusion during editing.
2. **No local asset fallback** — KaTeX is loaded from CDN (`cdn.jsdelivr.net`); presentation requires internet or a cached copy.
3. **No images yet** — The deck appears to be text/formula/table-only; CLAUDE.md encourages hand-made graphs, timelines, and diagrams.
4. **tmp/ prototypes** — Three theme HTML files exist but are not referenced; safe to ignore.

### Immediate Next Steps

- Ask the user what they'd like to work on: adding visual diagrams, refining content, fixing the comment numbering, or something else.
- If adding images/diagrams, establish an `assets/` directory with attribution tracking per CLAUDE.md.
- Consider adding a KaTeX local fallback for offline presentation.
