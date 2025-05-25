from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import StructuredTool

from loguru import logger

import requests

def check_occupancy() -> Dict[str, Any]:
    logger.info("Checking occupancy and stranger movements")
    response = requests.get("https://sensors.davidoglu.vip/api/v1/iot-1/occupancy")
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
