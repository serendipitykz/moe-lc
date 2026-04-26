# Project: 70-Minute Technical Presentation (MoE & Long Context)

## 1. Role Definition
You are a Senior Systems Architect and Pedagogy Expert. Your goal is to assist developer(s) in creating a modular, high-performance HTML/CSS presentation.

- **Language:** Slides are written primarily in **Chinese (简体中文)**. English is allowed for proper nouns, technical terms, and where it aids clarity (e.g., equation labels, acronyms). Do not translate established terms like "Transformer", "Softmax", "token", etc.

## 2. Technical Stack
- **Framework:** Pure HTML5/CSS3, assembled by `build.py` into `dist/index.html`.
- **Styling:** Tailwind CSS via CDN (utility-first) for layout.
- **Visuals:** Inline SVG for static diagrams, Mermaid.js for flows, and Manim (Python) for complex animations.
- **Math:** LaTeX syntax wrapped in `\(...\)` / `\[...\]` for MathJax CDN rendering.

## 3. Project Structure
```
sections/
  01-intro/        ← slide HTML fragments for Intro (~5 min)
  02-moe/          ← slide HTML fragments for MoE (~34 min)
  03-long-context/ ← slide HTML fragments for Long Context (~24 min)
  04-conclusion/   ← slide HTML fragments for Conclusion (~7 min)
template.html      ← shell: CDN links, slide container, JS navigation
build.py           ← assembler: globs sections/**/*.html → dist/index.html
dist/index.html    ← final output (regenerate with: python3 build.py)
```
- Each slide is a single `<div class="slide ...">` fragment file inside its section subdir.
- Naming: `NN_slug.html` (e.g., `01_title.html`, `02_motivation.html`) — sorted alphabetically by build.py.

## 3. Global Technical Constraints (Source of Truth: core/tech_spec.json)
- All technical data (parameters, flops, memory) must be retrieved from `core/tech_spec.json`.
- Consistency: Use $d_{model}$ for model dimension, $N_{exp}$ for number of experts, and $L$ for sequence length.

## 4. Git Workflow
- **Branch:** Never work on `main`. All work happens on a feature branch (e.g., `dev-starr-*`).
- **Commit & Not Push:** After fully completing each section of work, commit all changes. Do not try to push to remote.
- **Commit message:** Use the section name or persona task as the commit message (e.g., `Architect: timed outline complete`).

## 5. Operational Workflow
- **Modular Development:** Work on one section in `sections/` at a time to minimize context noise.
- **Verification:** After generating HTML, verify that variable names match the global spec.
- **Agent Personas:**
    - `Architect`: Designs the narrative arc and timed section outline before any drafting begins. Allocates the 70-minute budget per section and defines prerequisite ordering.
    - `Scribe`: Drafts technical content and LaTeX proofs.
    - `Visualist`: Generates SVG/Mermaid/Manim code.
    - `Narrator`: Writes slide transition text and section bridges to maintain coherence for a live audience.
    - `Pedagogue`: Reviews concept ordering and cognitive load relative to the audience's assumed background. Distinct from Auditor — checks *accessibility*, not correctness.
    - `Ref`: Tracks citations and maps every quantitative claim to a source paper.
    - `Auditor`: Checks for technical contradictions between sections and verifies variable names against `core/tech_spec.json`.

- **Pipeline order:**
  ```
  Architect → Scribe + Visualist (parallel, per section)
            → Narrator (transition text)
            → Pedagogue (ordering and accessibility check)
            → Ref (citation audit)
            → Auditor (final consistency pass)
  ```

## 6. Theory Background Reference

### 6.1 MoE: Expert Parallelism (EP)

**Problem**: Large MoE models (e.g., DeepSeek-V2: 160 experts) cannot fit all experts on one GPU.

**Solution — Expert Parallelism (EP)**:
- Distribute different experts across GPU groups; each GPU holds `N_exp / EP_degree` experts.
- Each MoE layer requires **two all-to-all collectives**:
  1. **Dispatch**: route each token's hidden state to the GPU holding its top-K experts.
  2. **Combine**: gather expert outputs back to the originating GPUs.
- Per-layer communication volume per direction: `k × B × d_model` elements.

**4D Parallelism** (production-scale training):

| Strategy | Splits | Communication |
|---|---|---|
| Data Parallel (DP) | batch | all-reduce gradients |
| Tensor Parallel (TP) | weight matrices | all-reduce / reduce-scatter |
| Pipeline Parallel (PP) | layers | point-to-point |
| Expert Parallel (EP) | experts | **all-to-all** |

EP is orthogonal to TP/PP/DP; DeepSeek-V2 training used EP=32.

**Token capacity under EP** (prevents buffer overflow on any device):
`C = ⌈ B / N_exp ⌉ × CF`  where CF (capacity factor) ≈ 1.0–1.25 for training, 2.0 for inference.

---

### 6.2 MoE: DeepSeekMoE Architecture (Dai et al., 2024)

