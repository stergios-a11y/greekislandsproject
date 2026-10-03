#!/usr/bin/env python3
"""Sea paths for the ferry network map.

For every segment the ferry map can draw (each FERRY_GRAPH edge and each pair of
consecutive stops on a FERRY_VISUAL_LINES line, with and without side harbours)
find a route over water around the islands, simplify it, and write
ferry-paths.json  { "lat,lng|lat,lng": [[lat, lng], ...] }.
The map falls back to a gentle curve for any segment missing from the file.

Land mask: tools/data/aegean_land.npz — OSM land polygons (via @geo-maps/
earth-lands-10m, ODbL) rasterised at 0.004° over 18.8–30.2°E, 34.2–41.8°N.

Needs numpy, scipy, scikit-image and node (to read the data out of script.js).
Run it whenever ports, edges or lines change:  python3 tools/build_ferry_paths.py
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
from skimage.graph import MCP_Geometric

ROOT = Path(__file__).resolve().parent.parent
W0, N0, RES = 18.8, 41.8, 0.004

NODE = r"""
const fs = require('fs');
const s = fs.readFileSync(process.argv[1], 'utf8');
function grab(name, open, close) {
  const i = s.indexOf('const ' + name + ' = ');
  if (i < 0) return null;
  let j = s.indexOf(open, i), depth = 0, k = j;
  for (; k < s.length; k++) { if (s[k] === open) depth++; else if (s[k] === close && --depth === 0) break; }
  return eval('(' + s.slice(j, k + 1) + ')');
}
const ISL = grab('ISLANDS_DATA', '{', '}'), IFP = grab('ISLAND_FERRY_PORTS', '{', '}'),
      MP = grab('MAINLAND_PORTS', '{', '}'), SP = grab('SIDE_PORTS', '{', '}') || {},
      EP = grab('EXTRA_PORTS', '{', '}') || {}, G = grab('FERRY_GRAPH', '[', ']'),
      LINES = grab('FERRY_VISUAL_LINES', '[', ']');
const port = k => MP[k] || (IFP[k] && ISL[k] ? IFP[k] : null) || ISL[k] || EP[k] || null;
const edge = (a, b) => G.find(e => (e.a === a && e.b === b) || (e.a === b && e.b === a));
const ends = (a, b, sides) => {
  let pa = port(a), pb = port(b);
  const e = edge(a, b);
  if (e && sides) {
    const atA = e.a === a ? e.ap : e.bp, atB = e.a === a ? e.bp : e.ap;
    if (atA && SP[atA]) pa = SP[atA];
    if (atB && SP[atB]) pb = SP[atB];
  }
  return pa && pb ? [[pa.lat, pa.lng], [pb.lat, pb.lng]] : null;
};
const segs = [], rank = { high: 0, med: 1, low: 2 };
LINES.slice().sort((x, y) => rank[x.freq] - rank[y.freq]).forEach(l => {
  for (let i = 0; i < l.stops.length - 1; i++) segs.push(ends(l.stops[i], l.stops[i + 1], !!l.sides)); });
G.slice().sort((x, y) => rank[x.freq] - rank[y.freq]).forEach(e => {
  segs.push(ends(e.a, e.b, true)); segs.push(ends(e.a, e.b, false)); });
