from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from .prompt import CODE_WRITER_INSTR, CODE_REVIEWER_INSTR, CODE_REFINEMENT_INSTR, MERMAID_GENERATOR_INSTR
# from google.adk.artifacts import InMemoryArtifactService

GEMINI_MODEL = 'gemini-2.5-pro'

# artifact_service = InMemoryArtifactService()

code_writer_agent = LlmAgent(
    name='code_writer_agent',
    model=GEMINI_MODEL,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    instruction=CODE_WRITER_INSTR,
    description='仕様通りにTerraformコードを作成する。',
    output_key='generated_code',
    tools=[google_search]
)

code_reviewer_agent = LlmAgent(
    name="code_reviewer_agent",
    model=GEMINI_MODEL,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    instruction=CODE_REVIEWER_INSTR,
    description="Reviews code and provides feedback.",
    output_key="code_review_comments", # Stores output in state['code_review_comments']
)

code_refinement_agent = LlmAgent(
    name="code_refinement_agent",
    model=GEMINI_MODEL,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    instruction=CODE_REFINEMENT_INSTR,
    description="Refactors code based on review comments.",
    output_key="refined_code", # Stores output in state['refined_code']
)

developer_agent = SequentialAgent(
    name='infra_developer_agent',
    description='アーキテクチャを基にベストプラクティスに沿ったTerraform IaCコードを作成します。',
    sub_agents=[
        code_writer_agent, 
        code_reviewer_agent,
        code_refinement_agent,
    ],
)


mermaid_generator_agent = LlmAgent(
    name='mermaid_generator_agent',
    model=GEMINI_MODEL,
    instruction=MERMAID_GENERATOR_INSTR,
    description='決まった仕様を基にMermaid図を作成します。',
    output_key='generated_mermaid',
)
