from pathlib import Path

import httpx

from app.config import get_settings
from app.models.schemas import Citation


class KnowledgeService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.local_kb_dir = Path(__file__).resolve().parents[3] / "knowledge-base"

    async def retrieve(self, query: str, topic: str) -> list[Citation]:
        if self.settings.foundry_iq_enabled:
            foundry_results = await self._retrieve_from_foundry_iq(query)
            if foundry_results:
                return foundry_results
        return self._retrieve_from_local_notes(topic)

    async def _retrieve_from_foundry_iq(self, query: str) -> list[Citation]:
        endpoint = self.settings.foundry_iq_endpoint.rstrip("/")
        url = f"{endpoint}/knowledgebases/{self.settings.foundry_iq_knowledge_base_id}:query"
        headers = {
            "api-key": self.settings.foundry_iq_api_key,
            "Content-Type": "application/json",
        }
        payload = {"query": query, "outputMode": "extractiveData", "topK": 5}
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
        except httpx.HTTPError:
            return []

        data = response.json()
        results = data.get("results") or data.get("citations") or []
        citations: list[Citation] = []
        for item in results[:5]:
            citations.append(
                Citation(
                    title=item.get("title", "Foundry IQ result"),
                    source=item.get("source", item.get("url", "Foundry IQ")),
                    snippet=item.get("snippet", item.get("content", ""))[:500],
                )
            )
        return citations

    def _retrieve_from_local_notes(self, topic: str) -> list[Citation]:
        citations: list[Citation] = []
        topic_words = {word.lower() for word in topic.split()}
        for path in self.local_kb_dir.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            if any(word in text.lower() for word in topic_words):
                citations.append(
                    Citation(
                        title=path.stem.replace("-", " ").title(),
                        source=str(path),
                        snippet=text.strip()[:500],
                    )
                )
        return citations[:3]
