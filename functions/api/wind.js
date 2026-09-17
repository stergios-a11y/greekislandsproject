/**
 * /api/wind?i=<island>&lat=<n>&lon=<n>
 *
 * Cloudflare Pages Function. Proxies MET Norway's locationforecast for one
 * point and returns the smallest thing the beach cards need:
 *
 *   { deg: <wind FROM, degrees>, ms: <m/s>, t: <ISO time of that reading> }
 *
 * Why a proxy at all: MET's terms ask for an identifying User-Agent (a
 * browser cannot set one) and ask browser clients to go through a proxy
 * and cache. So: identify ourselves, cache 30 minutes at the edge, and
 * snap the point to two decimals so every visitor to the same island hits
 * the same cache entry. 88 islands x 2 calls/hour is nothing against MET's
 * 20 requests/second ceiling.
 *
 * The lat/lon are bounded to Greece so this cannot be used as a general
 * weather proxy by anyone else. Data is CC BY 4.0; the page credits it.
 */
const UA = 'aegeanblueprint.com (https://aegeanblueprint.com)';
const TTL = 1800; // seconds

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const lat = Number(url.searchParams.get('lat'));
  const lon = Number(url.searchParams.get('lon'));
  if (!Number.isFinite(lat) || !Number.isFinite(lon) ||
      lat < 34 || lat > 41.8 || lon < 19 || lon > 30) {
    return json({ error: 'out of range' }, 400, 60);
  }
  const la = lat.toFixed(2), lo = lon.toFixed(2);

  const cache = caches.default;
  const cacheKey = new Request(`https://aegeanblueprint.com/api/wind?lat=${la}&lon=${lo}`, { method: 'GET' });
  const hit = await cache.match(cacheKey);
  if (hit) return hit;

  let out;
  try {
    const up = await fetch(`https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=${la}&lon=${lo}`, {
      headers: { 'User-Agent': UA, 'Accept': 'application/json' },
      cf: { cacheTtl: TTL, cacheEverything: true }
    });
    if (!up.ok) return json({ error: 'upstream ' + up.status }, 502, 120);
    const data = await up.json();
    const ts = (data.properties && data.properties.timeseries) || [];
    // First entry at or after now; MET's series starts at the current hour.
    const now = Date.now();
    const cur = ts.find(x => Date.parse(x.time) >= now - 3600e3) || ts[0];
    const d = cur && cur.data && cur.data.instant && cur.data.instant.details;
    if (!d || typeof d.wind_speed !== 'number' || typeof d.wind_from_direction !== 'number') {
      return json({ error: 'no wind in response' }, 502, 120);
    }
    out = { deg: d.wind_from_direction, ms: d.wind_speed, t: cur.time };
  } catch (e) {
    return json({ error: 'fetch failed' }, 502, 120);
  }

  const res = json(out, 200, TTL);
  await cache.put(cacheKey, res.clone());
  return res;
}

function json(body, status, maxAge) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': `public, max-age=${Math.min(maxAge, 300)}, s-maxage=${maxAge}`,
      'Access-Control-Allow-Origin': 'https://aegeanblueprint.com'
    }
  });
}
