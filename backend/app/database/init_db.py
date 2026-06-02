from app.database.session import Base, engine
from app.models.entities import Performance, Question, Topic, User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
