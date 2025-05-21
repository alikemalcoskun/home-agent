from app.agents.base import BaseAgent
from app.models.state import State
from app.models.blackboard import Blackboard
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
import json


class OrchestrationAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        self.name = "orchestration"
        self.description = f"""
            Your task is to create a plan to run the agents according to the information provided by the user or an IoT device.

            You will be given:
            - a user request,
            - a list of agents,
            - and a blackboard that contains the history of the plan and the agents' results.

            You need to determine if further actions are needed. For example:

            - If you checked the windows and some are open, you must add a new step to close those windows.
            - If you checked the lights and some are on, you must add a new step to turn those lights off.
            - If you checked the water tank and the water level is low, you should add a step to order water.
            - You must continue adding steps until all necessary actions are completed.

            If the plan is not completed, create a new plan and add a new 'pending' orchestration step to the history.

            If the plan is completed, add a new 'completed' orchestration step to the history with a **warm, friendly, assistant-like summary describing what was done and the results**, focusing on the outcome rather than the process.

            Do **not** describe your internal reasoning or what you did step-by-step. Instead, describe the final results to the user in a natural, conversational tone, like a helpful assistant speaking directly.

            **IT IS CRITICAL TO SET THE STATUS TO 'completed' IF THE PLAN IS COMPLETED.**

            ---

            ### Example 1:

            User request: "I'm leaving the house. Check windows and lights. Close or turn off those that are open/on. Also, order water if the water tank level is low."

            History indicates:
            - Bedroom window is open.
            - Living room lights are on.
            - Water tank level is low (2).

            Expected final orchestration step:

            
            "agent": "orchestration",
            "description": "I closed the open bedroom window, turned off the living room lights, and ordered water since the tank was running low. Your home is all set now! Feel free to ask if you need anything else 😊",
            "status": "completed"
            

            ---

            ### Example 2:

            User request: "Check the stove and make sure it is off. If it is on, turn it off."

            History:
            - Stove status is 'on'.

            Expected plan update:
            - Add a step to turn off the stove.

            When done, final orchestration step:

            
            "agent": "orchestration",
            "description": "The stove was on, so I turned it off for you. Everything is safe now. Let me know if you'd like me to check anything else!",
            "status": "completed"
            

            ---

            ### Example 3:

            User request: "Get today's weather and my calendar events."

            History:
            - Weather fetched: sunny, 22°C.
            - Calendar fetched: 3 meetings.

            Final orchestration step:

            
            "agent": "orchestration",
            "description": "It's sunny and 22 degrees today. You have 3 meetings on your calendar. Just say the word if you want more details!",
            "status": "completed"
            

            ---

            ### Important:

            - Invoke only the agents necessary for the next actions.
            - Always return the updated blackboard as valid JSON with the plan and history updated accordingly.
            - Use a friendly, helpful, and conversational tone in the final summary so the user feels like they’re talking to a smart assistant who understands and cares.

            ---

            Return the blackboard as JSON with the following format:

            {str(self.blackboard.get_schema())}

            **DO NOT MODIFY THE PROVIDED HISTORY. ONLY ADD NEW STEPS TO THE HISTORY.**
            """




    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
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
