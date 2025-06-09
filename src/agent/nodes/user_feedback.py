"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from typing import Any, Dict

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent.state import State
from langgraph.types import interrupt, Command

import json


def user_feedback(state: State) -> Dict[str, Any]:
    """Respond to user feedback."""
    feedback = input("Do you have any other questions? Or would you like to take a comprehension check?\n> ")
    return {"messages": [HumanMessage(content=feedback)]}

    # interrupt didn't stop the execution of the program
    # feedback = interrupt("Do you have any other questions? Or would you like to take a comprehension check?")
    # return {"messages": [HumanMessage(content=feedback)]}


if __name__ == "__main__":
    pass
