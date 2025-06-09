from langgraph.graph import StateGraph, START, END
from src.agent.state import State
from src.agent.nodes.clarify_user_request import clarify_user_request, ask_clarifying_questions, craft_final_request, \
    clarification_router
from src.agent.nodes.topic_researcher import start_researching
from src.agent.nodes.tool_route import route_to_tools
from langgraph.prebuilt import ToolNode
from src.tools.tavily import tavily_search_tool
from src.tools.list_tools import tools

graph = StateGraph(State)
graph.add_node("start_researching", start_researching)
graph.add_node("tools_node", ToolNode(tools))

graph.add_edge(START, "start_researching")
graph.add_conditional_edges(
    "start_researching",
    route_to_tools,
    {"tools_node": "tools_node", END: END})
graph.add_edge("tools_node", "start_researching")


# Compile the graph
app_v1 = graph.compile(name="Health Assistant Graph")
app_v1.get_graph().draw_mermaid_png(output_file_path="./graph_images/graph_v1.png")

if __name__ == "__main__":
# Run the graph
    result = app_v1.invoke({
        "messages": [],
        "topic": "infections",
        "focus_aspects": "",
        "needs_clarification": False,
        "clarifying_questions": [],
        "additional_information": []
    })

    for message in result["messages"]:
        message.pretty_print()
