"use client";

import { useState, useCallback } from "react";
import type { AgentState, TimelineStepConfig, CollapsedSteps } from "@/lib/types";
import { CollapsibleStep } from "./CollapsibleStep";
import { StepOutputContent } from "./StepOutputContent";
import { StaticMapCard } from "./StaticMapCard";

/* Each step gets a unique accent color matching the CollapsibleStep color map */
const TIMELINE_STEPS: (TimelineStepConfig & { accent: string })[] = [
  { id: "intake", label: "Parsed", stageKey: "intake", tool: null, accent: "blue" },
  { id: "market_research", label: "Market", stageKey: "market_research", tool: { icon: "🔍", name: "google_search" }, accent: "emerald" },
  { id: "competitor_mapping", label: "Competitors", stageKey: "competitor_mapping", tool: { icon: "📍", name: "search_places" }, accent: "orange" },
  { id: "gap_analysis", label: "Gap", stageKey: "gap_analysis", tool: { icon: "🐍", name: "python_code" }, accent: "purple" },
  { id: "strategy_synthesis", label: "Strategy", stageKey: "strategy_synthesis", tool: { icon: "🧠", name: "deep_thinking" }, accent: "rose" },
  { id: "report_generation", label: "Report", stageKey: "report_generation", tool: { icon: "📄", name: "html_report" }, accent: "indigo" },
];

/* Steps that render side-by-side in 63/37 columns */
const SIDE_BY_SIDE_IDS = new Set(["market_research", "competitor_mapping"]);

interface PipelineTimelineProps {
  state: AgentState;
  currentStage?: string;
  completedStages: string[];
}

