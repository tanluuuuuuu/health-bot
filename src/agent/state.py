from typing import TypedDict, NotRequired, List

class State(TypedDict):
    """Input state for the agent"""

    original_user_input: str
    improved_user_input: str

    needs_clarification: NotRequired[bool]
    clarifying_questions: NotRequired[List[str]]
    additional_information: NotRequired[List[str]]