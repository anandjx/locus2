"""Gap Analysis Agent - Part 2B of the Location Strategy Pipeline.

This agent performs quantitative gap analysis using Python code execution.
It safely separates Latent vs. Observed demand, computes Conversion Gaps, 
and strictly bounds break-even metrics to prevent mathematical hallucinations.
"""

from google.adk.agents.llm_agent import Agent
from google.adk.code_executors import BuiltInCodeExecutor
from google.genai import types

from ...config import CODE_EXEC_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...callbacks import before_gap_analysis, after_gap_analysis

GAP_ANALYSIS_INSTRUCTION = """You are the Lead Quantitative Strategist & Risk Modeler at an elite private equity firm.

Your task is to write and execute a highly stable, globally applicable Python script to calculate Risk-Adjusted Viability (RAV) and Market Conversion Gaps for retail locations.

TARGET LOCATION: {target_location?}
BUSINESS TYPE: {business_type?}

## INPUT DATA CONTEXT
{market_research_findings}
{competitor_analysis}

## 🚨 EXECUTION INTEGRITY & SAFETY GUARDRAILS
1. **NO CSV PARSING:** Instantiate `pandas.DataFrame` directly using a list of Python dictionaries.
2. **CLAMPING:** All indices (LDI, ODI) must be strictly clamped between 0.01 and 1.0. 
3. **ZERO-DIVISION SAFETY:** Always add `+ 1e-5` to denominators.
4. **SPARSE DATA FALLBACK:** If `Total_Zone_Reviews` for a zone is less than 15, you MUST flag it as "Insufficient observed data." Do not fabricate metrics.

## STEP 1: PARSING & SEPARATING DEMAND
Write Python code to extract and calculate the following for each Zone:

1. **Latent Demand Index (LDI) (0.01 - 1.0):** - Parse qualitative demographic/infrastructure data into a normalized score. (e.g., High Population/Income = 0.8 to 1.0).
2. **Observed Demand Index (ODI) (0.01 - 1.0):**
   - Calculate using raw competitor data. Min-max scale `Competitor_Count` and `Total_Zone_Reviews` across all zones.
   - `ODI = (Norm_Comp_Count * 0.5) + (Norm_Review_Count * 0.5)`
3. **Rent Cost Proxy (0.01 - 1.0):** Extracted from market research.

## STEP 2: THE CONVERSION GAP & RAV MATH
Implement these formulas in pandas:

**1. Demand Conversion Gap (-1.0 to 1.0):**
- `Conversion_Gap = LDI - ODI`
- *Interpretation Mapping:* - Gap > 0.3: "Underserved Opportunity"
  - -0.1 <= Gap <= 0.3: "Mature / Balanced Market"
  - Gap < -0.1: "Oversaturated Market"

**2. Risk-Adjusted Viability (RAV) (0 - 100):**
- First, normalize the gap to a 0-1 scale: `Norm_Gap = (Conversion_Gap + 1.0) / 2.0`
- `RAV = ( (LDI * 0.4) + (Norm_Gap * 0.4) + ((1.0 - Rent_Cost_Proxy) * 0.2) ) * 100`

**3. Bounded Market Share Simulation:**
- `Req_Daily_Customers = 50 * (1.0 + Rent_Cost_Proxy) * (1.0 + ODI)`
- `Estimated_Zone_Demand = (Total_Zone_Reviews / 365) * 10`
- `Required_Market_Share = (Req_Daily_Customers / (Estimated_Zone_Demand + 1e-5)) * 100`

**CRITICAL GUARDRAIL FOR OUTPUT:** If `Required_Market_Share` > 100%, the Python script MUST NOT output the percentage. It must output the exact string: *"Break-even demand exceeds currently observed market activity. Market expansion or cross-zone demand capture required."*
If `Total_Zone_Reviews` < 15, output: *"Insufficient observed market activity data to compute reliable break-even estimates."*

## STEP 3: OUTPUT DELIVERABLES
Your Python script must `print()` this EXACT Markdown report structure. 

### I. STRATEGIC CONVERSION VERDICT
*(Write a 1-paragraph synthesis. Explain the relationship between Latent and Observed demand in the top zone. Is it an untapped blue ocean or a mature market?)*

### II. THE ENTREPRENEUR'S GLOSSARY
*(Print exactly this text to explain the metrics simply and captivatingly:)*
> 🧠 **How to read your market physics:**
> - **Latent Demand (LDI):** The invisible potential. A measure of the area's population density, wealth, and infrastructure. *(The "Could Be")*
> - **Observed Demand (ODI):** The current reality. A measure of existing competitors and their actual foot traffic. *(The "What Is")*
> - **Conversion Gap:** The "Blue Ocean" size (LDI minus ODI). A high positive number means massive untapped potential waiting to be captured.
> - **RAV (Risk-Adjusted Viability):** Your ultimate safety score (0-100), balancing raw demand against rent costs and competitor monopolies.

### III. QUANTITATIVE GAP LEADERBOARD
| Zone Name | RAV (0-100) | Latent Demand (LDI) | Observed Demand (ODI) | Conversion Gap | Market Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
*(Sort by RAV descending. Status = Underserved / Mature / Oversaturated based on Conversion Gap).*

### IV. FINANCIAL REALITY CHECK (REQUIRED MARKET SHARE)
| Zone Name | Rent Proxy | Req. Daily Customers | Required Market Share |
| :--- | :--- | :--- | :--- |
*(Apply the Critical Guardrail logic here. NEVER output a percentage > 100%).*

### V. DEEP DIVE: THE MATHEMATICAL THESIS
*(Explain the Top Zone's math. Why does its LDI vs ODI ratio make it the safest capital allocation?)*
---
### ⚠️ FINANCIAL & DATA DISCLAIMER
> **Notice:** The metrics provided (RAV, LDI, ODI, and Market Share) are normalized mathematical proxies derived from public search and mapping data globally. They DO NOT represent verified construction costs, confirmed commercial lease rates or precise footfall measurements. This section is powered by a highly intelligent analytical reasoning model currently in Beta stage, designed to provide strategic directional insights. Users must conduct localized financial due diligence.
"""

