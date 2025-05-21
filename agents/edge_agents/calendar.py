from agents.edge_agents.edge import EdgeAgent
from typing import Dict, Any, List

from langchain_core.tools import Tool, StructuredTool

def get_today_events() -> List[Dict[str, Any]]:
    print("Getting today's events")
    return [
        {"title": "Meeting", "time": "10:00", "location": "Conference Room"},
        {"title": "Lunch", "time": "12:00", "location": "Cafeteria"}
    ]

def get_upcoming_events(days: int = 7) -> List[Dict[str, Any]]:
    print(f"Getting upcoming events for {days} days")
    return [
        {"title": "Meeting", "date": "2023-04-20", "time": "10:00", "location": "Conference Room"},
        {"title": "Lunch", "date": "2023-04-20", "time": "12:00", "location": "Cafeteria"},
        {"title": "Doctor Appointment", "date": "2023-04-22", "time": "14:00", "location": "Medical Center"}
    ]

def add_event(title: str, date: str, time: str, location: str = None) -> Dict[str, Any]:
    print(f"Adding event: {title} on {date} at {time}")
    return {"title": title, "date": date, "time": time, "location": location, "status": "added"}

def check_availability(date: str, time_slot: str) -> Dict[str, Any]:
    print(f"Checking availability for {date} at {time_slot}")
    return {"available": True, "conflicting_events": []}


class CalendarAgent(EdgeAgent):
    def __init__(self):
        super().__init__()
        self.name = "Calendar Agent"
        self.slug = "calendar"
        self.description = "Responsible for getting the calendar information from the Google Calendar API."
        
        # Mock function tools for calendar operations
        self.tools = [
            StructuredTool.from_function(
                name="get_today_events",
                description="Get today's calendar events",
                func=get_today_events,
                args_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            StructuredTool.from_function(
                name="get_upcoming_events",
                description="Get upcoming events for specified days",
                func=get_upcoming_events,
                args_schema={
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Number of days to get events for"
                        }
                    },
                    "required": ["days"]
                }
            ),
            StructuredTool.from_function(
                name="add_event",
                description="Add a new calendar event",
                func=add_event,
                args_schema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the event"
                        },
                        "date": {
                            "type": "string",
                            "description": "Date of the event (YYYY-MM-DD)"
                        },
                        "time": {
                            "type": "string",
                            "description": "Time of the event (HH:MM)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the event (optional)"
                        }
                    },
                    "required": ["title", "date", "time"]
                }
            ),
            StructuredTool.from_function(
                name="check_availability",
                description="Check availability for a date and time",
                func=check_availability,
                args_schema={
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date to check (YYYY-MM-DD)"
                        },
                        "time_slot": {
                            "type": "string",
                            "description": "Time slot to check (HH:MM)"
                        }
                    },
                    "required": ["date", "time_slot"]
                }
            )
        ]
