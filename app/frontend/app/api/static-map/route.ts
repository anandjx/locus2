import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET(req: NextRequest) {
    const { searchParams } = new URL(req.url);
    const markers = searchParams.getAll("marker");

    if (!markers || markers.length === 0) {
        return new NextResponse("Missing markers", { status: 400 });
    }

    // Use the backend MAPS_API_KEY (from environment variables)
    let apiKey = process.env.MAPS_API_KEY;
    if (!apiKey) {
        try {
            // Fallback: Read from the root python backend directory if Next.js didn't load it
            // process.cwd() = app/frontend, the .env lives at app/.env → one level up
            const envPath = path.resolve(process.cwd(), "../.env");
            const envContent = fs.readFileSync(envPath, "utf-8");
            const match = envContent.match(/MAPS_API_KEY=["']?([^"'\n\r]+)["']?/);
            if (match && match[1]) {
                apiKey = match[1].trim();
            }
        } catch (e) {
            console.error("Failed to read root .env file:", e);
        }
    }

    if (!apiKey) {
        return new NextResponse("Server missing Maps API Key", { status: 500 });
    }

    // Construct the Google Maps Static API URL
    const markerString = markers.map(m => `markers=color:red%7Cscale:2|${m}`).join("&");

    // Parse all coordinates to compute tight bounds
    const coords = markers
        .map(m => {
            const [lat, lng] = m.split(",").map(Number);
            return !isNaN(lat) && !isNaN(lng) ? { lat, lng } : null;
        })
        .filter(Boolean) as { lat: number; lng: number }[];

    let centerZoomParams = "";
    if (coords.length > 0) {
        const minLat = Math.min(...coords.map(c => c.lat));
        const maxLat = Math.max(...coords.map(c => c.lat));
        const minLng = Math.min(...coords.map(c => c.lng));
        const maxLng = Math.max(...coords.map(c => c.lng));

        const centerLat = (minLat + maxLat) / 2;
        const centerLng = (minLng + maxLng) / 2;

        // Calculate the span with padding (30% extra on each side)
        const latSpan = Math.max((maxLat - minLat) * 1.6, 0.005);
        const lngSpan = Math.max((maxLng - minLng) * 1.6, 0.005);

        // Derive zoom: ln(360 / span) / ln(2), capped between 12–16
        const zoomLat = Math.log2(180 / latSpan);
        const zoomLng = Math.log2(360 / lngSpan);
        const zoom = Math.max(12, Math.min(16, Math.floor(Math.min(zoomLat, zoomLng))));

        centerZoomParams = `&center=${centerLat},${centerLng}&zoom=${zoom}`;
    }

    const staticMapUrl = `https://maps.googleapis.com/maps/api/staticmap?size=600x400&scale=2&maptype=roadmap${centerZoomParams}&${markerString}&key=${apiKey}`;

    try {
        const response = await fetch(staticMapUrl);
        if (!response.ok) {
            throw new Error(`Google Maps API responded with ${response.status}`);
        }

        const imageBuffer = await response.arrayBuffer();

        // Return the image directly to the client
        return new NextResponse(imageBuffer, {
            headers: {
                "Content-Type": response.headers.get("Content-Type") || "image/png",
                "Cache-Control": "public, max-age=86400", // Cache for 24 hours
            },
        });
    } catch (error: any) {
        console.error("Static Map Error:", error.message);
        return new NextResponse(`Error fetching static map: ${error.message}`, { status: 500 });
    }
}
