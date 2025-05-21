from pydantic import BaseModel
from typing import List
from app.models.blackboard import Blackboard, Plan, History


class State(BaseModel):
    request: str
    agents: List[dict] = [
        {
            "name": "weather",
            "description": "Responsible for getting the weather information from the weather API.",
        },
        {
            "name": "news",
            "description": "Responsible for getting the news information from the news API.",
        },
        {
            "name": "calendar",
            "description": "Responsible for getting the calendar information from the Google Calendar API.",
        },
        {
            "name": "email",
            "description": "Responsible for getting the email information from the email IOT device.",
        },
        {
            "name": "shopping",
            "description": "Could shop for groceries and other items from the shopping API, get the shopping history, and current campaign offers.",
        },
        
        {
            "name": "window",
            "description": "Responsible for getting the windows status from the window IOT device.",
        },
        {
            "name": "light",
            "description": "Responsible for getting the light status from the light IOT device.",
        },
        {
            "name": "stove",
            "description": "Responsible for getting the stove status from the stove IOT device.",
        },
        {
            "name": "water_tank",
            "description": "Could get the water level from the water tank IOT device.",
        }
    ]
    blackboard: Blackboard = Blackboard(
        plan=Plan(steps=[]),
        history=History(steps=[]),
    )
