// export function AgentStatus({ stage }: { stage?: string }) {
//   if (!stage) return null;

//   return (
//     <div className="flex items-center gap-3 glass px-4 py-2 w-fit">
//       <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
//       <span className="text-sm text-white/70">
//         Agent reasoning: <span className="text-white">{stage}</span>
//       </span>
//     </div>
//   );
// }

// app/frontend/components/AgentStatus.tsx
export function AgentStatus({ stage }: { stage?: string }) {
  if (!stage) return null;

  return (
    <div className="flex items-center gap-3 bg-white/50 border border-slate-200 shadow-sm backdrop-blur-md px-4 py-2 w-fit rounded-full">
      <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
      <span className="text-sm text-slate-600 font-medium">
        Agent reasoning: <span className="text-indigo-600 font-semibold">{stage}</span>
      </span>
    </div>
  );
}