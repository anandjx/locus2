// import type { MarketCharacteristics } from "@/lib/types";

// interface MarketCardProps {
//   market: MarketCharacteristics;
// }

// /**
//  * MarketCard displays SOTA market characteristics and Conversion Gap physics.
//  */
// export function MarketCard({ market }: MarketCardProps) {
//   // Determine Market Status based on Conversion Gap
//   const isUnderserved = market.conversion_gap > 0.2;
//   const isSaturated = market.conversion_gap < -0.1;

//   const gapLabel = isUnderserved
//     ? "Blue Ocean (Underserved)"
//     : isSaturated
//       ? "Saturated (Red Ocean)"
//       : "Mature / Balanced";

//   const gapColor = isUnderserved
//     ? "bg-indigo-50 border-indigo-200 text-indigo-700"
//     : isSaturated
//       ? "bg-red-50 border-red-200 text-red-700"
//       : "bg-amber-50 border-amber-200 text-amber-700";

//   return (
//     <div className="bg-white rounded-xl shadow-sm border p-5 transition-all hover:shadow-md">
//       <div className="flex items-center justify-between mb-6">
//         <h3 className="font-semibold text-slate-900 flex items-center gap-2">
//           <span className="text-xl">📈</span>
//           Market Fundamentals
//         </h3>
//         <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${gapColor}`}>
//           {gapLabel}
//         </span>
//       </div>

//       {/* SOTA Conversion Gap Visualization */}
//       <div className="mb-6 p-4 rounded-lg bg-slate-50 border border-slate-100">
//         <div className="flex justify-between text-xs font-semibold text-slate-500 mb-2">
//           <span>Latent Demand (Potential)</span>
//           <span>Observed Activity</span>
//         </div>

//         {/* Visual Progress Bars */}
//         <div className="space-y-3">
//           <div className="relative w-full h-2 bg-slate-200 rounded-full overflow-hidden">
//             <div
//               className="absolute top-0 left-0 h-full bg-indigo-500 rounded-full"
//               style={{ width: `${Math.min(market.latent_demand_ldi * 100, 100)}%` }}
//             />
//           </div>
//           <div className="relative w-full h-2 bg-slate-200 rounded-full overflow-hidden">
//             <div
//               className="absolute top-0 left-0 h-full bg-slate-400 rounded-full"
//               style={{ width: `${Math.min(market.observed_demand_odi * 100, 100)}%` }}
//             />
//           </div>
//         </div>

//         <div className="mt-3 flex justify-between items-center">
//           <span className="text-xs text-slate-500">Conversion Gap</span>
//           <span className={`text-sm font-bold ${market.conversion_gap > 0 ? "text-indigo-600" : "text-red-600"}`}>
//             {market.conversion_gap > 0 ? "+" : ""}{market.conversion_gap.toFixed(2)}
//           </span>
//         </div>
//       </div>

//       {/* Traditional Market Rows */}
//       <div className="space-y-2">
//         <MarketRow label="Population Density" value={market.population_density} />
//         <MarketRow label="Income Level" value={market.income_level} />
//         <MarketRow label="Rental Cost" value={market.rental_cost_tier} />
//         <MarketRow label="Foot Traffic" value={market.foot_traffic_pattern} isText />
//         <MarketRow label="Infrastructure" value={market.infrastructure_access} isText />
//       </div>
//     </div>
//   );
// }

import type { MarketCharacteristics } from "@/lib/types";

interface MarketCardProps {
  market: MarketCharacteristics;
}

/**
 * MarketCard displays SOTA market characteristics and Conversion Gap physics.
 */
