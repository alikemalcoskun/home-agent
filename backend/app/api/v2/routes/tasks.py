from celery import shared_task
from fastapi import WebSocket
from loguru import logger
import json
import redis
import asyncio

# Initialize Redis client
redis_client = redis.Redis(
    host='redis',
    port=6379,
    db=0,
    decode_responses=True
)


async def connect(websocket: WebSocket, task_id: str):
    logger.info(f"Connecting to task {task_id}")
    await websocket.accept()

async def disconnect(websocket: WebSocket, task_id: str):
    logger.info(f"Disconnecting from task {task_id}")
    await websocket.close()
    logger.info(f"Disconnected from task {task_id}")

@shared_task
def broadcast_task_update(task_id: str, message: dict):
    """Celery task to broadcast updates to WebSocket clients"""
    # Publish message to Redis channel
    redis_client.publish(f"task:{task_id}", json.dumps(message))
    logger.info(f"Published message to task:{task_id}")

async def subscribe_to_task(task_id: str, websocket: WebSocket):
    """Subscribe to Redis channel for a task"""
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"task:{task_id}")
    
    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                await websocket.send_json(data)
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.error(f"Error in subscription: {e}")
    finally:
        pubsub.unsubscribe()