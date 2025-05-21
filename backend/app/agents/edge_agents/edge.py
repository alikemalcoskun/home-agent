from app.agents.base import BaseAgent
from typing import Dict, Any
from app.services.llm import LLMService
from app.models.blackboard import Blackboard, Status
import json
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

class EdgeAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        self.name = "Edge Agent"
        self.slug = "edge"
        self.description = "Edge Agent is responsible for checking the status of the edge devices."

        self.llm = LLMService()

        self.state = None
        self.blackboard = Blackboard()
        self.prompt = ""

        self.tools = []
        
    def get_prompt(self, state: Dict[str, Any]) -> str:
        return f"""
                    You are an edge agent named {self.name}. 
                    An edge agent is responsible for checking the status of the edge devices or APIs and running the corresponding actions.
                    An edge agent has a list of function tools to communicate with the edge devices.
                    DO NOT ADD ANY PARAMETERS TO THE FUNCTIONS OTHER THAN THE REQUIRED ONES.

                    Your description is: {self.description}

                    You are given a blackboard with a plan and a history.

                    You need to execute your task and update the blackboard plan and history.
                    DO NOT FORGET TO UPDATE THE HISTORY. You need to update the history of the blackboard with only your({self.name}) actions.
                    Add the result of the action to the description of the corresponding entry in the history.
                    
                    The blackboard is: {state.blackboard}

                    See the requested pending actions from user input.
                    Use the tools to execute the actions.
                    Update the blackboard plan and history with the results of the actions.
                    DO NOT RETURN ANYTHING ELSE. ONLY RETURN THE UPDATED BLACKBOARD JSON.

                    You need to return the blackboard as JSON with the following format:
                        {str(self.blackboard.get_schema())}
                    """

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the given step and return the results.
        """
        self.state = state
        self.blackboard = state.blackboard
        self.prompt = self.get_prompt(state)

        # Get pending edge actions from the blackboard
        pending_actions = [step for step in self.blackboard.plan.steps if step.status == Status.PENDING and step.agent == self.slug]

        if len(pending_actions) == 0:
            logger.info(f"No pending actions for {self.name}")
            return None

        user_prompt = '''
        Pending actions: {pending_actions}
        '''

        messages = [
            ("system", self.prompt),
            ("user", user_prompt),
        ]

        prompt = ChatPromptTemplate(messages)
        response = self.llm.invoke(prompt, is_response_json=True, tools=self.tools,
                                   input={"pending_actions": pending_actions})

        self.blackboard = Blackboard(**response)
        blackboard_dict = json.loads(self.blackboard.model_dump_json())
        
        return {"blackboard": blackboard_dict}
        