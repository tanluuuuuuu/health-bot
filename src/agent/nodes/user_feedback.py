"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from typing import Any, Dict

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from src.agent.state import State
from langgraph.types import interrupt, Command

import json

SYSTEM_QUESTION = "What would you like to do next?\n1. Ask another question about this topic\n2. Take a comprehension check\n3. Learn about a new health topic\n4. Exit the session\n> "

def user_feedback(state: State) -> Dict[str, Any]:
    """Respond to user feedback."""
    feedback = input(SYSTEM_QUESTION)
    return {"messages": [HumanMessage(content=feedback)]}

    # interrupt didn't stop the execution of the program
    # feedback = interrupt("Do you have any other questions? Or would you like to take a comprehension check?")
    # return {"messages": [HumanMessage(content=feedback)]}


if __name__ == "__main__":
    pass
