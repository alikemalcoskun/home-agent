from typing import List
from enum import Enum
from pydantic import BaseModel

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

    def get_schema():
        return f"""
        - status: string (pending, in_progress, completed, failed)
        """

class Step(BaseModel):
    agent: str
    description: str
    status: Status = Status.PENDING

    def __str__(self):
        return f"- Agent: {self.agent}\n- Description: {self.description}\n- Status: {self.status}"
    
    def get_schema():
        return f"""
        - agent: string
        - description: string
        - status: {Status.get_schema()}
        """

class Plan(BaseModel):
    steps: List[Step] = []
    status: Status = Status.PENDING

    def __str__(self):
        return f"Steps: {self.steps}\nStatus: {self.status}"
    
    def get_schema(self):
        return f"""
        - steps:
            {Step.get_schema()}
        - status:
            {Status.get_schema()}
        """

class History(BaseModel):
    steps: List[Step]
    status: Status = Status.PENDING

    def __str__(self):
        return f"Steps: {self.steps}\nStatus: {self.status}"
    
    def get_schema(self):
        return f"""
        - steps:
            {Step.get_schema()}
        - status:
            {Status.get_schema()}
        """

class Blackboard(BaseModel):
    plan: Plan = Plan(steps=[], status=Status.PENDING)
    history: History = History(steps=[], status=Status.PENDING)

    def __str__(self):
        return f"Plan: {self.plan}\nHistory: {self.history}"
    
    def get_schema(self):
        return f"""
        - plan:
            {self.plan.get_schema()}
        - history:
            {self.history.get_schema()}
        """
