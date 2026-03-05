"""Competitor Mapping Agent - Part 2A of the Location Strategy Pipeline.

This agent maps competitors using the Google Maps Places API to extract
structural market power, barrier classification, and price-tier gaps.
"""

from google.adk.agents.llm_agent import Agent
from google.genai import types

from ...config import FAST_MODEL, PRO_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...tools import search_places
from ...callbacks import before_competitor_mapping, after_competitor_mapping

COMPETITOR_MAPPING_INSTRUCTION = """You are an elite Retail Location Strategist and Structural Market Economist. Your mandate is to execute a rigorous Competitive Power Analysis using REAL-TIME Google Maps data.

TARGET LOCATION: {target_location?}
BUSINESS TYPE: {business_type?}
CURRENT DATE: {current_date}

## STRICT TOOL EXECUTION & ZERO HALLUCINATION DIRECTIVE
1. You MUST call the `search_places` tool to obtain ground-truth data.
2. Multi-Call Strategy: Execute exactly TWO precise searches:
   - Call 1: Direct Competitors (Search: "{business_type?} near {target_location?}")
   - Call 2: Complementary Ecosystem (Search for a related anchor category near {target_location?}).
3. Base ALL insights STRICTLY on the returned data. If a metric is unavailable, do not invent it.

## DELIVERABLE FORMAT

Synthesize your findings into this exact premium executive briefing format. Ensure the Markdown tables are perfectly formatted for UI rendering.

### I. EXECUTIVE SUMMARY
*(A 2-3 sentence verdict on the structural market power, dominant barrier to entry, and the overarching opportunity.)*

### II. VERIFIED COMPETITOR LEDGER (REAL-TIME DATA)
*(Generate two Markdown tables based strictly on the tool's returned data. Limit to top 15 Direct and top 5 Complementary businesses to prevent UI bloat.)*

**A. Direct Competitors: {business_type?}**
| Name | Address/Neighborhood | Rating | Reviews | Status |
| :--- | :--- | :--- | :--- | :--- |
| (Data) | (Data) | (Data) | (Data) | (Data) |

**B. Complementary Ecosystem (Top 5 by Volume)**
| Name | Address/Neighborhood | Rating | Reviews |
| :--- | :--- | :--- | :--- |
| (Data) | (Data) | (Data) | (Data) |

### III. STRUCTURAL MARKET POWER MODULES
*(Execute these 4 modules using the exact schema provided. Limit citations to 3 per module.)*

#### Module 1: Spatial Scope & Supply-Demand Validity
**Market Data & Facts**
*(Detail the geographic spread of the returned results. Are they localized to one street or spread across a district? Note if total supply is suspiciously low.)*
**Strategic Inference**
*(Classify the Spatial Scope: Street-Level, Neighborhood, or City-Cluster. Demand vs Supply Mismatch Flag: Does low competition indicate a "Blue Ocean" or simply a "Dead Zone" with no demand?)*
**Module Score: [0-10]/10**
*(Score based strictly on spatial viability.)*

#### Module 2: Concentration Index & Barrier Classification
**Market Data & Facts**
*(Calculate the Competitive Concentration Index (CCI) proxy: Do the top 2-3 players hold the vast majority of total reviews? Identify multi-branch chains vs. single outlets in the data.)*
**Strategic Inference**
*(Classify the structure: Monopoly, Oligopoly, or Fragmented. Classify the Primary Barrier to Entry: Brand/Legacy Barrier, Capital Barrier, Density Barrier, or Quality Barrier.)*
**Module Score: [0-10]/10**
*(Score the penetrability of the market structure.)*

#### Module 3: The Legacy vs. Loyalty Matrix
**Market Data & Facts**
*(Identify the "Institutional Volume Leaders" (Massive reviews, average/good ratings) vs. "Boutique Loyalty Leaders" (Lower reviews, exceptional 4.8+ ratings).)*
**Strategic Inference**
*(Legacy Brand Resistance Score: Acknowledge that massive volume = entrenched cultural habit, not just vulnerability. Differentiate the scalable threats from the niche boutiques.)*
**Module Score: [0-10]/10**
*(Score the vulnerability of the incumbents.)*

#### Module 4: Price-Tier White Space & Ecosystem Pull
**Market Data & Facts**
*(Proxy the price tiers based on brand names and location. Detail the complementary ecosystem data from Call 2.)*
**Strategic Inference**
*(Identify the Missing Tier: Is the market overwhelmingly budget or ultra-luxury with no aspirational mid-tier? Ecosystem Pull vs Push: Does the complementary ecosystem generate synergistic demand, or is it irrelevant to {business_type?}?)*
**Module Score: [0-10]/10**
*(Score the whitespace and ecosystem strength.)*

### IV. COMPETITIVE OPPORTUNITY INDEX (COI)
- **Total COI Score**: *(Average of the 4 Module Scores)*
- **Market Saturation Status**: *[Red Ocean / Blue Ocean / Fragmented Consolidation / Entrenched Legacy]*

### V. TARGETING VERDICT & ATTACK STRATEGY
*(Based on the barrier types and legacy resistance identified, formulate a precise entry strategy. Should the user execute a "Peripheral Interception" (setup near the cluster), a "Direct Quality Assault", or a "Tier-Gap Insertion"?)*
"""

competitor_mapping_agent = Agent(
    name="CompetitorMappingAgent",
    model=PRO_MODEL,
    description="Executes structural market power analysis using Google Maps Places API to classify competitive barriers, legacy resistance, and price-tier gaps.",
    instruction=COMPETITOR_MAPPING_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.0, 
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[search_places],
    output_key="competitor_analysis",
    before_agent_callback=before_competitor_mapping,
    after_agent_callback=after_competitor_mapping,
)














