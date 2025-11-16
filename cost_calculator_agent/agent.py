import asyncio
from google.adk.agents import SequentialAgent, ParallelAgent

from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import Agent


from cost_calculator_agent.prompt import COST_CALCULATOR_AGENT_INSTR
from cost_calculator_agent.sub_agents.architect.agent import solution_architect_agent
from cost_calculator_agent.sub_agents.developer.agent import developer_agent, mermaid_generator_agent

from google.adk.agents.callback_context import CallbackContext


def start_optimization(callback_context: CallbackContext):
    state = callback_context.state
    state['generated_architecture'] = None
    state['architecture_review_comments'] = None
    state['refined_architecture'] = None
    state['generated_code'] = None
    state['code_review_comments'] = None
    state['refined_code'] = None

    state['generated_mermaid'] = None

parallel_generator_agent = ParallelAgent(
    name='parallel_generator_agent',
    sub_agents=[developer_agent, mermaid_generator_agent]
)

cost_calculator_agent = Agent(
    model='gemini-2.5-flash',
    name='cost_calculator_agent',
    description="A helpful assistant that helps calculate the costs required to realize the user's specifications",
    instruction=COST_CALCULATOR_AGENT_INSTR,
    tools=[AgentTool(solution_architect_agent), AgentTool(parallel_generator_agent)],
    before_agent_callback=start_optimization,
)
# root_agent = cost_calculator_agent

async def main():
    app_name = 'laa_agent'
    user_id='27602980'
    session_id_run = "session_will_run"
    session_id_skip = "session_will_skip"

    runner = InMemoryRunner(agent=cost_calculator_agent, app_name=app_name)
    session_service = runner.session_service

    # セッション1を作成: エージェントが実行される（デフォルトで空の状態）
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_run
        # 初期状態がないので、コールバックチェック時 'skip_llm_agent' はFalse
    )

    # セッション2を作成: エージェントがスキップされる（状態にskip_llm_agent=Trueをセット）
    session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id_skip,
        
    )

    print("\n" + "="*20 + f" SCENARIO 1: Running Agent on Session '{session_id_run}' (Should Proceed) " + "="*20)
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_run,
        new_message=types.Content(role="user", parts=[types.Part(text="Hello, please respond.")])
    ):
        # 最終出力を表示（LLMまたはコールバックによる上書きのいずれか）
        if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
        elif event.is_error():
             print(f"Error Event: {event.error_details}")

    # --- シナリオ2: コールバックがエージェントをスキップする場合 ---
    print("\n" + "="*20 + f" SCENARIO 2: Running Agent on Session '{session_id_skip}' (Should Skip) " + "="*20)
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id_skip,
        new_message=types.Content(role="user", parts=[types.Part(text="This message won't reach the LLM.")])
    ):
         # 最終出力を表示（LLMまたはコールバックによる上書きのいずれか）
         if event.is_final_response() and event.content:
            print(f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}")
         elif event.is_error():
             print(f"Error Event: {event.error_details}")
if __name__ == "__main__":
#     # GOOGLE_API_KEY環境変数が設定されていることを確認（Vertex AI認証を使わない場合）
#     # またはApplication Default Credentials (ADC)がVertex AI用に構成されていることを確認
    asyncio.run(main())