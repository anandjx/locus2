"use client";

import { useState, useCallback } from "react";
import type { AgentState, TimelineStepConfig, CollapsedSteps } from "@/lib/types";
import { CollapsibleStep } from "./CollapsibleStep";
import { StepOutputContent } from "./StepOutputContent";

/* Each step gets a unique accent color for its completed state */
const TIMELINE_STEPS: (TimelineStepConfig & { accent: string })[] = [
  { id: "intake", label: "Parsed", stageKey: "intake", tool: null, accent: "sky" },
  { id: "market_research", label: "Market", stageKey: "market_research", tool: { icon: "🔍", name: "google_search" }, accent: "teal" },
  { id: "competitor_mapping", label: "Competitors", stageKey: "competitor_mapping", tool: { icon: "📍", name: "search_places" }, accent: "coral" },
  { id: "gap_analysis", label: "Gap", stageKey: "gap_analysis", tool: { icon: "🐍", name: "python_code" }, accent: "rose" },
  { id: "strategy_synthesis", label: "Strategy", stageKey: "strategy_synthesis", tool: { icon: "🧠", name: "deep_thinking" }, accent: "lavender" },
  { id: "report_generation", label: "Report", stageKey: "report_generation", tool: { icon: "📄", name: "html_report" }, accent: "indigo" },
];

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

      {/* ── Collapsible Step Details ── */}
      <div className="p-4 space-y-3">
        {TIMELINE_STEPS.map((step, index) => {
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

          if (!shouldShow) return null;

          const actualStatus = step.id === "intake" && showIntake ? "complete" : status;
          const isExpanded = actualStatus === "in_progress" || !collapsed[step.id];

          return (
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
          );
        })}
      </div>

      {/* All Complete */}
      {completedCount === TIMELINE_STEPS.length && (
        <div className="px-5 py-3 bg-gradient-to-r from-indigo-50/50 to-sky-50/30 border-t border-sky-100/50">
          <div className="flex items-center justify-center gap-2 text-indigo-700 text-sm font-medium">
            <span>✅</span>
            <span>Analysis Complete — scroll down for the full dashboard</span>
          </div>
        </div>
      )}
    </div>
  );
}