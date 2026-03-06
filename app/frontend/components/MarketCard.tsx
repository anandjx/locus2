import type { MarketCharacteristics } from "@/lib/types";

interface MarketCardProps {
  market: MarketCharacteristics;
}

export function MarketCard({ market }: MarketCardProps) {
  if (!market) return null;

  const gap = market?.conversion_gap ?? 0;
  const ldi = market?.latent_demand_ldi ?? 0;
  const odi = market?.observed_demand_odi ?? 0;

  const isUnderserved = gap > 0.2;
  const isSaturated = gap < -0.1;
  const gapLabel = isUnderserved ? "Blue Ocean" : isSaturated ? "Red Ocean" : "Balanced";
  const gapBadge = isUnderserved
    ? "text-teal-700 bg-teal-50 border-teal-200"
    : isSaturated ? "text-rose-700 bg-rose-50 border-rose-200"
      : "text-amber-700 bg-amber-50 border-amber-200";

  return (
    <div className="card card-teal animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          <span className="text-lg">📈</span> Market Intelligence
        </h3>
        <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${gapBadge}`}>
          {gapLabel}
        </span>
      </div>

      {/* Module 1: Demand Indicators */}
      <div className="mb-5 p-4 rounded-2xl bg-gradient-to-br from-teal-50/60 to-cyan-50/40 border border-teal-100/60">
        <h4 className="section-title text-teal-600 mb-3">📊 Demand Indicators</h4>
        <div className="space-y-3">
          <BarIndicator label="Latent Demand (LDI)" value={ldi} color="bg-gradient-to-r from-teal-400 to-teal-600" />
          <BarIndicator label="Observed Demand (ODI)" value={odi} color="bg-gradient-to-r from-slate-300 to-slate-400" />
        </div>
        <div className="mt-3 pt-3 border-t border-teal-100/60 flex justify-between items-center">
          <span className="text-[10px] font-semibold text-teal-500 uppercase tracking-wider">Conversion Gap</span>
          <span className={`text-base font-extrabold ${gap > 0 ? "text-teal-600" : "text-rose-600"}`}>
            {gap > 0 ? "+" : ""}{gap.toFixed(2)}
          </span>
        </div>
      </div>

      {/* Module 2: Demographics */}
      <div className="mb-5 p-4 rounded-2xl bg-gradient-to-br from-slate-50/80 to-white border border-slate-100">
        <h4 className="section-title text-slate-500 mb-3">👥 Demographics</h4>
        <div className="space-y-0">
          <AttrRow label="Population" value={market?.population_density || "Pending"} />
          <AttrRow label="Income Level" value={market?.income_level || "Pending"} />
        </div>
      </div>

      {/* Module 3: Location Profile */}
      <div className="p-4 rounded-2xl bg-gradient-to-br from-sky-50/50 to-indigo-50/30 border border-sky-100/50">
        <h4 className="section-title text-sky-600 mb-3">🏙️ Location Profile</h4>
        <div className="space-y-0">
          <AttrRow label="Rent Tier" value={market?.estimated_rent_tier || "Pending"} />
          <AttrRow label="Foot Traffic" value={market?.foot_traffic_pattern || "Pending"} isText />
          <AttrRow label="Infrastructure" value={market?.infrastructure_access || "Pending"} isText />
        </div>
      </div>
    </div>
  );
}

function BarIndicator({ label, value, color }: { label: string; value: number; color: string }) {
  const pct = Math.min(value * 100, 100);
  return (
    <div>
      <div className="flex justify-between text-[10px] font-semibold text-slate-500 mb-1">
        <span>{label}</span>
        <span className="text-teal-600">{pct.toFixed(0)}%</span>
      </div>
      <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full transition-all duration-700`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function AttrRow({ label, value, isText }: { label: string; value: string; isText?: boolean }) {
  const getStyle = (v: string) => {
    const n = v.toLowerCase();
    if (n.includes("high")) return "bg-teal-50 text-teal-700 border-teal-200";
    if (n.includes("medium") || n.includes("moderate")) return "bg-amber-50 text-amber-700 border-amber-200";
    if (n.includes("low")) return "bg-slate-100 text-slate-600 border-slate-200";
    return "bg-sky-50 text-sky-700 border-sky-200";
  };
  return (
    <div className="flex justify-between items-center py-2 border-b border-slate-50 last:border-0">
      <span className="text-slate-500 text-xs font-medium">{label}</span>
      {isText ? (
        <span className="text-xs text-slate-700 text-right max-w-[60%] leading-snug">{value}</span>
      ) : (
        <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold border ${getStyle(value)}`}>{value}</span>
      )}
    </div>
  );
}