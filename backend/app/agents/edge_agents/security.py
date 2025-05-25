from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import StructuredTool

from loguru import logger

import requests

def check_occupancy() -> Dict[str, Any]:
    logger.info("Checking occupancy and stranger movements")
    response = requests.get("https://sensors.davidoglu.vip/api/v1/iot-2/occupancy")
    response = response.json()
    if response.get("status") == "success":
        occupancy = True if response.get("message") == 1 else False
        logger.info("Occupancy checked successfully")
    else:
        occupancy = False
    return {
        "status": "success",
        "occupancy": occupancy
    }

def check_safe_box_door_status() -> Dict[str, Any]:
    logger.info("Checking safe box door status")
    response = requests.get("https://sensors.davidoglu.vip/api/v1/iot-2/heading")
    response = response.json()
    if response.get("status") == "success":
        heading = response.get("message")
        # if heading in in range of 0-180, it is open, close otherwise
        if heading is not None:
            if heading < 180:
                safe_box_door_status = "open"
            else:
                safe_box_door_status = "close"
        logger.info("Heading checked successfully")
    else:
        safe_box_door_status = None
    return {
        "status": "success",
        "safe_box_door_status": safe_box_door_status
    }


class SecurityAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Security Agent"
        self.slug = "security"
        self.description = "Responsible for monitoring home security, checking occupancy, detecting stranger movements, and managing security systems."
        
        # Mock function tools for security operations
        self.tools = [
            StructuredTool.from_function(
                name="check_occupancy",
                description="Check occupancy and detect stranger movements",
                func=check_occupancy,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
