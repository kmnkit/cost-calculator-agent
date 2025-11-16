from google.adk.agents import SequentialAgent, LlmAgent
from google.genai.types import GenerateContentConfig

from cost_calculator_agent.shared_libraries import Architecture

from .prompt import ARCHITECT_INSTR, ARCHITECTURE_REVIEW_INSTR, ARCHITECTURE_REFINEMENT_INSTR

architect_agent=LlmAgent(
    model='gemini-2.5-flash',
    name='architect_agent',
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    description='ユーザーが提示した仕様を基にAWS Architectを構成します。',
    instruction=ARCHITECT_INSTR,
    output_key='generated_architecture',   
    generate_content_config=GenerateContentConfig(
        temperature=0.75,
    )
)

architecture_review_agent=LlmAgent(
    model='gemini-2.5-flash',
    name='architecture_review_agent',
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    description='AWS architectureが仕様どおりに設計されたかをレビューします。',    
    instruction=ARCHITECTURE_REVIEW_INSTR,
    output_key='architecture_review_comments',
)

architecture_refinement_agent=LlmAgent(
    model='gemini-2.5-pro',
    name='architecture_refinement_agent',
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    description='レビューを基にアーキテクチャを改善します。',
    instruction=ARCHITECTURE_REFINEMENT_INSTR,
    output_key='refined_architecture',
)

solution_architect_agent = SequentialAgent(
    name='solution_architect_agent',
    description='Userの仕様に基づきAWSアーキテクチャを構成し、レビューしてブラッシュアップしたアーキテクチャを提供します',
    sub_agents=[
        architect_agent, 
        architecture_review_agent,
        architecture_refinement_agent,
    ],
)
