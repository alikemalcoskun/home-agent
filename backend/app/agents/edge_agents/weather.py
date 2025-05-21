from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import StructuredTool

from loguru import logger

def get_current_weather() -> Dict[str, Any]:
    logger.info("Getting current weather")
    return {
        "temperature": 72,
        "condition": "sunny",
        "humidity": 45,
        "wind_speed": 5
    }

def get_weather_forecast(days: int = 3) -> Dict[str, Any]:
    logger.info(f"Getting weather forecast for {days} days")
    return {
        "forecast": [
            {"day": "today", "temperature": 72, "condition": "sunny"},
            {"day": "tomorrow", "temperature": 68, "condition": "cloudy"},
            {"day": "day_after", "temperature": 65, "condition": "rainy"}
        ]
    }

def get_weather_alerts() -> Dict[str, Any]:
    logger.info("Getting weather alerts")
    return {
        "alerts": [
            {"type": "rain", "severity": "moderate", "time": "evening"}
        ]
    }


class WeatherAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Weather Agent"
        self.slug = "weather"
        self.description = "Responsible for getting the weather information from the weather API."
        
        # Mock function tools for weather operations
        self.tools = [
            StructuredTool.from_function(
                name="get_current_weather",
                description="Get the current weather conditions",
                func=get_current_weather,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_weather_forecast",
                description="Get weather forecast for specified days",
                func=get_weather_forecast,
                args_schema={
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days to get the forecast for"
                        }
                    },
                    "required": ["days"]
                }
            ),
            StructuredTool.from_function(
                name="get_weather_alerts",
                description="Get any weather alerts or warnings",
                func=get_weather_alerts,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]