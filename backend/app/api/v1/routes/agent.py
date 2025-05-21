from fastapi import APIRouter, status, HTTPException
from app.models.agent import AgentRequest, AgentResponse

import json
from app.services.orchestration import OrchestrationService
from app.models.state import State

from loguru import logger


router = APIRouter()

@router.post(
        path="/run",
        name="Agent Workflow Run",
        description=(
            "Run the agents orchestrator to analyze the data."
        ),
        response_description="The status of the service.",
        status_code=status.HTTP_200_OK,
        response_model=AgentResponse)
def run_workflow(request: AgentRequest):
    if not request.query or request.query == "":
        raise HTTPException(status_code=400, detail="No query provided.")
    
    if not request.owner or request.owner == "":
        raise HTTPException(status_code=400, detail="No owner provided.")

    orchestrator = OrchestrationService()
    orchestrator.generate_workflow()
    orchestrator.compile_workflow()

    initial_state = State(request= f"{request.owner}: {request.query}")
    try:
        state_dict = orchestrator.invoke(initial_state.model_dump())
    except Exception as e:
        logger.error(f"Error: {e}")
        error_message = "An error occurred while running the agent orchestrator: " + str(e)
        raise HTTPException(status_code=500, detail=error_message)
    state = State(**state_dict)  # Convert dictionary back to State model

    return AgentResponse(blackboard=state.blackboard)

