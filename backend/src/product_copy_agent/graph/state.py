import pandas as pd

from typing import Annotated, TypedDict, Optional
from langgraph.graph import add_messages

class AgentState(TypedDict):
    """LangGraph state schema for product copy validation agent."""
    user_choice: Optional[str]
    instruction_file: Optional[str]
    input_file_df: Optional[pd.DataFrame]
    latest_prompt: Optional[str]
    output_file: Optional[str]
    prompt_exists: bool
    input_file: Optional[str]
    logs: Annotated[list, add_messages]
    messages: Annotated[list, add_messages]  # holds Human/AI/System messages


def initial_state() -> AgentState:
    """Initial state for the LangGraph agent."""
    return {
        "user_choice": None,
        "instruction_file": None,
        "input_file": None,
        "latest_prompt": None,
        "output_file": None,
        "prompt_exists": False,
        "input_file": None,
        "messages": [],
        "logs": [],
    }