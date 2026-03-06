import React from "react";

interface StaticMapCardProps {
    coordinates?: string[];
}

export function StaticMapCard({ coordinates }: StaticMapCardProps) {
    if (!coordinates || coordinates.length === 0) {
        return (
            <div className="bg-white rounded-xl shadow-sm border p-5 transition-all hover:shadow-md h-64 flex flex-col items-center justify-center text-slate-400">
                <span className="text-3xl mb-2">🗺️</span>
                <p className="text-sm font-medium">Map data unavailable</p>
            </div>
        );
    }

    // Construct the URL to our secure Next.js API route
    // We pass each coordinate as a separate `marker` query parameter
    const searchParams = new URLSearchParams();
    coordinates.forEach((coord) => {
        // Only add valid coordinates to prevent broken images
        if (coord && typeof coord === "string" && coord.includes(",")) {
            searchParams.append("marker", coord);
        }
    });

    const imageUrl = `/api/static-map?${searchParams.toString()}`;

    return (
        <div className="bg-white rounded-xl shadow-sm border p-5 transition-all hover:shadow-md">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-slate-900 flex items-center gap-2">
                    <span className="text-xl">📍</span>
                    Competitor Map
                </h3>
                <span className="px-3 py-1 rounded-full text-xs font-semibold border bg-indigo-50 text-indigo-700 border-indigo-200">
                    {coordinates.length} Locations
                </span>
            </div>

            <div className="relative w-full h-64 rounded-lg overflow-hidden border border-slate-100 bg-slate-50 flex items-center justify-center">
                {/* Using a standard img tag with the API route source */}
                <img
                    src={imageUrl}
                    alt="Competitor Map"
                    className="w-full h-full object-cover"
                    loading="lazy"
                />
                {/* Simple skeleton loader that gets hidden once the image loads over it */}
                <div className="absolute inset-0 flex items-center justify-center -z-10 bg-slate-100 animate-pulse text-slate-400 text-sm">
                    Loading Map...
                </div>
            </div>
        </div>
    );
}
