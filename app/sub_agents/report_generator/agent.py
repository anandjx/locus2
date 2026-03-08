"""Report Generator Agent - Part 4 of the Location Strategy Pipeline.

This agent generates a professional HTML executive report from the
structured LocationIntelligenceReport data using the generate_html_report tool.
"""

from google.adk.agents import LlmAgent
from google.genai import types

from ...config import FAST_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
from ...tools import generate_html_report
from ...callbacks import before_report_generator, after_report_generator

REPORT_GENERATOR_INSTRUCTION = """You are an institutional grade Executive Report Generator for an elite private equity location intelligence firm.

Your task is to create a professional HTML executive report using the `generate_html_report` tool.

TARGET LOCATION: {target_location?}
BUSINESS TYPE: {business_type?}
CURRENT DATE: {current_date?}

## Strategic Report Data
{strategic_report}

## Your Mission
Format the strategic report data and call the `generate_html_report` tool to create an 8-slide McKinsey/BCG-style HTML presentation.

## Steps

### Step 1: Format the Report Data
Prepare a comprehensive data summary from the strategic report above. You MUST explicitly extract and include these SOTA metrics so they appear in the final report:
- **Organic RAV** (Risk-Adjusted Viability score)
- **Latent Demand Index (LDI)** & **Observed Demand Index (ODI)**
- **Conversion Gap** (Blue Ocean vs Red Ocean status)
- **Concentration Index (CCI)**
- **Required Market Share** (Break-even proxy and Demand Deficit warnings)
- Top recommendation details (strengths, concerns, opportunity type)
- Competition metrics (total competitors, chain dominance)
- Market characteristics (population, income, rental costs)

### Step 2: Call the Tool
Call the `generate_html_report` tool. You must pass:
1. `report_data`: Your formatted data from Step 1.
2. `business_type`: "{business_type?}"
3. `target_location`: "{target_location?}"

### Step 3: Report Result
Confirm the report was generated successfully.
"""

report_generator_agent = LlmAgent(
    name="ReportGeneratorAgent",
    model="gemini-2.5-pro", # Pro model recommended for complex data formatting and tool adherence
    description="Generates professional McKinsey/BCG-style HTML executive reports using the generate_html_report tool",
    instruction=REPORT_GENERATOR_INSTRUCTION,
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                initial_delay=RETRY_INITIAL_DELAY,
                attempts=RETRY_ATTEMPTS,
            ),
        ),
    ),
    tools=[generate_html_report],
    output_key="report_generation_result",
    before_agent_callback=before_report_generator,
    after_agent_callback=after_report_generator,
)












# """Report Generator Agent - Part 4 of the Location Strategy Pipeline.

# This agent generates a professional HTML executive report from the
# structured LocationIntelligenceReport data using the generate_html_report tool.

# The tool handles:
# - Calling Gemini to generate 7-slide McKinsey/BCG style HTML
# - Saving the HTML as an artifact for download in adk web
# """

# from google.adk.agents import LlmAgent
# from google.genai import types

# from ...config import FAST_MODEL, RETRY_INITIAL_DELAY, RETRY_ATTEMPTS
# from ...tools import generate_html_report
# from ...callbacks import before_report_generator, after_report_generator


# REPORT_GENERATOR_INSTRUCTION = """You are an executive report generator for location intelligence analysis.

# Your task is to create a professional HTML executive report using the generate_html_report tool.

# TARGET LOCATION: {target_location?}
# BUSINESS TYPE: {business_type?}
# CURRENT DATE: {current_date?}

# ## Strategic Report Data
# {strategic_report}

# ## Your Mission
# Format the strategic report data and call the generate_html_report tool to create a
# McKinsey/BCG-style 7-slide HTML presentation.

# ## Steps

# ### Step 1: Format the Report Data
# Prepare a comprehensive data summary from the strategic report above, including:
# - Analysis overview (location, business type, date, market validation)
# - Top recommendation details (location, score, opportunity type, strengths, concerns)
# - Competition metrics (total competitors, density, chain dominance, ratings)
# - Market characteristics (population, income, infrastructure, foot traffic, rental costs)
# - Alternative locations (name, score, strength, concern, why not top)
# - Next steps (actionable items)
# - Key insights (strategic observations)
# - Methodology summary

# ### Step 2: Call the Tool
# Call the generate_html_report tool with the formatted report data.
# The tool will:
# - Generate a professional 7-slide HTML report
# - Save it as an artifact named "executive_report.html"
# - Return the status and artifact details

# ### Step 3: Report Result
# After the tool returns, confirm the report was generated successfully.
# If there was an error, report what went wrong.
# """

# report_generator_agent = LlmAgent(
#     name="ReportGeneratorAgent",
#     model="gemini-2.5-pro",
#     description="Generates professional McKinsey/BCG-style HTML executive reports using the generate_html_report tool",
#     instruction=REPORT_GENERATOR_INSTRUCTION,
#     generate_content_config=types.GenerateContentConfig(
#         http_options=types.HttpOptions(
#             retry_options=types.HttpRetryOptions(
#                 initial_delay=RETRY_INITIAL_DELAY,
#                 attempts=RETRY_ATTEMPTS,
#             ),
#         ),
#     ),
#     tools=[generate_html_report],
#     output_key="report_generation_result",
#     before_agent_callback=before_report_generator,
#     after_agent_callback=after_report_generator,
# )