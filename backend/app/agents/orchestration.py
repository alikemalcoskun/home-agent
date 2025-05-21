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
            Your task is to orchestrate agents in order to fulfill the user's request, using the planning history (blackboard) and the agent outputs.

            You are given:
            - A user request
            - A list of available agents (with their capabilities)
            - A blackboard that contains the orchestration history and agent results

            ---

            🎯 OBJECTIVE
            Create a dynamic, step-by-step plan to achieve the user's intent. At each step, analyze agent results and determine if further action is needed.

            ---

            📌 INSTRUCTIONS

            1. Think step by step:
            - What is the user trying to achieve?
            - What was the last agent's output?
            - Does it fully satisfy the request?
            - If not, what is the next necessary agent to call?

            2. If the plan is not yet complete:
            - Add the next required action as a new 'pending' step in the history
            - Do NOT re-run already executed agents unless new information changes the context

            3. If the plan is completed:
            - Add a new 'completed' step to the history
            - Include a friendly **summary** written in the voice of a helpful assistant

            ---

            🗣️ SUMMARY BEHAVIOR

            If the plan is completed, you must add a new 'completed' orchestration step to the history.

            This step must include a friendly assistant-style **summary** that:
            - Clearly states the **final results**, not just what was done
            - Avoids formal or robotic tone
            - Mentions the actual **data retrieved** (e.g., number of meetings, weather condition, match results)
            - Uses natural, conversational language

            Bad example (too formal):
            "The user's request has been fulfilled. Calendar events were retrieved."

            Good example (assistant style):
            "📅 You have 3 meetings today, and ⚽️ Galatasaray won 2-1! Let me know if you'd like me to remind you before your first meeting 😊"

            ---

            📦 OUTPUT FORMAT

            Return the updated blackboard as JSON using this schema:
            {str(self.blackboard.get_schema())}

            Only add new entries. Do not modify existing steps.
            Invoke only the agents needed for the next action!
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
