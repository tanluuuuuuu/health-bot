from __future__ import annotations
from typing import Any, Dict
from src.agent.state import State
from src.agent.utils import reset_graph_state

def summarize_search_result(state: State) -> Dict[str, Any]:
    user_input = input("Enter a health topic:\n> ")
    return {
        "topic": user_input,
    }

if __name__ == "__main__":
    pass
