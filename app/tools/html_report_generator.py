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
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI', system-ui, sans-serif;
    background: #f8fafc; color: #0f172a; line-height: 1.65;
    -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
  }}

  /* ── SLIDE LAYOUT ── */
  .slide {{
    min-height: 100vh; position: relative; padding: 3.5rem 2rem 5.5rem;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    page-break-after: always;
    background:
      radial-gradient(ellipse 80% 50% at 20% 80%, rgba(99,102,241,0.04), transparent),
      radial-gradient(ellipse 60% 40% at 85% 15%, rgba(124,58,237,0.03), transparent);
  }}
  .slide-inner {{ max-width: 1100px; width: 100%; z-index: 2; }}

  /* ── PREMIUM GLASSMORPHISM FOOTER — brushed steel + glass ── */
 .slide-footer {{
  position: absolute; bottom: 0; left: 0; width: 100%; z-index: 10;
  text-align: center; padding: 20px 0; font-size: 0.78rem;
  font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase;

  background-image: linear-gradient(
    180deg,
    #f8fafc 0%,
    #e2e8f0 40%,
    #cbd5f5 70%,
    #ffffff 100%
  );

  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;

  filter: drop-shadow(0 0 3px rgba(148,163,184,0.12));
}}

.slide-footer::before {{
  content: '';
  position: absolute;
  inset: 0;
  z-index: -1;

  backdrop-filter: blur(12px) saturate(1.4);

  background: linear-gradient(
    to top,
    rgba(255,255,255,0.35),
    rgba(255,255,255,0.05)
  );

  border-top: 1px solid rgba(255,255,255,0.6);

  box-shadow: 0 -4px 12px rgba(99,102,241,0.04);
}}

  /* ── TYPOGRAPHY ── */
  h1 {{ font-size: 2.8rem; font-weight: 800; color: #0f172a; margin-bottom: 0.5rem;
       letter-spacing: -0.025em; text-shadow: 0 4px 32px rgba(79,70,229,0.1); }}
  h2 {{ font-size: 1.65rem; font-weight: 700; color: #1e293b; margin-bottom: 1.2rem;
       border-bottom: 2px solid rgba(226,232,240,0.7); padding-bottom: 0.5rem; letter-spacing: -0.01em; }}
  h3 {{ font-size: 1.2rem; font-weight: 700; color: #334155; margin-bottom: 0.8rem; }}
  h4 {{ font-size: 1.05rem; font-weight: 600; color: #0f172a; margin-bottom: 0.3rem; }}
  .subtitle {{ font-size: 1.1rem; font-weight: 500; color: #64748b; margin-bottom: 2rem; letter-spacing: 0.02em; }}

  /* ── CARDS — layered glass shadows ── */
  .card {{
    background: rgba(255,255,255,0.88); border-radius: 16px; padding: 1.6rem;
    backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px);
    box-shadow:
      0 1px 3px rgba(15,23,42,0.04),
      0 6px 24px -4px rgba(79,70,229,0.07),
      0 16px 56px -12px rgba(79,70,229,0.05);
    border: 1px solid rgba(255,255,255,0.9);
    margin-bottom: 1rem;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
  }}
  .card:hover {{
    transform: translateY(-2px);
    box-shadow:
      0 2px 6px rgba(15,23,42,0.05),
      0 10px 36px -6px rgba(79,70,229,0.1),
      0 24px 72px -16px rgba(79,70,229,0.08);
  }}

  /* ── HERO STATS — frosted glass ── */
  .hero-stat {{
    background: linear-gradient(135deg, rgba(255,255,255,1) 0%, rgba(248,250,252,0.92) 100%);
    box-shadow:
      0 8px 32px -8px rgba(79,70,229,0.14),
      inset 0 1px 0 rgba(255,255,255,1),
      0 0 0 1px rgba(226,232,240,0.5);
    border-radius: 20px; padding: 2.2rem; text-align: center;
    border: none;
  }}
  .hero-stat .value {{ font-size: 3.2rem; font-weight: 800; letter-spacing: -0.03em;
       text-shadow: 0 2px 12px rgba(0,0,0,0.04); }}
  .hero-stat .label {{ font-size: 0.82rem; font-weight: 600; color: #64748b;
       text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.6rem; }}

  /* ── GRIDS ── */
  .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.2rem; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.2rem; }}
  .grid-4 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.2rem; }}

  /* ── ACCENT CARDS ── */
  .strength-card {{ border-left: 4px solid #10b981; }}
  .concern-card {{ border-left: 4px solid #f43f5e; }}
  .card-icon {{ font-size: 1.6rem; margin-bottom: 0.5rem; text-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
  .evidence, .mitigation {{ font-size: 0.85rem; color: #475569; margin-top: 0.6rem; padding-top: 0.6rem; border-top: 1px solid rgba(241,245,249,0.8); }}

  /* ── BADGES ── */
  .badge {{
    display: inline-block; padding: 0.3rem 0.85rem; border-radius: 9999px;
    font-size: 0.8rem; font-weight: 600; color: #fff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-shadow: 0 1px 2px rgba(0,0,0,0.1);
  }}

  /* ── STAT BOXES ── */
  .stat-box {{ text-align: center; padding: 1.4rem; }}
  .stat-box .val {{ font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; }}
  .stat-box .lbl {{ font-size: 0.78rem; font-weight: 600; color: #64748b;
       text-transform: uppercase; letter-spacing: 0.08em; margin-top: 0.3rem; }}

  /* ── ALTERNATIVES ── */
  .alt-card {{ position: relative; overflow: hidden; }}
  .alt-rank {{
    position: absolute; top: 0; right: 0;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); color: #fff;
    font-weight: 800; font-size: 0.9rem; padding: 0.4rem 1rem;
    border-radius: 0 16px 0 16px; box-shadow: -2px 2px 10px rgba(79,70,229,0.2);
  }}
  .alt-area {{ font-size: 0.85rem; font-weight: 500; color: #64748b; margin-bottom: 0.4rem; }}
  .alt-score {{ font-size: 1.8rem; font-weight: 800; margin: 0.5rem 0; letter-spacing: -0.02em; }}
  .alt-type {{ font-size: 0.85rem; color: #4f46e5; font-weight: 700; margin-bottom: 0.5rem; }}
  .alt-detail {{ font-size: 0.85rem; color: #334155; margin-bottom: 0.35rem; }}
  .tag-green {{ color: #10b981; font-weight: 700; }}
  .tag-red {{ color: #f43f5e; font-weight: 700; }}
  .tag-gray {{ color: #64748b; font-weight: 700; }}

  /* ── INSIGHTS & STEPS ── */
  .insight-item {{ margin-bottom: 0.8rem; padding-left: 0.8rem; border-left: 3px solid #6366f1; font-weight: 500; }}
  .step-item {{ display: flex; gap: 1rem; align-items: flex-start; margin-bottom: 1rem; font-weight: 500; }}
  .step-num {{
    flex-shrink: 0; width: 30px; height: 30px; border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #4f46e5); color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.9rem; box-shadow: 0 4px 12px rgba(79,70,229,0.25);
  }}

  /* ── CHARTS ── */
  .gap-bar {{ height: 24px; border-radius: 9999px; position: relative; overflow: hidden;
       background: #e2e8f0; box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); }}
  .gap-fill {{ height: 100%; border-radius: 9999px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); }}
  .muted {{ font-size: 0.85rem; color: #64748b; }}

  /* ── CTA BANNER — neon indigo ── */
  .cta-banner {{
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: #fff; border-radius: 20px; padding: 3rem; text-align: center;
    box-shadow:
      0 10px 40px rgba(79,70,229,0.3),
      0 0 80px rgba(124,58,237,0.12),
      inset 0 1px 1px rgba(255,255,255,0.25);
    margin-top: 2rem; border: 1px solid rgba(255,255,255,0.1);
  }}
  .cta-banner h3 {{ color: #fff; font-size: 1.5rem; font-weight: 800; margin-bottom: 0.8rem;
       border: none; text-shadow: 0 2px 8px rgba(0,0,0,0.15); }}
  .cta-banner p {{ color: rgba(255,255,255,0.92); font-size: 1rem; line-height: 1.6; }}

  /* ── DISCLAIMER ── */
  .disclaimer {{ font-size: 0.78rem; color: #64748b; line-height: 1.6; margin-top: 1.5rem;
       padding: 1.2rem; background: rgba(241,245,249,0.8); border-radius: 12px;
       border: 1px solid rgba(226,232,240,0.6); backdrop-filter: blur(4px); }}

  /* ── RESPONSIVE ── */
  @media (max-width: 640px) {{
    .slide {{ padding: 1.5rem 1rem 4.5rem; }}
    h1 {{ font-size: 2rem; }}
    .hero-stat .value {{ font-size: 2.4rem; }}
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