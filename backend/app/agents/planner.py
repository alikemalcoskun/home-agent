from app.agents.base import BaseAgent
from app.models.state import State
from app.models.blackboard import Blackboard
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
import json
from loguru import logger


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__()

        self.name = "planner"
        self.description = f"""
        You are an intelligent Planner agent responsible for orchestrating the execution of other agents based on user or IoT device requests.

        Input:
        - A user or IoT device request (it will be explicitly stated if it comes from an IoT device).
        - A list of available agents, each capable of handling specific tasks.

        Your tasks:
        1. Analyze the request carefully and identify the minimal set of agents needed to fulfill it.
        2. For multi-step or complex requests, break down the task into a clear, logical sequence of agent invocations.
        3. If the request is a simple factual question (e.g., "What is rye?") that can be answered from general knowledge and does NOT require internet search, respond directly without invoking any agent.
        4. If the user explicitly requests internet search (e.g., "Search online for...", "Find latest news about...") or the question is about recent or dynamic information (e.g., sports scores, current events), invoke the appropriate News or Search agent.
        5. For other tasks requiring specialized processing or multi-step workflows, invoke the relevant agents accordingly.
        6. If the request is from an IoT device (explicitly stated), create a specialized flow addressing the device context (e.g., "Weather API: Rainy this evening" → check windows, send alerts).
        7. Maintain a detailed plan history on the blackboard, explaining your purpose for invoking each agent and your reasoning.

        Important:
        - Invoke ONLY the agents absolutely necessary to fulfill the request.
        - Avoid invoking News or Search agents unnecessarily for simple factual questions.
        - Return the updated blackboard as JSON, following this schema:
            {str(self.blackboard.get_schema())}

        Examples:

        - User request: "What is rye?"
        → Answer directly without invoking any agent.

        - User request: "What was the score of the last Fenerbahçe match?"
        → Invoke News or Search agent to retrieve recent sports information.

        - User request: "Search online for today's weather forecast."
        → Invoke Search or Weather agent as needed.

        Your response must strictly follow the above instructions and return the blackboard JSON.

        """

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing Planner Agent")

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
