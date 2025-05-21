from fastapi import APIRouter
from app.api.v1.routes import agent
from app.api.v1.routes import key

router = APIRouter()

router.include_router(
    agent.router, tags=["Agent"], prefix="/agent")
router.include_router(
    key.router, tags=["Key"], prefix="/key")
