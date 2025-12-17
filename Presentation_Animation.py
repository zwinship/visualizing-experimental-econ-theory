from manim import *
import numpy as np

class EffortModel(Scene):
    # =============================
    # PARAMETERS - EDIT THESE
    # =============================
    F_COEFF = 5  # Coefficient for f(e) = F_COEFF * √e
    C_COEFF = 5  # Coefficient for c(e) = C_COEFF * e²
    SHARE = 0.5  # Share of production function in payoff

    QUICK_TEST = False  # Set to True for shorter test video

    # Behavioral parameters
    ALPHA = 0.25   # Altruism parameter
    LAMBDA = 1.4   # Loss aversion parameter

    def f(self, e):
        """Production function: F_COEFF√e"""
        if e < 0:
            return 0
        return self.F_COEFF * np.sqrt(e)

    def c(self, e):
        """Cost function: C_COEFF·e²"""
        return self.C_COEFF * e**2

    def payoff(self, e, k=1.0):
        """Payoff: k·F_COEFF√e - C_COEFF·e²"""
        if e <= 0:
            return 0
        return k * self.F_COEFF * np.sqrt(e) - self.C_COEFF * e**2

    def e_star(self, k):
        """
        Optimal effort from FOC: k·F_COEFF/(2√e) = 2·C_COEFF·e
        => e = (F_COEFF·k/(4·C_COEFF))^(2/3)
        """
        numerator = self.F_COEFF * k
        denominator = 4 * self.C_COEFF
        if denominator == 0 or numerator / denominator < 0:
            return 0
        return (numerator / denominator) ** (2 / 3)

    def construct(self):

        if self.QUICK_TEST:
            self.quick_test_mode()
            return

        # =============================
        # SECTION 1: Title
        # =============================
        title = Text("Theoretical Predictions Across Treatments").scale(0.8)
        self.play(Write(title), run_time=2.0)
        self.wait(1.5)
        self.play(title.animate.scale(0.7).to_edge(UP), run_time=1.3)

        # =============================
        # SECTION 2: Show total payoff formula
        # =============================
        payoff_intro = MathTex(
            f"\\text{{Total Payoff}} = 5 + {self.SHARE} \\cdot f(e) - c(e)"
        ).scale(1.1)

        self.play(Write(payoff_intro), run_time=2.0)
        self.wait(6.0)

        self.play(FadeOut(payoff_intro), run_time=1.2)

        # =============================
        # SECTION 3: Show f(e) and c(e) functional forms
        # =============================
        f_def = MathTex(f"f(e) = {self.F_COEFF}\\sqrt{{e}}", color=BLUE).scale(1.1).shift(UP * 1.2)
        f_text = Text("(production as a function of effort)", font_size=24, color=BLUE).next_to(
            f_def, DOWN, buff=0.3
        )

        c_def = MathTex(f"c(e) = {self.C_COEFF}e^2", color=RED).scale(1.1).shift(DOWN * 0.8)
        c_text = Text("(cost as a function of effort)", font_size=24, color=RED).next_to(
            c_def, DOWN, buff=0.3
        )

        self.play(Write(f_def), Write(f_text), run_time=2.0)
        self.wait(2.5)

        self.play(Write(c_def), Write(c_text), run_time=2.0)
        self.wait(2.5)

        # =============================
        # SECTION 4: Show gap concept visually
        # =============================
        self.play(
            FadeOut(f_text),
            FadeOut(c_text),
            f_def.animate.shift(UP * 0.3).scale(0.8),
            c_def.animate.shift(UP * 0.3).scale(0.8),
            run_time=1.5,
        )

        explanation = Text(
            "To find equilibrium, we maximize the gap: f(e) - c(e)",
            font_size=28,
        ).shift(DOWN * 2.5)

        self.play(Write(explanation), run_time=2.0)
        self.wait(1.0)

        # Clear and show graph
        self.play(
            FadeOut(f_def),
            FadeOut(c_def),
            FadeOut(explanation),
            run_time=1.2,
        )

        # Axes for f(e) and c(e) and the gap
        axes = Axes(
            x_range=[0, 1, 0.25],
            y_range=[0, 2, 0.5],
            x_length=7,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.3)

        x_labels = VGroup(
            MathTex("1").scale(0.7).next_to(axes.coords_to_point(1, 0), DOWN)
        )

        labels = axes.get_axis_labels(
            MathTex("e").scale(0.8),
            MathTex("").scale(0.8),
        )

        self.play(Create(axes), Write(labels), Write(x_labels), run_time=1)

        SCALE = 0.39

        # Draw curves
        f_graph = axes.plot(lambda e: self.f(e) * SCALE, color=BLUE, stroke_width=4)
        c_graph = axes.plot(lambda e: self.c(e) * SCALE, color=RED, stroke_width=4)

        # Labels scale automatically because coords_to_point uses the scaled values
        f_label = MathTex("f(e)", color=BLUE).scale(0.7).next_to(
            axes.coords_to_point(0.8, self.f(0.8) * SCALE), UP, buff=0.2
        )
        c_label = MathTex("c(e)", color=RED).scale(0.7).next_to(
            axes.coords_to_point(0.75, self.c(0.75) * SCALE), DOWN + RIGHT, buff=0.15
        )

        self.play(Create(f_graph), Write(f_label), run_time=1.2)
        self.play(Create(c_graph), Write(c_label), run_time=1.2)
        self.wait(0.5)

        # Smooth animated slider showing gap
        e_tracker = ValueTracker(0.1)

        gap_line = always_redraw(
            lambda: Line(
                axes.coords_to_point(e_tracker.get_value(), self.c(e_tracker.get_value()) * SCALE),
                axes.coords_to_point(e_tracker.get_value(), self.f(e_tracker.get_value()) * SCALE),
                color=YELLOW,
                stroke_width=4,
            )
        )

        gap_label = always_redraw(
            lambda: MathTex("Gap", color=YELLOW).scale(0.6).next_to(
                axes.coords_to_point(
                    e_tracker.get_value(),
                    (self.f(e_tracker.get_value()) * SCALE + self.c(e_tracker.get_value()) * SCALE) / 2,
                ),
                RIGHT,
                buff=0.2,
            )
        )

        self.play(Create(gap_line), Write(gap_label), run_time=1.0)

        # Move slider
        self.play(e_tracker.animate.set_value(0.8), run_time=1.8, rate_func=linear)
        e_optimal = self.e_star(1.0)
        self.play(e_tracker.animate.set_value(e_optimal), run_time=1.0, rate_func=linear)

        # Mark equilibrium (label only)
        e_equilibrium = self.e_star(1.0)
        e_marker = MathTex("e^*", color=YELLOW).scale(0.8).next_to(
            axes.coords_to_point(e_equilibrium, 0), DOWN, buff=0.3
        )
        self.play(Write(e_marker), run_time=1.5)

        # =============================
        # SECTION 5: Back to payoff formula
        # =============================
        self.play(
            FadeOut(axes),
            FadeOut(labels),
            FadeOut(x_labels),
            FadeOut(f_graph),
            FadeOut(c_graph),
            FadeOut(f_label),
            FadeOut(c_label),
            FadeOut(gap_line),
            FadeOut(gap_label),
            FadeOut(e_marker),
            run_time=1.5,
        )

        payoff_text = Text("Combining into total payoff:", font_size=32).shift(UP * 2)
        self.play(Write(payoff_text), run_time=1.5)

        # 1) Generic payoff with f(e) and c(e)
        payoff_formula = MathTex(
            f"\\text{{Payoff}} = {self.SHARE} \\cdot f(e) - c(e)"
        ).scale(0.9).shift(UP * 0.8)
        self.play(Write(payoff_formula), run_time=2.0)
        self.wait(1.5)

        # 2) New line: plug in functional forms (no awkward morph)
        substituted = MathTex(
            f"\\text{{Payoff}} = {self.SHARE}({self.F_COEFF}\\sqrt{{e}}) - {self.C_COEFF}e^2"
        ).scale(0.9)
        substituted.next_to(payoff_formula, DOWN, buff=0.5)

        self.play(Write(substituted), run_time=2.0)
        self.wait(1.5)

        # 3) Simplified numeric form
        benefit_coeff = self.SHARE * self.F_COEFF
        simplified = MathTex(
            f"\\text{{Payoff}} = {benefit_coeff:.2f}\\sqrt{{e}} - {self.C_COEFF}e^2"
        ).scale(0.95)
        simplified.next_to(substituted, DOWN, buff=0.5)

        self.play(Write(simplified), run_time=2.0)
        self.wait(3.0)

        # =============================
        # SECTION 6: Graph control payoff curve
        # =============================
        self.play(
            FadeOut(payoff_text),
            FadeOut(payoff_formula),
            FadeOut(substituted),
            run_time=1.5,
        )

        graph_text = Text("Control Group: Gain for Self", color=GREEN, font_size=30).shift(
            UP * 2.0
        )
        self.play(
            simplified.animate.scale(0.75).to_corner(UR).shift(DOWN * 0.5 + LEFT * 0.3),
            Write(graph_text),
            run_time=1.5,
        )

        axes_payoff = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.5)

        x_labels_p = VGroup(
            MathTex("1").scale(0.7).next_to(axes_payoff.coords_to_point(1, 0), DOWN)
        )

        labels_p = axes_payoff.get_axis_labels(
            MathTex("e").scale(0.8),
            MathTex("\\text{Payoff}").scale(0.8),
        )
        labels_p.next_to(axes_payoff.get_y_axis(), LEFT, buff=0.1)

        self.play(Create(axes_payoff), Write(labels_p), Write(x_labels_p), run_time=1.2)

        control_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=1.0),
            color=GREEN,
            stroke_width=4,
        )

        self.play(Create(control_curve), run_time=1.2)
        self.wait(1.5)

        e_control = self.e_star(1.0)
        control_line = DashedLine(
            axes_payoff.coords_to_point(e_control, 0),
            axes_payoff.coords_to_point(e_control, self.payoff(e_control, 1.0)),
            color=GREEN,
            stroke_width=3,
        )
        control_label = MathTex("e^*", color=GREEN).scale(0.65).next_to(
            axes_payoff.coords_to_point(e_control, 0), DOWN, buff=0.3
        )

        self.play(
            Create(control_line),
            Write(control_label),
            run_time=2.0,
        )
        self.wait(1.0)

        # =============================
        # SECTION 7: Altruism - formula
        # =============================
        self.play(
            FadeOut(control_curve),
            FadeOut(control_line),
            FadeOut(control_label),
            FadeOut(axes_payoff),
            FadeOut(labels_p),
            FadeOut(x_labels_p),
            FadeOut(simplified),
            run_time=1.5,
        )

        alt_title = Text("Altruism: Gain for Teammate", color=BLUE, font_size=30).shift(
            UP * 2.0
        )
        self.play(Transform(graph_text, alt_title), run_time=1.5)
        self.wait(0.8)

        alpha_explanation = Text(
            "When you work for your teammate's bonus:",
            font_size=28,
        ).shift(UP * 1.2)
        self.play(Write(alpha_explanation), run_time=2.0)
        self.wait(0.8)

        benefit_coeff = self.SHARE * self.F_COEFF
        alpha_formula = MathTex(
            f"\\text{{Payoff}} = \\alpha \\cdot {benefit_coeff:.2f}\\sqrt{{e}} - {self.C_COEFF}e^2"
        ).scale(0.95).shift(UP * 0.2)
        self.play(Write(alpha_formula), run_time=2.0)
        self.wait(2)

        alpha_value = MathTex(
            f"\\text{{where }} \\alpha < 1 \\text{{ (we expect }} \\alpha = {self.ALPHA})"
        ).scale(0.8).shift(DOWN * 0.6)
        self.play(Write(alpha_value), run_time=2.0)
        self.wait(1.5)

        shift_explanation = Text(
            "This shifts the curve down and moves equilibrium left",
            font_size=26,
            color=BLUE,
        ).shift(DOWN * 1.5)
        self.play(Write(shift_explanation), run_time=2.0)
        self.wait(3)

        # =============================
        # SECTION 8: Show altruism curve
        # =============================
        self.play(
            FadeOut(alpha_explanation),
            FadeOut(alpha_formula),
            FadeOut(alpha_value),
            FadeOut(shift_explanation),
            run_time=1.2,
        )

        axes_payoff = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.5)

        x_labels_p = VGroup(
            MathTex("1").scale(0.7).next_to(axes_payoff.coords_to_point(1, 0), DOWN)
        )

        labels_p = axes_payoff.get_axis_labels(
            MathTex("e").scale(0.8),
            MathTex("\\text{Payoff}").scale(0.8),
        )
        labels_p.next_to(axes_payoff.get_y_axis(), LEFT, buff=0.1)

        self.play(Create(axes_payoff), Write(labels_p), Write(x_labels_p), run_time=1.2)

        control_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=1.0),
            color=GREEN,
            stroke_width=3,
            stroke_opacity=0.5,
        )
        control_label_ref = Text("Control", color=GREEN, font_size=20).to_corner(UR).shift(
            DOWN * 1.2 + LEFT * 0.3
        )

        self.play(Create(control_curve), Write(control_label_ref), run_time=1.2)
        self.wait(0.8)

        alt_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=self.ALPHA),
            color=BLUE,
            stroke_width=4,
        )

        self.play(
            ReplacementTransform(control_curve.copy(), alt_curve),
            run_time=3.0,
        )
        self.wait(1.5)

        e_alt = self.e_star(self.ALPHA)
        alt_line = DashedLine(
            axes_payoff.coords_to_point(e_alt, 0),
            axes_payoff.coords_to_point(e_alt, self.payoff(e_alt, self.ALPHA)),
            color=BLUE,
            stroke_width=3,
        )
        alt_label = MathTex("e^*", color=BLUE).scale(0.65).next_to(
            axes_payoff.coords_to_point(e_alt, 0), DOWN, buff=0.3
        )

        e_control = self.e_star(1.0)
        control_line_ref2 = DashedLine(
            axes_payoff.coords_to_point(e_control, 0),
            axes_payoff.coords_to_point(e_control, self.payoff(e_control, 1.0)),
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5,
        )
        control_label_ref2 = MathTex("e^*", color=GREEN).scale(0.6).next_to(
            axes_payoff.coords_to_point(e_control, 0), DOWN, buff=0.8
        )

        self.play(
            Create(alt_line),
            Write(alt_label),
            Create(control_line_ref2),
            Write(control_label_ref2),
            run_time=2.5,
        )
        self.wait(1.0)

        # =============================
        # SECTION 9: Loss Aversion - formula
        # =============================
        self.play(
            FadeOut(control_curve),
            FadeOut(alt_curve),
            FadeOut(alt_line),
            FadeOut(alt_label),
            FadeOut(control_line_ref2),
            FadeOut(control_label_ref2),
            FadeOut(control_label_ref),
            FadeOut(axes_payoff),
            FadeOut(labels_p),
            FadeOut(x_labels_p),
            run_time=1.5,
        )

        loss_title = Text("Loss Aversion: Loss for Self", color=RED, font_size=30).shift(
            UP * 2.0
        )
        self.play(Transform(graph_text, loss_title), run_time=1.5)
        self.wait(0.8)

        lambda_explanation = Text(
            "When you frame as avoiding losses:",
            font_size=28,
        ).shift(UP * 1.2)
        self.play(Write(lambda_explanation), run_time=2.0)
        self.wait(0.8)

        benefit_coeff = self.SHARE * self.F_COEFF
        lambda_formula = MathTex(
            f"\\text{{Payoff}} = \\lambda \\cdot {benefit_coeff:.2f}\\sqrt{{e}} - {self.C_COEFF}e^2"
        ).scale(0.95).shift(UP * 0.2)
        self.play(Write(lambda_formula), run_time=2.0)
        self.wait(2)

        lambda_value = MathTex(
            f"\\text{{where }} \\lambda > 1 \\text{{ (we expect }} \\lambda = {self.LAMBDA})"
        ).scale(0.8).shift(DOWN * 0.6)
        self.play(Write(lambda_value), run_time=2.0)
        self.wait(2)

        shift_explanation2 = Text(
            "This shifts the curve up and moves equilibrium right",
            font_size=26,
            color=RED,
        ).shift(DOWN * 1.5)
        self.play(Write(shift_explanation2), run_time=2.0)
        self.wait(3)

        # =============================
        # SECTION 10: Show loss aversion curve
        # =============================
        self.play(
            FadeOut(lambda_explanation),
            FadeOut(lambda_formula),
            FadeOut(lambda_value),
            FadeOut(shift_explanation2),
            run_time=1.2,
        )

        axes_payoff = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.5)

        x_labels_p = VGroup(
            MathTex("1").scale(0.7).next_to(axes_payoff.coords_to_point(1, 0), DOWN)
        )

        labels_p = axes_payoff.get_axis_labels(
            MathTex("e").scale(0.8),
            MathTex("\\text{Payoff}").scale(0.8),
        )
        labels_p.next_to(axes_payoff.get_y_axis(), LEFT, buff=0.1)

        self.play(Create(axes_payoff), Write(labels_p), Write(x_labels_p), run_time=1.2)

        control_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=1.0),
            color=GREEN,
            stroke_width=3,
            stroke_opacity=0.5,
        )
        control_label_ref = Text("Control", color=GREEN, font_size=20).to_corner(UR).shift(
            DOWN * 1.2 + LEFT * 0.3
        )

        self.play(Create(control_curve), Write(control_label_ref), run_time=1.2)
        self.wait(0.8)

        loss_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=self.LAMBDA),
            color=RED,
            stroke_width=4,
        )

        self.play(
            ReplacementTransform(control_curve.copy(), loss_curve),
            run_time=3.0,
        )
        self.wait(1.5)

        e_loss = self.e_star(self.LAMBDA)
        loss_line = DashedLine(
            axes_payoff.coords_to_point(e_loss, 0),
            axes_payoff.coords_to_point(e_loss, self.payoff(e_loss, self.LAMBDA)),
            color=RED,
            stroke_width=3,
        )
        loss_label = MathTex("e^*", color=RED).scale(0.65).next_to(
            axes_payoff.coords_to_point(e_loss, 0), DOWN, buff=0.8
        )

        control_line_ref2 = DashedLine(
            axes_payoff.coords_to_point(e_control, 0),
            axes_payoff.coords_to_point(e_control, self.payoff(e_control, 1.0)),
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5,
        )
        control_label_ref2 = MathTex("e^*", color=GREEN).scale(0.6).next_to(
            axes_payoff.coords_to_point(e_control, 0), DOWN, buff=0.3
        )

        self.play(
            Create(loss_line),
            Write(loss_label),
            Create(control_line_ref2),
            Write(control_label_ref2),
            run_time=2.5,
        )
        self.wait(1.0)

        # =============================
        # SECTION 11: Combined - formula
        # =============================
        self.play(
            FadeOut(control_curve),
            FadeOut(loss_curve),
            FadeOut(loss_line),
            FadeOut(loss_label),
            FadeOut(control_line_ref2),
            FadeOut(control_label_ref2),
            FadeOut(control_label_ref),
            FadeOut(axes_payoff),
            FadeOut(labels_p),
            FadeOut(x_labels_p),
            run_time=1.5,
        )

        comb_title = Text("Combined: Loss for Teammate", color=PURPLE, font_size=30).shift(
            UP * 2.0
        )
        self.play(Transform(graph_text, comb_title), run_time=1.5)
        self.wait(0.8)

        comb_explanation = Text("Both effects together:", font_size=28).shift(UP * 1.2)
        self.play(Write(comb_explanation), run_time=2.0)
        self.wait(0.8)

        benefit_coeff = self.SHARE * self.F_COEFF
        comb_formula = MathTex(
            f"\\text{{Payoff}} = \\lambda \\alpha \\cdot {benefit_coeff:.2f}\\sqrt{{e}} - {self.C_COEFF}e^2"
        ).scale(0.95).shift(UP * 0.2)
        self.play(Write(comb_formula), run_time=2.0)
        self.wait(2)

        k_combined = self.LAMBDA * self.ALPHA
        comb_value = MathTex(
            f"\\text{{where }} \\lambda \\alpha = {k_combined:.2f}"
        ).scale(0.8).shift(DOWN * 0.6)
        self.play(Write(comb_value), run_time=2.0)
        self.wait(2)

        shift_explanation3 = Text(
            "Intermediate effect: between altruism and control",
            font_size=26,
            color=PURPLE,
        ).shift(DOWN * 1.5)
        self.play(Write(shift_explanation3), run_time=2.0)
        self.wait(3)

        # =============================
        # SECTION 12: Show combined curve
        # =============================
        self.play(
            FadeOut(comb_explanation),
            FadeOut(comb_formula),
            FadeOut(comb_value),
            FadeOut(shift_explanation3),
            run_time=1.2,
        )

        axes_payoff = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.5)

        x_labels_p = VGroup(
            MathTex("1").scale(0.7).next_to(axes_payoff.coords_to_point(1, 0), DOWN)
        )

        labels_p = axes_payoff.get_axis_labels(
            MathTex("e").scale(0.8),
            MathTex("\\text{Payoff}").scale(0.8),
        )
        labels_p.next_to(axes_payoff.get_y_axis(), LEFT, buff=0.1)

        self.play(Create(axes_payoff), Write(labels_p), Write(x_labels_p), run_time=1.2)

        control_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=1.0),
            color=GREEN,
            stroke_width=3,
            stroke_opacity=0.5,
        )
        control_label_ref = Text("Control", color=GREEN, font_size=20).to_corner(UR).shift(
            DOWN * 1.2 + LEFT * 0.3
        )

        self.play(Create(control_curve), Write(control_label_ref), run_time=1.2)
        self.wait(0.8)

        comb_curve = axes_payoff.plot(
            lambda e: self.payoff(e, k=k_combined),
            color=PURPLE,
            stroke_width=4,
        )

        self.play(
            ReplacementTransform(control_curve.copy(), comb_curve),
            run_time=3.0,
        )
        self.wait(1.5)

        e_comb = self.e_star(k_combined)
        comb_line = DashedLine(
            axes_payoff.coords_to_point(e_comb, 0),
            axes_payoff.coords_to_point(e_comb, self.payoff(e_comb, k_combined)),
            color=PURPLE,
            stroke_width=3,
        )
        comb_label = MathTex("e^*", color=PURPLE).scale(0.65).next_to(
            axes_payoff.coords_to_point(e_comb, 0), DOWN, buff=0.3
        )

        control_line_ref2 = DashedLine(
            axes_payoff.coords_to_point(e_control, 0),
            axes_payoff.coords_to_point(e_control, self.payoff(e_control, 1.0)),
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5,
        )
        control_label_ref2 = MathTex("e^*", color=GREEN).scale(0.6).next_to(
            axes_payoff.coords_to_point(e_control, 0), DOWN, buff=0.8
        )

        self.play(
            Create(comb_line),
            Write(comb_label),
            Create(control_line_ref2),
            Write(control_label_ref2),
            run_time=2.5,
        )
        self.wait(2.0)

        self.play(
            FadeOut(control_curve),
            FadeOut(comb_curve),
            FadeOut(comb_line),
            FadeOut(comb_label),
            FadeOut(control_line_ref2),
            FadeOut(control_label_ref2),
            FadeOut(control_label_ref),
            run_time=1.5,
        )

        # =============================
        # SECTION 13 — Final Comparison of All Four Treatments
        # =============================
        final_title = Text("Predicted Effort Ranking", font_size=36).shift(UP * 2.0)
        self.play(Transform(graph_text, final_title), run_time=1.5)
        self.wait(1.5)

        # --- Draw all four payoff curves ---
        control_curve_final = axes_payoff.plot(
            lambda e: self.payoff(e, k=1.0), color=GREEN, stroke_width=4
        )
        alt_curve_final = axes_payoff.plot(
            lambda e: self.payoff(e, k=self.ALPHA), color=BLUE, stroke_width=4
        )
        loss_curve_final = axes_payoff.plot(
            lambda e: self.payoff(e, k=self.LAMBDA), color=RED, stroke_width=4
        )

        k_combined = self.LAMBDA * self.ALPHA
        comb_curve_final = axes_payoff.plot(
            lambda e: self.payoff(e, k=k_combined), color=PURPLE, stroke_width=4
        )

        self.play(
            Create(control_curve_final),
            Create(alt_curve_final),
            Create(loss_curve_final),
            Create(comb_curve_final),
            run_time=3.0
        )
        self.wait(1.2)

        # --- Compute equilibria ---
        e_control = self.e_star(1.0)
        e_alt     = self.e_star(self.ALPHA)
        e_loss    = self.e_star(self.LAMBDA)
        e_comb    = self.e_star(k_combined)

        # --- Create equilibrium vertical dashed lines ---
        line_control_final = DashedLine(
            axes_payoff.coords_to_point(e_control, 0),
            axes_payoff.coords_to_point(e_control, self.payoff(e_control, 1.0)),
            color=GREEN,
            stroke_width=3
        )
        line_alt_final = DashedLine(
            axes_payoff.coords_to_point(e_alt, 0),
            axes_payoff.coords_to_point(e_alt, self.payoff(e_alt, self.ALPHA)),
            color=BLUE,
            stroke_width=3
        )
        line_loss_final = DashedLine(
            axes_payoff.coords_to_point(e_loss, 0),
            axes_payoff.coords_to_point(e_loss, self.payoff(e_loss, self.LAMBDA)),
            color=RED,
            stroke_width=3
        )
        line_comb_final = DashedLine(
            axes_payoff.coords_to_point(e_comb, 0),
            axes_payoff.coords_to_point(e_comb, self.payoff(e_comb, k_combined)),
            color=PURPLE,
            stroke_width=3
        )

        self.play(
            Create(line_control_final),
            Create(line_alt_final),
            Create(line_loss_final),
            Create(line_comb_final),
            run_time=2.0
        )
        self.wait(1.0)

        # --- e* labels placed LOW on x-axis to avoid curve overlap ---
        label_y_offset = -0.35  # pushes labels down to avoid curve collisions

        label_control_final = MathTex("e^*", color=GREEN).scale(0.7).next_to(
            axes_payoff.coords_to_point(e_control, 0), DOWN, buff=abs(label_y_offset)
        )
        label_alt_final = MathTex("e^*", color=BLUE).scale(0.7).next_to(
            axes_payoff.coords_to_point(e_alt, 0), DOWN, buff=abs(label_y_offset)
        )
        label_loss_final = MathTex("e^*", color=RED).scale(0.7).next_to(
            axes_payoff.coords_to_point(e_loss, 0), DOWN, buff=abs(label_y_offset)
        )
        label_comb_final = MathTex("e^*", color=PURPLE).scale(0.7).next_to(
            axes_payoff.coords_to_point(e_comb, 0), DOWN, buff=abs(label_y_offset)
        )

        self.play(
            Write(label_control_final),
            Write(label_alt_final),
            Write(label_loss_final),
            Write(label_comb_final),
            run_time=2.0
        )
        self.wait(1.2)

        # --- Legend: Only treatment names, in curve colors ---
        legend = VGroup(
            Text("Control", font_size=24, color=GREEN),
            Text("Altruism", font_size=24, color=BLUE),
            Text("Loss Aversion", font_size=24, color=RED),
            Text("Combined", font_size=24, color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL).shift(DOWN * 0.3 + RIGHT * 0.2)

        self.play(FadeIn(legend), run_time=1.6)
        self.wait(3.0)

    def quick_test_mode(self):
        """Short test showing all 4 curves at once."""
        title = Text("Effort Model Test").scale(0.6).to_edge(UP)
        self.add(title)

        axes = Axes(
            x_range=[0, 1, 0.25],
            y_range=[-1, 4, 1],
            x_length=7,
            y_length=4.5,
            tips=False,
            axis_config={"include_numbers": False},
        ).shift(DOWN * 0.3)

        x_labels = VGroup(
            MathTex("0").scale(0.7).next_to(axes.coords_to_point(0, 0), DOWN),
            MathTex("1").scale(0.7).next_to(axes.coords_to_point(1, 0), DOWN),
        )

        labels = axes.get_axis_labels(
            MathTex("e").scale(0.7),
            MathTex("\\text{Payoff}").scale(0.7),
        )
        labels.next_to(axes.get_y_axis(), LEFT, buff=0.1)

        self.add(axes, labels, x_labels)

        k_combined = self.LAMBDA * self.ALPHA

        control_curve = axes.plot(
            lambda e: self.payoff(e, k=1.0), color=GREEN, stroke_width=3
        )
        alt_curve = axes.plot(
            lambda e: self.payoff(e, k=self.ALPHA), color=BLUE, stroke_width=3
        )
        loss_curve = axes.plot(
            lambda e: self.payoff(e, k=self.LAMBDA), color=RED, stroke_width=3
        )
        comb_curve = axes.plot(
            lambda e: self.payoff(e, k=k_combined), color=PURPLE, stroke_width=3
        )

        control_label = Text("Control", color=GREEN, font_size=16).to_corner(UL).shift(
            DOWN * 0.5 + RIGHT * 0.3
        )
        alt_label = Text("Altruism", color=BLUE, font_size=16).next_to(
            control_label, DOWN, aligned_edge=LEFT
        )
        loss_label = Text("Loss aversion", color=RED, font_size=16).next_to(
            alt_label, DOWN, aligned_edge=LEFT
        )
        comb_label = Text("Combined", color=PURPLE, font_size=16).next_to(
            loss_label, DOWN, aligned_edge=LEFT
        )

        self.play(
            Create(control_curve),
            Create(alt_curve),
            Create(loss_curve),
            Create(comb_curve),
            run_time=2.0,
        )
        self.play(
            Write(control_label),
            Write(alt_label),
            Write(loss_label),
            Write(comb_label),
            run_time=2.0,
        )
        self.wait(3.0)
