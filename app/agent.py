# app/agent.py

"""Locus Agent - Root Agent Definition.

This module defines the root agent for the Location Strategy Pipeline.
It uses a SequentialAgent to orchestrate 5 specialized sub-agents:

1. MarketResearchAgent - Live web research with Google Search
2. CompetitorMappingAgent - Competitor mapping with Maps Places API
3. GapAnalysisAgent - Quantitative analysis with Python code execution
4. StrategyAdvisorAgent - Strategic synthesis with extended reasoning
5. ReportGeneratorAgent - HTML executive report generation

The pipeline analyzes a target location for a specific business type and
produces comprehensive location intelligence including recommendations
and an HTML report.

Authentication:
    Uses Google AI Studio (API key) instead of Vertex AI.
    Set environment variables:
        GOOGLE_API_KEY=your_api_key
        GOOGLE_GENAI_USE_VERTEXAI=FALSE
        MAPS_API_KEY=your_maps_api_key

Usage:
    Run with: adk web locus_adk

    The agent expects initial state variables:
    - target_location: The geographic area to analyze (e.g., "Bangalore, India")
    - business_type: Type of business to open (e.g., "coffee shop")

    Optional state variables:
    - maps_api_key: Google Maps API key for Places search
"""

from google.adk.agents import SequentialAgent
from google.adk.agents.llm_agent import Agent
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.agent_tool import AgentTool
from google.genai import types as genai_types


from .sub_agents.intake_agent.agent import intake_agent
from .sub_agents.market_research.agent import market_research_agent
from .sub_agents.competitor_mapping.agent import competitor_mapping_agent
from .sub_agents.gap_analysis.agent import gap_analysis_agent
from .sub_agents.strategy_advisor.agent import strategy_advisor_agent

from .sub_agents.report_generator.agent import report_generator_agent

from .config import FAST_MODEL, APP_NAME

# location_strategy_pipeline
location_strategy_pipeline = SequentialAgent(
    name="LocationStrategyPipeline",
    description="""Comprehensive retail location strategy analysis pipeline.

This agent analyzes a target location for a specific business type and produces:
1. Market research findings from live web data
2. Competitor mapping from Google Maps Places API
3. Quantitative gap analysis with zone rankings
4. Strategic recommendations with structured JSON output
5. Professional HTML executive report

To use, get the following details:
- target_location: {target_location}
- business_type: {business_type}

The analysis runs automatically through all stages and produces artifacts
including JSON report and HTML report.
""",
    sub_agents=[
        market_research_agent,      # Part 1: Market research with search
        competitor_mapping_agent,   # Part 2A: Competitor mapping with Maps
        gap_analysis_agent,         # Part 2B: Gap analysis with code exec
        strategy_advisor_agent,     # Part 3: Strategy synthesis
        report_generator_agent,     # Part 4: HTML report generation
    ],
)

def _auto_transfer_callback(callback_context, llm_request):
    """Programmatically transfer to pipeline after IntakeAgent completes.

    When the LLM calls transfer_to_agent through the normal flow, ag_ui_adk
    adds a 'default_api.' namespace prefix that causes a ValueError.
    This callback bypasses the LLM entirely: after IntakeAgent sets
    target_location and business_type in state, we intercept the next
    model call and inject the transfer_to_agent function call directly.

    This means:
      - The LLM never needs to call transfer_to_agent (no prefix issue)
      - The pipeline runs as sub_agent (real-time state streaming works)
    """
    target_location = callback_context.state.get("target_location", "")
    business_type = callback_context.state.get("business_type", "")

    # Only transfer if IntakeAgent has completed (state is populated)
    # and pipeline hasn't started yet
    if target_location and business_type:
        pipeline_stage = callback_context.state.get("pipeline_stage", "")
        if not pipeline_stage or pipeline_stage == "intake":
            # Must return a fully mocked LlmResponse, which ADK expects
            content = genai_types.Content(
                parts=[
                    genai_types.Part(
                        function_call=genai_types.FunctionCall(
                            name="transfer_to_agent",
                            args={"agent_name": "LocationStrategyPipeline"}
                        )
                    )
                ],
                role="model",
            )
            return LlmResponse(
                content=content,
                finish_reason=genai_types.FinishReason.STOP,
            )

    return None


# Root agent orchestrating the complete location strategy pipeline
root_agent = Agent(
    model=FAST_MODEL,
    name=APP_NAME,
    description='A strategic partner for retail businesses, guiding them to optimal physical locations that foster growth and profitability.',
    instruction="""Your primary role is to orchestrate the retail location analysis.
    Your persona is a Premier Retail Strategy Analyst—elite, data-driven, and visionary for the brand Intsemble.
1. Start by greeting the user with a high-energy, professional welcome that positions you as a leading expert in retail location intelligence. Tell them you are ready to engineer their market dominance.
2. Check if the `TARGET_LOCATION` (Geographic area to analyze (e.g., "Park-Street, Kolkata")) and `BUSINESS_TYPE` (Type of business (e.g., "coffee shop", "bakery", "gym")) have been provided.
3. If they are missing, or you are in doubt and you cannot parse or understand the `TARGET_LOCATION` or `BUSINESS_TYPE`, clearly **ask the user clarifying questions to get the required information.**
4. Once you have the necessary details, call the `IntakeAgent` tool to process them.
5. After the `IntakeAgent` is successful, the analysis pipeline will start automatically.

**CRITICAL TOOL USAGE INSTRUCTIONS:**
- When calling the `IntakeAgent`, use the name EXACTLY as "IntakeAgent".
- DO NOT add prefixes like "default_api.IntakeAgent" or "functions.IntakeAgent".
- Correct Format: `IntakeAgent(target_location="...", business_type="...")`
- After IntakeAgent succeeds, the pipeline starts automatically. You do NOT need to call any other tool.

Your main function is to manage this workflow conversationally.""",
    tools=[AgentTool(intake_agent)],
    sub_agents=[location_strategy_pipeline],
    before_model_callback=_auto_transfer_callback,
)