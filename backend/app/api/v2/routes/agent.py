from fastapi import APIRouter, status, HTTPException
from celery import Celery
from typing import Dict
from app.models.agent import AgentRequest
from app.services.orchestration import OrchestrationService
from app.models.state import State
from loguru import logger
import json
from app.api.v2.routes.tasks import broadcast_task_update

# Initialize Celery with both broker and result backend
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Define a Celery task for agent processing
@celery_app.task
def process_agent_task(request_data: Dict):
    try:
        orchestrator = OrchestrationService()
        orchestrator.generate_workflow()
        orchestrator.compile_workflow()

        initial_state = State(request=f"{request_data['owner']}: {request_data['query']}")
        state_dict = orchestrator.invoke(initial_state.model_dump())
        state = State(**state_dict)
        
        # Convert blackboard to dictionary for JSON serialization
        blackboard_dict = json.loads(state.blackboard.model_dump_json())

        # Send update to WebSocket
        broadcast_task_update(
            process_agent_task.request.id,
            {
                "status": "completed",
                "blackboard": blackboard_dict
            }
        )
        
        logger.info(f"Blackboard: {blackboard_dict}, {type(blackboard_dict)}")
        
        return {
            "status": "completed",
            "blackboard": blackboard_dict
        }
    except Exception as e:
        logger.error(f"Error in agent task: {e}")
        # Send error to WebSocket
        broadcast_task_update(
            process_agent_task.request.id,
            {
                "status": "error",
                "error": str(e)
            }
        )
        return {
            "status": "error",
            "error": str(e)
        }

router = APIRouter()

@router.post(
    path="/run",
    name="Async Agent Workflow Run",
    description="Run the agents orchestrator asynchronously to analyze the data.",
    response_description="The task ID for tracking the async process.",
    status_code=status.HTTP_202_ACCEPTED
)
async def run_agent_workflow(request: AgentRequest):
    if not request.query or request.query == "":
        raise HTTPException(status_code=400, detail="No query provided.")
    
    if not request.owner or request.owner == "":
        raise HTTPException(status_code=400, detail="No owner provided.")

    # Queue the task in Celery
    task = process_agent_task.delay({
        "query": request.query,
        "owner": request.owner
    })
    
    return {
        "task_id": task.id,
        "status": "processing",
        "message": "Agent workflow has been queued for processing"
    }

@router.get(
    path="/status/{task_id}",
    name="Get Agent Task Status",
    description="Get the status of an async agent task",
    response_description="The current status of the task",
    status_code=status.HTTP_200_OK
)
async def get_task_status(task_id: str):
    task = process_agent_task.AsyncResult(task_id)
    
    if task.ready():
        if task.successful():
            return task.result
        else:
            # Handle different types of task failures
            error_message = "Unknown error"
            if isinstance(task.result, dict) and 'error' in task.result:
                error_message = task.result['error']
            elif isinstance(task.result, Exception):
                error_message = str(task.result)
            elif task.result is not None:
                error_message = str(task.result)
                
            raise HTTPException(
                status_code=500,
                detail=f"Task failed: {error_message}"
            )
            
    return {
        "task_id": task_id,
        "status": "processing"
    } 