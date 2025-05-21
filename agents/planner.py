from agents.base import BaseAgent
from models.state import State
from models.blackboard import Blackboard
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
import json


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        self.name = "planner"
        self.description = f"""
        Your task is to create a plan to run the agents according to the information provided by the user or an IOT device.

        You will be given a user request and a list of agents.

        You need to create a plan to run the agents according to the user's request.

        If your request is request by an IOT device(it is informed in the request).
        Create a new flow by the information provided by the IOT device.
        For example, if the user request is "Weather API: Rainy this evening", check the windows.
        
        Please add your plan details(what is your purpose to invoke the agent) to the history of the blackboard.

        INVOKE ONLY THE AGENTS THAT ARE NEEDED FOR THE REQUEST!

        You need to return the blackboard as JSON with the following format:
            {str(self.blackboard.get_schema())}
        """

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print(f"Executing Planner Agent")

        self.state = state
        self.blackboard = state.blackboard
        self.prompt = self.get_prompt(state)

        user_prompt = '''
        List of agents: {agents}
        User request: {request}
        '''

        messages = [
            ("system", self.prompt),
            ("user", user_prompt),
        ]

        prompt = ChatPromptTemplate(messages)
        response = self.llm.invoke(prompt, is_response_json=True,
                                   input={"agents": state.agents, "request": state.request})

        self.blackboard = Blackboard(**response)
        blackboard_dict = json.loads(self.blackboard.model_dump_json())
        
        return {"blackboard": blackboard_dict}
