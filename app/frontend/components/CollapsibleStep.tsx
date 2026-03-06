"use client";

import { memo } from "react";
import type { TimelineStepConfig } from "@/lib/types";

/* ── Per-step accent color map ── */
const ACCENT_STYLES: Record<string, {
  complete: { border: string; bg: string; badge: string; text: string };
}> = {
  sky: { complete: { border: "border-l-sky-400", bg: "bg-sky-50/30", badge: "bg-sky-500 text-white", text: "text-sky-700" } },
  teal: { complete: { border: "border-l-teal-400", bg: "bg-teal-50/30", badge: "bg-teal-500 text-white", text: "text-teal-700" } },
  coral: { complete: { border: "border-l-orange-400", bg: "bg-orange-50/30", badge: "bg-orange-500 text-white", text: "text-orange-700" } },
  rose: { complete: { border: "border-l-rose-400", bg: "bg-rose-50/30", badge: "bg-rose-500 text-white", text: "text-rose-700" } },
  lavender: { complete: { border: "border-l-violet-400", bg: "bg-violet-50/30", badge: "bg-violet-500 text-white", text: "text-violet-700" } },
  indigo: { complete: { border: "border-l-indigo-400", bg: "bg-indigo-50/30", badge: "bg-indigo-500 text-white", text: "text-indigo-700" } },
};

interface CollapsibleStepProps {
  step: TimelineStepConfig;
  stepNumber: number;
  status: "pending" | "in_progress" | "complete";
  accent: string;
  children: React.ReactNode;
  isExpanded: boolean;
  onToggle: () => void;
}

export const CollapsibleStep = memo(function CollapsibleStep({
  step, stepNumber, status, accent, children, isExpanded, onToggle,
}: CollapsibleStepProps) {

  const accentStyle = ACCENT_STYLES[accent] || ACCENT_STYLES.sky;

  const styles = status === "complete" ? {
    container: `border-l-[3px] ${accentStyle.complete.border} ${accentStyle.complete.bg} border border-slate-100/80`,
    badge: accentStyle.complete.badge,
    badgeContent: "✓",
    textColor: accentStyle.complete.text,
  } : status === "in_progress" ? {
    container: "border-l-[3px] border-l-amber-400 bg-amber-50/30 border border-amber-100",
    badge: "bg-amber-500 text-white",
    badgeContent: stepNumber.toString(),
    textColor: "text-amber-700",
  } : {
    container: "border-l-[3px] border-l-slate-200 bg-slate-50/20 border border-slate-100",
    badge: "bg-slate-200 text-slate-500",
    badgeContent: stepNumber.toString(),
    textColor: "text-slate-500",
  };

  const canToggle = status === "complete";

  return (
    <div className={`rounded-2xl transition-all duration-300 ${styles.container}`}>
      {/* Header */}
      <div
        className={`flex items-center gap-3 px-4 py-3 ${canToggle ? "cursor-pointer select-none" : ""}`}
        onClick={canToggle ? onToggle : undefined}
      >
        <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-xs font-semibold flex-shrink-0 ${styles.badge}`}>
          {styles.badgeContent}
        </div>

        <span className={`font-medium flex-1 text-sm ${styles.textColor}`}>
          {step.label}
        </span>

        {step.tool && (
          <span className="px-2 py-0.5 bg-white/80 border border-slate-100 text-slate-500 text-[10px] font-mono rounded-md flex items-center gap-1">
            <span>{step.tool.icon}</span>
            <span>{step.tool.name}</span>
          </span>
        )}

        {status === "in_progress" && (
          <span className="text-[10px] text-amber-600 font-semibold flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-amber-500 rounded-full animate-pulse" />
            Running
          </span>
        )}

        {canToggle && (
          <svg
            className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${isExpanded ? "rotate-180" : ""}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        )}
      </div>

      {/* Content */}
      <div className={`overflow-hidden transition-all duration-300 ease-in-out ${isExpanded && status !== "pending" ? "max-h-[80rem] opacity-100" : "max-h-0 opacity-0"
        }`}>
        <div className="px-4 pb-4 ml-10">
          <div className="border-l-2 border-slate-200/40 pl-4 text-sm">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
});