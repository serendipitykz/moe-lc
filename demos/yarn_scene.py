from manimlib import *
import numpy as np

BG       = "#111827"
EMERALD  = "#10b981"
AMBER    = "#f59e0b"
GRAY_TXT = "#9ca3af"
DARK_BOX = "#1f2937"
BORDER   = "#374151"

N_BANDS = 10
D       = N_BANDS * 2


class YaRNScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ────────────────────────────────────────────────────────────
        title = Text("YaRN: NTK-aware RoPE Extension", font_size=36, color=EMERALD)
        sub   = Text("High-freq interpolation + low-freq extrapolation: 4K to 128K",
                     font_size=20, color=GRAY_TXT)
        sub.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.6)
        self.play(title.animate.scale(0.55).to_corner(UL, buff=0.35),
                  FadeOut(sub))

        # ── Layout constants ─────────────────────────────────────────────────
        BAR_W    = 0.55
        GAP      = 0.12
        MAX_H    = 3.2
        ORIGIN_Y = DOWN * 1.6
        DIVIDE   = N_BANDS // 2

        def bar_center(i):
            total = BAR_W + GAP
            left_edge = -(N_BANDS * total) / 2 + BAR_W / 2
            return RIGHT * (left_edge + i * total)

        # ── Manual axes ──────────────────────────────────────────────────────
        total_w = N_BANDS * (BAR_W + GAP) + 0.4
        baseline = Line(
            ORIGIN_Y + LEFT  * (total_w / 2),
            ORIGIN_Y + RIGHT * (total_w / 2),
            stroke_color="#6b7280", stroke_width=1.5
        )
        y_axis = Line(
            ORIGIN_Y + LEFT * (total_w / 2),
            ORIGIN_Y + LEFT * (total_w / 2) + UP * (MAX_H + 0.5),
            stroke_color="#6b7280", stroke_width=1.5
        )
        x_lbl = Text("Frequency components (low -> high)", font_size=17, color=GRAY_TXT)
        x_lbl.next_to(baseline, DOWN, buff=0.25)
        y_lbl = Text("Scale", font_size=17, color=GRAY_TXT)
        y_lbl.next_to(y_axis, LEFT, buff=0.15).rotate(PI / 2)

        scale1_mark = Line(
            ORIGIN_Y + LEFT  * (total_w / 2) + UP * MAX_H + LEFT  * 0.12,
            ORIGIN_Y + LEFT  * (total_w / 2) + UP * MAX_H + RIGHT * 0.12,
            stroke_color=GRAY_TXT, stroke_width=1.2
        )
        scale1_lbl = Text("1.0", font_size=15, color=GRAY_TXT)
        scale1_lbl.next_to(scale1_mark, LEFT, buff=0.08)

        self.play(ShowCreation(baseline), ShowCreation(y_axis),
                  FadeIn(x_lbl), FadeIn(y_lbl),
                  FadeIn(scale1_mark), FadeIn(scale1_lbl))
        self.wait(0.3)

        # ── Build bars ───────────────────────────────────────────────────────
        def make_bars(scales, colors):
            bars = VGroup()
            for i in range(N_BANDS):
                h = MAX_H * scales[i]
                bar = Rectangle(
                    width=BAR_W, height=h,
                    fill_color=colors[i], fill_opacity=0.80,
                    stroke_color=colors[i], stroke_width=1.0
                )
                bar.move_to(bar_center(i) + ORIGIN_Y + UP * h / 2)
                bars.add(bar)
            return bars

        bars_orig = make_bars([1.0] * N_BANDS, [EMERALD] * N_BANDS)
        ctx_lbl = Text("Original RoPE  (context = 4K)", font_size=20, color=EMERALD)
        ctx_lbl.to_edge(UP, buff=1.1)

        self.play(LaggedStart(*[FadeIn(b) for b in bars_orig], lag_ratio=0.08),
                  FadeIn(ctx_lbl), run_time=1.4)
        self.wait(0.8)

        # ── Low / high-freq divider ───────────────────────────────────────────
        div_x   = bar_center(DIVIDE - 0.5)
        div_bot = ORIGIN_Y + div_x
        div_top = ORIGIN_Y + UP * (MAX_H + 0.6) + div_x
        divider = DashedLine(div_bot, div_top,
                             dash_length=0.12, stroke_color="#4b5563",
                             stroke_width=1.5)

        low_lbl  = Text("low-freq", font_size=17, color=AMBER)
        high_lbl = Text("high-freq", font_size=17, color="#6ee7b7")
        low_lbl.move_to(bar_center(DIVIDE // 2 - 0.5) + ORIGIN_Y + UP * (MAX_H + 0.75))
        high_lbl.move_to(bar_center(DIVIDE + (N_BANDS - DIVIDE) // 2) + ORIGIN_Y + UP * (MAX_H + 0.75))

        self.play(ShowCreation(divider), FadeIn(low_lbl), FadeIn(high_lbl))
        self.wait(0.5)

        # ── Transform to YaRN scaling ─────────────────────────────────────────
        scales_yarn = [1.0 if i < DIVIDE else 0.35 for i in range(N_BANDS)]
        colors_yarn = [AMBER if i < DIVIDE else "#6ee7b7" for i in range(N_BANDS)]
        bars_yarn = make_bars(scales_yarn, colors_yarn)

        yarn_lbl = Text("YaRN  (context = 128K)", font_size=20, color=AMBER)
        yarn_lbl.move_to(ctx_lbl)

        self.play(
            *[Transform(bars_orig[i], bars_yarn[i]) for i in range(N_BANDS)],
            Transform(ctx_lbl, yarn_lbl),
            run_time=1.6
        )
        self.wait(0.8)

        # ── Annotation arrows ─────────────────────────────────────────────────
        low_arrow = Arrow(
            low_lbl.get_bottom() + DOWN * 0.1,
            bar_center(DIVIDE // 2 - 0.5) + ORIGIN_Y + UP * (MAX_H + 0.15),
            buff=0, stroke_color=AMBER, stroke_width=1.8, fill_color=AMBER
        )
        high_arrow = Arrow(
            high_lbl.get_bottom() + DOWN * 0.1,
            bar_center(DIVIDE + 1) + ORIGIN_Y + UP * (MAX_H * 0.35 + 0.15),
            buff=0, stroke_color="#6ee7b7", stroke_width=1.8, fill_color="#6ee7b7"
        )
        self.play(ShowCreation(low_arrow), ShowCreation(high_arrow))
        self.wait(0.4)

        # ── Caption ──────────────────────────────────────────────────────────
        cap_lo = Text("Low-freq: extrapolation (scale kept)", font_size=19, color=AMBER)
        cap_hi = Text("High-freq: interpolation (scale compressed)", font_size=19, color="#6ee7b7")
        VGroup(cap_lo, cap_hi).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        self.play(Write(cap_lo), Write(cap_hi))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.3)
