"""HTML Report Generator tool for creating executive reports.

Uses direct text generation to create McKinsey/BCG style HTML presentations 
from strategic report data. Saves the generated HTML as a dynamically named artifact.
"""

import logging
import os
from datetime import datetime
from google.adk.tools import ToolContext
from google.genai import types
from google.genai.errors import ServerError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ..config import PRO_MODEL

logger = logging.getLogger("LocationStrategyPipeline")


def _create_genai_client():
    """Create a genai.Client that works in both local (API key) and Cloud Run (Vertex AI) modes."""
    from google import genai

    if os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE":
        logger.info("Initializing genai.Client in Vertex AI mode")
        return genai.Client(
            vertexai=True,
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
        )
    else:
        logger.info("Initializing genai.Client in API Key mode")
        return genai.Client()

async def generate_html_report(
    report_data: str, 
    business_type: str, 
    target_location: str, 
    tool_context: ToolContext
) -> dict:
    """Generate a McKinsey/BCG style HTML executive report and save as artifact.

    Args:
        report_data: The strategic report data formatted by the agent.
        business_type: The type of business (used for dynamic filename).
        target_location: The location analyzed (used for dynamic filename).
        tool_context: ADK ToolContext for saving artifacts.
    """
    try:
        client = _create_genai_client()
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Create a clean, safe filename (e.g., Gym_Versova_Mumbai_Locus_Report.html)
        safe_biz = str(business_type).replace(" ", "_").replace("/", "-") if business_type else "Business"
        safe_loc = str(target_location).replace(" ", "_").replace("/", "-") if target_location else "Location"
        artifact_filename = f"{safe_biz}_{safe_loc}_Locus_Report.html"

        prompt = f"""Generate a comprehensive, professional HTML report for a location intelligence analysis.

This report MUST be in the style of elite McKinsey/BCG consulting presentations, perfectly inheriting the 'Locus by Intsemble' UI theme (Slate, Indigo, White Glass, Soft Glows).

CRITICAL GUARDRAIL - ZERO HALLUCINATION:
If a specific metric or list (like the Competitor List, Required Market Share, LDI, or CCI) is missing from the data provided, DO NOT invent numbers or names. OMIT that specific visual element or state "Data Insufficient for Calculation". Your credibility relies on absolute factual accuracy.

1. STRUCTURE - Create 8 distinct slides (full-screen sections, min-height: 100vh, position: relative):

   SLIDE 1 - EXECUTIVE SUMMARY
   - Large, prominent display of recommended location
   - Business type and target location
   - High-level market validation and Organic RAV Score

   SLIDE 2 - TOP RECOMMENDATION DETAILS
   - Strengths with evidence & Concerns with mitigations

   SLIDE 3 - STRUCTURAL MARKET POWER (Competition)
   - Competition metrics (total competitors, chain dominance, CCI)
   - TRANSPARENCY REQUIREMENT: Add a "Competitor Data Snapshot" footer/subsection at the bottom of the slide. Display a clean, compact grid or list of the actual competitors used in this analysis. STRICTLY include only: Name, Rating, and Number of Reviews. Do not infer missing fields. If no specific competitor names are provided in the data, omit this subsection entirely.

   SLIDE 4 - MARKET PHYSICS & FINANCIAL GAP
   - Visually display Latent Demand (LDI) vs Observed Demand (ODI) and Conversion Gap
   - Display Required Market Share and Demand Deficit warnings
   - TRANSPARENCY REQUIREMENT: Directly beneath the "Required Daily Customers (Break-even Proxy)" metric, add a clearly labeled, small-text explanatory subsection titled "How This Number Is Estimated". Explain simply that this is a structural proxy derived by scaling a baseline daily customer threshold against the zone's Estimated Rent Tier and Competitive Density (ODI). DO NOT introduce new math, fabricated basket sizes, or specific dollar amounts.

   SLIDE 5 - MARKET FUNDAMENTALS
   - Population density, income level, rental costs in a grid

   SLIDE 6 - ALTERNATIVE LOCATIONS
   - Comparison cards with scores and pros/cons

   SLIDE 7 - KEY INSIGHTS & GO-TO-MARKET ATTACK STRATEGY
   - Strategic insights and actionable next steps

   SLIDE 8 - METHODOLOGY, DISCLAIMER & THE LOCUS APP CTA
   - Methodology of the analysis
   - The Legal Disclaimer (provided in section 3 below)
   - A VISUALLY DOMINANT CALL-TO-ACTION (CTA) section. This CTA must be the visual centerpiece of the slide — large, eye-catching, and impossible to miss. Design it as a premium card or banner with a strong indigo-to-purple gradient background, large bold white text, and a glowing border or shadow. The CTA text should communicate: "This report provides a concise executive snapshot.

For the complete interactive experience, including deep dives into granular Market Research with source-backed insights, live Competitor Mapping visualized on Google Maps and Deep Gap Analysis powered by the Quantitative Leaderboard, return to the Locus App UI.

2. DESIGN & CSS REQUIREMENTS (The Intsemble Theme):
   - Palette: Slate backgrounds (#f8fafc), crisp white cards, Indigo accents (#4f46e5), Emerald for positives (#059669), Rose for risks (#e11d48).
   - Clean sans-serif typography: font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif.
   
   GLOBAL SOFT GLOWS (Premium Locus Feel):
   - Apply a subtle, premium soft indigo glow to ALL content cards throughout the report. Use: `box-shadow: 0 4px 24px -4px rgba(79, 70, 229, 0.08), 0 0 12px rgba(79, 70, 229, 0.04); border: 1px solid rgba(226, 232, 240, 0.8);`
   - Apply a slightly stronger glow to slide headers/titles: `text-shadow: 0 0 40px rgba(79, 70, 229, 0.06);`
   - Apply a glowing highlight to hero stat numbers (RAV scores, LDI, etc.): `box-shadow: 0 8px 32px -8px rgba(79, 70, 229, 0.12); background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);`
   - Keep all glows subtle and professional — this is a consulting document, not a gaming UI.
   
   PER-SLIDE FOOTER (replaces any floating watermark):
   - DO NOT create any fixed/floating watermark elements (no `.locus-watermark`, no `position: fixed` watermarks).
   - Instead, at the absolute bottom of EVERY slide section (inside each slide div, as the last child), add a footer div with the text: "LOCUS | A PRODUCT BY INTSEMBLE".
   - Style this footer to be dominant but elegant: `position: absolute; bottom: 0; left: 0; width: 100%; text-align: center; padding: 18px 0; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #475569; background: linear-gradient(to top, rgba(248,250,252,0.95), transparent); box-shadow: 0 -4px 20px rgba(99, 102, 241, 0.15);`
   - This footer must appear on every single slide consistently.
   
   RESPONSIVE & CAPTIVATING LAYOUT:
   - The entire report must be visually captivating — use generous white space, elegant transitions between sections, and clean visual hierarchy.
   - Ensure the report renders beautifully on mobile devices and edge browsers: use relative units (rem, %, vw), `max-width: 100%` on images/tables, and CSS Grid/Flexbox with `flex-wrap: wrap`.
   - Each slide should have `padding-bottom: 60px` to account for the footer.
   - Smooth scroll behavior: `html {{ scroll-behavior: smooth; }}`
   
   Explainers/Notes: Style the "How This Number Is Estimated" and "Competitor Snapshot" subsections with muted text (color: #64748b; font-size: 0.85rem) so they provide transparency without visual clutter.

3. REQUIRED DISCLAIMER TEXT (Place on Slide 8):
   "LEGAL & FINANCIAL DISCLAIMER: Insights are probabilistic and derived from localized data samples. Break-even figures and market physics (RAV, LDI, ODI) are estimations for strategic directional comparison only. Locus, a product of Intsemble, disclaims liability for capital-intensive decisions. Users must conduct independent, localized commercial and financial due diligence."

4. DATA TO INCLUDE (USE EXACTLY THIS DATA):
{report_data}

5. OUTPUT:
   - Generate ONLY the complete HTML code (<!DOCTYPE html> to </html>).
   - NO markdown code fences (do not output ```html).
"""

        logger.info("Generating HTML report using Gemini...")

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=2, min=2, max=30),
            retry=retry_if_exception_type(ServerError),
            before_sleep=lambda retry_state: logger.warning(
                f"Gemini API error, retrying in {retry_state.next_action.sleep} seconds... "
                f"(attempt {retry_state.attempt_number}/3)"
            ),
        )
        def generate_with_retry():
            return client.models.generate_content(
                model=PRO_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.2), # Dropped temp to ensure CSS/Structure stays flawless and limits hallucination
            )

        response = generate_with_retry()
        html_code = response.text

        # Strip markdown code fences if present
        if html_code.startswith("```"):
            if html_code.startswith("```html") or html_code.startswith("```HTML"):
                html_code = html_code[7:]
            else:
                html_code = html_code[3:]
            if html_code.rstrip().endswith("```"):
                html_code = html_code.rstrip()[:-3]
        html_code = html_code.strip()

        if not html_code.startswith("<!DOCTYPE") and not html_code.startswith("<html"):
            logger.warning("Generated content may not be valid HTML")

        html_artifact = types.Part.from_bytes(
            data=html_code.encode('utf-8'),
            mime_type="text/html"
        )

        version = await tool_context.save_artifact(
            filename=artifact_filename,
            artifact=html_artifact
        )

        tool_context.state["html_report_content"] = html_code

        logger.info(f"Saved HTML report artifact: {artifact_filename} (version {version})")

        return {
            "status": "success",
            "message": f"HTML report generated and saved as artifact '{artifact_filename}'",
            "artifact_filename": artifact_filename,
            "artifact_version": version,
            "html_length": len(html_code),
        }

    except Exception as e:
        logger.error(f"Failed to generate HTML report: {e}")
        return {
            "status": "error",
            "error_message": f"Failed to generate HTML report: {str(e)}",
        }











