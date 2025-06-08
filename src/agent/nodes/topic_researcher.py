"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations
from typing import Any, Dict
from src.llm_models.openai_model_with_tools import openai_with_tools
from src.agent.utils import load_prompt_template
from src.agent.state import State
from langchain_core.messages import HumanMessage, AIMessage


# def get_topic_from_user(state: State):
#     human_message = HumanMessage(
#         content=f"Tell me everything I need to know about {state['topic']}, {state['focus_aspects']}. Summarize the results in 3-5 sentences in patient-friendly language.")
#     return {"topic": topic, "messages": [human_message]}
