from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.agents.jee_mentor_agent import JeeMentorAgent
from app.database.session import get_db
from app.models.schemas import (
    AnalyticsResponse,
    HistoryItem,
    SimilarRequest,
    SimilarResponse,
    SolveRequest,
    SolveResponse,
    TopicMetric,
)
from app.services.analytics_service import get_analytics, get_history, save_solved_question
from app.services.knowledge_service import KnowledgeService
from app.services.ocr_service import OCRService
from app.utils.topic_detection import detect_topic

router = APIRouter()


@router.post("/solve", response_model=SolveResponse)
async def solve_question(payload: SolveRequest, db: Session = Depends(get_db)) -> SolveResponse:
    detection = detect_topic(payload.question)
    knowledge = KnowledgeService()
    citations = await knowledge.retrieve(payload.question, detection.topic)
    agent = JeeMentorAgent()
    result = await agent.solve(payload.question, detection.subject, detection.topic, citations)
    question = save_solved_question(
        db=db,
        user_id=payload.user_id,
        prompt=payload.question,
        subject=detection.subject,
        topic_name=detection.topic,
        confidence=detection.confidence_score,
        answer=result["answer"],
        formulas=result["formulas"],
        citations=[citation.model_dump() for citation in citations],
    )
    return SolveResponse(
        question_id=question.id,
        detection=detection,
        subject=detection.subject,
        topic=detection.topic,
        confidence=detection.confidence_score,
        answer=result["answer"],
        formulas=result["formulas"],
        formulas_used=result["formulas_used"],
        reasoning_steps=result["reasoning_steps"],
        final_answer=result["final_answer"],
        concepts=result["concepts"],
        citations=citations,
    )


@router.post("/generate-similar", response_model=SimilarResponse)
async def generate_similar(payload: SimilarRequest) -> SimilarResponse:
    detection = detect_topic(payload.question)
    subject = payload.subject or detection.subject
    topic = payload.topic or detection.topic
    return SimilarResponse(questions=JeeMentorAgent().generate_similar(payload.question, subject, topic))


@router.post("/ocr")
async def extract_question(file: UploadFile = File(...)) -> dict[str, str]:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload an image file.")
    try:
        text = await OCRService().extract_text(file)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"text": text}


@router.get("/analytics", response_model=AnalyticsResponse)
async def analytics(db: Session = Depends(get_db)) -> AnalyticsResponse:
    return get_analytics(db)


@router.get("/history", response_model=list[HistoryItem])
async def history(db: Session = Depends(get_db)) -> list[HistoryItem]:
    return [
        HistoryItem(
            id=item.id,
            prompt=item.prompt,
            subject=item.subject,
            topic=item.topic,
            confidence_score=item.confidence_score,
            created_at=item.created_at,
        )
        for item in get_history(db)
    ]


@router.get("/weak-topics", response_model=list[TopicMetric])
async def weak_topics(db: Session = Depends(get_db)) -> list[TopicMetric]:
    return get_analytics(db).weak_topics