# """HTML Report Generator tool for creating executive reports.

# Uses direct text generation (same as original notebook Part 4) to create
# McKinsey/BCG style 7-slide HTML presentations from strategic report data.
# Saves the generated HTML as an artifact for download in adk web.
# """

# import logging
# from datetime import datetime
# from google.adk.tools import ToolContext
# from google.genai import types
# from google.genai.errors import ServerError
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# from ..config import PRO_MODEL

# logger = logging.getLogger("LocationStrategyPipeline")


# async def generate_html_report(report_data: str, tool_context: ToolContext) -> dict:
#     """Generate a McKinsey/BCG style HTML executive report and save as artifact.

#     This tool creates a professional 7-slide HTML presentation from the
#     location intelligence report data using direct text generation with Gemini.
#     The generated HTML is automatically saved as an artifact for viewing in adk web.

#     Args:
#         report_data: The strategic report data in a formatted string containing
#                     analysis overview, top recommendation, competition metrics,
#                     market characteristics, alternatives, insights, and methodology.
#         tool_context: ADK ToolContext for saving artifacts.

#     Returns:
#         dict: A dictionary containing:
#             - status: "success" or "error"
#             - message: Status message
#             - artifact_filename: Name of saved artifact (if successful)
#             - artifact_version: Version number of artifact (if successful)
#             - html_length: Character count of generated HTML
#             - error_message: Error details (if failed)
#     """
#     try:
#         from google import genai

