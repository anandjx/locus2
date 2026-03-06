export function AgentStatus({ stage }: { stage?: string }) {
  if (!stage) return null;

  return (
    <div className="flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-white/70 border border-indigo-100 shadow-sm backdrop-blur-md">
      <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse-soft" />
      <span className="text-xs text-slate-500 font-medium">
        <span className="text-indigo-600 font-semibold">{stage}</span>
      </span>
    </div>
  );
}