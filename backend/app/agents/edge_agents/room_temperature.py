from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import StructuredTool

from loguru import logger
import requests

def get_room_temperatures() -> Dict[str, Any]:
    logger.info("Getting room temperatures from IOT API")
    # https://sensors.davidoglu.vip/api/v1/iot-1/temperature
    response = requests.get("https://sensors.davidoglu.vip/api/v1/iot-1/temperature")
    return response.json()

def get_room_humidity() -> Dict[str, Any]:
    logger.info("Getting room humidity")
    # https://sensors.davidoglu.vip/api/v1/iot-1/humidity
    response = requests.get("https://sensors.davidoglu.vip/api/v1/iot-1/humidity")
    return response.json()

class RoomTemperatureAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Room Temperature Agent"
        self.slug = "room_temperature"
        self.description = "Responsible for getting and controlling room temperatures from the HVAC IoT system."
        
        # Mock function tools for room temperature operations
        self.tools = [
            StructuredTool.from_function(
                name="get_room_temperatures",
                description="Get temperatures for all rooms",
                func=get_room_temperatures,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_room_humidity",
                description="Get humidity for all rooms",
                func=get_room_humidity,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
