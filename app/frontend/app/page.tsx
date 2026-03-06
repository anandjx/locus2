"use client";

import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";

import { PipelineTimeline } from "@/components/PipelineTimeline";
import { LocationReport } from "@/components/LocationReport";
import { CompetitorCard } from "@/components/CompetitorCard";
import { MarketCard } from "@/components/MarketCard";
import { AlternativeLocations } from "@/components/AlternativeLocations";
import { ArtifactViewer } from "@/components/ArtifactViewer";
import { AgentStatus } from "@/components/AgentStatus";
import { StaticMapCard } from "@/components/StaticMapCard";

import type { AgentState } from "@/lib/types";

const AGENT_CONFIG = {
  agentName: "locus",
  productName: "LOCUS",
  tagline: "Where decisions meet intelligence",
  company: "Intsemble",
  totalStages: 6,
};

export default function Home() {
  const { state } = useCoAgent<AgentState>({
    name: AGENT_CONFIG.agentName,
  });

  useCoAgentStateRender<AgentState>({
    name: AGENT_CONFIG.agentName,
    render: ({ state }) => {
      if (!state || !state.pipeline_stage) return null;
      return (
        <div className="glass px-4 py-2">
          <span className="text-sm text-white/70">
            Agent processing:{" "}
            <span className="text-white">{state.pipeline_stage}</span>
          </span>
        </div>
      );
    },
  });

  const isProcessing = !!state?.pipeline_stage && !state?.strategic_report;
  const pipelineStarted = !!state?.target_location || !!state?.pipeline_stage;
  const rec = state?.strategic_report?.top_recommendation;
  const coords = rec?.competition?.competitor_coordinates;

  /* Progressive data availability checks */
  const hasMarket = !!rec?.market;
  const hasCompetitor = !!rec?.competition;
  const hasReport = !!state?.strategic_report;
  const hasAlternatives = (state?.strategic_report?.alternative_locations?.length ?? 0) > 0;

  return (
    <div className="transition-opacity duration-300 min-h-screen">
      {isProcessing && (
        <style dangerouslySetInnerHTML={{
          __html: `
            .copilotKitInput, [data-copilotkit-chat-input] { pointer-events: none !important; opacity: 0.6 !important; }
            .copilotKitButton { pointer-events: none !important; opacity: 0.6 !important; }
          `
        }} />
      )}
      <CopilotSidebar
        defaultOpen={false}
        clickOutsideToClose={true}
        labels={{
          title: AGENT_CONFIG.productName,
          initial: `Welcome to **${AGENT_CONFIG.productName}**.

I am your AI-powered location intelligence system.

Provide your **business idea** and **geographic region clearly** and I will analyze the demand dynamics, the competitive landscape and the location viability to deliver strategic recommendations.
<br />
**A fully structured HTML report will be delivered at the end of the analysis**.

**Try examples:**
- "Coworking space in Viman Nagar, Pune" 
- "Coffee shop in Park Street, Kolkata"
- "Analyze Manhattan for a fitness studio"
- "Best bakery location in Berlin"

⚠️ **IMPORTANT**: Once your query is confirmed, you can **close this sidebar** using the **X** button (top-right) to instantly view the **full-screen interactive report** updating live
`,
        }}
      >
        <main className="min-h-screen relative z-10">
          <div className="max-w-[1440px] mx-auto px-5 py-6 lg:px-8">

            {/* ===== HEADER — Original glassmorphic style ===== */}
            <header className="mb-8 animate-fade-in">
              <div className="flex items-end justify-between gap-4">
                <div>
                  <h1 className="text-5xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-indigo-100 to-cyan-600">
                    {AGENT_CONFIG.productName}
                  </h1>
                  <p className="text-slate-600 text-lg">
                    {AGENT_CONFIG.tagline}
                    <span className="mx-2 text-slate-300">|</span>
                    A product by{" "}
                    <span className="font-medium text-slate-600">
                      {AGENT_CONFIG.company}
                    </span>
                  </p>
                </div>
                <AgentStatus stage={state?.pipeline_stage} />
              </div>
            </header>

            {/* ===== ACTIVE PIPELINE — shown as soon as target_location is set ===== */}
            {pipelineStarted && (
              <>
                {/* Pipeline Timeline */}
                <div className="mb-6 animate-slide-up">
                  <PipelineTimeline
                    state={state}
                    currentStage={state.pipeline_stage}
                    completedStages={state.stages_completed || []}
                  />
                </div>

                {/* ── Two-Column Dashboard: Market (63%) | Competitor (37%) ── */}
                {/* Shows immediately — cards appear progressively as data arrives */}
                <div className="grid grid-cols-1 lg:grid-cols-[63%_1fr] gap-6 mb-6">
                  {/* Left Column — Market Intelligence */}
                  <div className="space-y-6">
                    {hasMarket ? (
                      <MarketCard market={rec!.market} />
                    ) : (
                      <SkeletonCard
                        icon="📈"
                        title="Market Intelligence"
                        accent="teal"
                        message={
                          state?.stages_completed?.includes("gap_analysis")
                            ? "Synthesizing market data..."
                            : state?.stages_completed?.includes("market_research")
                              ? "Market research complete — awaiting analysis..."
                              : "Collecting market data..."
                        }
                      />
                    )}
                  </div>

                  {/* Right Column — Competitor Profile */}
                  <div className="space-y-6">
                    {hasCompetitor ? (
                      <CompetitorCard competition={rec!.competition} />
                    ) : (
                      <SkeletonCard
                        icon="⚔️"
                        title="Competition Profile"
                        accent="coral"
                        message={
                          state?.stages_completed?.includes("competitor_mapping")
                            ? "Competitor data collected — awaiting synthesis..."
                            : "Mapping competitors..."
                        }
                      />
                    )}
                  </div>
                </div>

                {/* ── Map — separate full-width card ── */}
                {coords && coords.length > 0 && (
                  <div className="mb-6 animate-fade-in delay-1">
                    <StaticMapCard coordinates={coords} />
                  </div>
                )}

                {/* ── Hero Report — shows after strategy synthesis ── */}
                {hasReport && (
                  <div className="mb-6 animate-slide-up delay-1">
                    <LocationReport report={state.strategic_report!} />
                  </div>
                )}

                {/* ── Alternative Locations ── */}
                {hasAlternatives && (
                  <div className="mb-6 animate-fade-in delay-2">
                    <AlternativeLocations
                      locations={state.strategic_report!.alternative_locations}
                    />
                  </div>
                )}

                {/* ── HTML Report Viewer ── */}
                {state.html_report_content && (
                  <div className="mb-6 animate-fade-in delay-3">
                    <ArtifactViewer htmlReport={state.html_report_content} />
                  </div>
                )}
              </>
            )}

            {/* ===== WELCOME STATE — shown when no pipeline is active ===== */}
            {!pipelineStarted && (
              <div className="glass p-14 text-center mt-12 animate-fade-in">
                <div className="text-7xl mb-6">🌍</div>
                <h2 className="text-3xl font-semibold text-slate-500 mb-4">
                  Discover the Optimal Location for your Business
                </h2>
                <p className="text-slate-700 max-w-xl mx-auto mb-10 text-lg leading-relaxed text-center">
                  Enter your business idea and city in the chat to receive
                  AI-driven market research, competitor analysis and
                  strategic recommendations.
                  <br />
                  <span className="mt-2 inline-block text-slate-500 text-base">
                    To begin, click the <span className="font-medium text-slate-700">💬 chat bubble</span> in the lower-right corner.
                  </span>
                </p>

                <div className="grid md:grid-cols-3 gap-6 max-w-3xl mx-auto">
                  <FeatureCard icon="🔍" title="Market Research" description="Live analysis of demand and demographics" />
                  <FeatureCard icon="📍" title="Competitor Mapping" description="Real-world competitor intelligence" />
                  <FeatureCard icon="🧠" title="AI Strategy" description="Deep reasoning and decision synthesis" />
                </div>
              </div>
            )}
          </div>
        </main>
      </CopilotSidebar>
    </div>
  );
}

