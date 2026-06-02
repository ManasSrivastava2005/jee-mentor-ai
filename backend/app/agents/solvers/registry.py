from app.agents.solvers.base import BaseSolver, SolverResult
from app.agents.solvers.calculus_integration import CalculusIntegrationSolver
from app.agents.solvers.differential_equation import DifferentialEquationSolver
from app.agents.solvers.electrostatics import ElectrostaticsSolver
from app.agents.solvers.laplace_transform import LaplaceTransformSolver
from app.models.schemas import Citation, TopicDetection


class SolverRegistry:
    def __init__(self, solvers: list[BaseSolver] | None = None) -> None:
        self.solvers = solvers or [
            ElectrostaticsSolver(),
            LaplaceTransformSolver(),
            DifferentialEquationSolver(),
            CalculusIntegrationSolver(),
        ]

    def solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> SolverResult | None:
        for solver in self.solvers:
            if solver.can_solve(question, detection, citations):
                return solver.solve(question, detection, citations)
        return None
