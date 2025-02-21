from typing import List, Callable, Union
from pydantic import BaseModel
from config import MEMORY

AgentFunction = Callable[[], Union[str, "Agent", dict]]

class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o-mini"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent."
    functions: List[AgentFunction] = []
    max_tokens: int = 2048
    temperature: float = 0.75
    top_p: float = 1.0
    memory = MEMORY

    class Config:
        extra = "allow"  # Dynamic