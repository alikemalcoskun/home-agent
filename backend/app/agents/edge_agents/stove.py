from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import StructuredTool

from loguru import logger

def check_stove_status() -> str:
    logger.info("Checking stove status")
    return "off"

def turn_stove_off() -> str:
    logger.info("Turning off stove")
    return "off"

def get_stove_temperature() -> int:
    logger.info("Getting stove temperature")
    return 0

def get_cooking_timer() -> int:
    logger.info("Getting cooking timer")
    return 0

def set_cooking_timer(minutes: int) -> str:
    logger.info(f"Setting cooking timer for {minutes} minutes")
    return f"Timer set for {minutes} minutes"


class StoveAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Stove Agent"
        self.slug = "stove"
        self.description = "Responsible for getting the stove status from the stove IoT device."
        
        # Mock function tools for stove operations
        self.tools = [
            StructuredTool.from_function(
                name="check_stove_status",
                description="Check the status of the stove",
                func=check_stove_status,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="turn_stove_off",
                description="Turn off the stove",
                func=turn_stove_off,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_stove_temperature",
                description="Get the temperature of the stove",
                func=get_stove_temperature,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_cooking_timer",
                description="Get the cooking timer",
                func=get_cooking_timer,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="set_cooking_timer",
                description="Set the cooking timer",
                func=set_cooking_timer,
                args_schema={
                    "type": "object",
                    "properties": {
                        "minutes": {
                            "type": "integer",
                            "description": "Number of minutes to set the timer for"
                        }
                    },
                    "required": ["minutes"]
                }
            )
        ]
