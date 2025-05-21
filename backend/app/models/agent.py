from pydantic import BaseModel
from app.models.blackboard import Blackboard


class AgentRequest  (BaseModel):
    query: str
    owner: str = "user"

class AgentResponse(BaseModel):
    blackboard: Blackboard