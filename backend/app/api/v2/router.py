from fastapi import APIRouter
from app.api.v2.routes import agent, websocket

router = APIRouter(tags=["Async"])

router.include_router(
    agent.router, prefix="/async/agent") 
router.include_router(
    websocket.router, prefix="/async/ws") 