#         # Initialize client (uses GOOGLE_API_KEY from env)
#         client = genai.Client()

#         current_date = datetime.now().strftime("%Y-%m-%d")

#         # Comprehensive prompt for multi-slide HTML generation
#         # Adapted from original notebook Part 4
#         prompt = f"""Generate a comprehensive, professional HTML report for a location intelligence analysis.

# This report should be in the style of McKinsey/BCG consulting presentations:
# - Multi-slide format using full-screen scrollable sections
# - Modern, clean, executive-ready design
# - Data-driven visualizations
# - Professional color scheme and typography

# CRITICAL REQUIREMENTS:

# 1. STRUCTURE - Create 7 distinct slides (full-screen sections):

#    SLIDE 1 - EXECUTIVE SUMMARY & TOP RECOMMENDATION
#    - Large, prominent display of recommended location and score
#    - Business type and target location
#    - High-level market validation
#    - Eye-catching hero section

#    SLIDE 2 - TOP RECOMMENDATION DETAILS
#    - All strengths with evidence (cards/boxes)
#    - All concerns with mitigation strategies
#    - Opportunity type and target customer segment

#    SLIDE 3 - COMPETITION ANALYSIS
#    - Competition metrics (total competitors, density, chain dominance)
#    - Visual representation of key numbers (large stat boxes)
#    - Average ratings, high performers count

#    SLIDE 4 - MARKET CHARACTERISTICS
#    - Population density, income level, infrastructure
#    - Foot traffic patterns, rental costs
#    - Grid/card layout for each characteristic

