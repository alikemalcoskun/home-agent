from agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any

from langchain_core.tools import Tool, StructuredTool

def check_window_status(window_id: str, location: str) -> str:
    print(f"Checking window status for {window_id} in {location}")
    return "closed"

def close_window(window_id: str, location: str) -> str:
    print(f"Closing window for {window_id} in {location}")
    return "closed"

def open_window(window_id: str, location: str) -> str:
    print(f"Opening window for {window_id} in {location}")
    return "open"

def get_all_windows_status() -> Dict[str, str]:
    print("Getting all windows status")
    return {"living_room": "closed", "bedroom": "open", "kitchen": "closed", "bathroom": "closed"}


class WindowAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Window Agent"
        self.slug = "window"
        self.description = "Responsible for getting the windows status from the window IoT device."
        
        # Mock function tools for window operations
        self.tools = [
            StructuredTool.from_function(
                name="check_window_status",
                description="Check the status of the window",
                func=check_window_status,
                args_schema={
                    "type": "object",
                    "properties": {
                        "window_id": {
                            "type": "string",
                            "description": "ID of the window to check"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the window"
                        }
                    },
                    "required": ["window_id", "location"]
                }
            ),
            StructuredTool.from_function(
                name="close_window",
                description="Close the window",
                func=close_window,
                args_schema={
                    "type": "object",
                    "properties": {
                        "window_id": {
                            "type": "string",
                            "description": "ID of the window to close"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the window"
                        }
                    },
                    "required": ["window_id", "location"]
                }
            ),
            StructuredTool.from_function(
                name="open_window",
                description="Open the window",
                func=open_window,
                args_schema={
                    "type": "object",
                    "properties": {
                        "window_id": {
                            "type": "string",
                            "description": "ID of the window to open"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the window"
                        }
                    },
                    "required": ["window_id", "location"]
                }
            ),
            StructuredTool.from_function(
                name="get_all_windows_status",
                description="Get the status of all windows",
                func=get_all_windows_status,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