console.log(JSON.stringify(segs.filter(Boolean)));
"""

def key(p, q):
    return f"{p[0]:.4f},{p[1]:.4f}|{q[0]:.4f},{q[1]:.4f}"

def main():
    land = np.unpackbits(np.load(ROOT / 'tools/data/aegean_land.npz')['bits'])
    shape = tuple(np.load(ROOT / 'tools/data/aegean_land.npz')['shape'])
    land = land[:shape[0] * shape[1]].reshape(shape).astype(bool)
    water = ~land
    # Keep only the open sea: harbour basins and lakes cut off by breakwaters at
    # this resolution would otherwise trap a port's start cell.
    lab, _ = ndimage.label(water, structure=np.ones((3, 3)))
    sea_id = lab[int((N0 - 36.5) / RES), int((24.0 - W0) / RES)]   # open water SW of Milos
    water = lab == sea_id
    dist_land = ndimage.distance_transform_edt(water)               # in cells
    # Stay a little off the coast where there is room; mid-channel otherwise.
    cost = np.where(water, 1.0 + 2.0 * np.clip(1.0 - dist_land / 3.0, 0, 1), -1.0)
    _, (nr, nc) = ndimage.distance_transform_edt(~water, return_indices=True)

    out = subprocess.run(['node', '-e', NODE, str(ROOT / 'script.js')], capture_output=True, text=True, check=True)
    segs = json.loads(out.stdout)
    todo = {}
    for p, q in segs:
        if key(p, q) in todo or key(q, p) in todo: continue
        todo[key(p, q)] = (p, q)

    def cell(lat, lng):
        r = int((N0 - lat) / RES); c = int((lng - W0) / RES)
        return nr[r, c], nc[r, c]          # nearest open-water cell
    def ll(rc):
        return [round(float(N0 - (rc[0] + 0.5) * RES), 4), round(float(W0 + (rc[1] + 0.5) * RES), 4)]
    dist_water = ndimage.distance_transform_edt(~water)          # 0 on water, cells inland otherwise
    used = np.zeros_like(water)
    # Near a port, sailing along an already-drawn route is cheaper, so routes
    # leave a harbour as one trunk and branch further out. Out at sea, no pull.
    REUSE, NEAR = 0.6, 30            # cost factor; radius in cells (~12 km)
    near_port = np.zeros_like(water)
    for p_, q_ in todo.values():
        for la, ln in (p_, q_):
            near_port[int((N0 - la) / RES), int((ln - W0) / RES)] = True
    near_port = ndimage.distance_transform_edt(~near_port) <= NEAR

    def on_water(pts, slack=1.5):
        rr = np.clip(np.round([p[0] for p in pts]).astype(int), 0, land.shape[0] - 1)
        cc = np.clip(np.round([p[1] for p in pts]).astype(int), 0, land.shape[1] - 1)
        return bool(np.all(dist_water[rr, cc] <= slack))

    def simplify(pts, tol=0.35):
        keep = [0, len(pts) - 1]; stack = [(0, len(pts) - 1)]
        P = np.asarray(pts, float)
        while stack:
            i, j = stack.pop()
            if j <= i + 1: continue
            a, b = P[i], P[j]; d = b - a; L = np.hypot(*d) or 1e-9
            seg = P[i + 1:j]
            dist = np.abs(d[0] * (seg[:, 1] - a[1]) - d[1] * (seg[:, 0] - a[0])) / L
            k = int(np.argmax(dist))
            if dist[k] > tol:
                keep.append(i + 1 + k); stack += [(i, i + 1 + k), (i + 1 + k, j)]
        return [pts[i] for i in sorted(set(keep))]

    paths = {}
    for k, (p, q) in todo.items():
        s, e = cell(*p), cell(*q)
        r0, r1 = max(min(s[0], e[0]) - 250, 0), min(max(s[0], e[0]) + 250, land.shape[0])
        c0, c1 = max(min(s[1], e[1]) - 250, 0), min(max(s[1], e[1]) + 250, land.shape[1])
        sub = cost[r0:r1, c0:c1]
        sub = np.where(used[r0:r1, c0:c1] & near_port[r0:r1, c0:c1] & (sub > 0), sub * REUSE, sub)
        m = MCP_Geometric(sub, fully_connected=True)
        ls, le = (s[0] - r0, s[1] - c0), (e[0] - r0, e[1] - c0)
        m.find_costs([ls], [le])
        try:
            tr = [(r + r0, c + c0) for r, c in m.traceback(le)]
        except Exception:
            print('  no sea path', k); continue
        rr = np.array([t[0] for t in tr], float); cc = np.array([t[1] for t in tr], float)
        used[rr.astype(int), cc.astype(int)] = True
        # Smooth the grid path into a curve: the widest Gaussian that keeps it at sea.
        best = list(zip(rr, cc))
        for sigma in (7, 5, 3.5, 2):
            if len(tr) < 4: break
            sr = ndimage.gaussian_filter1d(rr, sigma, mode='nearest')
            sc = ndimage.gaussian_filter1d(cc, sigma, mode='nearest')
            # fade the smoothing out towards both ends so a route leaves and
            # reaches its harbour along the real channel (no hooks at the port)
            n = len(rr); idx = np.arange(n); T = 2.0 * sigma
            w = np.clip(np.minimum(idx, n - 1 - idx) / T, 0, 1)
            sr = w * sr + (1 - w) * rr; sc = w * sc + (1 - w) * cc
            cand = list(zip(sr, sc))
            if on_water(cand):
                best = cand; break
        poly = [ll(x) for x in simplify(best)]
        paths[k] = [[round(p[0], 4), round(p[1], 4)]] + poly + [[round(q[0], 4), round(q[1], 4)]]
    (ROOT / 'ferry-paths.json').write_text(json.dumps(paths, separators=(',', ':')))
    print(f'ferry-paths.json: {len(paths)} segments')

if __name__ == '__main__':
    main()
