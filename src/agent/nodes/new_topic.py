"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from typing import Any, Dict

from langchain.chains.question_answering.map_reduce_prompt import messages
from langchain_core.messages import HumanMessage

from src.llm_models.openai_models import openai_model
from src.agent.utils import load_prompt_template
from src.agent.state import State
from langgraph.graph.message import REMOVE_ALL_MESSAGES, RemoveMessage
from src.agent.utils import reset_graph_state

import json


def start_new_topic(state: State) -> Dict[str, Any]:
    user_input = input("Enter a health topic:\n> ")
    return {
        "topic": user_input,
    }

def start_new_topic_with_new_state(state: State) -> Dict[str, Any]:
    new_state = reset_graph_state(state)
    user_input = input("Enter a health topic:\n> ")
    new_state["topic"] = user_input
    return new_state

if __name__ == "__main__":
    pass
