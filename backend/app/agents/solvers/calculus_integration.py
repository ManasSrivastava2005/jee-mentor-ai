from app.agents.solvers.base import BaseSolver, SolverResult
from app.models.schemas import Citation, TopicDetection


class CalculusIntegrationSolver(BaseSolver):
    name = "calculus_integration"

    def can_solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> bool:
        return False

    def solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> SolverResult:
        raise NotImplementedError("Calculus integration solver is planned for a later phase.")
