import asyncio
from google.adk.agents import SequentialAgent, ParallelAgent

from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import Agent

from cost_calculator_agent.prompt import COST_CALCULATOR_AGENT_INSTR
from cost_calculator_agent.sub_agents.architect.agent import solution_architect_agent
from cost_calculator_agent.sub_agents.developer.agent import developer_agent, mermaid_generator_agent

from cost_calculator_agent.tools.memory import _load_precreated_itinerary

# parallel_generator_agent = ParallelAgent(
#     name='parallel_generator_agent',
#     sub_agents=[developer_agent, mermaid_generator_agent]
# )

cost_calculator_agent = Agent(
    model='gemini-2.5-flash',
    name='cost_calculator_agent',
    description="A helpful assistant that helps calculate the costs required to realize the user's specifications",
    instruction=COST_CALCULATOR_AGENT_INSTR,
    tools=[AgentTool(solution_architect_agent), AgentTool(mermaid_generator_agent)],
    before_agent_callback=_load_precreated_itinerary,
)
root_agent = cost_calculator_agent
