from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing import Dict
import os
from dotenv import load_dotenv
from src.llm_models.openai_models import openai_model
from src.agent.utils import load_prompt_template

load_dotenv()
SUMMARY_PROMPT_TEMPLATE = load_prompt_template("search_summarization")

tavily_client = TavilySearch(
    tavily_api_key=os.getenv('TAVILY_API_KEY'),
    max_results=2,
    topic="general",
    include_raw_content=True
)

@tool("tavily_search_tool", parse_docstring=True)
def tavily_search_tool(topic: str, query: str) -> str:
    """Search the web for information using Tavily.

        Args:
            topic: The topic for which to search answers.
            query: The search query string

        Returns:
            Dict containing search results with URLs, titles, and content snippets
    """
    result = tavily_client.invoke(query)
    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        topic=topic,
        search_results=result,
    )
    summary_response = openai_model.invoke(prompt).content
    return summary_response


