from manimlib import *
import numpy as np

BG       = "#111827"
INDIGO   = "#818cf8"
EMERALD  = "#10b981"
AMBER    = "#f59e0b"
RED_DIM  = "#f87171"
GRAY_TXT = "#9ca3af"
DARK_BOX = "#1f2937"
BORDER   = "#374151"

CELL_COLORS = ["#064e3b", "#065f46", "#047857", "#059669", "#10b981"]


def cell_color_by_dist(dist, n=4):
    idx = max(0, (n - 1) - dist)
    return CELL_COLORS[min(idx, len(CELL_COLORS) - 1)]


class ALiBiScene(Scene):
    def construct(self):
        self.camera.background_color = BG
        N = 4

        # ── Title ────────────────────────────────────────────────────────────
        title = Text("ALiBi: Attention with Linear Biases", font_size=36,
                     color=INDIGO)
        sub   = Text("Linear bias replaces position vectors — extrapolates naturally",
                     font_size=20, color=GRAY_TXT)
        sub.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.6)
        self.play(title.animate.scale(0.55).to_corner(UL, buff=0.35),
                  FadeOut(sub))

        # ── Token sequence ───────────────────────────────────────────────────
        tok_words = ["tok0", "tok1", "tok2", "tok3"]
        tok_group = VGroup()
        for i, w in enumerate(tok_words):
            box = Rectangle(width=1.0, height=0.52,
                            fill_color=DARK_BOX, fill_opacity=1,
                            stroke_color=BORDER, stroke_width=1.5)
            txt = Text(w, font_size=18, color=WHITE)
            txt.move_to(box)
            tok_group.add(VGroup(box, txt))
        tok_group.arrange(RIGHT, buff=0.45)
        tok_group.to_edge(UP, buff=1.3)
        self.play(LaggedStart(*[FadeIn(t) for t in tok_group], lag_ratio=0.2),
                  run_time=1.0)
        self.wait(0.4)

        # ── Helper: 4x4 matrix mob ───────────────────────────────────────────
        CELL = 0.65
        GAP  = 0.06

        def make_matrix(values_fn, label_str, label_color, pos):
            cells = VGroup()
            for i in range(N):
                for j in range(N):
                    val_str, fill = values_fn(i, j)
                    sq = Square(side_length=CELL,
                                fill_color=fill, fill_opacity=0.90,
                                stroke_color="#111827", stroke_width=1.2)
                    txt = Text(val_str, font_size=14, color=WHITE)
                    txt.move_to(sq)
                    cells.add(VGroup(sq, txt))
            cells.arrange_in_grid(N, N, buff=GAP)
            cells.move_to(pos)
            lbl = Text(label_str, font_size=22, color=label_color)
            lbl.next_to(cells, UP, buff=0.28)
            return cells, lbl

        SLOPE = 0.25

        def qkt_fn(i, j):
            return "0.50", cell_color_by_dist(0, N)

        def bias_fn(i, j):
            d = abs(i - j)
            return f"{SLOPE * d:.2f}", CELL_COLORS[min(d, len(CELL_COLORS) - 1)]

        def score_fn(i, j):
            d = abs(i - j)
            return f"{0.50 - SLOPE * d:.2f}", cell_color_by_dist(d, N)

        # ── QK^T matrix ──────────────────────────────────────────────────────
        mat_qkt, lbl_qkt = make_matrix(qkt_fn, "QK^T", WHITE,
                                       LEFT * 3.6 + DOWN * 0.5)
        self.play(FadeIn(mat_qkt), Write(lbl_qkt))
        self.wait(0.5)

        # ── Bias matrix ──────────────────────────────────────────────────────
        minus = Text("-", font_size=38, color=WHITE)
        minus.move_to(LEFT * 1.8 + DOWN * 0.5)

        mat_bias, lbl_bias = make_matrix(bias_fn, "m|i-j|", RED_DIM,
                                         DOWN * 0.5)
        self.play(Write(minus))
        self.play(FadeIn(mat_bias), Write(lbl_bias))
        self.wait(0.6)

        # ── Result matrix ────────────────────────────────────────────────────
        eq = Text("=", font_size=38, color=WHITE)
        eq.move_to(RIGHT * 1.8 + DOWN * 0.5)

        mat_score, lbl_score = make_matrix(score_fn, "score", EMERALD,
                                           RIGHT * 3.6 + DOWN * 0.5)
        self.play(Write(eq))
        self.play(FadeIn(mat_score), Write(lbl_score))
        self.wait(0.7)

        # ── Highlight diagonal ───────────────────────────────────────────────
        diag_rects = VGroup()
        for i in range(N):
            rect = SurroundingRectangle(mat_score[i * N + i], color=AMBER,
                                        buff=0.04, stroke_width=2.5)
            diag_rects.add(rect)
        self.play(ShowCreation(diag_rects))
        self.wait(0.4)

        cap = Text("Diagonal = max score: penalty grows with distance |i-j|",
                   font_size=19, color=GRAY_TXT)
        cap.to_edge(DOWN, buff=0.45)
        self.play(Write(cap))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.3)
