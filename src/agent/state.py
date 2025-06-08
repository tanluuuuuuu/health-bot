from typing import TypedDict, NotRequired, List

class State(TypedDict):
    """Input state for the agent"""

    topic: str
    focus_aspects: NotRequired[str]

    needs_clarification: NotRequired[bool]
    clarifying_questions: NotRequired[List[str]]
    additional_information: NotRequired[List[str]]