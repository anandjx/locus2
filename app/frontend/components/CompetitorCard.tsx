import type { CompetitionProfile } from "@/lib/types";

interface CompetitorCardProps {
  competition: CompetitionProfile;
}

/**
 * CompetitorCard displays SOTA competition statistics and market power dynamics.
 */
export function CompetitorCard({ competition }: CompetitorCardProps) {
  if (!competition) return null;
  // 1. SAFE FALLBACKS: Default to 0 if the backend hasn't supplied the new metrics yet
  const cci = competition?.concentration_index_cci ?? 0;
  const reqDailyCustomers = competition?.req_daily_customers ?? 0;
  const feasibilityNote = competition?.feasibility_note ?? "Pending";

  // Determine Market Structure based on safe CCI
  const isMonopoly = cci >= 0.8;
  const isFragmented = cci <= 0.4;

  const structureLabel = isMonopoly
    ? "Oligopoly / Entrenched"
    : isFragmented
      ? "Highly Fragmented"
      : "Balanced Competition";

  const structureColor = isMonopoly
    ? "text-red-700 bg-red-50 border-red-200"
    : isFragmented
      ? "text-green-700 bg-green-50 border-green-200"
      : "text-amber-700 bg-amber-50 border-amber-200";

  // Check for Demand Deficit using the new Gap Analysis rule
  const isDemandDeficit = reqDailyCustomers > 130;

  return (
    <div className="bg-white rounded-xl shadow-sm border p-5 transition-all hover:shadow-md">
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-semibold text-slate-900 flex items-center gap-2">
          <span className="text-xl">⚔️</span>
          Market Power & Viability
        </h3>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${structureColor}`}>
          {structureLabel}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <StatBlock
          label="Concentration (CCI)"
          // Use the safe 'cci' variable here
          value={`${(cci * 100).toFixed(0)}%`}
          icon="🥧"
          subtitle="Top 2 Players Share"
        />
        <StatBlock
          label="Break-Even (Daily)"
          // Use the honest break-even proxy
          value={reqDailyCustomers.toString()}
          icon="🎯"
          subtitle={feasibilityNote}
          highlight={isDemandDeficit}
          alert={isDemandDeficit}
        />
        <StatBlock
          label="Chain Dominance"
          value={`${(competition.chain_dominance_pct ?? 0).toFixed(0)}%`}
          icon="🏢"
          highlight={(competition.chain_dominance_pct ?? 0) > 50}
        />
        <StatBlock
          label="Avg Rating"
          value={`⭐ ${(competition.avg_competitor_rating ?? 0).toFixed(1)}`}
          icon=""
        />
        <StatBlock
          label="Total Competitors"
          value={(competition.total_competitors ?? 0).toString()}
          icon="📊"
        />
        <StatBlock
          label="High Performers"
          value={(competition.high_performers_count ?? 0).toString()}
          icon="🏆"
          subtitle="4.5+ rating"
        />
      </div>

      {isDemandDeficit && (
        <div className="mt-4 p-3 bg-red-50 border border-red-100 rounded-lg text-sm text-red-800 flex items-start gap-2">
          <span>⚠️</span>
          <p>
            <strong>Demand Deficit Warning:</strong> {feasibilityNote}. Break-even requires high volume traffic.
            You must execute destination marketing to pull customers from outside zones.
          </p>
        </div>
      )}
    </div>
  );
}

function StatBlock({
  label,
  value,
  icon,
  subtitle,
  highlight,
  alert,
}: {
  label: string;
  value: string;
  icon?: string;
  subtitle?: string;
  highlight?: boolean;
  alert?: boolean;
}) {
  return (
    <div
      className={`p-3 rounded-lg text-center ${alert ? "bg-red-50 border border-red-200"
        : highlight ? "bg-amber-50 border border-amber-200"
          : "bg-slate-50 border border-slate-100"
        }`}
    >
      {icon && <span className="text-sm">{icon}</span>}
      <div className={`text-xl font-bold ${alert ? "text-red-700"
        : highlight ? "text-amber-700"
          : "text-indigo-600"
        }`}>
        {value}
      </div>
      <div className="text-xs font-medium text-slate-500 mt-1">{label}</div>
      {subtitle && <div className={`text-[10px] mt-0.5 ${alert ? "text-red-500 font-semibold" : "text-slate-400"}`}>{subtitle}</div>}
    </div>
  );
}













// import type { CompetitionProfile } from "@/lib/types";

// interface CompetitorCardProps {
//   competition: CompetitionProfile;
// }

// /**
//  * CompetitorCard displays competition statistics from the analysis.
//  */
// export function CompetitorCard({ competition }: CompetitorCardProps) {
//   // Determine competition intensity
//   const intensity =
//     competition.total_competitors > 20
//       ? "High"
//       : competition.total_competitors > 10
//       ? "Medium"
//       : "Low";

//   const intensityColor =
//     intensity === "High"
//       ? "text-red-600 bg-red-50"
//       : intensity === "Medium"
//       ? "text-yellow-600 bg-yellow-50"
//       : "text-green-600 bg-green-50";

//   return (
//     <div className="bg-white rounded-xl shadow-sm border p-5">
//       <div className="flex items-center justify-between mb-4">
//         <h3 className="font-semibold text-gray-900 flex items-center gap-2">
//           <span className="text-xl">🏪</span>
//           Competition Profile
//         </h3>
//         <span className={`px-2 py-1 rounded-full text-xs font-medium ${intensityColor}`}>
//           {intensity} Competition
//         </span>
//       </div>

//       <div className="grid grid-cols-2 gap-4">
//         <StatBlock
//           label="Total Competitors"
//           value={competition.total_competitors.toString()}
//           icon="📊"
//         />
//         <StatBlock
//           label="Density/km²"
//           value={competition.density_per_km2.toFixed(1)}
//           icon="📍"
//         />
//         <StatBlock
//           label="Chain Dominance"
//           value={`${competition.chain_dominance_pct.toFixed(0)}%`}
//           icon="🏢"
//           highlight={competition.chain_dominance_pct > 50}
//         />
//         <StatBlock
//           label="Avg Rating"
//           value={`⭐ ${competition.avg_competitor_rating.toFixed(1)}`}
//           icon=""
//         />
//         <StatBlock
//           label="High Performers"
//           value={competition.high_performers_count.toString()}
//           icon="🏆"
//           subtitle="4.5+ rating"
//           highlight={competition.high_performers_count > 5}
//         />
//         <StatBlock
//           label="Market Share"
//           value={`${(100 / (competition.total_competitors + 1)).toFixed(0)}%`}
//           icon="🎯"
//           subtitle="Potential"
//         />
//       </div>
//     </div>
//   );
// }

// function StatBlock({
//   label,
//   value,
//   icon,
//   subtitle,
//   highlight,
// }: {
//   label: string;
//   value: string;
//   icon?: string;
//   subtitle?: string;
//   highlight?: boolean;
// }) {
//   return (
//     <div
//       className={`p-3 rounded-lg text-center ${
//         highlight ? "bg-amber-50 border border-amber-200" : "bg-gray-50"
//       }`}
//     >
//       {icon && <span className="text-sm">{icon}</span>}
//       <div className={`text-xl font-bold ${highlight ? "text-amber-700" : "text-blue-600"}`}>
//         {value}
//       </div>
//       <div className="text-xs text-gray-500">{label}</div>
//       {subtitle && <div className="text-xs text-gray-400 mt-0.5">{subtitle}</div>}
//     </div>
//   );
// }