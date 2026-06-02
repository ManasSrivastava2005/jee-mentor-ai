from app.agents.solvers.base import BaseSolver, SolverResult
from app.models.schemas import Citation, TopicDetection


class ElectrostaticsSolver(BaseSolver):
    name = "electrostatics"

    def can_solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> bool:
        text = question.lower()
        return (
            detection.subject == "Physics"
            and detection.topic == "Electrostatics"
            and "charge" in text
            and "center" in text
            and "cube" in text
            and ("flux" in text or "electric flux" in text)
            and ("one face" in text or "face of the cube" in text)
        )

    def solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> SolverResult:
        formulas_used = self._retrieve_formulas(citations)
        reasoning_steps = [
            "The point charge q is at the center of the cube, so the cube is a closed Gaussian surface enclosing charge q.",
            "By Gauss's law, the total electric flux through the whole cube is Phi_total = q/epsilon_0.",
            "Because the charge is at the center, all six faces are symmetric and receive equal flux.",
            "Therefore, flux through one face is Phi_face = Phi_total/6 = q/(6 epsilon_0).",
        ]
        final_answer = "q/(6 epsilon_0)"
        return {
            "answer": self._format_answer(reasoning_steps, final_answer),
            "formulas": formulas_used,
            "formulas_used": formulas_used,
            "reasoning_steps": reasoning_steps,
            "final_answer": final_answer,
            "concepts": ["Gauss's law", "Closed Gaussian surface", "Symmetry of cube faces"],
        }

    def _retrieve_formulas(self, citations: list[Citation]) -> list[str]:
        snippets = "\n".join(citation.snippet for citation in citations).lower()
        formulas = []
        if "q_enclosed / epsilon_0" in snippets or "gauss" in snippets:
            formulas.append("Phi_total = q_enclosed / epsilon_0")
        if "equally divided among six faces" in snippets or "six faces" in snippets:
            formulas.append("Phi_face = Phi_total / 6")
        return formulas or ["Phi_total = q_enclosed / epsilon_0", "Phi_face = Phi_total / 6"]
