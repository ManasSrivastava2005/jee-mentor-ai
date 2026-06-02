import json
from datetime import datetime

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.entities import Performance, Question, Topic, User
from app.models.schemas import AnalyticsResponse, TopicMetric


def get_or_create_demo_user(db: Session, user_id: int | None = None) -> User:
    if user_id:
        existing = db.get(User, user_id)
        if existing:
            return existing
    user = db.scalar(select(User).where(User.email == "demo@jee-mentor.ai"))
    if not user:
        user = User()
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def save_solved_question(
    db: Session,
    user_id: int | None,
    prompt: str,
    subject: str,
    topic_name: str,
    confidence: float,
    answer: str,
    formulas: list[str],
    citations: list[dict],
) -> Question:
    user = get_or_create_demo_user(db, user_id)
    topic = db.scalar(select(Topic).where(Topic.subject == subject, Topic.name == topic_name))
    if not topic:
        topic = Topic(subject=subject, name=topic_name)
        db.add(topic)
        db.flush()

    question = Question(
        user_id=user.id,
        topic_id=topic.id,
        prompt=prompt,
        subject=subject,
        topic=topic_name,
        confidence_score=confidence,
        answer=answer,
        formulas=json.dumps(formulas),
        citations=json.dumps(citations),
    )
    db.add(question)

    performance = db.scalar(select(Performance).where(Performance.user_id == user.id, Performance.topic_id == topic.id))
    if not performance:
        performance = Performance(user_id=user.id, topic_id=topic.id, attempts=0, correct=0, average_confidence=0.0)
        db.add(performance)
    performance.attempts += 1
    performance.correct += 1 if confidence >= 0.7 else 0
    performance.average_confidence = round(
        ((performance.average_confidence * (performance.attempts - 1)) + confidence) / performance.attempts,
        3,
    )
    performance.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(question)
    return question


def get_history(db: Session, limit: int = 50) -> list[Question]:
    return list(db.scalars(select(Question).order_by(desc(Question.created_at)).limit(limit)))


def get_analytics(db: Session) -> AnalyticsResponse:
    rows = db.execute(
        select(Topic.subject, Topic.name, Performance.attempts, Performance.correct, Performance.average_confidence)
        .join(Performance, Performance.topic_id == Topic.id)
        .order_by(desc(Performance.attempts))
    ).all()
    metrics = [
        TopicMetric(
            subject=row.subject,
            topic=row.name,
            attempts=row.attempts,
            correct=row.correct,
            accuracy=round(row.correct / row.attempts, 2) if row.attempts else 0,
            average_confidence=row.average_confidence,
        )
        for row in rows
    ]
    weak = sorted(metrics, key=lambda item: (item.accuracy, item.average_confidence))[:5]
    return AnalyticsResponse(
        most_attempted_topics=metrics[:5],
        weak_topics=weak,
        recommended_revision_areas=[
            f"Revise {item.topic} in {item.subject}: redo formulas, then solve 10 mixed problems."
            for item in weak
        ],
    )