#    SLIDE 5 - ALTERNATIVE LOCATIONS
#    - Each alternative in a comparison card
#    - Scores, opportunity types, strengths/concerns
#    - Why each is not the top choice

#    SLIDE 6 - KEY INSIGHTS & NEXT STEPS
#    - Strategic insights (bullet points or cards)
#    - Actionable next steps (numbered list)

#    SLIDE 7 - METHODOLOGY
#    - How the analysis was performed
#    - Data sources and approach

# 2. DESIGN:
#    - Use professional consulting color palette:
#      * Primary: Navy blue (#1e3a8a, #3b82f6) for headers/trust
#      * Success: Green (#059669, #10b981) for positive metrics
#      * Warning: Amber (#d97706, #f59e0b) for concerns
#      * Neutral: Grays (#6b7280, #e5e7eb) for backgrounds
#    - Modern sans-serif fonts (system: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto)
#    - Cards with subtle shadows and rounded corners
#    - Generous white space and padding
#    - Responsive grid layouts

# 3. TECHNICAL:
#    - Self-contained: ALL CSS embedded in <style> tag
#    - No external dependencies (no CDNs, no external images)
#    - Each slide: min-height: 100vh; page-break-after: always;
#    - Smooth scroll behavior
#    - Print-friendly

# 4. DATA TO INCLUDE (use EXACTLY this data, DO NOT INVENT):

# {report_data}

# 5. OUTPUT:
#    - Generate ONLY the complete HTML code
#    - Start with <!DOCTYPE html>
#    - End with </html>
#    - NO explanations before or after the HTML
#    - NO markdown code fences

# Make it visually stunning, data-rich, and executive-ready.

# Current date: {current_date}
# """

#         logger.info("Generating HTML report using Gemini...")

#         # Retry wrapper for handling model overload errors
#         @retry(
#             stop=stop_after_attempt(3),
#             wait=wait_exponential(multiplier=2, min=2, max=30),
#             retry=retry_if_exception_type(ServerError),
#             before_sleep=lambda retry_state: logger.warning(
#                 f"Gemini API error, retrying in {retry_state.next_action.sleep} seconds... "
#                 f"(attempt {retry_state.attempt_number}/3)"
#             ),
#         )
#         def generate_with_retry():
#             return client.models.generate_content(
#                 model=PRO_MODEL,
#                 contents=prompt,
#                 config=types.GenerateContentConfig(temperature=1.0),
#             )

#         # Direct text generation (NOT code execution)
#         # Same as original notebook: types.GenerateContentConfig(temperature=1.0)
#         response = generate_with_retry()

#         # Extract HTML from response.text
#         html_code = response.text
#         # Strip markdown code fences if present
#         if html_code.startswith("```"):
#             # Remove opening fence (```html or ```)
#             if html_code.startswith("```html"):
#                 html_code = html_code[7:]
#             elif html_code.startswith("```HTML"):
#                 html_code = html_code[7:]
#             else:
#                 html_code = html_code[3:]

#             # Remove closing fence
#             if html_code.rstrip().endswith("```"):
#                 html_code = html_code.rstrip()[:-3]

#             html_code = html_code.strip()

#         # Validate we got HTML
#         if not html_code.strip().startswith("<!DOCTYPE") and not html_code.strip().startswith("<html"):
#             logger.warning("Generated content may not be valid HTML")

#         # Save as artifact with proper MIME type so it appears in ADK web UI
#         html_artifact = types.Part.from_bytes(
#             data=html_code.encode('utf-8'),
#             mime_type="text/html"
#         )
#         artifact_filename = "executive_report.html"

#         version = await tool_context.save_artifact(
#             filename=artifact_filename,
#             artifact=html_artifact
#         )

#         # Also store in state for AG-UI frontend display
#         tool_context.state["html_report_content"] = html_code

#         logger.info(f"Saved HTML report artifact: {artifact_filename} (version {version})")

#         return {
#             "status": "success",
#             "message": f"HTML report generated and saved as artifact '{artifact_filename}'",
#             "artifact_filename": artifact_filename,
#             "artifact_version": version,
#             "html_length": len(html_code),
#         }

#     except Exception as e:
#         logger.error(f"Failed to generate HTML report: {e}")
#         return {
#             "status": "error",
#             "error_message": f"Failed to generate HTML report: {str(e)}",
#         }