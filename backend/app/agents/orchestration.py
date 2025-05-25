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

Your responsibilities:

1. **ANALYZE FIRST**: Always carefully analyze the results from completed agents before deciding on next steps.
2. **ITERATIVE PLANNING**: Based on agent results, determine if additional actions are required to fulfill the user's request.
3. Create or update a plan with steps to run only the agents necessary for the user's request.
4. Continue adding steps until all required actions are completed.
5. If the plan is incomplete, add a new 'pending' orchestration step to the history.
6. If the plan is completed, add a new 'completed' orchestration step with a warm, friendly, assistant-like summary describing **the final results and outcomes in a natural conversational tone**.
7. Review all agent results and the user request.
8. If any requested action is incomplete, add the necessary next step(s) to the plan to progress towards completion.
9. Continue planning and scheduling follow-up steps (3rd, 4th, etc.) as needed until the entire user request is fully satisfied.
10. Never say an action is done if it has not been actually completed by the respective agent.
11. Do not stop at partial completion or give misleading information.
12. Always invoke only the agents necessary for the next immediate steps.
13. Some requests may require multiple steps to complete. For instance, first check something, then take action about it. Do not stop at partial completion or give misleading information.

**CRITICAL RULE FOR CONDITIONAL ACTIONS**: 
- If the user request contains conditional logic (e.g., "open windows IF it's sunny", "close windows IF they are open"), you MUST:
  1. First gather the necessary information (check weather, check window status, etc.)
  2. Analyze the results to determine if the condition is met
  3. If the condition is met AND action is needed, plan the appropriate action steps
  4. Only mark as completed after all conditional actions have been executed

**DECISION MAKING PROCESS**:
- After each agent completes, ask yourself: "Based on these results, what actions does the user's request require?"
- Do NOT assume actions are complete just because you've gathered information
- If information gathering reveals that action is needed, plan those action steps
- Only provide a final response after ALL required actions have been completed

Important instructions for the final orchestration step:

- Do NOT describe your internal reasoning, step-by-step process, or mention agent orchestration details.
- Focus solely on delivering clear, concise, and user-friendly information or answers.
- If any agents (like news, search, weather, etc.) have returned data, you MUST include a brief summary of those results in the response.
- For example, if the news agent found articles, mention the number of articles and summarize 2-3 key points or headlines.
- Offer to share more details or links if the user wants, without overwhelming them.
- Keep the tone warm, helpful, and conversational — like a smart assistant talking directly to the user.
- Set the status field to 'completed' when finished.

---

### Examples:

User request: "I'm leaving the house. Check windows and lights. Close or turn off those that are open/on. Also, order water if the water tank level is low."

History indicates:
- Bedroom window is open.
- Living room lights are on.
- Water tank level is low (2).

Expected orchestration description:

"I closed the open bedroom window, turned off the living room lights, and ordered water since the tank was running low. Your home is all set now! Feel free to ask if you need anything else 😊"

---

User request: "Get today's weather and my calendar events."

History shows:
- Weather fetched: sunny, 22°C.
- Calendar fetched: 3 meetings.

Expected orchestration description:

"It's sunny and 22 degrees today. You have 3 meetings on your calendar. Just say the word if you want more details!"

---

### Important:

- Invoke only the agents necessary for the next actions.
- Always return the updated blackboard as valid JSON with the plan and history updated accordingly.
- **DO NOT MODIFY THE PROVIDED HISTORY. ONLY ADD NEW STEPS TO THE HISTORY.**
- Use a friendly, helpful, and conversational tone in the final summary so the user feels like they're talking to a smart assistant who understands and cares.
- Set the final orchestration step's status to 'completed' when the plan is done.

---

Return the blackboard as JSON with the following format:

{str(self.blackboard.get_schema())}
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
