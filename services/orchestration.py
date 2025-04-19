from models.state import State

from langgraph.graph import StateGraph, START, END
from IPython.display import Image

from agents.orchestration import OrchestrationAgent



class OrchestrationService:
    def __init__(self):
        self.router_builder = StateGraph(State)
        self.workflow = None

        # Agents
        self.orchestration_agent = OrchestrationAgent()

    def generate_workflow(self) -> StateGraph:
        # Add nodes
        self.router_builder.add_node("orchestration_agent", self.orchestration_agent.execute)

        # Add edges to connect nodes
        self.router_builder.add_edge(START, "orchestration_agent")
        self.router_builder.add_edge("orchestration_agent", END)

    def compile_workflow(self):
        # Compile workflow
        self.workflow = self.router_builder.compile()

    def invoke(self, state):
        # Invoke workflow
        return self.workflow.invoke(state)

    def draw_workflow(self):
        # Show the workflow
        img = Image(self.workflow.get_graph().draw_mermaid_png())
        with open("workflow.png", "wb") as f:
            f.write(img.data)