export function PipelineTimeline({ state, currentStage, completedStages }: PipelineTimelineProps) {
  const [collapsed, setCollapsed] = useState<CollapsedSteps>({});
  const toggleStep = useCallback((stepId: string) => {
    setCollapsed((prev) => ({ ...prev, [stepId]: !prev[stepId] }));
  }, []);

  const getStepStatus = useCallback(
    (step: TimelineStepConfig): "pending" | "in_progress" | "complete" => {
      if (completedStages.includes(step.stageKey)) return "complete";
      if (currentStage === step.stageKey || currentStage === step.id) return "in_progress";
      return "pending";
    },
    [completedStages, currentStage]
  );

  const completedCount = completedStages.length;
  const showIntake = Boolean(state.target_location);

  /* Pre-compute visibility and status for all steps */
  const stepData = TIMELINE_STEPS.map((step, index) => {
    const status = getStepStatus(step);
    const shouldShow =
      step.id === "intake"
        ? showIntake
        : completedStages.includes(step.stageKey) ||
        currentStage === step.stageKey ||
        currentStage === step.id ||
        (status === "pending" && index > 0 &&
          (completedStages.includes(TIMELINE_STEPS[index - 1].stageKey) ||
            currentStage === TIMELINE_STEPS[index - 1].stageKey));
    const actualStatus = step.id === "intake" && showIntake ? "complete" : status;
    /* DEFAULT EXPANDED — collapsed[id] === true means user explicitly collapsed */
    const isExpanded = actualStatus === "in_progress" || collapsed[step.id] !== true;
    return { step, index, shouldShow, actualStatus, isExpanded };
  });

  /* Separate "before", "side-by-side", and "after" groups */
  const beforeSteps = stepData.filter(d => d.shouldShow && !SIDE_BY_SIDE_IDS.has(d.step.id) && d.index < 2);
  const marketStep = stepData.find(d => d.step.id === "market_research");
  const competitorStep = stepData.find(d => d.step.id === "competitor_mapping");
  const afterSteps = stepData.filter(d => d.shouldShow && !SIDE_BY_SIDE_IDS.has(d.step.id) && d.index >= 3);

  const showMarket = marketStep?.shouldShow;
  const showCompetitor = competitorStep?.shouldShow;
  const showSideBySide = showMarket || showCompetitor;

  /* Get map coordinates from strategic report */
  const coords = state?.strategic_report?.top_recommendation?.competition?.competitor_coordinates;

  return (
    <div className="card card-sky overflow-hidden">
      {/* ── Horizontal Pipeline Dots ── */}
      <div className="px-6 pt-5 pb-4 bg-gradient-to-r from-sky-50/40 to-white/80 border-b border-sky-100/50">
        <div className="flex items-center gap-3 mb-3">
          <span className="text-lg">📍</span>
          <div className="min-w-0">
            <h2 className="text-base font-semibold text-slate-900 capitalize truncate">
              {state.business_type || "Business"} in {state.target_location || "Location"}
            </h2>
          </div>
          <div className="ml-auto text-xs text-slate-400 font-medium whitespace-nowrap">
            {completedCount}/{TIMELINE_STEPS.length}
          </div>
        </div>

        <div className="flex items-center">
          {TIMELINE_STEPS.map((step, i) => {
            const st = step.id === "intake" && showIntake ? "complete" : getStepStatus(step);
            return (
              <div key={step.id} className="flex items-center flex-1 last:flex-none">
                <div className="flex flex-col items-center gap-1">
                  <div
                    className={`step-dot ${st === "complete" ? "step-dot-complete" : st === "in_progress" ? "step-dot-active" : ""}`}
                    title={step.label}
                  >
                    {st === "complete" ? "✓" : step.tool?.icon || (i + 1)}
                  </div>
                  <span className="text-[10px] font-medium text-slate-400 whitespace-nowrap">{step.label}</span>
                </div>
                {i < TIMELINE_STEPS.length - 1 && (
                  <div className={`step-connector ${st === "complete" ? "step-connector-done" : ""}`} />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Step Details — increased spacing between cards ── */}
      <div className="p-5 space-y-5">

        {/* 1) Before steps (Parsed/Intake) — full width */}
        {beforeSteps.map(({ step, index, actualStatus, isExpanded }) => (
          <CollapsibleStep
            key={step.id}
            step={step}
            stepNumber={index + 1}
            status={actualStatus}
            accent={step.accent}
            isExpanded={isExpanded}
            onToggle={() => toggleStep(step.id)}
          >
            <StepOutputContent stepId={step.id} state={state} />
          </CollapsibleStep>
        ))}

        {/* 2) Market + Competitors — SIDE BY SIDE 63/37 with breathing room */}
        {showSideBySide && (
          <div className="grid gap-5" style={{ gridTemplateColumns: '63% 1fr' }}>
            {/* Left: Market (63%) */}
            <div className="min-w-0">
              {showMarket && marketStep && (
                <CollapsibleStep
                  step={marketStep.step}
                  stepNumber={2}
                  status={marketStep.actualStatus}
                  accent={marketStep.step.accent}
                  isExpanded={marketStep.isExpanded}
                  onToggle={() => toggleStep(marketStep.step.id)}
                >
                  <StepOutputContent stepId={marketStep.step.id} state={state} />
                </CollapsibleStep>
              )}
            </div>

            {/* Right: Competitors (37%) — min-w-0 + overflow-hidden for breathing room */}
            <div className="min-w-0 overflow-hidden">
              {showCompetitor && competitorStep && (
                <CollapsibleStep
                  step={competitorStep.step}
                  stepNumber={3}
                  status={competitorStep.actualStatus}
                  accent={competitorStep.step.accent}
                  isExpanded={competitorStep.isExpanded}
                  onToggle={() => toggleStep(competitorStep.step.id)}
                >
                  <StepOutputContent stepId={competitorStep.step.id} state={state} />
                </CollapsibleStep>
              )}
            </div>
          </div>
        )}

        {/* 3) Map — full width below Market + Competitors */}
        {coords && coords.length > 0 && (
          <StaticMapCard coordinates={coords} />
        )}

        {/* 4) Remaining steps (Gap, Strategy, Report) — full width */}
        {afterSteps.map(({ step, index, actualStatus, isExpanded }) => (
          <CollapsibleStep
            key={step.id}
            step={step}
            stepNumber={index + 1}
            status={actualStatus}
            accent={step.accent}
            isExpanded={isExpanded}
            onToggle={() => toggleStep(step.id)}
          >
            <StepOutputContent stepId={step.id} state={state} />
          </CollapsibleStep>
        ))}
      </div>

      {/* All Complete */}
      {completedCount === TIMELINE_STEPS.length && (
        <div className="px-5 py-3 bg-gradient-to-r from-indigo-50/50 to-sky-50/30 border-t border-sky-100/50">
          <div className="flex items-center justify-center gap-2 text-indigo-700 text-sm font-medium">
            <span>✅</span>
            <span>Analysis Complete</span>
          </div>
        </div>
      )}
    </div>
  );
}