from models.state import State
from models.blackboard import Blackboard, Plan, History, Status
from langgraph.graph import StateGraph, START, END
from IPython.display import Image
from agents.orchestration import OrchestrationAgent
from agents.edge_agents.window import WindowAgent
from agents.edge_agents.light import LightAgent
from agents.edge_agents.stove import StoveAgent
from agents.edge_agents.water_tank import WaterTankAgent
from agents.edge_agents.weather import WeatherAgent
from agents.edge_agents.news import NewsAgent
from agents.edge_agents.calendar import CalendarAgent
from agents.edge_agents.email import EmailAgent
from agents.edge_agents.shopping import ShoppingAgent
from typing import Dict, Any


class OrchestrationService:
    def __init__(self):
        self.router_builder = StateGraph(State)
        self.workflow = None
        self.iteration_count = 0
        self.max_iterations = 2  # Maximum number of iterations to prevent infinite loops

        # Initialize agents
        self.orchestration_agent = OrchestrationAgent()
        self.edge_agents = {
            "window": WindowAgent(),
            "light": LightAgent(),
            "stove": StoveAgent(),
            "water_tank": WaterTankAgent(),
            "weather": WeatherAgent(),
            "news": NewsAgent(),
            "calendar": CalendarAgent(),
            "email": EmailAgent(),
            "shopping": ShoppingAgent()
        }

    def generate_workflow(self) -> StateGraph:
        # Add nodes for each step in the pipeline
        self.router_builder.add_node("get_plan", self._get_plan)
        self.router_builder.add_node("execute_edge_agents", self._execute_edge_agents)
        self.router_builder.add_node("check_completion", self._check_completion)

        # Add edges to connect nodes
        self.router_builder.add_edge(START, "get_plan")
        self.router_builder.add_edge("get_plan", "execute_edge_agents")
        self.router_builder.add_edge("execute_edge_agents", "check_completion")
        self.router_builder.add_conditional_edges(
            "check_completion",
            self._should_continue,
            {
                True: "get_plan",
                False: END
            }
        )

    def _get_plan(self, state: State) -> State:
        """Get plan from orchestration agent"""
        
        # Increment iteration counter
        self.iteration_count += 1
        
        result = self.orchestration_agent.execute(state)
        state.blackboard = Blackboard(**result["blackboard"])
        return state

    def _execute_edge_agents(self, state: State) -> State:
        """Execute edge agents based on the plan"""
        # Get pending steps from the plan
        pending_steps = [step for step in state.blackboard.plan.steps 
                         if step.status == Status.PENDING]
        
        # Execute each pending step with the appropriate agent
        for step in pending_steps:
            agent_name = step.agent
            if agent_name in self.edge_agents:
                agent = self.edge_agents[agent_name]
                result = agent.execute(state)
                state.blackboard = Blackboard(**result["blackboard"])
        
        return state

    def _check_completion(self, state: State) -> State:
        """Check if we should continue or end the session"""
        # Check if all steps in the plan are completed
        all_completed = all(step.status == Status.COMPLETED 
                           for step in state.blackboard.plan.steps)
        
        # If all steps are completed, mark the plan as completed
        if all_completed:
            state.blackboard.plan.status = Status.COMPLETED
        
        return state

    def _should_continue(self, state: State) -> bool:
        """Conditional edge function to determine if we should continue"""
        # Continue if the plan is not completed and we haven't exceeded max iterations
        return (state.blackboard.plan.status != Status.COMPLETED and 
                self.iteration_count < self.max_iterations)

    def compile_workflow(self):
        """Compile the workflow"""
        self.workflow = self.router_builder.compile()

    def invoke(self, state: State) -> State:
        """Invoke the workflow with initial state"""
        return self.workflow.invoke(state)

    def draw_workflow(self):
        """Generate and save workflow visualization"""
        img = Image(self.workflow.get_graph().draw_mermaid_png())
        with open("workflow.png", "wb") as f:
            f.write(img.data)