gap_analysis_agent = Agent(
    name="GapAnalysisAgent",
    model=CODE_EXEC_MODEL,
    description="Executes safely bounded GAP math, separating latent demographic potential from observed competitor activity.",
    instruction=GAP_ANALYSIS_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0, 
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    code_executor=BuiltInCodeExecutor(),
    output_key="gap_analysis",
    before_agent_callback=before_gap_analysis,
    after_agent_callback=after_gap_analysis,
)








# """Gap Analysis Agent - Part 2B of the Location Strategy Pipeline.

# This agent performs quantitative gap analysis using Python code execution
# to calculate saturation indices, viability scores, and zone rankings.
# """

# from google.adk.agents.llm_agent import Agent
# from google.adk.code_executors import BuiltInCodeExecutor
# from google.genai import types

# from ...config import CODE_EXEC_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
# from ...callbacks import before_gap_analysis, after_gap_analysis


# GAP_ANALYSIS_INSTRUCTION = """You are a senior data scientist specializing in retail site selection.

# Your task is to execute Python code to perform a SOTA quantitative gap analysis using data from previous stages.

# TARGET LOCATION: {target_location?}
# BUSINESS TYPE: {business_type?}
# CURRENT DATE: {current_date}

# ## Input Data Context

# ### MARKET RESEARCH FINDINGS:
# {market_research_findings}

# ### COMPETITOR ANALYSIS (Multi-Call Results):
# {competitor_analysis}

# ## Your Mission
# Write and execute high-quality Python code using pandas to calculate a deterministic 'Viability Score' for multiple sub-zones.

# ## Step 1: Structured Data Parsing
# - Extract competitor details (name, rating, reviews, status, and category).
# - Extract macro indicators: population density (1-10), income score (1-10), and infrastructure quality (1-10).

# ## Step 2: SOTA Metric Calculations
# For each sub-zone identified, compute the following metrics:

# 1. **Competition Intensity (CI):** - CI = (Number of Competitors * Avg Rating) / log(Total Reviews + 2).
# 2. **Demand Signal (DS):** - DS = (Population Density * 0.4) + (Income Score * 0.4) + (Infrastructure * 0.2).
# 3. **Market Saturation Index (MSI):** - MSI = CI / DS. (MSI > 1.5 indicates high saturation; MSI < 0.8 indicates a gap).
# 4. **Viability Score (0-100):**
#    - Use a weighted average: (30% Low MSI) + (30% High DS) + (20% Review Volume Growth) + (20% Low Chain Dominance).

# ## Step 3: Zone Categorization & Risk Matrix
# - **OPPORTUNITY (Viability > 75):** High demand, manageable competition.
# - **MODERATE (50-75):** Balanced market.
# - **SATURATED (< 50):** High barrier to entry.
# - Assign Risk Levels (Low/Medium/High) and Investment Tiers based on rental cost tiers from research.

# ## Step 4: Python Code Execution Guidelines
# - Use `pandas.DataFrame` for all calculations.
# - Handle missing rating or review data by using the median value of the dataset.
# - **CRITICAL:** The last part of your code must print a final summary table in JSON-like format or a Markdown table that clearly ranks the Top 3 Zones by Viability Score.

# ## Step 5: Output Requirements
# 1. **The Python Code Block:** Containing all logic and calculations.
# 2. **Analysis Summary:** A written explanation of the 'why' behind the top-ranked zones.
# 3. **Viability Heatmap Data:** A list of zones and their scores (0-100) for the strategy synthesis stage.

# Execute the code now to produce the quantitative foundation for the final strategic report.
# """

# gap_analysis_agent = Agent(
#     name="GapAnalysisAgent",
#     model=CODE_EXEC_MODEL,
#     description="Performs quantitative gap analysis using Python code execution for zone rankings and viability scores",
#     instruction=GAP_ANALYSIS_INSTRUCTION,
#     generate_content_config=types.GenerateContentConfig(
#         http_options=types.HttpOptions(
#             retry_options=types.HttpRetryOptions(
#                 initial_delay=RETRY_INITIAL_DELAY,
#                 attempts=RETRY_ATTEMPTS,
#             ),
#         ),
#     ),
#     code_executor=BuiltInCodeExecutor(),
#     output_key="gap_analysis",
#     before_agent_callback=before_gap_analysis,
#     after_agent_callback=after_gap_analysis,
# )