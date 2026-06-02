from app.agents.solvers import SolverRegistry
from app.config import get_settings
from app.models.schemas import Citation, SimilarQuestion, TopicDetection


SYSTEM_INSTRUCTIONS = """
You are JEE Mentor AI, a rigorous but encouraging JEE Physics, Chemistry, and Mathematics tutor.
Classify the subject and topic, solve step by step, show formulas, explain reasoning, and cite grounded knowledge.
Never invent citations. If retrieved context is insufficient, say what assumption is being made.
"""


class JeeMentorAgent:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.solver_registry = SolverRegistry()

    async def solve(self, question: str, subject: str, topic: str, citations: list[Citation]) -> dict:
        detection = TopicDetection(subject=subject, topic=topic, confidence_score=1.0)
        if self.settings.foundry_enabled:
            foundry_answer = await self._solve_with_foundry(question, subject, topic, citations)
            if foundry_answer:
                return foundry_answer
        deterministic_answer = self.solver_registry.solve(question, detection, citations)
        if deterministic_answer:
            return deterministic_answer
        return self._solve_locally(question, subject, topic, citations)

    async def _solve_with_foundry(
        self, question: str, subject: str, topic: str, citations: list[Citation]
    ) -> dict | None:
        try:
            from azure.ai.projects.aio import AIProjectClient
            from azure.identity.aio import DefaultAzureCredential
        except ImportError:
            return None

        context = "\n\n".join(f"{c.title}: {c.snippet}" for c in citations)
        prompt = (
            f"{SYSTEM_INSTRUCTIONS}\n\nSubject: {subject}\nTopic: {topic}\n"
            f"Retrieved context:\n{context}\n\nQuestion:\n{question}"
        )
        try:
            async with AIProjectClient(
                endpoint=self.settings.foundry_project_endpoint,
                credential=DefaultAzureCredential(),
            ) as project:
                thread = await project.agents.threads.create()
                await project.agents.messages.create(thread_id=thread.id, role="user", content=prompt)
                run = await project.agents.runs.create_and_process(
                    thread_id=thread.id,
                    agent_id=self.settings.foundry_agent_id,
                )
                if run.status != "completed":
                    return None
                messages = project.agents.messages.list(thread_id=thread.id)
                async for message in messages:
                    if message.role == "assistant" and message.content:
                        text = message.content[0].text.value
                        return {
                            "answer": text,
                            "formulas": self._formula_hints(subject, topic),
                            "formulas_used": self._formula_hints(subject, topic),
                            "reasoning_steps": [text],
                            "final_answer": self._extract_final_answer(text),
                            "concepts": self._concept_hints(topic),
                        }
        except Exception:
            return None
        return None

    def _solve_locally(self, question: str, subject: str, topic: str, citations: list[Citation]) -> dict:
        formulas = self._formula_hints(subject, topic)
        reasoning_steps = [
            f"Detected this as a {subject} problem from {topic}.",
            "Retrieved the relevant formulas from the knowledge base.",
            "No deterministic local solver is registered for this exact problem pattern yet.",
        ]
        answer = "\n".join(
            [
                "Derivation:",
                *[f"{index}. {step}" for index, step in enumerate(reasoning_steps, start=1)],
                "",
                "Final answer: Requires Foundry Agent Service for this exact problem type.",
            ]
        )
        return {
            "answer": answer,
            "formulas": formulas,
            "formulas_used": formulas,
            "reasoning_steps": reasoning_steps,
            "final_answer": "Requires Foundry Agent Service for this exact problem type.",
            "concepts": self._concept_hints(topic),
        }

    def _extract_final_answer(self, text: str) -> str:
        for marker in ("Final answer:", "final answer:"):
            if marker in text:
                return text.split(marker, 1)[1].strip().splitlines()[0]
        return text.strip().splitlines()[-1] if text.strip() else ""

    def generate_similar(self, question: str, subject: str, topic: str) -> list[SimilarQuestion]:
        return [
            SimilarQuestion(
                difficulty="Easy",
                question=f"A direct {topic} question in {subject}: identify the key formula and compute the requested value for simple numbers.",
                hint="Start by writing the definition and listing given quantities.",
            ),
            SimilarQuestion(
                difficulty="Medium",
                question=f"A JEE Main style {topic} problem with two linked concepts and one algebraic transformation.",
                hint="Break it into two subproblems before substituting values.",
            ),
            SimilarQuestion(
                difficulty="Hard",
                question=f"A JEE Advanced style {topic} problem requiring comparison of cases and a final expression.",
                hint="Use a symbolic variable first, then test boundary cases.",
            ),
        ]

    def _formula_hints(self, subject: str, topic: str) -> list[str]:
        formulas = {
            "Electrostatics": [
                "Phi_total = q_enclosed / epsilon_0",
                "Phi_face = Phi_total / 6 for a centered charge in a cube",
                "F = k q1 q2 / r^2",
                "E = F/q",
                "V = kq/r",
                "C = Q/V",
            ],
            "Thermodynamics": ["Delta U = Q - W", "PV^gamma = constant", "eta = 1 - T_c/T_h"],
            "Differential Equations": ["dy/dx = f(x)g(y)", "Integral dy/g(y) = Integral f(x) dx + C"],
            "Laplace Transform": ["L{f(t)} = Integral_0^infinity e^(-st) f(t) dt", "L{f'} = sF(s) - f(0)"],
            "Organic Chemistry": ["Markovnikov orientation", "Inductive effect: -I/+I", "Resonance stabilization"],
        }
        return formulas.get(topic, ["Define variables", "Choose governing equation", "Simplify and verify units"])

    def _concept_hints(self, topic: str) -> list[str]:
        return [
            f"Pattern recognition for {topic}",
            "Formula selection from given constraints",
            "Dimensional or logical verification",
        ]
