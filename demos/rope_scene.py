from manimlib import *
import numpy as np

BG       = "#111827"
EMERALD  = "#10b981"
AMBER    = "#f59e0b"
GRAY_TXT = "#9ca3af"
DARK_BOX = "#1f2937"
BORDER   = "#374151"


class RoPEScene(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Title ────────────────────────────────────────────────────────────
        title = Text("RoPE: Rotary Position Embedding", font_size=38, color=EMERALD)
        sub   = Text("Position encoded as rotation angle", font_size=22, color=GRAY_TXT)
        sub.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.5)
        self.wait(0.6)
        self.play(title.animate.scale(0.55).to_corner(UL, buff=0.35),
                  FadeOut(sub))

        # ── Token sequence ───────────────────────────────────────────────────
        tok_words  = ["The", "cat", "sat", "on"]
        tok_colors = [EMERALD, "#34d399", "#6ee7b7", "#a7f3d0"]

        tok_group = VGroup()
        for i, (w, c) in enumerate(zip(tok_words, tok_colors)):
            box = Rectangle(width=1.1, height=0.58,
                            fill_color=DARK_BOX, fill_opacity=1,
                            stroke_color=BORDER, stroke_width=1.5)
            txt = Text(w, font_size=20, color=WHITE)
            pos = Text(f"m = {i}", font_size=14, color=c)
            txt.move_to(box)
            pos.next_to(box, DOWN, buff=0.12)
            tok_group.add(VGroup(box, txt, pos))

        tok_group.arrange(RIGHT, buff=0.5)
        tok_group.move_to(UP * 2.2)
        self.play(LaggedStart(*[FadeIn(t) for t in tok_group], lag_ratio=0.2),
                  run_time=1.2)
        self.wait(0.4)

        # ── Unit circle ──────────────────────────────────────────────────────
        CX = DOWN * 0.5
        R  = 1.9

        circle = Circle(radius=R, stroke_color=BORDER, stroke_width=1.5)
        circle.move_to(CX)
        h_ax = Line(CX + LEFT  * (R + 0.4), CX + RIGHT * (R + 0.4),
                    stroke_color="#4b5563", stroke_width=1.2)
        v_ax = Line(CX + DOWN  * (R + 0.4), CX + UP    * (R + 0.4),
                    stroke_color="#4b5563", stroke_width=1.2)
        ctr  = Dot(CX, radius=0.06, color="#6b7280")
        circ_lbl = Text("unit circle", font_size=16, color=GRAY_TXT)
        circ_lbl.next_to(circle, DOWN, buff=0.18)

        self.play(ShowCreation(circle), ShowCreation(h_ax), ShowCreation(v_ax),
                  FadeIn(ctr), FadeIn(circ_lbl))
        self.wait(0.3)

        THETA = PI / 4.5

        def vec_tip(m):
            angle = PI / 2 - m * THETA
            return CX + R * np.array([np.cos(angle), np.sin(angle), 0])

        # ── Draw q vectors for each token position ────────────────────────────
        drawn_vecs   = []
        drawn_labels = []
        prev_highlight = None

        for i in range(4):
            tip = vec_tip(i)
            direction = normalize(tip - CX)

            vec = Arrow(CX, tip, buff=0,
                        stroke_color=tok_colors[i], stroke_width=2.5,
                        fill_color=tok_colors[i])
            lbl = Tex(f"q_{{m={i}}}", font_size=20, color=tok_colors[i])
            lbl.move_to(tip + direction * 0.42)

            hi = SurroundingRectangle(tok_group[i], color=tok_colors[i],
                                      buff=0.06, stroke_width=2)
            anims = [ShowCreation(vec), Write(lbl), ShowCreation(hi)]
            if prev_highlight:
                anims.append(FadeOut(prev_highlight))

            self.play(*anims, run_time=0.65)
            drawn_vecs.append(vec)
            drawn_labels.append(lbl)
            prev_highlight = hi
            self.wait(0.25)

        self.play(FadeOut(prev_highlight))
        self.wait(0.3)

        # ── Relative angle arc between m=1 and m=3 ──────────────────────────
        a1 = PI / 2 - 1 * THETA
        a3 = PI / 2 - 3 * THETA

        arc = Arc(radius=0.55, start_angle=a3, angle=(a1 - a3),
                  arc_center=CX,
                  stroke_color=AMBER, stroke_width=2.5)
        arc_mid = (a1 + a3) / 2
        arc_lbl = Tex("m - n = 2", font_size=22, color=AMBER)
        arc_lbl.move_to(CX + 0.95 * np.array([np.cos(arc_mid),
                                               np.sin(arc_mid), 0]))

        self.play(ShowCreation(arc), Write(arc_lbl))
        self.wait(0.5)

        # ── Key insight ──────────────────────────────────────────────────────
        insight = Tex(
            r"\langle R_m q,\; R_n k \rangle",
            r"\text{ depends only on }",
            r"m - n",
            font_size=28
        )
        insight[0].set_color(EMERALD)
        insight[2].set_color(AMBER)

        ins_box = Rectangle(
            width=insight.get_width() + 0.8,
            height=insight.get_height() + 0.45,
            fill_color="#064e3b", fill_opacity=0.4,
            stroke_color=EMERALD, stroke_width=1.5
        )
        ins_box.to_edge(DOWN, buff=0.45)
        insight.move_to(ins_box)

        self.play(FadeIn(ins_box), Write(insight))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.3)