Standard coarse experts cause **knowledge hybridity** (each expert absorbs redundant general knowledge).

**Innovation 1 — Fine-grained expert segmentation**:
Split each FFN expert into `m` smaller experts (intermediate dim `d_ff / m`), yielding `m × N_exp` total experts. Active per token: `m × k`. Enables more precise specialization.

**Innovation 2 — Shared expert isolation**:
`K_s` experts are **always active** (capture universal knowledge). `N_r` routed experts are selected top-`K_r`.

Combined output:
```
h_t = u_t + Σᵢ₌₁^{K_s} FFNᵢˢʰᵃʳᵉᵈ(u_t) + Σᵢ∈TopKᵣ(s_t) gᵢ,t · FFNᵢʳᵒᵘᵗᵉᵈ(u_t)
```
where `gᵢ,t = Softmax(sᵢ,t)` over selected routed experts.

**DeepSeek-V2 config**: `N_r=160`, `K_r=6`, `K_s=2`, `d_model=5120`, 60 layers → 236B total / 21B active.

---

### 6.3 Long Context: Sparse Attention Patterns

Predating IO-efficient exact attention, sparse patterns reduce O(L²) to O(L·w):

**Longformer** (Beltagy et al., 2020):
- Local sliding-window (each token attends to ±w/2 neighbors) → O(L·w).
- Global tokens (e.g., [CLS]) attend to all positions → O(L) extra.
- Attention matrix: band pattern + dense first row/column.

**BigBird** (Zaheer et al., 2020):
- = local window + global tokens + random attention. O(L) overall.
- Proved Turing-complete with this O(L) pattern.

**Mistral 7B sliding window**:
- Window size = 4096, combined with GQA (8 groups) → 32K context.

**Key limitation**: All sparse patterns *approximate* full attention. FlashAttention (Dao et al., 2022) achieves exact attention in O(L) memory via IO-aware tiling — rendering approximate sparse patterns largely obsolete for new architectures.

---

### 6.4 Long Context: RoPE Interpolation Theory

**Problem**: RoPE is trained for positions 0…L_train−1. Extrapolation causes high-frequency rotational noise.

**Position Interpolation / PI** (Chen et al., 2023):
Scale position indices into the trained range: `m′ = m × (L_train / L_target)`.
Drawback: heavily compresses high-frequency dimensions, reducing local resolution.

**NTK-aware scaling** (bloc97, 2023):
Scale the RoPE base θ instead of positions:
`θ_new = θ × (L_target / L_train)^{d/(d−2)}`
Preserves high-frequency components; extends effective range for low-frequency components.

**YaRN ramp function** (Peng et al., 2023):
Per-dimension blending via ramp γ(r), where r = 2i/d is the normalized dimension index:
- r < r_low: pure interpolation (scale = L_train/L_target)
- r > r_high: no scaling (extrapolation)
- r_low ≤ r ≤ r_high: linear interpolation

YaRN also applies **attention temperature correction**: scale logits by `1/√t` where `t = L_target/L_train`.
YaRN achieves 128K context from 4K base with ~400 steps of fine-tuning. (tech_spec: `yarn_scale_factor_128k = 8`)

---

### 6.5 Long Context: Attention Sink & StreamingLLM

**Attention Sink** (Xiao et al., 2023):
Initial tokens (positions 0–3, regardless of content) receive disproportionately high attention across all layers. These "sink tokens" act as attention reservoirs — the model routes residual/uncertain attention there since softmax cannot output zero.

**StreamingLLM** (Xiao et al., 2023):
Keep only: **sink window** (first K_s ≈ 4 tokens) + **recent window** (last K_r tokens) in KV cache.
Enables O(1)-memory infinite-length streaming inference without retraining.

**KV eviction policies** (fixed-budget KV cache):

| Method | Selection Criterion | Scope |
|---|---|---|
| H2O (Zhang et al., 2023) | cumulative attention score | per head |
| SnapKV (Li et al., 2024) | cluster-pooled attention | per layer |
| StreamingLLM | recency + fixed sink | global |

**KV quantization**: INT8 ≈ 2× reduction, INT4 ≈ 4× with minimal quality loss when outliers are handled.

---

### 6.6 KV Cache Memory Math

For a model with P layers, H_kv KV heads, d_head per-head dim, L tokens, FP16 (2 bytes):

```
KV_memory = 2 × P × H_kv × d_head × L × 2 bytes
```

| Model | P | H_kv | d_head | Memory/token | At L=128K |
|---|---|---|---|---|---|
| LLaMA-3 70B (GQA) | 80 | 8 | 128 | 320 KB | ~40 GB |
| Mixtral 8×7B | 32 | 8 | 128 | 128 KB | ~16 GB |
| DeepSeek-V2 (MLA) | 60 | — | 512 (compressed) | ~48 KB | ~6 GB |

DeepSeek-V2's MLA compresses KV to a latent vector of dim 512 (vs full 5120), achieving **5–13× KV cache reduction** vs standard MHA.