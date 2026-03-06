import type { AlternativeLocation } from "@/lib/types";

interface AlternativeLocationsProps {
  locations: AlternativeLocation[];
}

export function AlternativeLocations({ locations }: AlternativeLocationsProps) {
  if (!locations || locations.length === 0) return null;

  return (
    <div className="card card-chiffon overflow-hidden animate-fade-in delay-2">
      <div className="flex items-center justify-between mb-5">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          <span className="text-lg">🗺️</span> Alternative Locations
        </h3>
        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold border bg-amber-50 text-amber-700 border-amber-200">
          {locations.length} Options
        </span>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {locations.map((loc, i) => {
          const scoreBg =
            loc.overall_score >= 75 ? "from-emerald-500 to-green-600"
              : loc.overall_score >= 50 ? "from-amber-500 to-orange-500"
                : "from-slate-400 to-slate-500";

          return (
            <div
              key={i}
              className="p-3.5 bg-gradient-to-br from-amber-50/40 to-white rounded-2xl border border-amber-100/50 hover:border-amber-200 hover:shadow-md transition-all duration-200"
            >
              <div className="flex justify-between items-start mb-2.5">
                <div className="min-w-0">
                  <h4 className="font-semibold text-slate-900 text-xs truncate">{loc.location_name}</h4>
                  <p className="text-[10px] text-slate-500 truncate">{loc.area}</p>
                </div>
                <div className={`w-10 h-10 rounded-xl flex flex-col items-center justify-center text-white bg-gradient-to-br ${scoreBg} shadow-sm flex-shrink-0 ml-2`}>
                  <span className="text-xs font-bold leading-none">{loc.overall_score}</span>
                  <span className="text-[7px] opacity-70">/100</span>
                </div>
              </div>

              <span className="inline-block px-2 py-0.5 bg-amber-50 text-amber-700 rounded-md text-[9px] font-bold mb-2 border border-amber-100">
                {loc.opportunity_type}
              </span>

              <div className="space-y-1.5 mb-2">
                <div>
                  <div className="text-[9px] text-slate-400 uppercase tracking-wider font-semibold">Strength</div>
                  <div className="text-[10px] text-emerald-700 flex items-start gap-1">
                    <span className="flex-shrink-0">✅</span><span>{loc.key_strength}</span>
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-slate-400 uppercase tracking-wider font-semibold">Concern</div>
                  <div className="text-[10px] text-amber-700 flex items-start gap-1">
                    <span className="flex-shrink-0">⚠️</span><span>{loc.key_concern}</span>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-amber-100/50">
                <p className="text-[9px] text-slate-400 italic leading-relaxed">{loc.why_not_top}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}