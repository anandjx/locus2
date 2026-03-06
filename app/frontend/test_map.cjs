import fs from "fs";
import path from "path";

// 1. Check API Key matching
let apiKey = process.env.MAPS_API_KEY;
if (!apiKey) {
    try {
        const envPath = path.resolve(process.cwd(), "../../.env");
        console.log("Reading from:", envPath);
        const envContent = fs.readFileSync(envPath, "utf-8");
        const match = envContent.match(/MAPS_API_KEY=["']?([^"'\n\r]+)["']?/);
        if (match && match[1]) {
            apiKey = match[1].trim();
            console.log("Found API Key starting with:", apiKey.substring(0, 5));
        } else {
            console.log("No regex match found in .env");
        }
    } catch (e) {
        console.error("Error reading file:", e.message);
    }
}

// 2. Test Fetch
async function test() {
    const markers = ["19.135,72.815", "19.14,72.82"];
    const markerString = markers.map(m => `markers=color:red|${m}`).join("&");
    const staticMapUrl = `https://maps.googleapis.com/maps/api/staticmap?size=600x400&scale=2&${markerString}&key=${apiKey}`;

    console.log("Fetching URL:", staticMapUrl.substring(0, 100) + "...");

    try {
        const response = await fetch(staticMapUrl);
        console.log("Status:", response.status);
        if (!response.ok) {
            const text = await response.text();
            console.log("Error text:", text);
        } else {
            console.log("Success! Image size:", (await response.arrayBuffer()).byteLength);
        }
    } catch (e) {
        console.error("Fetch failed:", e);
    }
}

test();
