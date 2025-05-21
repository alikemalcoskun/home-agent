from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger
from app.api.v2.routes.tasks import connect, disconnect, subscribe_to_task
import asyncio

router = APIRouter()

@router.websocket("/task/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await connect(websocket, task_id)
    try:
        # Start subscription in background
        subscription_task = asyncio.create_task(subscribe_to_task(task_id, websocket))
        # Keep connection alive
        while True:
            await websocket.receive_text()
    except asyncio.TimeoutError:
        logger.info("WebSocket timeout, keeping connection alive")
    except WebSocketDisconnect:
        pass
    finally:
        if 'subscription_task' in locals():
            subscription_task.cancel()
        await disconnect(websocket, task_id) 