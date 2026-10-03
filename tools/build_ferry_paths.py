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
const segs = [];
G.forEach(e => { segs.push(ends(e.a, e.b, true)); segs.push(ends(e.a, e.b, false)); });
LINES.forEach(l => { for (let i = 0; i < l.stops.length - 1; i++) {
  segs.push(ends(l.stops[i], l.stops[i + 1], !!l.sides)); } });
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
    cost = np.where(water, 1.0 + 3.0 * np.clip(1.0 - dist_land / 5.0, 0, 1), -1.0)
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
        return [round(N0 - (rc[0] + 0.5) * RES, 4), round(W0 + (rc[1] + 0.5) * RES, 4)]
    def clear(a, b):
        n = int(max(abs(a[0] - b[0]), abs(a[1] - b[1])) * 2) + 2
        rr = np.linspace(a[0], b[0], n).round().astype(int); cc = np.linspace(a[1], b[1], n).round().astype(int)
        return bool(np.all(water[rr, cc]))

    paths = {}
    for k, (p, q) in todo.items():
        s, e = cell(*p), cell(*q)
        r0, r1 = max(min(s[0], e[0]) - 250, 0), min(max(s[0], e[0]) + 250, land.shape[0])
        c0, c1 = max(min(s[1], e[1]) - 250, 0), min(max(s[1], e[1]) + 250, land.shape[1])
        m = MCP_Geometric(cost[r0:r1, c0:c1], fully_connected=True)
        ls, le = (s[0] - r0, s[1] - c0), (e[0] - r0, e[1] - c0)
        m.find_costs([ls], [le])
        try:
            tr = [(r + r0, c + c0) for r, c in m.traceback(le)]
        except Exception:
            print('  no sea path', k); continue
        # string-pull: keep only the turning points
        pts = [tr[0]]; i = 0
        while i < len(tr) - 1:
            j = len(tr) - 1
            while j > i + 1 and not clear(tr[i], tr[j]): j -= 1
            pts.append(tr[j]); i = j
        # Chaikin smoothing, up to three rounds, each kept only if it stays on water
        cur = pts
        for _ in range(3):
            sm = [cur[0]]
            for a, b in zip(cur, cur[1:]):
                sm += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]),
                       (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
            sm.append(cur[-1])
            if not all(clear(a, b) for a, b in zip(sm, sm[1:])): break
            cur = sm
        poly = [ll(x) for x in cur]
        paths[k] = [[round(p[0], 4), round(p[1], 4)]] + poly + [[round(q[0], 4), round(q[1], 4)]]
    (ROOT / 'ferry-paths.json').write_text(json.dumps(paths, separators=(',', ':')))
    print(f'ferry-paths.json: {len(paths)} segments')

if __name__ == '__main__':
    main()
