import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings
from app.database.init_db import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("jee-mentor-ai")

settings = get_settings()
app = FastAPI(
    title="JEE Mentor AI API",
    description="Reasoning agent backend for JEE question solving with Foundry IQ grounding.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    logger.info("JEE Mentor AI API started in %s mode", settings.app_env)


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "foundry_agent_service": settings.foundry_enabled,
        "foundry_iq": settings.foundry_iq_enabled,
    }


app.include_router(router)
