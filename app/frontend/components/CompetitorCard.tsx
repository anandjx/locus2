import type { CompetitionProfile } from "@/lib/types";

interface CompetitorCardProps {
  competition: CompetitionProfile;
}

export function CompetitorCard({ competition }: CompetitorCardProps) {
  if (!competition) return null;

  const cci = competition?.concentration_index_cci ?? 0;
  const reqDailyCustomers = competition?.req_daily_customers ?? 0;
  const feasibilityNote = competition?.feasibility_note ?? "Pending";

  const isMonopoly = cci >= 0.8;
  const isFragmented = cci <= 0.4;
  const structureLabel = isMonopoly ? "Oligopoly" : isFragmented ? "Fragmented" : "Balanced";
  const structureBadge = isMonopoly
    ? "text-rose-700 bg-rose-50 border-rose-200"
    : isFragmented ? "text-emerald-700 bg-emerald-50 border-emerald-200"
      : "text-amber-700 bg-amber-50 border-amber-200";

  const isDemandDeficit = reqDailyCustomers > 130;

  return (
    <div className="card card-coral animate-fade-in delay-1">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          <span className="text-lg">⚔️</span> Competition Profile
        </h3>
        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${structureBadge}`}>
          {structureLabel}
        </span>
      </div>

      {/* Module 1: Market Power */}
      <div className="mb-5 p-4 rounded-2xl bg-gradient-to-br from-orange-50/60 to-amber-50/30 border border-orange-100/60">
        <h4 className="section-title text-orange-600 mb-3">🥧 Market Power</h4>
        <div className="grid grid-cols-2 gap-2.5">
          <Stat label="CCI" value={`${(cci * 100).toFixed(0)}%`} sub="Top 2 Share" />
          <Stat label="Chains" value={`${(competition.chain_dominance_pct ?? 0).toFixed(0)}%`} sub="Chain Share" />
        </div>
      </div>

      {/* Module 2: Competitor Landscape */}
      <div className="mb-5 p-4 rounded-2xl bg-gradient-to-br from-slate-50/80 to-white border border-slate-100">
        <h4 className="section-title text-slate-500 mb-3">📊 Landscape</h4>
        <div className="grid grid-cols-2 gap-2.5">
          <Stat label="Total" value={(competition.total_competitors ?? 0).toString()} />
          <Stat label="High Perf." value={(competition.high_performers_count ?? 0).toString()} sub="4.5+ ⭐" />
          <Stat label="Avg Rating" value={(competition.avg_competitor_rating ?? 0).toFixed(1)} />
          <Stat label="Break-Even" value={reqDailyCustomers.toString()} sub="daily cust." alert={isDemandDeficit} />
        </div>
      </div>

      {/* Module 3: Feasibility */}
      <div className={`p-4 rounded-2xl border ${isDemandDeficit ? "bg-gradient-to-br from-rose-50/60 to-red-50/30 border-rose-100/60" : "bg-gradient-to-br from-emerald-50/50 to-green-50/30 border-emerald-100/50"}`}>
        <h4 className={`section-title mb-2 ${isDemandDeficit ? "text-rose-600" : "text-emerald-600"}`}>
          {isDemandDeficit ? "⚠️" : "✅"} Feasibility Assessment
        </h4>
        <p className={`text-xs leading-relaxed ${isDemandDeficit ? "text-rose-800" : "text-emerald-800"}`}>
          {feasibilityNote}
        </p>
      </div>
    </div>
  );
}

function Stat({ label, value, sub, alert }: {
  label: string; value: string; sub?: string; alert?: boolean;
}) {
  return (
    <div className={`metric-card ${alert ? "!bg-rose-50 !border-rose-200" : ""}`}>
      <div className={`text-lg font-extrabold ${alert ? "metric-value-danger" : "metric-value-coral"}`}>{value}</div>
      <div className="text-[10px] font-semibold text-slate-500 mt-0.5">{label}</div>
      {sub && <div className={`text-[9px] mt-0.5 ${alert ? "text-rose-500 font-semibold" : "text-slate-400"}`}>{sub}</div>}
    </div>
  );
}