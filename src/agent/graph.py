from langgraph.graph import StateGraph, START, END
from src.agent.state import State
from src.agent.clarify_user_request import clarify_user_request, ask_clarifying_questions, clarification_router, craft_final_request

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

if __name__ == "__main__":
    # Run the graph
    result = app.invoke({
        "original_user_input": "I'm experiencing headaches and I've been struggling for the past week.",
        "user_input": "",
        "needs_clarification": False,
        "clarifying_questions": [],
        "additional_information": []
    })

    print(result)