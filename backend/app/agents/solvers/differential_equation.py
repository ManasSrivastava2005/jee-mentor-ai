from app.agents.solvers.base import BaseSolver, SolverResult
from app.models.schemas import Citation, TopicDetection


class DifferentialEquationSolver(BaseSolver):
    name = "differential_equation"

    def can_solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> bool:
        return False

    def solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> SolverResult:
        raise NotImplementedError("Differential equation solver is planned for a later phase.")
