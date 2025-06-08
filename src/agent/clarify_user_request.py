"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from typing import Any, Dict
from src.llm_models.openai_models import openai_model
from src.agent.utils import load_prompt_template
from src.agent.state import State

import json

def clarify_user_request(state: State) -> Dict[str, Any]:
    """Process user's health topic query and generate clarifying questions.

    This function analyzes the user's initial query about a health topic and generates
    relevant clarifying questions to better understand their specific needs before
    providing a comprehensive answer.

    Args:
        state: Contains the user's initial health topic query
        config: Runtime configuration for the model

    Returns:
        Dictionary containing the clarification questions and original query
    """
    prompt_template = load_prompt_template("clarify_user_request")
    prompt = prompt_template.format(
        user_input=state["original_user_input"]
    )
    response = openai_model.invoke(prompt)
    try:
        parsed_response = json.loads(response.content)
        needs_clarification = parsed_response.get("needs_clarification", False)
        clarifying_questions = parsed_response.get("clarifying_questions", [])

        return {
            "improved_user_input": response.content,
            "needs_clarification": needs_clarification,
            "clarifying_questions": clarifying_questions
        }

    except json.JSONDecodeError:
        # Handle case where response is not valid JSON
        return {
            "needs_clarification": False,
            "clarifying_questions": []
        }


def ask_clarifying_questions(state: State) -> Dict[str, Any]:
    """Ask the user clarifying questions and collect their responses."""
    additional_info = []
    for question in state["clarifying_questions"]:
        print(f"I need you to clarify one thing: {question}")
        human_response = input("Your answer: ")
        additional_info.append(f"""
        Question: {question}
        User answer: {human_response}
""")

    return {
        "additional_information": additional_info,
        "needs_clarification": False,
        "clarifying_questions": []
    }

def clarification_router(state: State) -> str:
    """Route based on whether clarification is needed."""
    if state["needs_clarification"] and state["clarifying_questions"]:
        return "ask_questions"
    return "end"

def craft_final_request(state: State) -> Dict[str, Any]:
    """Craft the final request for the LLM model."""
    prompt = load_prompt_template("craft_user_final_request").format(
        original_user_input=state["original_user_input"],
        additional_information=state["additional_information"].join("\n")
    )
    response = openai_model.invoke(prompt)
    return {
        "improved_user_input": response.content,
    }

if __name__ == "__main__":
    from langgraph.graph import StateGraph, START, END
    from src.agent.state import State
    from src.agent.clarify_user_request import clarify_user_request, ask_clarifying_questions, clarification_router, \
        craft_final_request

    graph = StateGraph(State)
    graph.add_node("clarify", clarify_user_request)
    graph.add_node("ask_questions", ask_clarifying_questions)
    graph.add_node("final_request", craft_final_request)

    # Add edges - in this simple case, just from start to our node
    graph.add_edge(START, "clarify")
    graph.add_conditional_edges(
        "clarify",
        clarification_router,
        {
            "ask_questions": "ask_questions",
            "end": END
        }
    )
    graph.add_edge("ask_questions", "final_request")
    graph.add_edge("final_request", END)

    # Compile the graph
    app = graph.compile(name="Health Assistant Graph")

    # Run the graph
    result = app.invoke({
        "original_user_input": "I'm experiencing headaches and I've been struggling for the past week.",
        "improved_user_input": "",
        "needs_clarification": False,
        "clarifying_questions": [],
        "additional_information": []
    })

    print(result)
