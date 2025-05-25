from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import Tool, StructuredTool

from loguru import logger

def check_light_status(light_id: str, location: str) -> str:
    logger.info(f"Checking light status for {light_id} in {location}")
    return "off"

def turn_light_on(light_id: str, location: str) -> str:
    logger.info(f"Turning on light for {light_id} in {location}")
    return "on"

def turn_light_off(light_id: str, location: str) -> str:
    logger.info(f"Turning off light for {light_id} in {location}")
    return "off"

def get_all_lights_status() -> Dict[str, str]:
    logger.info("Getting all lights status")
    return {"living_room": "off", "bedroom": "off", "kitchen": "on", "bathroom": "off"}


class LightAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Light Agent"
        self.slug = "light"
        self.description = "Responsible for getting the light status from the light IoT device."
        
        # Mock function tools for light operations
        self.tools = [
            StructuredTool.from_function(
                name="check_light_status",
                description="Check the status of the light",
                func=check_light_status,
                args_schema={
                    "type": "object",
                    "properties": {
                        "light_id": {
                            "type": "string",
                            "description": "ID of the light to check"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the light"
                        }
                    },
                    "required": ["light_id", "location"]
                }
            ),
            StructuredTool.from_function(
                name="turn_light_on",
                description="Turn on the light",
                func=turn_light_on,
                args_schema={
                    "type": "object",
                    "properties": {
                        "light_id": {
                            "type": "string",
                            "description": "ID of the light to turn on"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the light"
                        }
                    },
                    "required": ["light_id", "location"]
                }
            ),
            StructuredTool.from_function(
                name="turn_light_off",
                description="Turn off the light",
                func=turn_light_off,
                args_schema={
                    "type": "object",
                    "properties": {
                        "light_id": {
                            "type": "string",
                            "description": "ID of the light to turn off"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the light"
                        }
                    },
                    "required": ["light_id", "location"]
                }
            ),
            StructuredTool.from_function(
                name="get_all_lights_status",
                description="Get the status of all lights",
                func=get_all_lights_status,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]

