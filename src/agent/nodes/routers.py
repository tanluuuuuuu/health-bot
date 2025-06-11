from src.agent.state import State
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langgraph.graph import END
from src.llm_models.openai_models import openai_model
from src.agent.utils import load_prompt_template
from src.agent.nodes.user_feedback import SYSTEM_QUESTION

next_action_feedback_prompt_template = load_prompt_template("next_action_baseon_feedback")

def clarification_router(state: State) -> str:
    """Route based on whether clarification is needed."""
    if state["needs_clarification"] and state["clarifying_questions"]:
        return "ask_questions"
    return "end"


def research_router(state: State) -> str:
    """
        Use in the conditional_edge to route to the ToolNode if the last message
        has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        message = state[-1]
    elif messages := state.get("messages", []):
        message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(message, "tool_calls") and len(message.tool_calls) > 0:
        return "tools_node"
    if isinstance(message, ToolMessage):
        return "tools_node"
    return "user_feedback"

def feedback_router(state: State) -> str:
    """
    """
    if isinstance(state, list):
        message = state[-1]
    elif messages := state.get("messages", []):
        message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if isinstance(message, HumanMessage):
        prompt = next_action_feedback_prompt_template.format(
            user_query=message,
            system_previous_question=SYSTEM_QUESTION,
        )
        response = openai_model.invoke(prompt).content
        if response == "start_researching":
            return "start_researching"
        elif response == "generate_quiz":
            return "generate_quiz"
        elif response == "start_new_topic":
            print("Are you sure? Start new topic we delete previous context and start a new one.\n> (y/n): ")
            user_input = input()
            if user_input.lower() == "y":
                return "start_new_topic"
            return "user_feedback"
        elif response == "END":
            return END
        else:
            raise ValueError(f"Invalid response from feedback_route_to_tools: {response}")
    return END
