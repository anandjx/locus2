"use client";

import { useState } from "react";

interface ArtifactViewerProps {
  htmlReport?: string;
}

export function ArtifactViewer({ htmlReport }: ArtifactViewerProps) {
  if (!htmlReport) return null;

  return (
    <div className="card card-lavender overflow-hidden animate-fade-in delay-3">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          <span className="text-lg">📄</span> Executive Report
        </h3>
        <div className="flex gap-2">
          <button
            onClick={() => {
              const blob = new Blob([htmlReport], { type: "text/html" });
              const url = URL.createObjectURL(blob);
              window.open(url, "_blank");
            }}
            className="px-2.5 py-1 text-[10px] font-bold bg-gradient-to-r from-violet-500 to-purple-600 text-white rounded-lg hover:from-violet-600 hover:to-purple-700 transition-all shadow-sm"
          >
            Open in Tab
          </button>
          <button
            onClick={() => {
              const blob = new Blob([htmlReport], { type: "text/html" });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = "executive_report.html";
              a.click();
              URL.revokeObjectURL(url);
            }}
            className="px-2.5 py-1 text-[10px] font-bold bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-all border border-slate-200"
          >
            ⬇ Download
          </button>
        </div>
      </div>

      {/* Report Preview */}
      <iframe
        srcDoc={htmlReport}
        className="w-full h-[500px] border border-violet-100/50 rounded-2xl"
        title="Executive Report"
        sandbox="allow-same-origin"
      />
    </div>
  );
}