/* ── Skeleton placeholder card shown while data loads ── */
function SkeletonCard({ icon, title, accent, message }: {
  icon: string; title: string; accent: string; message: string;
}) {
  const accentClass = accent === "teal" ? "card-teal" : "card-coral";
  return (
    <div className={`card ${accentClass} animate-fade-in`}>
      <div className="flex items-center gap-2 mb-4">
        <span className="text-lg">{icon}</span>
        <h3 className="font-bold text-slate-900">{title}</h3>
      </div>
      <div className="space-y-3">
        <div className="h-3 bg-slate-200/60 rounded-full w-3/4 animate-pulse" />
        <div className="h-3 bg-slate-200/40 rounded-full w-1/2 animate-pulse delay-1" />
        <div className="h-3 bg-slate-200/30 rounded-full w-2/3 animate-pulse delay-2" />
      </div>
      <p className="text-xs text-slate-400 mt-4 flex items-center gap-1.5">
        <span className="w-1.5 h-1.5 bg-teal-400 rounded-full animate-pulse" />
        {message}
      </p>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: string; title: string; description: string }) {
  return (
    <div className="glass p-5 text-left transition-all hover:-translate-y-1">
      <div className="text-2xl mb-2">{icon}</div>
      <h3 className="font-medium text-slate-900 mb-1">{title}</h3>
      <p className="text-sm text-slate-600 leading-relaxed">{description}</p>
    </div>
  );
}
