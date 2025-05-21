from fastapi import APIRouter
from app.api.v2.routes import agent

router = APIRouter(tags=["Async"])

router.include_router(
    agent.router, prefix="/async/agent") 