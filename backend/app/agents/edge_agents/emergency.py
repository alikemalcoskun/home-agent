from app.agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import StructuredTool

from loguru import logger

def call_emergency(emergency_type: str, location: str = "home") -> Dict[str, Any]:
    logger.info(f"Calling emergency services for {emergency_type} at {location}")
    emergency_numbers = {
        "fire": "911",
        "police": "911", 
        "medical": "911",
        "ambulance": "911",
        "general": "911"
    }
    number = emergency_numbers.get(emergency_type.lower(), "911")
    return {
        "status": "emergency_called",
        "emergency_type": emergency_type,
        "number_called": number,
        "location": location,
        "call_time": "2025-05-25 16:30:00",
        "estimated_arrival": "5-10 minutes"
    }

def get_emergency_contacts() -> Dict[str, Any]:
    logger.info("Getting emergency contacts")
    return {
        "contacts": [
            {"name": "Fire Department", "number": "911", "type": "fire"},
            {"name": "Police", "number": "911", "type": "police"},
            {"name": "Medical Emergency", "number": "911", "type": "medical"},
            {"name": "Family Contact", "number": "+1-555-0123", "type": "family"},
            {"name": "Neighbor", "number": "+1-555-0456", "type": "neighbor"}
        ]
    }

def check_emergency_status() -> Dict[str, Any]:
    logger.info("Checking emergency status")
    return {
        "active_emergencies": [],
        "last_emergency": "none",
        "emergency_systems": {
            "smoke_detector": "active",
            "security_alarm": "active", 
            "panic_button": "ready"
        },
        "status": "all_clear"
    }

def trigger_alarm(alarm_type: str) -> Dict[str, Any]:
    logger.info(f"Triggering {alarm_type} alarm")
    return {
        "alarm_type": alarm_type,
        "status": "alarm_triggered",
        "timestamp": "2025-05-25 16:30:00",
        "actions_taken": ["sound_alarm", "notify_contacts", "call_emergency"]
    }


class EmergencyAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Emergency Agent"
        self.slug = "emergency"
        self.description = "Responsible for handling emergency situations, calling emergency services, and managing emergency contacts."
        
        # Mock function tools for emergency operations
        self.tools = [
            StructuredTool.from_function(
                name="call_emergency",
                description="Call emergency services",
                func=call_emergency,
                args_schema={
                    "type": "object",
                    "properties": {
                        "emergency_type": {
                            "type": "string",
                            "description": "Type of emergency (fire, police, medical, ambulance, general)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the emergency"
                        }
                    },
                    "required": ["emergency_type"]
                }
            ),
            StructuredTool.from_function(
                name="get_emergency_contacts",
                description="Get list of emergency contacts",
                func=get_emergency_contacts,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="check_emergency_status",
                description="Check current emergency status and systems",
                func=check_emergency_status,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="trigger_alarm",
                description="Trigger emergency alarm",
                func=trigger_alarm,
                args_schema={
                    "type": "object",
                    "properties": {
                        "alarm_type": {
                            "type": "string",
                            "description": "Type of alarm to trigger (fire, security, panic, medical)"
                        }
                    },
                    "required": ["alarm_type"]
                }
            )
        ]
