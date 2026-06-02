import re

import sympy as sp

from app.agents.solvers.base import BaseSolver, SolverResult
from app.models.schemas import Citation, TopicDetection


class LaplaceTransformSolver(BaseSolver):
    name = "laplace_transform"

    def can_solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> bool:
        text = self._normalize(question)
        if detection.topic != "Laplace Transform" and "laplace" not in text:
            return False
        return self._extract_forward_expression(text) is not None or self._extract_inverse_expression(text) is not None

    def solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> SolverResult:
        text = self._normalize(question)
        inverse_expression = self._extract_inverse_expression(text)
        if inverse_expression:
            return self._solve_inverse(inverse_expression)

        forward_expression = self._extract_forward_expression(text)
        if not forward_expression:
            raise ValueError("Laplace solver cannot parse this question.")
        return self._solve_forward(forward_expression)

    def _solve_forward(self, expression_text: str) -> SolverResult:
        t, s = sp.symbols("t s")

        derivative_match = re.fullmatch(r"(?:d/dt|derivative of|f')\s*f?\(?t?\)?", expression_text)
        if derivative_match or "f'(t)" in expression_text or "f prime" in expression_text:
            formulas_used = ["L{f'(t)} = sF(s) - f(0)"]
            reasoning_steps = [
                "Identify the expression as the first derivative of a function f(t).",
                "Apply the first derivative property of the Laplace transform.",
                "Substitute the generic transform F(s) = L{f(t)}.",
            ]
            final_answer = "sF(s) - f(0)"
            return self._result(formulas_used, reasoning_steps, final_answer, ["First derivative property"])

        expression = self._parse_time_expression(expression_text)
        transform = sp.laplace_transform(expression, t, s, noconds=True)
        final_answer = str(sp.simplify(transform))
        formulas_used = [self._formula_for_forward_expression(expression_text)]
        reasoning_steps = [
            f"Read the requested function as f(t) = {self._display(expression_text)}.",
            f"Use the table result: {formulas_used[0]}.",
            f"Therefore L{{{self._display(expression_text)}}} = {final_answer}.",
        ]
        return self._result(formulas_used, reasoning_steps, final_answer, ["Laplace transform table"])

    def _solve_inverse(self, expression_text: str) -> SolverResult:
        t, s = sp.symbols("t s")
        expression = self._parse_s_expression(expression_text)
        inverse = sp.inverse_laplace_transform(expression, s, t)
        final_answer = str(sp.simplify(inverse))
        formulas_used = [self._formula_for_inverse_expression(expression_text, final_answer)]
        reasoning_steps = [
            f"Read the requested transform as F(s) = {expression_text}.",
            "Match it with the standard inverse Laplace transform table.",
            f"Therefore L^-1{{{expression_text}}} = {final_answer}.",
        ]
        return self._result(formulas_used, reasoning_steps, final_answer, ["Inverse Laplace transform table"])

    def _result(
        self, formulas_used: list[str], reasoning_steps: list[str], final_answer: str, concepts: list[str]
    ) -> SolverResult:
        return {
            "answer": self._format_answer(reasoning_steps, final_answer),
            "formulas": formulas_used,
            "formulas_used": formulas_used,
            "reasoning_steps": reasoning_steps,
            "final_answer": final_answer,
            "concepts": concepts,
        }

    def _extract_forward_expression(self, text: str) -> str | None:
        patterns = [
            r"l\{([^{}]+)\}",
            r"laplace transform of ([^.?,]+)",
            r"laplace of ([^.?,]+)",
            r"find l\(([^)]+)\)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return self._clean_expression(match.group(1))
        return None

    def _extract_inverse_expression(self, text: str) -> str | None:
        patterns = [
            r"l\^-1\{([^{}]+)\}",
            r"inverse laplace transform of ([^.?,]+)",
            r"inverse laplace of ([^.?,]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return self._clean_expression(match.group(1))
        return None

    def _parse_time_expression(self, expression_text: str) -> sp.Expr:
        t = sp.symbols("t")
        expression = self._to_sympy_text(expression_text)
        a = sp.symbols("a")
        return sp.sympify(expression, locals={"t": t, "a": a, "e": sp.E, "sin": sp.sin, "cos": sp.cos, "exp": sp.exp})

    def _parse_s_expression(self, expression_text: str) -> sp.Expr:
        s = sp.symbols("s")
        expression = self._to_sympy_text(expression_text)
        return sp.sympify(expression, locals={"s": s})

    def _to_sympy_text(self, expression_text: str) -> str:
        expression = self._clean_expression(expression_text)
        expression = re.sub(r"\be\^\(([^)]+)\)", r"exp(\1)", expression)
        expression = re.sub(r"\be\^([a-z0-9*+\-/]+)", r"exp(\1)", expression)
        expression = expression.replace("^", "**")
        expression = re.sub(r"(\d)([a-z])", r"\1*\2", expression)
        expression = re.sub(r"([a-z])(\d)", r"\1*\2", expression)
        return expression

    def _formula_for_forward_expression(self, expression_text: str) -> str:
        expression = self._clean_expression(expression_text)
        if expression == "1":
            return "L{1} = 1/s"
        if expression == "t":
            return "L{t} = 1/s^2"
        power_match = re.fullmatch(r"t\^(\d+)", expression)
        if power_match:
            return "L{t^n} = n! / s^(n+1)"
        if expression.startswith("e^") or expression.startswith("exp"):
            return "L{e^(at)} = 1/(s-a)"
        if expression.startswith("sin"):
            return "L{sin(at)} = a/(s^2+a^2)"
        if expression.startswith("cos"):
            return "L{cos(at)} = s/(s^2+a^2)"
        return "L{f(t)} = integral_0^infinity e^(-st) f(t) dt"

    def _formula_for_inverse_expression(self, expression_text: str, final_answer: str) -> str:
        if final_answer == "1":
            return "L^-1{1/s} = 1"
        if final_answer == "t":
            return "L^-1{1/s^2} = t"
        if "sin" in final_answer:
            return "L^-1{a/(s^2+a^2)} = sin(at)"
        if "cos" in final_answer:
            return "L^-1{s/(s^2+a^2)} = cos(at)"
        if "exp" in final_answer:
            return "L^-1{1/(s-a)} = e^(at)"
        return "Use the inverse Laplace transform table"

    def _clean_expression(self, expression: str) -> str:
        expression = expression.strip().rstrip(".")
        expression = expression.replace(" ", "")
        expression = expression.replace("{", "").replace("}", "")
        return expression

    def _normalize(self, question: str) -> str:
        return question.lower().replace("−", "-")

    def _display(self, expression_text: str) -> str:
        return expression_text.replace("**", "^")
