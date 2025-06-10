from src.agent.graph import app
from src.agent.graph_v1 import app_v1
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.tool import ToolMessage

# user_input = input("Enter a health topic:\n> ")
result = app.invoke({
    "topic": "",
    "messages": [],
},
    config = {"configurable": {"thread_id": "1"}}
)

for message in result["messages"]:
    if isinstance(message, ToolMessage):
        continue
    message.pretty_print()
