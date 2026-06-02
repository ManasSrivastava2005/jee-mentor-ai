from abc import ABC, abstractmethod
from typing import TypedDict

from app.models.schemas import Citation, TopicDetection


class SolverResult(TypedDict):
    answer: str
    formulas: list[str]
    formulas_used: list[str]
    reasoning_steps: list[str]
    final_answer: str
    concepts: list[str]


class BaseSolver(ABC):
    name: str = "base"

    @abstractmethod
    def can_solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> bool:
        """Return true when this solver can deterministically solve the question."""

    @abstractmethod
    def solve(self, question: str, detection: TopicDetection, citations: list[Citation]) -> SolverResult:
        """Return a deterministic solution."""

    def _format_answer(self, reasoning_steps: list[str], final_answer: str) -> str:
        return "\n".join(
            [
                "Derivation:",
                *[f"{index}. {step}" for index, step in enumerate(reasoning_steps, start=1)],
                "",
                f"Final answer: {final_answer}",
            ]
        )
