from langchain_tavily import TavilySearch
import os

tavily_search_tool = TavilySearch(
    api_key=os.getenv('TAVILY_API_KEY'),
    max_results=2,
    topic="general",
    include_raw_content=True
    # include_answer=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)
# tavily_search_tool.invoke("apple meaning")