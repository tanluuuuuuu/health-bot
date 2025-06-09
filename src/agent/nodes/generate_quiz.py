from __future__ import annotations
from typing import Any, Dict
from src.llm_models.openai_model_with_tools import openai_with_tools
from src.agent.utils import load_prompt_template
from src.agent.state import State
from langchain_core.messages import HumanMessage, AIMessage


def generate_quiz(state: State):
    response = openai_with_tools.invoke(state["messages"])
    return {"messages": [response]}
