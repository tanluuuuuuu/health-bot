from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from src.tools.tavily import tavily_search_tool

load_dotenv()

openai_model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    streaming=False,
    base_url = "https://openai.vocareum.com/v1",
    max_tokens=250
)

tools = [tavily_search_tool]
openai_with_tools = openai_model.bind_tools(tools=tools)

