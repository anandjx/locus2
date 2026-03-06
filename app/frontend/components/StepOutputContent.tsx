"use client";

import type { AgentState } from "@/lib/types";
import {
  summarizeCompetitorAnalysis,
} from "@/lib/summaryHelpers";
import { ScrollableMarkdown } from "./ScrollableMarkdown";
import { TabbedGapAnalysis } from "./TabbedGapAnalysis";
import { LocationReport } from "./LocationReport";

interface StepOutputContentProps {
  stepId: string;
  state: AgentState;
}

/**
 * Renders the appropriate output content for each pipeline step.
 * This component handles the different output types per stage.
 */
export function StepOutputContent({ stepId, state }: StepOutputContentProps) {
  switch (stepId) {
    case "intake":
      return (
        <p className="text-gray-600 text-sm">
          Analyzing <span className="font-medium text-gray-900">{state.business_type}</span> locations in{" "}
          <span className="font-medium text-gray-900">{state.target_location}</span>
          {state.additional_context && (
            <span className="text-gray-500 ml-1">({state.additional_context})</span>
          )}
        </p>
      );

    case "market_research":
      return (
        <ScrollableMarkdown
          content={state.market_research_findings || ""}
          maxHeight="40rem"
        />
      );

    case "competitor_mapping":
      // Show summary stats at top, then full content if available
      const summary = summarizeCompetitorAnalysis(state.competitor_analysis, state.strategic_report);
      return (
        <div className="space-y-2">
          <p className="text-gray-700 text-sm font-medium">{summary}</p>
          {state.competitor_analysis && (
            <ScrollableMarkdown
              content={state.competitor_analysis}
              maxHeight="36rem"
            />
          )}
        </div>
      );

    case "gap_analysis":
      return (
        <TabbedGapAnalysis
          content={state.gap_analysis || ""}
          code={state.gap_analysis_code}
        />
      );

    case "strategy_synthesis":
      if (!state.strategic_report) {
        return <p className="text-gray-500 text-sm italic">Synthesizing strategy...</p>;
      }
      return <LocationReport report={state.strategic_report} />;

    case "report_generation":
      if (!state.html_report_content) {
        return <p className="text-gray-500 text-sm italic">Generating report...</p>;
      }
      return (
        <div className="flex items-center gap-3">
          <span className="text-sm text-green-700">7-slide McKinsey-style presentation ready</span>
          <div className="flex gap-2">
            <button
              onClick={() => {
                const blob = new Blob([state.html_report_content!], { type: "text/html" });
                const url = URL.createObjectURL(blob);
                window.open(url, "_blank");
              }}
              className="px-3 py-1 text-xs bg-blue-500 text-white/90 rounded hover:bg-blue-600 transition-colors"
            >
              View Report
            </button>
            <button
              onClick={() => {
                const blob = new Blob([state.html_report_content!], { type: "text/html" });
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "executive_report.html";
                a.click();
                URL.revokeObjectURL(url);
              }}
              className="px-3 py-1 text-xs bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors"
            >
              Download HTML
            </button>
          </div>
        </div>
      );

    default:
      return null;
  }
}