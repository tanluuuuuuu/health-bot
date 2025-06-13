"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from typing import Any, Dict
from src.llm_models.openai_model_with_tools import openai_with_tools
from src.agent.utils import load_prompt_template
from src.agent.state import State
from langchain_core.messages import HumanMessage, AIMessage


def start_researching(state: State):
    response = openai_with_tools.invoke(state["messages"])
    return {"messages": [response]}
