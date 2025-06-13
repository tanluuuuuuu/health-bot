from __future__ import annotations
from typing import Any, Dict
from src.agent.state import State
from src.agent.utils import reset_graph_state

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
