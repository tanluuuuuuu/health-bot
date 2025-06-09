from src.agent.state import State
from langchain_core.messages import ToolMessage
from langgraph.graph import END


def clarification_router(state: State) -> str:
    """Route based on whether clarification is needed."""
    if state["needs_clarification"] and state["clarifying_questions"]:
        return "ask_questions"
    return "end"


def rout_to_tools(state: State) -> str:
    """
        Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools_node"
    return END