export function MarketCard({ market }: MarketCardProps) {
  if (!market) return null;
  // 1. SAFE FALLBACKS: Prevent crashes if backend data is missing
  const gap = market?.conversion_gap ?? 0;
  const ldi = market?.latent_demand_ldi ?? 0;
  const odi = market?.observed_demand_odi ?? 0;

  // Determine Market Status based on safe gap
  const isUnderserved = gap > 0.2;
  const isSaturated = gap < -0.1;

  const gapLabel = isUnderserved
    ? "Blue Ocean (Underserved)"
    : isSaturated
      ? "Saturated (Red Ocean)"
      : "Mature / Balanced";

  const gapColor = isUnderserved
    ? "bg-indigo-50 border-indigo-200 text-indigo-700"
    : isSaturated
      ? "bg-red-50 border-red-200 text-red-700"
      : "bg-amber-50 border-amber-200 text-amber-700";

  return (
    <div className="bg-white rounded-xl shadow-sm border p-5 transition-all hover:shadow-md">
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-semibold text-slate-900 flex items-center gap-2">
          <span className="text-xl">📈</span>
          Market Fundamentals
        </h3>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${gapColor}`}>
          {gapLabel}
        </span>
      </div>

      {/* SOTA Conversion Gap Visualization */}
      <div className="mb-6 p-4 rounded-lg bg-slate-50 border border-slate-100">
        <div className="flex justify-between text-xs font-semibold text-slate-500 mb-2">
          <span>Latent Demand (Potential)</span>
          <span>Observed Activity</span>
        </div>

        {/* Visual Progress Bars - USING SAFE VARIABLES */}
        <div className="space-y-3">
          <div className="relative w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="absolute top-0 left-0 h-full bg-indigo-500 rounded-full"
              style={{ width: `${Math.min(ldi * 100, 100)}%` }}
            />
          </div>
          <div className="relative w-full h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="absolute top-0 left-0 h-full bg-slate-400 rounded-full"
              style={{ width: `${Math.min(odi * 100, 100)}%` }}
            />
          </div>
        </div>

        <div className="mt-3 flex justify-between items-center">
          <span className="text-xs text-slate-500">Conversion Gap</span>
          <span className={`text-sm font-bold ${gap > 0 ? "text-indigo-600" : "text-red-600"}`}>
            {gap > 0 ? "+" : ""}{gap.toFixed(2)}
          </span>
        </div>
      </div>

      {/* Traditional Market Rows */}
      <div className="space-y-2">
        <MarketRow label="Population Density" value={market?.population_density || "Pending"} />
        <MarketRow label="Income Level" value={market?.income_level || "Pending"} />
        <MarketRow label="Rental Cost Tier" value={market?.estimated_rent_tier || "Pending"} />
        <MarketRow label="Foot Traffic" value={market?.foot_traffic_pattern || "Pending"} isText />
        <MarketRow label="Infrastructure" value={market?.infrastructure_access || "Pending"} isText />
      </div>
    </div>
  );
}

function MarketRow({
  label,
  value,
  isText = false,
}: {
  label: string;
  value: string;
  isText?: boolean;
}) {
  const getValueStyle = (val: string) => {
    const normalized = val.toLowerCase();
    if (normalized.includes("high")) return "bg-green-50 text-green-700 border border-green-200";
    if (normalized.includes("medium") || normalized.includes("moderate")) return "bg-amber-50 text-amber-700 border border-amber-200";
    if (normalized.includes("low")) return "bg-slate-100 text-slate-600 border border-slate-200";
    return "bg-indigo-50 text-indigo-700 border border-indigo-200";
  };

  return (
    <div className="flex justify-between items-center py-2.5 border-b border-slate-100 last:border-0">
      <span className="text-slate-500 text-sm font-medium">{label}</span>
      {isText ? (
        <span className="text-sm text-slate-700 text-right max-w-[60%] leading-snug">
          {value}
        </span>
      ) : (
        <span className={`px-3 py-1 rounded-md text-xs font-bold ${getValueStyle(value)}`}>
          {value}
        </span>
      )}
    </div>
  );
}




// import type { MarketCharacteristics } from "@/lib/types";

// interface MarketCardProps {
//   market: MarketCharacteristics;
// }

// /**
//  * MarketCard displays market characteristics from the analysis.
//  */
// export function MarketCard({ market }: MarketCardProps) {
//   return (
//     <div className="bg-white rounded-xl shadow-sm border p-5">
//       <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
//         <span className="text-xl">📈</span>
//         Market Characteristics
//       </h3>

//       <div className="space-y-3">
//         <MarketRow
//           label="Population Density"
//           value={market.population_density}
//         />
//         <MarketRow
//           label="Income Level"
//           value={market.income_level}
//         />
//         <MarketRow
//           label="Rental Cost"
//           value={market.rental_cost_tier}
//         />
//         <MarketRow
//           label="Foot Traffic"
//           value={market.foot_traffic_pattern}
//           isText
//         />
//         <MarketRow
//           label="Infrastructure"
//           value={market.infrastructure_access}
//           isText
//         />
//       </div>
//     </div>
//   );
// }

// function MarketRow({
//   label,
//   value,
//   isText = false,
// }: {
//   label: string;
//   value: string;
//   isText?: boolean;
// }) {
//   // Determine color based on value for standard High/Medium/Low values
//   const getValueStyle = (val: string) => {
//     const normalized = val.toLowerCase();
//     if (normalized === "high" || normalized.includes("high")) {
//       return "bg-green-100 text-green-800";
//     }
//     if (normalized === "medium" || normalized.includes("medium") || normalized.includes("moderate")) {
//       return "bg-yellow-100 text-yellow-800";
//     }
//     if (normalized === "low" || normalized.includes("low")) {
//       return "bg-gray-100 text-gray-800";
//     }
//     // For non-standard values, use neutral styling
//     return "bg-blue-50 text-blue-800";
//   };

//   return (
//     <div className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0">
//       <span className="text-gray-600 text-sm">{label}</span>
//       {isText ? (
//         <span className="text-sm text-gray-800 text-right max-w-[60%]">
//           {value}
//         </span>
//       ) : (
//         <span
//           className={`px-3 py-1 rounded-full text-sm font-medium ${getValueStyle(
//             value
//           )}`}
//         >
//           {value}
//         </span>
//       )}
//     </div>
//   );
// }