import type { ReportDisplayProps } from "@/lib/types";

export function LocationReport({ report }: ReportDisplayProps) {
  const rec = report.top_recommendation;
  const scoreBg =
    rec.overall_score >= 75 ? "from-emerald-500 to-green-600"
      : rec.overall_score >= 50 ? "from-amber-500 to-orange-500"
        : "from-red-500 to-rose-600";

  return (
    <div className="card card-sky overflow-hidden animate-fade-in">
      {/* Hero Header */}
      <div className="p-5 bg-gradient-to-r from-sky-50/60 to-white border-b border-sky-100/50 -mx-5 -mt-5 mb-5 px-5 pt-5">
        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2.5 mb-1">
              <span className="text-xl">📍</span>
              <h2 className="text-xl font-bold text-slate-900">{rec.location_name}</h2>
            </div>
            <p className="text-slate-500 text-sm">{rec.area}</p>
            {rec.opportunity_type && (
              <span className="inline-block mt-2 px-2.5 py-0.5 bg-sky-50 text-sky-700 rounded-full text-[10px] font-bold border border-sky-200">
                {rec.opportunity_type}
              </span>
            )}
          </div>
          <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${scoreBg} flex flex-col items-center justify-center text-white shadow-lg animate-ring-pulse`}>
            <div className="text-2xl font-extrabold leading-none">{rec.overall_score}</div>
            <div className="text-[9px] opacity-70">/100</div>
          </div>
        </div>

        {/* Quick Info */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          <div className="metric-card">
            <div className="text-[10px] text-slate-400">👥 Target Segment</div>
            <div className="text-xs font-semibold text-slate-700 mt-0.5 truncate">{rec.best_customer_segment || "—"}</div>
          </div>
          <div className="metric-card">
            <div className="text-[10px] text-slate-400">🚶 Foot Traffic</div>
            <div className="text-xs font-semibold text-slate-700 mt-0.5 truncate">{rec.estimated_foot_traffic || "—"}</div>
          </div>
        </div>
      </div>

      {/* Strengths & Concerns — side by side */}
      <div className="grid md:grid-cols-2 gap-5 mb-5">
        {/* Strengths Module */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-emerald-50/60 to-green-50/30 border border-emerald-100/60">
          <h4 className="section-title text-emerald-600 mb-3">💪 Strengths</h4>
          <div className="space-y-2">
            {rec.strengths.map((s: any, i: number) => (
              <div key={i} className="p-2.5 bg-white/70 rounded-xl border border-emerald-100/50">
                <div className="font-semibold text-emerald-800 text-xs flex items-center gap-1.5">
                  <span className="w-4 h-4 bg-emerald-500 text-white rounded flex items-center justify-center text-[8px] flex-shrink-0">✓</span>
                  {s.factor}
                </div>
                <p className="text-[10px] text-slate-600 mt-1 leading-relaxed">{s.description}</p>
                {s.evidence_from_analysis && (
                  <p className="text-[9px] text-slate-400 mt-1 italic">📎 {s.evidence_from_analysis}</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Concerns Module */}
        <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-50/60 to-orange-50/30 border border-amber-100/60">
          <h4 className="section-title text-amber-600 mb-3">⚠️ Concerns & Mitigations</h4>
          <div className="space-y-2">
            {rec.concerns.map((c: any, i: number) => (
              <div key={i} className="p-2.5 bg-white/70 rounded-xl border border-amber-100/50">
                <div className="font-semibold text-amber-800 text-xs flex items-center gap-1.5">
                  <span className="w-4 h-4 bg-amber-500 text-white rounded flex items-center justify-center text-[8px] flex-shrink-0">!</span>
                  {c.risk}
                </div>
                <p className="text-[10px] text-slate-600 mt-1 leading-relaxed">{c.description}</p>
                <div className="mt-1.5 p-1.5 bg-white/80 rounded-lg border border-amber-100/50">
                  <p className="text-[9px] text-slate-700">
                    <span className="font-bold text-amber-700">Mitigation:</span> {c.mitigation_strategy}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Next Steps Module */}
      {rec.next_steps && rec.next_steps.length > 0 && (
        <div className="p-4 rounded-2xl bg-gradient-to-br from-indigo-50/50 to-violet-50/30 border border-indigo-100/50">
          <h4 className="section-title text-indigo-600 mb-3">🎯 Recommended Next Steps</h4>
          <ol className="space-y-1.5">
            {rec.next_steps.map((step: string, i: number) => (
              <li key={i} className="flex items-start gap-2.5 text-slate-700 text-xs">
                <span className="w-5 h-5 bg-indigo-100 text-indigo-700 rounded-lg flex items-center justify-center text-[10px] font-bold flex-shrink-0">
                  {i + 1}
                </span>
                <span className="leading-relaxed">{step}</span>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}