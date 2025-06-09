from typing import TypedDict, NotRequired, List
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    """Input state for the agent"""

    messages: Annotated[list, add_messages]
    topic: str

    focus_aspects: NotRequired[str]

    needs_clarification: NotRequired[bool]
    clarifying_questions: NotRequired[List[str]]
    additional_information: NotRequired[List[str]]