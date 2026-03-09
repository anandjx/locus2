"""HTML Report Generator tool for creating executive reports.

100% Python-templated — zero truncation risk, zero hallucination,
zero API-call silence (instant generation, no SSE timeout).
Generates McKinsey/BCG style HTML presentations from strategic report data.
Saves the generated HTML as a dynamically named artifact.
"""

import json
import logging
from datetime import datetime
from google.adk.tools import ToolContext
from google.genai import types

logger = logging.getLogger("LocationStrategyPipeline")


# ─────────────────────────────────────────────────────────────────────
# Helper: safely extract data from the strategic report (dict or Pydantic)
# ─────────────────────────────────────────────────────────────────────

def _get(obj, key, default=""):
    """Safely get a value from dict or Pydantic model."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _to_dict(obj):
    """Convert obj to dict if it's a Pydantic model."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception:
            return {}
    return {}


# ─────────────────────────────────────────────────────────────────────
# Core HTML builder
# ─────────────────────────────────────────────────────────────────────

def _build_report_html(report: dict, business_type: str, target_location: str) -> str:
    """Build a complete McKinsey/BCG-style HTML report from structured data."""

    analysis_date = report.get("analysis_date", datetime.now().strftime("%Y-%m-%d"))
    market_validation = report.get("market_validation", "Analysis Complete")
    total_competitors = report.get("total_competitors_found", 0)
    zones_analyzed = report.get("zones_analyzed", 0)

    rec = report.get("top_recommendation", {})
    rec_name = rec.get("location_name", "N/A")
    rec_area = rec.get("area", "")
    rec_score = rec.get("overall_score", 0)
    rec_opp = rec.get("opportunity_type", "")
    rec_segment = rec.get("best_customer_segment", "")
    rec_traffic = rec.get("estimated_foot_traffic", "")

    strengths = rec.get("strengths", [])
    concerns = rec.get("concerns", [])
    next_steps = rec.get("next_steps", [])

    comp = rec.get("competition", {})
    mkt = rec.get("market", {})

    alts = report.get("alternative_locations", [])
    insights = report.get("key_insights", [])
    methodology = report.get("methodology_summary", "Multi-agent AI analysis pipeline.")

    # Score color
    if rec_score >= 75:
        score_color = "#059669"
    elif rec_score >= 50:
        score_color = "#d97706"
    else:
        score_color = "#e11d48"

    # Opportunity badge color
    opp_colors = {
        "High Potential": "#059669",
        "Metro First-Mover": "#4f46e5",
        "Residential Sticky": "#7c3aed",
        "Underserved": "#059669",
    }
    opp_color = "#4f46e5"
    for k, v in opp_colors.items():
        if k.lower() in rec_opp.lower():
            opp_color = v
            break

    # ── Build strength cards ──
    strength_cards = ""
    for s in strengths:
        s = _to_dict(s) if not isinstance(s, dict) else s
        strength_cards += f"""
        <div class="card strength-card">
          <div class="card-icon">✦</div>
          <h4>{s.get("factor", "")}</h4>
          <p>{s.get("description", "")}</p>
          <div class="evidence"><strong>Evidence:</strong> {s.get("evidence_from_analysis", "")}</div>
        </div>"""

    # ── Build concern cards ──
    concern_cards = ""
    for c in concerns:
        c = _to_dict(c) if not isinstance(c, dict) else c
        concern_cards += f"""
        <div class="card concern-card">
          <div class="card-icon">⚠</div>
          <h4>{c.get("risk", "")}</h4>
          <p>{c.get("description", "")}</p>
          <div class="mitigation"><strong>Mitigation:</strong> {c.get("mitigation_strategy", "")}</div>
        </div>"""

    # ── Build alt cards ──
    alt_cards = ""
    for i, a in enumerate(alts):
        a = _to_dict(a) if not isinstance(a, dict) else a
        a_score = a.get("overall_score", 0)
        alt_cards += f"""
        <div class="card alt-card">
          <div class="alt-rank">#{i + 2}</div>
          <h4>{a.get("location_name", "")}</h4>
          <div class="alt-area">{a.get("area", "")}</div>
          <div class="alt-score" style="color:{score_color}">{a_score}/100</div>
          <div class="alt-type">{a.get("opportunity_type", "")}</div>
          <div class="alt-detail"><span class="tag-green">Strength:</span> {a.get("key_strength", "")}</div>
          <div class="alt-detail"><span class="tag-red">Concern:</span> {a.get("key_concern", "")}</div>
          <div class="alt-detail"><span class="tag-gray">Not #1:</span> {a.get("why_not_top", "")}</div>
        </div>"""

    # ── Build insight items ──
    insight_items = ""
    for ins in insights:
        insight_items += f'<li class="insight-item">{ins}</li>\n'

    # ── Build next-step items ──
    step_items = ""
    for idx, ns in enumerate(next_steps):
        step_items += f'<li class="step-item"><span class="step-num">{idx + 1}</span>{ns}</li>\n'

    # ── Competitor snapshot rows ──
    comp_coords = comp.get("competitor_coordinates", [])
    cci = comp.get("concentration_index_cci", 0)
    req_daily = comp.get("req_daily_customers", 0)
    feasibility = comp.get("feasibility_note", "")

    # ── Market metrics ──
    ldi = mkt.get("latent_demand_ldi", 0)
    odi = mkt.get("observed_demand_odi", 0)
    gap = mkt.get("conversion_gap", 0)
    gap_label = "Blue Ocean (Underserved)" if gap > 0 else "Red Ocean (Oversaturated)"
    gap_color = "#059669" if gap > 0 else "#e11d48"

    # ── Assemble complete HTML ──
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Locus Intelligence Report — {business_type} in {target_location}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #f8fafc; color: #1e293b; line-height: 1.6;
  }}
  .slide {{
    min-height: 100vh; position: relative; padding: 3rem 2rem 5rem;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    page-break-after: always;
  }}
  .slide-inner {{ max-width: 1100px; width: 100%; }}
  .slide-footer {{
    position: absolute; bottom: 0; left: 0; width: 100%;
    text-align: center; padding: 18px 0; font-size: 0.75rem;
    font-weight: 300; letter-spacing: 0.15em; text-transform: uppercase;
    color: #475569;
    background: linear-gradient(to top, rgba(248,250,252,0.95), transparent);
    box-shadow: 0 -4px 20px rgba(99, 102, 241, 0.15);
  }}
  h1 {{ font-size: 2.5rem; font-weight: 800; color: #1e293b; margin-bottom: 0.5rem;
       text-shadow: 0 0 40px rgba(79, 70, 229, 0.06); }}
  h2 {{ font-size: 1.6rem; font-weight: 700; color: #334155; margin-bottom: 1.2rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
  h3 {{ font-size: 1.2rem; font-weight: 600; color: #475569; margin-bottom: 0.8rem; }}
  h4 {{ font-size: 1rem; font-weight: 600; color: #1e293b; margin-bottom: 0.3rem; }}
  .subtitle {{ font-size: 1.1rem; color: #64748b; margin-bottom: 2rem; }}
  .card {{
    background: #fff; border-radius: 12px; padding: 1.5rem;
    box-shadow: 0 4px 24px -4px rgba(79, 70, 229, 0.08), 0 0 12px rgba(79, 70, 229, 0.04);
    border: 1px solid rgba(226, 232, 240, 0.8);
    margin-bottom: 1rem;
  }}
  .hero-stat {{
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    box-shadow: 0 8px 32px -8px rgba(79, 70, 229, 0.12);
    border-radius: 16px; padding: 2rem; text-align: center;
    border: 1px solid rgba(226, 232, 240, 0.8);
  }}
  .hero-stat .value {{ font-size: 3rem; font-weight: 800; }}
  .hero-stat .label {{ font-size: 0.85rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.3rem; }}
  .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
  .grid-4 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; }}
  .strength-card {{ border-left: 4px solid #059669; }}
  .concern-card {{ border-left: 4px solid #e11d48; }}
  .card-icon {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
  .evidence, .mitigation {{ font-size: 0.85rem; color: #64748b; margin-top: 0.5rem; padding-top: 0.5rem; border-top: 1px solid #f1f5f9; }}
  .badge {{
    display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px;
    font-size: 0.8rem; font-weight: 600; color: #fff;
  }}
  .stat-box {{ text-align: center; padding: 1.2rem; }}
  .stat-box .val {{ font-size: 1.8rem; font-weight: 700; }}
  .stat-box .lbl {{ font-size: 0.78rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }}
  .alt-card {{ position: relative; overflow: hidden; }}
  .alt-rank {{
    position: absolute; top: 0; right: 0; background: #4f46e5; color: #fff;
    font-weight: 700; font-size: 0.85rem; padding: 0.3rem 0.8rem;
    border-radius: 0 12px 0 12px;
  }}
  .alt-area {{ font-size: 0.85rem; color: #64748b; margin-bottom: 0.3rem; }}
  .alt-score {{ font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0; }}
  .alt-type {{ font-size: 0.8rem; color: #4f46e5; font-weight: 600; margin-bottom: 0.5rem; }}
  .alt-detail {{ font-size: 0.85rem; color: #475569; margin-bottom: 0.3rem; }}
  .tag-green {{ color: #059669; font-weight: 600; }}
  .tag-red {{ color: #e11d48; font-weight: 600; }}
  .tag-gray {{ color: #64748b; font-weight: 600; }}
  .insight-item {{ margin-bottom: 0.8rem; padding-left: 0.5rem; border-left: 3px solid #4f46e5; }}
  .step-item {{ display: flex; gap: 0.8rem; align-items: flex-start; margin-bottom: 0.8rem; }}
  .step-num {{
    flex-shrink: 0; width: 28px; height: 28px; border-radius: 50%;
    background: #4f46e5; color: #fff; display: flex; align-items: center;
    justify-content: center; font-weight: 700; font-size: 0.85rem;
  }}
  .gap-bar {{ height: 24px; border-radius: 12px; position: relative; overflow: hidden; background: #e2e8f0; }}
  .gap-fill {{ height: 100%; border-radius: 12px; transition: width 0.8s ease; }}
  .muted {{ font-size: 0.85rem; color: #64748b; }}
  .cta-banner {{
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: #fff; border-radius: 16px; padding: 2.5rem; text-align: center;
    box-shadow: 0 8px 32px rgba(79, 70, 229, 0.3), 0 0 60px rgba(124, 58, 237, 0.15);
    margin-top: 2rem;
  }}
  .cta-banner h3 {{ color: #fff; font-size: 1.4rem; margin-bottom: 0.8rem; border: none; }}
  .cta-banner p {{ color: rgba(255,255,255,0.9); font-size: 0.95rem; }}
  .disclaimer {{ font-size: 0.78rem; color: #94a3b8; line-height: 1.5; margin-top: 1.5rem; padding: 1rem; background: #f1f5f9; border-radius: 8px; }}
  @media (max-width: 640px) {{
    .slide {{ padding: 1.5rem 1rem 4rem; }}
    h1 {{ font-size: 1.8rem; }}
    .hero-stat .value {{ font-size: 2.2rem; }}
    .grid-2, .grid-3, .grid-4 {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<!-- ═══ SLIDE 1: EXECUTIVE SUMMARY ═══ -->
<section class="slide" style="background: linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);">
  <div class="slide-inner" style="text-align:center;">
    <div style="margin-bottom:1rem;">
      <span class="badge" style="background:#4f46e5;">LOCUS INTELLIGENCE</span>
    </div>
    <h1>{business_type.title()} — {target_location}</h1>
    <p class="subtitle">Location Intelligence Report · {analysis_date}</p>

    <div class="grid-3" style="margin-top:2rem;">
      <div class="hero-stat">
        <div class="value" style="color:{score_color}">{rec_score}</div>
        <div class="label">Organic RAV Score</div>
      </div>
      <div class="hero-stat">
        <div class="value" style="color:#4f46e5">{rec_name}</div>
        <div class="label">Top Recommendation</div>
      </div>
      <div class="hero-stat">
        <div class="value" style="color:#475569">{total_competitors}</div>
        <div class="label">Competitors Analyzed</div>
      </div>
    </div>

    <div class="card" style="margin-top:2rem; text-align:left;">
      <h3>Market Validation</h3>
      <p>{market_validation}</p>
    </div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 2: TOP RECOMMENDATION ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Top Recommendation — {rec_name}</h2>
    <div class="grid-2" style="margin-bottom:1.5rem;">
      <div class="card">
        <div class="stat-box">
          <div class="val" style="color:{score_color}">{rec_score}/100</div>
          <div class="lbl">Overall Score</div>
        </div>
      </div>
      <div class="card">
        <div class="stat-box">
          <div class="val" style="color:{opp_color}">{rec_opp}</div>
          <div class="lbl">Opportunity Type</div>
        </div>
      </div>
    </div>

    <h3 style="color:#059669">▲ Strengths</h3>
    <div class="grid-2">{strength_cards}</div>

    <h3 style="color:#e11d48; margin-top:1.5rem;">▼ Concerns</h3>
    <div class="grid-2">{concern_cards}</div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 3: COMPETITION ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Structural Market Power — Competition</h2>
    <div class="grid-4">
      <div class="card stat-box">
        <div class="val">{comp.get("total_competitors", 0)}</div>
        <div class="lbl">Total Competitors</div>
      </div>
      <div class="card stat-box">
        <div class="val">{comp.get("density_per_km2", 0):.1f}</div>
        <div class="lbl">Density / km²</div>
      </div>
      <div class="card stat-box">
        <div class="val">{comp.get("chain_dominance_pct", 0):.0f}%</div>
        <div class="lbl">Chain Dominance</div>
      </div>
      <div class="card stat-box">
        <div class="val">{comp.get("avg_competitor_rating", 0):.1f}</div>
        <div class="lbl">Avg Rating</div>
      </div>
      <div class="card stat-box">
        <div class="val">{comp.get("high_performers_count", 0)}</div>
        <div class="lbl">High Performers (4.5+)</div>
      </div>
      <div class="card stat-box">
        <div class="val">{cci:.2f}</div>
        <div class="lbl">Concentration Index (CCI)</div>
      </div>
    </div>
    <div class="card" style="margin-top:1.5rem;">
      <h3>Required Daily Customers (Break-even Proxy)</h3>
      <div style="font-size:2rem; font-weight:700; color:#4f46e5; margin:0.5rem 0;">{req_daily}</div>
      <p class="muted">{feasibility}</p>
      <div class="muted" style="margin-top:0.8rem; padding-top:0.8rem; border-top:1px solid #e2e8f0;">
        <strong>How This Number Is Estimated:</strong> This is a structural proxy derived by scaling a baseline daily customer threshold against the zone's Estimated Rent Tier and Competitive Density (ODI). It serves as a directional break-even indicator, not an absolute financial projection.
      </div>
    </div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 4: MARKET PHYSICS ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Market Physics &amp; Financial Gap</h2>
    <div class="grid-3">
      <div class="card stat-box">
        <div class="val" style="color:#4f46e5">{ldi:.2f}</div>
        <div class="lbl">Latent Demand (LDI)</div>
      </div>
      <div class="card stat-box">
        <div class="val" style="color:#7c3aed">{odi:.2f}</div>
        <div class="lbl">Observed Demand (ODI)</div>
      </div>
      <div class="card stat-box">
        <div class="val" style="color:{gap_color}">{gap:+.2f}</div>
        <div class="lbl">Conversion Gap</div>
      </div>
    </div>
    <div class="card" style="margin-top:1rem;">
      <h4>Demand Gap Visualization</h4>
      <div style="margin:1rem 0;">
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#64748b; margin-bottom:0.3rem;">
          <span>LDI: {ldi:.2f}</span><span>ODI: {odi:.2f}</span>
        </div>
        <div class="gap-bar">
          <div class="gap-fill" style="width:{min(ldi * 100, 100):.0f}%; background:#4f46e5;"></div>
        </div>
        <div class="gap-bar" style="margin-top:0.4rem;">
          <div class="gap-fill" style="width:{min(odi * 100, 100):.0f}%; background:#7c3aed;"></div>
        </div>
      </div>
      <div class="badge" style="background:{gap_color};">{gap_label}</div>
    </div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 5: MARKET FUNDAMENTALS ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Market Fundamentals</h2>
    <div class="grid-3">
      <div class="card stat-box">
        <div class="val">{mkt.get("population_density", "N/A")}</div>
        <div class="lbl">Population Density</div>
      </div>
      <div class="card stat-box">
        <div class="val">{mkt.get("income_level", "N/A")}</div>
        <div class="lbl">Income Level</div>
      </div>
      <div class="card stat-box">
        <div class="val">{mkt.get("estimated_rent_tier", "N/A")}</div>
        <div class="lbl">Estimated Rent Tier</div>
      </div>
    </div>
    <div class="grid-2" style="margin-top:1rem;">
      <div class="card">
        <h4>Infrastructure Access</h4>
        <p>{mkt.get("infrastructure_access", "N/A")}</p>
      </div>
      <div class="card">
        <h4>Foot Traffic Pattern</h4>
        <p>{mkt.get("foot_traffic_pattern", "N/A")}</p>
      </div>
    </div>
    <div class="grid-2" style="margin-top:1rem;">
      <div class="card">
        <h4>Best Customer Segment</h4>
        <p>{rec_segment}</p>
      </div>
      <div class="card">
        <h4>Estimated Foot Traffic</h4>
        <p>{rec_traffic}</p>
      </div>
    </div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 6: ALTERNATIVES ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Alternative Locations</h2>
    <div class="grid-2">{alt_cards if alt_cards else '<div class="card"><p class="muted">No alternative locations analyzed.</p></div>'}</div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 7: INSIGHTS & STRATEGY ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Key Insights &amp; Go-To-Market Strategy</h2>
    <div class="card">
      <h3>Strategic Insights</h3>
      <ul style="list-style:none; padding:0;">{insight_items if insight_items else '<li class="muted">No insights available.</li>'}</ul>
    </div>
    <div class="card" style="margin-top:1rem;">
      <h3>Actionable Next Steps</h3>
      <ul style="list-style:none; padding:0;">{step_items if step_items else '<li class="muted">No steps defined.</li>'}</ul>
    </div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

<!-- ═══ SLIDE 8: METHODOLOGY & DISCLAIMER ═══ -->
<section class="slide">
  <div class="slide-inner">
    <h2>Methodology, Disclaimer &amp; Locus App</h2>
    <div class="card">
      <h3>Methodology</h3>
      <p>{methodology}</p>
    </div>

    <div class="disclaimer">
      <strong>LEGAL &amp; FINANCIAL DISCLAIMER:</strong> Insights are probabilistic and derived from localized data samples. Break-even figures and market physics (RAV, LDI, ODI) are estimations for strategic directional comparison only. Locus, a product of Intsemble, disclaims liability for capital-intensive decisions. Users must conduct independent, localized commercial and financial due diligence.
    </div>

    <div class="cta-banner">
      <h3>This report provides a concise executive snapshot.</h3>
      <p>For the complete interactive experience — including deep dives into granular Market Research with source-backed insights, live Competitor Mapping visualized on Google Maps, and Deep Gap Analysis powered by the Quantitative Leaderboard — return to the <strong>Locus App UI</strong>.</p>
    </div>
  </div>
  <div class="slide-footer">LOCUS | A PRODUCT BY INTSEMBLE</div>
</section>

</body>
</html>"""

    return html


# ─────────────────────────────────────────────────────────────────────
# ADK Tool
# ─────────────────────────────────────────────────────────────────────

async def generate_html_report(
    report_data: str,
    business_type: str,
    target_location: str,
    tool_context: ToolContext
) -> dict:
    """Generate a McKinsey/BCG style HTML executive report and save as artifact.

    100% Python-templated: instant generation, zero Gemini API call,
    zero SSE idle timeout risk.

    Args:
        report_data: The strategic report data formatted by the agent (used as fallback).
        business_type: The type of business (used for dynamic filename).
        target_location: The location analyzed (used for dynamic filename).
        tool_context: ADK ToolContext for saving artifacts.
    """
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Create a clean, safe filename
        safe_biz = str(business_type).replace(" ", "_").replace("/", "-") if business_type else "Business"
        safe_loc = str(target_location).replace(" ", "_").replace("/", "-") if target_location else "Location"
        artifact_filename = f"{safe_biz}_{safe_loc}_Locus_Report.html"

        # ── Get structured report from state (set by StrategyAdvisorAgent output_key) ──
        raw_report = tool_context.state.get("strategic_report", {})
        report = _to_dict(raw_report)

        if not report:
            logger.warning("strategic_report not found in state; returning error")
            return {
                "status": "error",
                "error_message": "Strategic report data not found in pipeline state.",
            }

        logger.info(f"Report Generator: Building Python-templated report for {business_type} in {target_location}")

        # ── Generate HTML instantly via Python templates ──
        html_code = _build_report_html(report, business_type or "", target_location or "")

        # ── Save artifact ──
        html_artifact = types.Part.from_bytes(
            data=html_code.encode('utf-8'),
            mime_type="text/html"
        )

        version = await tool_context.save_artifact(
            filename=artifact_filename,
            artifact=html_artifact
        )

        # ── Save to state for frontend display ──
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