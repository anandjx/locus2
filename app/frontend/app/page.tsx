"use client";

import Link from "next/link";
import { CopilotSidebar } from "@copilotkit/react-ui";
import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";

import { PipelineTimeline } from "@/components/PipelineTimeline";
import { LocationReport } from "@/components/LocationReport";
import { AlternativeLocations } from "@/components/AlternativeLocations";
import { ArtifactViewer } from "@/components/ArtifactViewer";
import { AgentStatus } from "@/components/AgentStatus";

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
  const hasReport = !!state?.strategic_report;
  const hasAlternatives = (state?.strategic_report?.alternative_locations?.length ?? 0) > 0;

  return (
    <div className="transition-opacity duration-300 min-h-screen flex flex-col">
      {/* Chat disclaimer injected via CSS */}
      <style dangerouslySetInnerHTML={{
        __html: `
          ${isProcessing ? '.copilotKitInput, [data-copilotkit-chat-input] { pointer-events: none !important; opacity: 0.6 !important; } .copilotKitButton { pointer-events: none !important; opacity: 0.6 !important; }' : ''}
          .copilotKitMessages::after {
            content: 'AI-generated strategy. Verify all results before asset deployment. Not professional real estate advice.';
            display: block;
            padding: 6px 16px;
            font-size: 10px;
            font-style: italic;
            color: rgba(100, 116, 139, 0.6);
            text-align: center;
            line-height: 1.4;
          }
        `
      }} />
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

**Examples:**
- "Coworking space in Viman Nagar, Pune" 
- "Analyze Manhattan for a fitness studio"  
- "Coffee shop in Park Street, Kolkata"  
- "Best bakery location in Berlin"  

It usually takes about **3 minutes to 5 minutes** after confirmation of the location and business idea by Locus, for the **analysis to begin and generate the report**.

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
                  <h1 className="text-7xl font-black bg-clip-text text-transparent bg-gradient-to-r from-indigo-100 to-cyan-600">
                    {AGENT_CONFIG.productName}
                  </h1>
                  <p className="text-slate-600 text-lg">
                    {AGENT_CONFIG.tagline}
                    <span className="mx-2 text-slate-100">|</span>
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
                  Enter your business idea and precise location with city name in the chat to receive
                  AI-driven deep market research, competitor analysis
                  and strategic recommendations.
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

        {/* ===== GLOBAL FOOTER — Legal & Compliance ===== */}
        <footer className="mt-auto border-t border-slate-100/60 bg-white/40 backdrop-blur-sm">
          <div className="max-w-[1440px] mx-auto px-5 py-4 lg:px-8 flex items-center justify-between gap-4 flex-wrap">
            <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
              <span>© {new Date().getFullYear()} Intsemble</span>
              <span className="text-slate-200">·</span>
              <Link href="/terms" target="_blank" rel="noopener noreferrer" className="hover:text-slate-600 transition-colors underline-offset-2 hover:underline">
                Terms
              </Link>
              <span className="text-slate-200">·</span>
              <Link href="/privacy" target="_blank" rel="noopener noreferrer" className="hover:text-slate-600 transition-colors underline-offset-2 hover:underline">
                Privacy
              </Link>
            </div>
            <p className="text-[9px] text-slate-300 font-medium tracking-wide">
              Powered by Google Maps Platform
            </p>
          </div>
        </footer>
      </CopilotSidebar>
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
