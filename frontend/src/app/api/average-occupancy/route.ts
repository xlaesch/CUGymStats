import crypto from "node:crypto";
import { NextResponse } from "next/server";
import { z } from "zod";

// Ensure Node.js runtime (required for node:crypto)
export const runtime = "nodejs";

// In-memory caches/limits for the BFF layer
const cache = new Map<string, { expiresAt: number; payload: any }>();
const rate = new Map<string, { window: number; count: number }>();

const CACHE_TTL_SECONDS = parseInt(process.env.BFF_CACHE_TTL_SECONDS || "30", 10); // short cache
const RATE_LIMIT_RPM = parseInt(process.env.BFF_RATE_LIMIT_RPM || "600", 10); // heavy limit in BFF

const schema = z.object({
	dayofweek: z
		.string()
		.regex(/^\d+$/)
		.transform((s) => parseInt(s, 10))
		.refine((n) => n >= 0 && n <= 6, { message: "dayofweek must be 0-6" }),
	location: z.string().optional(),
});

function tooMany(ip: string): boolean {
	const now = Math.floor(Date.now() / 1000);
	const window = Math.floor(now / 60);
	const rec = rate.get(ip);
	if (!rec || rec.window !== window) {
		rate.set(ip, { window, count: 1 });
		return false;
	}
	rec.count += 1;
	return rec.count > RATE_LIMIT_RPM;
}

function hmacSign(method: string, urlPath: string, query: string, body: string): Record<string, string> {
	const secret = process.env.DOMAIN_API_SECRET || process.env.API_SHARED_SECRET;
	if (!secret) {
		throw new Error("DOMAIN_API_SECRET is not configured in the environment");
	}
	const ts = Math.floor(Date.now() / 1000).toString();
	const nonce = crypto.randomUUID();
	const canonical = [ts, nonce, method.toUpperCase(), urlPath, query, body].join("\n");
	const signature = crypto.createHmac("sha256", secret).update(canonical).digest("hex");
	return {
		"X-Timestamp": ts,
		"X-Nonce": nonce,
		"X-Signature": signature,
	};
}

export async function GET(req: Request) {
	try {
		// Rate limit by IP
		const ip = (req.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "unknown";
		if (tooMany(ip)) {
			return NextResponse.json({ error: "Too Many Requests" }, { status: 429 });
		}

		const url = new URL(req.url);
		const parse = schema.safeParse({
			dayofweek: url.searchParams.get("dayofweek") ?? "",
			location: url.searchParams.get("location") ?? undefined,
		});
		if (!parse.success) {
			const first = parse.error.issues?.[0]?.message || "Invalid input";
			return NextResponse.json({ error: first }, { status: 400 });
		}
		const defaultLocation = process.env.DEFAULT_LOCATION || "Helen Newman Fitness Center";
		const location = (parse.data.location && parse.data.location.trim()) || defaultLocation;
		const { dayofweek } = parse.data;

		// Cache key scoped to input
		const cacheKey = `avg:${location}:${dayofweek}`;
		const cached = cache.get(cacheKey);
		const now = Math.floor(Date.now() / 1000);
		if (cached && cached.expiresAt > now) {
			return NextResponse.json(cached.payload, { status: 200, headers: { "X-Cache": "HIT" } });
		}

		// Call the Domain API (Flask)
		const domainBase = process.env.DOMAIN_API_BASE || "http://127.0.0.1:5000";
		const path = "/api/average-occupancy";
		const qs = "";
		const body = ""; // GET body is empty
		const headers = {
			...hmacSign("GET", path, qs, body),
			"X-Forwarded-For": ip,
			"X-Location": location,
			"X-Day-Of-Week": String(dayofweek),
		} as Record<string, string>;

		const resp = await fetch(`${domainBase}${path}`, {
			method: "GET",
			headers,
			// Do NOT forward cookies or secrets to the browser
			cache: "no-store",
		});

		if (!resp.ok) {
			const text = await resp.text();
			return NextResponse.json({ error: `Upstream error ${resp.status}`, details: text }, { status: 502 });
		}

		const data = await resp.json();
		cache.set(cacheKey, { payload: data, expiresAt: now + CACHE_TTL_SECONDS });
		return NextResponse.json(data, { status: 200, headers: { "X-Cache": "MISS" } });
	} catch (err: any) {
		console.error("BFF error /api/average-occupancy:", err);
		return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
	}
}
