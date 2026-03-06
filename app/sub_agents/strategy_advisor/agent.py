"""Strategy Advisor Agent - Part 3 of the Location Strategy Pipeline.

This agent synthesizes LDI, ODI, and Conversion Gaps into an institutional-grade 
Capital Allocation Memo using extended reasoning, outputting a structured JSON report.
"""

from google.adk.agents import LlmAgent
from google.adk.planners import BuiltInPlanner
from google.genai import types
from google.genai.types import ThinkingConfig

from ...config import PRO_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...schemas import LocationIntelligenceReport
from ...callbacks import before_strategy_advisor, after_strategy_advisor

STRATEGY_ADVISOR_INSTRUCTION = """You are the Managing Partner at an elite Private Equity and Retail Strategy firm. Your mandate is to synthesize complex market sentiment, spatial competitor mapping, and quantitative gap analyses into a definitive, institutional-grade Capital Allocation Memo.

TARGET LOCATION: {target_location?}
BUSINESS TYPE: {business_type?}
CURRENT DATE: {current_date?}

## AVAILABLE INTELLIGENCE
### PHASE 1: MARKET RESEARCH (Social Sentiment & Macro Demographics)
{market_research_findings?}

### PHASE 2A: COMPETITOR MAPPING (Spatial Monopolies & Missing Price Tiers)
{competitor_analysis?}

### PHASE 2B: QUANTITATIVE GAP ANALYSIS (LDI, ODI, and Conversion Gaps)
{gap_analysis?}

## YOUR MISSION
Synthesize these inputs into a ruthless, evidence-backed investment thesis. You must map these insights directly into the required JSON output schema fields, elevating the language to a professional private equity standard.

## THE SOTA SYNTHESIS FRAMEWORK

### 1. The Investment Thesis (Top Recommendation)
Defend the winning zone using the structural math from Phase 2B:
- **Quantitative Anchor:** Explicitly cite the Risk-Adjusted Viability (RAV) score and the Demand Conversion Gap (Latent Demand Index vs. Observed Demand Index). 
- **The Market Status:** Is this an "Underserved Opportunity" (High LDI, Low ODI) or a "Mature Market" requiring a margin/quality play?
- **The "Unfair Advantage":** Combine the social complaints (Phase 1) with the Missing Price Tier (Phase 2A) to dictate the exact product-market fit.

### 2. Operational & Financial Reality Check
Translate the Break-Even guards into operational directives:
- **The Capital Requirement:** Address the Rent Proxy. Does this zone require a lean build-out or premium flagship capital?
- **The Demand Generation Mandate:** Check the Phase 2B Market Share metric. If it states *"Break-even demand exceeds currently observed market activity,"* your strategy MUST explicitly dictate aggressive marketing, cross-zone customer acquisition, or destination-marketing to create net-new demand. Do not pretend existing footfall is enough.

### 3. The Attack Vector (Go-To-Market Strategy)
Provide exact tactical positioning:
- How to exploit the specific weaknesses of the Top 2 Volume Leaders mapped in Phase 2A (e.g., "Attack the legacy leader's 4.1 rating by targeting the 'Missing Premium Tier' with experiential retail").
- Micro-location strategy (e.g., "Intercept traffic on the periphery rather than fighting head-to-head").

### 4. Risk Mitigation & Capital Traps
- Explicitly identify the worst-performing zone (The Capital Trap). Explain mathematically why deploying capital there is dangerous (e.g., Negative Conversion Gap = Oversaturated, combined with High Rent).

### 5. Alternative Phased Expansion
- Identify 2 alternative locations as Phase 2 expansion targets.
- Briefly explain their distinct market profiles (e.g., "Secondary option targets a high-LDI student demographic vs. the primary premium residential demographic").

## OUTPUT REQUIREMENTS
Your response MUST strictly conform to the provided JSON schema. 
Translate the advanced frameworks above (Investment Thesis, Attack Vector, Capital Traps, Break-Even Mandates) into the closest matching fields in your schema (e.g., `strengths`, `concerns`, `next_steps`, `strategic_insights`). 
CRITICAL DATA HANDOFF: You MUST extract the exact lat/lng coordinates of competitors from Phase 2A and map them strictly into the `competitor_coordinates` JSON array within the `competition` profile (e.g., ["40.7128,-74.0060", "40.7138,-74.0160"]). Do not omit this data.
Use precise, data-backed language. NO generic business advice.
"""

