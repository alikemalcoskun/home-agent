from abc import ABC, abstractmethod
from typing import Any, Dict
from services.llm import LLMService
from models.blackboard import Blackboard

class BaseAgent(ABC):
    def __init__(self):
        self.name = "Agent"
        self.description = "description"

        self.llm = LLMService()

        self.state = None
        self.blackboard = Blackboard()
        self.prompt = ""
        
    def get_prompt(self, state: Dict[str, Any]) -> str:
        return f"""
                    You are an agent named {self.name}.

                    Your description is: {self.description}

                    You are given a blackboard with a plan and a history.

                    You need to execute your task and update the blackboard plan and history.
                    DO NOT FORGET TO UPDATE THE HISTORY. You need to update the history of the blackboard with only your({self.name}) actions.
                    
                    The blackboard is: {state.blackboard}

                    """

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the given step and return the results.
        """
        pass
        