# """Competitor Mapping Agent - Part 2A of the Location Strategy Pipeline.

# This agent maps competitors using the Google Maps Places API to get
# ground-truth data about existing businesses and structural market gaps.
# """

# from google.adk.agents.llm_agent import Agent
# from google.genai import types

# from ...config import FAST_MODEL, PRO_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
# from ...tools import search_places
# from ...callbacks import before_competitor_mapping, after_competitor_mapping

# COMPETITOR_MAPPING_INSTRUCTION = """You are an elite Retail Location Strategist and Spatial Data Scientist at a top-tier management consulting firm. Your mandate is to extract structural market dynamics using REAL-TIME Google Maps data.

# TARGET LOCATION: {target_location?}
# BUSINESS TYPE: {business_type?}
# CURRENT DATE: {current_date}

# ## STRICT TOOL EXECUTION & ANTI-BLOAT DIRECTIVE
# 1. You MUST call the `search_places` tool to obtain ground-truth data.
# 2. Multi-Call Strategy: Execute exactly TWO precise searches to map the ecosystem without bloating the context window:
#    - Call 1: Direct Competitors (Search: "{business_type?} near {target_location?}", radius: 3000m)
#    - Call 2: Complementary Ecosystem (Search for a related anchor category, e.g., if target is a Gym, search for "Health Food Stores" or "Corporate Parks" near {target_location?}).
# 3. Base ALL insights strictly on the returned tool data (Name, Address, Rating, Total Ratings, Price Level). Do NOT hallucinate businesses that the tool did not return.

# ## EXECUTION SCHEMA
# Synthesize the tool data into the following premium, client-ready markdown structure. 

# ### Module 1: Spatial Density & Clustering
# **Market Data & Facts**
# *(List the total number of direct competitors found. Identify 1-2 specific streets/neighborhoods where competitors are heavily clustered. Max 3 citations/examples.)*
# **Strategic Inference**
# *(Classify the zone: High Density / Moderate Density / Low Density. Is there a "Blue Ocean" dead zone where demand exists but supply is absent?)*
# **Module Score: [0-10]/10**
# *(Score the geographic opportunity based strictly on density and clustering.)*

# ### Module 2: Market Dominance & Foot-Traffic Signals
# **Market Data & Facts**
# *(List the Top 3 Volume Leaders by total review count. List the Top 3 Quality Leaders by highest rating with meaningful volume. Note if any business dominates BOTH.)*
# **Strategic Inference**
# *(Who actually owns the market share? Are the volume leaders highly rated, or are consumers settling for mediocre quality due to lack of options?)*
# **Module Score: [0-10]/10**
# *(Score the vulnerability of the dominant players.)*

# ### Module 3: Price Tier & Quality Segmentation
# **Market Data & Facts**
# *(Extract price levels if available. Proxy price tiers based on brand positioning keywords in names, e.g., "Artisanal", "Express", "Luxury", and location prestige.)*
# **Strategic Inference**
# *(Is the area dominated by Mass-Segment/Budget players or Premium positioning? Explicitly state the MISSING TIER. E.g., "Strong premium presence, but missing high-quality mid-tier.")*
# **Module Score: [0-10]/10**
# *(Score the pricing gap opportunity.)*

# ### Module 4: The Complementary Ecosystem 
# **Market Data & Facts**
# *(Detail the results of your second search call. What anchor institutions or complementary businesses exist nearby?)*
# **Strategic Inference**
# *(How does this ecosystem support foot traffic for {business_type?}? e.g., "Proximity to 3 major gyms supports a sports nutrition business.")*
# **Module Score: [0-10]/10**
# *(Score the strength of the surrounding commercial ecosystem.)*

# ---

# ## DELIVERABLE FORMAT

# After completing the 4 modules using the schema above, synthesize your findings into this premium executive briefing:

# ### I. EXECUTIVE SUMMARY
# *(A 2-sentence market structure verdict.)*

# ### II. COMPETITIVE OPPORTUNITY INDEX (COI)
# - **Total COI Score**: *(Calculate the average of all 4 Module Scores out of 10)*
# - **Market Saturation Status**: *[Red Ocean (Saturated) / Blue Ocean (Open) / Fragmented (Consolidation Opportunity)]*

# ### III. 🔥 THE DOMINANCE VULNERABILITY (Strategic Insight)
# *(Identify the specific weakness of the top competitor. Are they highly reviewed but outdated? Are they a franchise lacking local charm?)*

# ### IV. TARGETING VERDICT & MICRO-LOCATION STRATEGY
# *(Based on spatial clustering, where EXACTLY should the entrepreneur physically position their business to intercept traffic while avoiding head-to-head combat?)*

# ### V. VERIFIED COMPETITOR LEDGER
# *(A clean, bulleted list of the top 5 most important competitors found, including Name, Rating, and Total Reviews.)*
# """

# competitor_mapping_agent = Agent(
#     name="CompetitorMappingAgent",
#     model=PRO_MODEL,
#     description="Maps competitors using Google Maps Places API to extract spatial dominance, price tiers, and structural market gaps.",
#     instruction=COMPETITOR_MAPPING_INSTRUCTION,
#     generate_content_config=types.GenerateContentConfig(
#         temperature=0.0, # Ensures deterministic synthesis of the JSON tool output
#         http_options=types.HttpOptions(
#             retry_options=types.HttpRetryOptions(
#                 initial_delay=RETRY_INITIAL_DELAY,
#                 attempts=RETRY_ATTEMPTS,
#             ),
#         ),
#     ),
#     tools=[search_places],
#     output_key="competitor_analysis",
#     before_agent_callback=before_competitor_mapping,
#     after_agent_callback=after_competitor_mapping,
# )





















