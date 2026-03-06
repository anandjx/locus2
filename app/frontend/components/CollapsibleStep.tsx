"use client";

import { memo } from "react";
import type { TimelineStepConfig } from "@/lib/types";

/* ── Per-step accent color map ──
   Parsed=blue, Market=emerald, Competitors=orange,
   Gap=purple, Strategy=rose, Report=indigo           */
const ACCENT_STYLES: Record<string, {
  complete: { border: string; bg: string; badge: string; text: string; shadow: string; gradient: string };
}> = {
  blue: {
    complete: {
      border: "border-l-blue-400",
      bg: "bg-blue-50/25",
      badge: "bg-blue-500 text-white",
      text: "text-blue-700",
      shadow: "shadow-[0_2px_12px_rgba(59,130,246,0.08)]",
      gradient: "from-blue-50/40 to-white/80",
    },
  },
  emerald: {
    complete: {
      border: "border-l-emerald-400",
      bg: "bg-emerald-50/25",
      badge: "bg-emerald-500 text-white",
      text: "text-emerald-700",
      shadow: "shadow-[0_2px_12px_rgba(16,185,129,0.08)]",
      gradient: "from-emerald-50/40 to-white/80",
    },
  },
  orange: {
    complete: {
      border: "border-l-orange-400",
      bg: "bg-orange-50/25",
      badge: "bg-orange-500 text-white",
      text: "text-orange-700",
      shadow: "shadow-[0_2px_12px_rgba(249,115,22,0.08)]",
      gradient: "from-orange-50/40 to-white/80",
    },
  },
  purple: {
    complete: {
      border: "border-l-purple-400",
      bg: "bg-purple-50/25",
      badge: "bg-purple-500 text-white",
      text: "text-purple-700",
      shadow: "shadow-[0_2px_12px_rgba(168,85,247,0.08)]",
      gradient: "from-purple-50/40 to-white/80",
    },
  },
  rose: {
    complete: {
      border: "border-l-rose-400",
      bg: "bg-rose-50/25",
      badge: "bg-rose-500 text-white",
      text: "text-rose-700",
      shadow: "shadow-[0_2px_12px_rgba(244,63,94,0.08)]",
      gradient: "from-rose-50/40 to-white/80",
    },
  },
  indigo: {
    complete: {
      border: "border-l-indigo-400",
      bg: "bg-indigo-50/25",
      badge: "bg-indigo-500 text-white",
      text: "text-indigo-700",
      shadow: "shadow-[0_2px_12px_rgba(99,102,241,0.08)]",
      gradient: "from-indigo-50/40 to-white/80",
    },
  },
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

  const accentStyle = ACCENT_STYLES[accent] || ACCENT_STYLES.blue;

  const styles = status === "complete" ? {
    container: `border-l-4 ${accentStyle.complete.border} ${accentStyle.complete.bg} border border-slate-100/60 ${accentStyle.complete.shadow} bg-gradient-to-br ${accentStyle.complete.gradient}`,
    badge: accentStyle.complete.badge,
    badgeContent: "✓",
    textColor: accentStyle.complete.text,
  } : status === "in_progress" ? {
    container: "border-l-4 border-l-amber-400 bg-gradient-to-br from-amber-50/30 to-white/80 border border-amber-100/60 shadow-[0_2px_12px_rgba(245,158,11,0.08)]",
    badge: "bg-amber-500 text-white",
    badgeContent: stepNumber.toString(),
    textColor: "text-amber-700",
  } : {
    container: "border-l-4 border-l-slate-200 bg-gradient-to-br from-slate-50/20 to-white/60 border border-slate-100/60",
    badge: "bg-slate-200 text-slate-500",
    badgeContent: stepNumber.toString(),
    textColor: "text-slate-500",
  };

  const canToggle = status === "complete" || status === "in_progress";

  return (
    <div className={`rounded-2xl transition-all duration-300 hover:shadow-md ${styles.container}`}>
      {/* Header */}
      <div
        className={`flex items-center gap-3 px-5 py-3.5 ${canToggle ? "cursor-pointer select-none" : ""}`}
        onClick={canToggle ? onToggle : undefined}
      >
        <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold flex-shrink-0 shadow-sm ${styles.badge}`}>
          {styles.badgeContent}
        </div>

        <span className={`font-semibold flex-1 text-sm ${styles.textColor}`}>
          {step.label}
        </span>

        {step.tool && (
          <span className="px-2.5 py-1 bg-white/90 border border-slate-100/80 text-slate-500 text-[10px] font-mono rounded-lg flex items-center gap-1 shadow-sm">
            <span>{step.tool.icon}</span>
            <span>{step.tool.name}</span>
          </span>
        )}

        {status === "in_progress" && (
          <span className="text-[10px] text-amber-600 font-bold flex items-center gap-1.5">
            <span className="w-2 h-2 bg-amber-500 rounded-full animate-pulse" />
            Running
          </span>
        )}

        {canToggle && (
          <svg
            className={`w-4 h-4 text-slate-400 transition-transform duration-300 ${isExpanded ? "rotate-180" : ""}`}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        )}
      </div>

      {/* Content — no artificial height constraints, grows naturally */}
      <div className={`overflow-hidden transition-all duration-400 ease-in-out ${isExpanded && status !== "pending" ? "max-h-[200rem] opacity-100" : "max-h-0 opacity-0"
        }`}>
        <div className="px-5 pb-5">
          <div className="text-sm leading-relaxed">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
});