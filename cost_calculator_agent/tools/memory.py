import json
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from google.adk.agents.callback_context import CallbackContext

def memorize(key: str, value: str, tool_context: ToolContext):
    """
    Memorize pieces of information, one key-value pair at a time.

    Args:
        key: the label indexing the memory to store the value.
        value: the information to be stored.
        tool_context: The ADK tool context.

    Returns:
        A status message.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    return {"status": f'Stored "{key}": "{value}"'}

def _load_precreated_itinerary(callback_context: CallbackContext):
    """
    Sets up the initial state.
    Set this as a callback as before_agent_call of the root_agent.
    This gets called before the system instruction is contructed.

    Args:
        callback_context: The callback context.
    """    
    data = {}
    with open("cost_calculator_agent/profiles/default.json", "r") as file:
        data = json.load(file)
        print(f"\nLoading Initial State: {data}\n")
    state = callback_context.state
    state.update(data['state'])