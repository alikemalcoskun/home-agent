from agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import StructuredTool

def check_water_level() -> int:
    print("Checking water level")
    return 5

def get_water_usage(timeframe: str) -> Dict[str, int]:
    print(f"Getting water usage for {timeframe}")
    return {"daily": 100, "weekly": 700, "monthly": 3000}

def check_water_quality() -> str:
    print("Checking water quality")
    return "good"

def get_tank_status() -> Dict[str, Any]:
    print("Getting tank status")
    return {"level": 5, "quality": "good", "last_maintenance": "2023-01-01"}

def set_water_alert(threshold: int) -> str:
    print(f"Setting water alert for threshold {threshold}")
    return f"Alert set for water level below {threshold}%"


class WaterTankAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Water Tank Agent"
        self.slug = "water_tank"
        self.description = "Responsible for getting the water level from the water tank IoT device."
        
        # Mock function tools for water tank operations
        self.tools = [
            StructuredTool.from_function(
                name="check_water_level",
                description="Check the water level in the tank",
                func=check_water_level,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_water_usage",
                description="Get water usage statistics",
                func=get_water_usage,
                args_schema={
                    "type": "object",
                    "properties": {
                        "timeframe": {
                            "type": "string",
                            "description": "Timeframe to get water usage for (e.g., daily, weekly, monthly)"
                        }
                    },
                    "required": ["timeframe"]
                }
            ),
            StructuredTool.from_function(
                name="check_water_quality",
                description="Check the quality of water in the tank",
                func=check_water_quality,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_tank_status",
                description="Get the overall status of the water tank",
                func=get_tank_status,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="set_water_alert",
                description="Set an alert for low water level",
                func=set_water_alert,
                args_schema={
                    "type": "object",
                    "properties": {
                        "threshold": {
                            "type": "integer",
                            "description": "Water level threshold to trigger the alert"
                        }
                    },
                    "required": ["threshold"]
                }
            )
        ]