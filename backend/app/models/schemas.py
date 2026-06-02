from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"


class Citation(BaseModel):
    title: str
    source: str
    snippet: str


class TopicDetection(BaseModel):
    subject: str
    topic: str
    confidence_score: float = Field(ge=0, le=1)


class SolveRequest(BaseModel):
    question: str = Field(min_length=5)
    user_id: int | None = None


class SolveResponse(BaseModel):
    question_id: int
    detection: TopicDetection
    subject: str
    topic: str
    confidence: float
    answer: str
    formulas: list[str]
    formulas_used: list[str]
    reasoning_steps: list[str]
    final_answer: str
    concepts: list[str]
    citations: list[Citation]


class SimilarQuestion(BaseModel):
    difficulty: Difficulty
    question: str
    hint: str


class SimilarRequest(BaseModel):
    question: str
    topic: str | None = None
    subject: str | None = None


class SimilarResponse(BaseModel):
    questions: list[SimilarQuestion]


class HistoryItem(BaseModel):
    id: int
    prompt: str
    subject: str
    topic: str
    confidence_score: float
    created_at: datetime


class TopicMetric(BaseModel):
    subject: str
    topic: str
    attempts: int
    correct: int
    accuracy: float
    average_confidence: float


class AnalyticsResponse(BaseModel):
    most_attempted_topics: list[TopicMetric]
    weak_topics: list[TopicMetric]
    recommended_revision_areas: list[str]
