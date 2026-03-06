"use client";

import { useState } from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";
import { ScrollableMarkdown } from "./ScrollableMarkdown";
import { parseCodeBlocks, extractPythonCode } from "@/lib/parseCodeBlocks";

interface TabbedGapAnalysisProps {
  content: string;
  code?: string;
}

type TabType = "results" | "code";

export function TabbedGapAnalysis({ content, code }: TabbedGapAnalysisProps) {
  const [activeTab, setActiveTab] = useState<TabType>("results");

  if (!content) {
    return <p className="text-rose-400 text-sm italic animate-pulse-soft">Analyzing market gaps...</p>;
  }

  const { textContent, codeBlocks } = parseCodeBlocks(content);
  const pythonCode = code || extractPythonCode(content);
  const hasCode = !!pythonCode || codeBlocks.length > 0;

  return (
    <div className="space-y-2">
      {/* Tab Navigation — rose themed */}
      <div className="flex gap-1 border-b border-rose-200/50">
        <TabButton active={activeTab === "results"} onClick={() => setActiveTab("results")}>
          📊 Results
        </TabButton>
        {hasCode && (
          <TabButton active={activeTab === "code"} onClick={() => setActiveTab("code")}>
            🐍 Code
          </TabButton>
        )}
      </div>

      {/* Tab Content — taller for gap analysis */}
      <div className="pt-2">
        {activeTab === "results" && (
          <ScrollableMarkdown content={textContent || content} maxHeight="24rem" />
        )}

        {activeTab === "code" && hasCode && (
          <div className="overflow-y-auto rounded-xl border border-rose-100/50" style={{ maxHeight: "24rem" }}>
            <SyntaxHighlighter
              language="python"
              style={oneLight}
              customStyle={{
                margin: 0,
                padding: "1rem",
                fontSize: "0.75rem",
                borderRadius: "0.75rem",
                backgroundColor: "#fef2f2",
              }}
              showLineNumbers
              wrapLines
            >
              {pythonCode}
            </SyntaxHighlighter>
          </div>
        )}
      </div>
    </div>
  );
}

function TabButton({ children, active, onClick }: {
  children: React.ReactNode; active: boolean; onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`px-3 py-1.5 text-xs font-semibold rounded-t-lg transition-colors ${active
          ? "bg-rose-50 text-rose-700 border-b-2 border-rose-500"
          : "text-slate-500 hover:text-slate-700 hover:bg-rose-50/50"
        }`}
    >
      {children}
    </button>
  );
}