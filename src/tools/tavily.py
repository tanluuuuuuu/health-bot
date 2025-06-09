from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

tavily_search_tool = TavilySearch(
    tavily_api_key=os.getenv('TAVILY_API_KEY'),
    max_results=2,
    topic="general",
    include_raw_content=True
)
# print(tavily_search_tool.invoke("apple meaning"))
