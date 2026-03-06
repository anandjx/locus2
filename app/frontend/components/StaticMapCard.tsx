import React from "react";

interface StaticMapCardProps {
    coordinates?: string[];
}

export function StaticMapCard({ coordinates }: StaticMapCardProps) {
    if (!coordinates || coordinates.length === 0) {
        return (
            <div className="card card-indigo p-5 h-40 flex flex-col items-center justify-center text-slate-400">
                <span className="text-3xl mb-2">🗺️</span>
                <p className="text-xs font-medium">Map data unavailable</p>
            </div>
        );
    }

    const searchParams = new URLSearchParams();
    coordinates.forEach((coord) => {
        if (coord && typeof coord === "string" && coord.includes(",")) {
            searchParams.append("marker", coord);
        }
    });

    const imageUrl = `/api/static-map?${searchParams.toString()}`;

    return (
        <div className="card card-indigo overflow-hidden animate-fade-in delay-2">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-900 flex items-center gap-2">
                    <span className="text-lg">🌐</span> Geospatial Market Visualization
                </h3>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold border bg-indigo-50 text-indigo-700 border-indigo-200">
                    {coordinates.length} Locations
                </span>
            </div>

            {/* Map Container */}
            <div className="relative w-full h-64 rounded-2xl overflow-hidden border border-indigo-100/50 bg-slate-50 ring-2 ring-indigo-100/40">
                <img
                    src={imageUrl}
                    alt="Competitor Map"
                    className="w-full h-full object-cover"
                    loading="lazy"
                />
                <div className="absolute inset-0 flex items-center justify-center -z-10 bg-slate-100 animate-pulse text-slate-400 text-xs">
                    Loading Map...
                </div>
            </div>
        </div>
    );
}