strategy_advisor_agent = LlmAgent(
    name="StrategyAdvisorAgent",
    model=PRO_MODEL, 
    description="Synthesizes multi-agent findings into an institutional-grade investment memo using extended reasoning and structured JSON.",
    instruction=STRATEGY_ADVISOR_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    planner=BuiltInPlanner(
        thinking_config=ThinkingConfig(
            include_thoughts=False,  
            thinking_budget=-1,  
        )
    ),
    output_schema=LocationIntelligenceReport,
    output_key="strategic_report",
    before_agent_callback=before_strategy_advisor,
    after_agent_callback=after_strategy_advisor,
)













# """Strategy Advisor Agent - Part 3 of the Location Strategy Pipeline.

# This agent synthesizes all findings into actionable recommendations using
# extended reasoning (thinking mode) and outputs a structured JSON report.
# """

# from google.adk.agents import LlmAgent
# from google.adk.planners import BuiltInPlanner
# from google.genai import types
# from google.genai.types import ThinkingConfig

# from ...config import PRO_MODEL, CODE_EXEC_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
# from ...schemas import LocationIntelligenceReport
# from ...callbacks import before_strategy_advisor, after_strategy_advisor


# STRATEGY_ADVISOR_INSTRUCTION = """You are the best senior strategy consultant synthesizing location intelligence findings.

# Your task is to analyze all research and provide actionable strategic recommendations.

# TARGET LOCATION: {target_location}
# BUSINESS TYPE: {business_type}
# CURRENT DATE: {current_date}

# ## Available Data

# ### MARKET RESEARCH FINDINGS (Part 1):
# {market_research_findings}

# ### COMPETITOR ANALYSIS (Part 2A):
# {competitor_analysis}

# ### GAP ANALYSIS (Part 2B):
# {gap_analysis}

# ## Your Mission
# Synthesize all findings into a comprehensive strategic recommendation.

# ## Analysis Framework

# ### 1. Data Integration
# Review all inputs carefully:
# - Market research demographics and trends
# - Competitor locations, ratings, and patterns
# - Quantitative gap analysis metrics and zone rankings

# ### 2. Strategic Synthesis
# For each promising zone, evaluate:
# - Opportunity Type: Categorize (e.g., "Metro First-Mover", "Residential Sticky", "Mall Impulse")
# - Overall Score: 0-100 weighted composite
# - Strengths: Top 3-4 factors with evidence from the analysis
# - Concerns: Top 2-3 risks with specific mitigation strategies
# - Competition Profile: Summarize density, quality, chain presence
# - Market Characteristics: Population, income, infrastructure, foot traffic, costs
# - Best Customer Segment: Primary target demographic
# - Next Steps: 3-5 specific actionable recommendations

# ### 3. Top Recommendation Selection
# Choose the single best location based on:
# - Highest weighted opportunity score
# - Best balance of opportunity vs risk
# - Most aligned with business type requirements
# - Clear competitive advantage potential

# ### 4. Alternative Locations
# Identify 2-3 alternative locations:
# - Brief scoring and categorization
# - Key strength and concern for each
# - Why it's not the top choice

# ### 5. Strategic Insights
# Provide 4-6 key insights that span the entire analysis:
# - Market-level observations
# - Competitive dynamics
# - Timing considerations
# - Success factors

# ## Output Requirements
# Your response MUST conform to the LocationIntelligenceReport schema.
# Ensure all fields are populated with specific, actionable information.
# Use evidence from the analysis to support all recommendations.
# """

# strategy_advisor_agent = LlmAgent(
#     name="StrategyAdvisorAgent",
#     model=CODE_EXEC_MODEL,
#     description="Synthesizes findings into strategic recommendations using extended reasoning and structured output",
#     instruction=STRATEGY_ADVISOR_INSTRUCTION,
#     generate_content_config=types.GenerateContentConfig(
#         http_options=types.HttpOptions(
#             retry_options=types.HttpRetryOptions(
#                 initial_delay=RETRY_INITIAL_DELAY,
#                 attempts=RETRY_ATTEMPTS,
#             ),
#         ),
#     ),
#     planner=BuiltInPlanner(
#         thinking_config=ThinkingConfig(
#             include_thoughts=False,  # Must be False when using output_schema
#             thinking_budget=-1,  # -1 means unlimited thinking budget
#         )
#     ),
#     output_schema=LocationIntelligenceReport,
#     output_key="strategic_report",
#     before_agent_callback=before_strategy_advisor,
#     after_agent_callback=after_strategy_advisor,
# )