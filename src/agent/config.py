from typing import TypedDict
from langchain_core.runnables import RunnableConfig

class Configuration(TypedDict):
    """Configurable parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    """
    config = RunnableConfig(recursion_limit=2000, configurable={"thread_id": "2"})