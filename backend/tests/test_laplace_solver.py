import sympy as sp

from app.agents.solvers.laplace_transform import LaplaceTransformSolver
from app.models.schemas import TopicDetection


DETECTION = TopicDetection(subject="Mathematics", topic="Laplace Transform", confidence_score=0.9)


def solve(question: str) -> str:
    result = LaplaceTransformSolver().solve(question, DETECTION, [])
    return result["final_answer"]


def assert_equivalent(actual: str, expected: str) -> None:
    s, t = sp.symbols("s t")
    actual_expr = sp.sympify(actual, locals={"s": s, "t": t, "sin": sp.sin, "cos": sp.cos, "exp": sp.exp})
    expected_expr = sp.sympify(expected, locals={"s": s, "t": t, "sin": sp.sin, "cos": sp.cos, "exp": sp.exp})
    assert sp.simplify(actual_expr - expected_expr) == 0


def test_laplace_of_one() -> None:
    assert_equivalent(solve("Find the Laplace transform of 1."), "1/s")


def test_laplace_of_t() -> None:
    assert_equivalent(solve("Find L{t}."), "1/s**2")


def test_laplace_of_t_power_n() -> None:
    assert_equivalent(solve("Find the Laplace transform of t^3."), "6/s**4")


def test_laplace_of_exponential() -> None:
    assert_equivalent(solve("Find L{e^(2t)}."), "1/(s-2)")


def test_laplace_of_sine() -> None:
    assert_equivalent(solve("Find L{sin(3t)}."), "3/(s**2+9)")


def test_laplace_of_cosine() -> None:
    assert_equivalent(solve("Find L{cos(4t)}."), "s/(s**2+16)")


def test_laplace_first_derivative_property() -> None:
    assert solve("Find L{f'(t)}.") == "sF(s) - f(0)"


def test_inverse_laplace_simple_rational() -> None:
    assert_equivalent(solve("Find inverse Laplace of 1/s^2."), "t")
