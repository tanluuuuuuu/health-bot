from langgraph.graph import StateGraph, START, END
from src.agent.state import State
from src.agent.nodes.clarify_user_request import clarify_user_request, ask_clarifying_questions, craft_final_request, \
    clarification_router
from src.agent.nodes.user_feedback import user_feedback
from src.agent.nodes.topic_researcher import start_researching
from src.agent.nodes.tool_route import route_to_tools, feedback_router
from langgraph.prebuilt import ToolNode
from src.tools.tavily import tavily_search_tool
from src.tools.list_tools import tools
from langgraph.checkpoint.memory import MemorySaver
from src.agent.nodes.generate_quiz import generate_quiz
from src.agent.nodes.new_topic import start_new_topic, start_new_topic_with_new_state

graph = StateGraph(State)
graph.add_node("start_new_topic", start_new_topic)
graph.add_node("start_new_topic_with_new_state", start_new_topic_with_new_state)
graph.add_node("clarify", clarify_user_request)
graph.add_node("ask_questions", ask_clarifying_questions)
graph.add_node("final_request", craft_final_request)
graph.add_node("start_researching", start_researching)
graph.add_node("tools_node", ToolNode(tools))
graph.add_node("user_feedback", user_feedback)
graph.add_node("generate_quiz", generate_quiz)

# Add edges - in this simple case, just from start to our node
graph.add_edge(START, "start_new_topic")
graph.add_edge("start_new_topic", "clarify")
graph.add_edge("clarify", "ask_questions")
# graph.add_conditional_edges(
#     "clarify",
#     clarification_router,
#     {
#         "ask_questions": "ask_questions",
#         "start_researching": "start_researching"
#     }
# )
graph.add_edge("ask_questions", "final_request")
graph.add_edge("final_request", "start_researching")
graph.add_conditional_edges(
    "start_researching",
    route_to_tools,
    {
        "tools_node": "tools_node",
        "user_feedback": "user_feedback"
    }
)
graph.add_edge("tools_node", "start_researching")
graph.add_conditional_edges(
    "user_feedback",
    feedback_router,
    {
        "start_researching": "start_researching",
        "generate_quiz": "generate_quiz",
        "start_new_topic": "start_new_topic_with_new_state",
        "user_feedback": "user_feedback",
        END: END
    }
)
graph.add_edge("generate_quiz", "user_feedback")
graph.add_edge("start_new_topic_with_new_state", "clarify")


# Compile the graph
memory = MemorySaver()
app = graph.compile(name="Health Assistant Graph", checkpointer=memory)
app.get_graph().draw_mermaid_png(output_file_path="./graph_images/graph.png")

if __name__ == "__main__":
    # Run the graph
    result = app.invoke({
        "messages": [],
        "topic": "infections",
        "focus_aspects": "",
        "needs_clarification": False,
        "clarifying_questions": [],
        "additional_information": []
    })

    for message in result["messages"]:
        message.pretty_print()
