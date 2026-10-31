#!/usr/bin/env python3
"""Make ferry routes that share a stretch of sea run on one line (Oct 2026).

Each sea path in ferry-paths.json is computed on its own, so two boats that use
the same channel were drawn as two lines a few hundred metres apart. Paths are
processed in file order (busiest first, as build_ferry_paths.py writes them):
every interior point of a path within TOL_KM of a line already processed is
moved onto that line, so shared stretches coincide exactly and the routes split
where they really part. End points (the harbours) never move.

Run by build_ferry_paths.py; can also be run alone:  python3 tools/snap_ferry_paths.py
Pure Python, no extra packages.
"""
import json, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOL_KM, STEP_KM, CELL_KM, KEEP_KM = 3.0, 0.4, 3.0, 0.03
LAT0 = 38.0
SHORT_KM = 15        # crossings shorter than this (Glyfa-Agiokampos) are never pulled onto another route
KX, KY = 111.32 * math.cos(math.radians(LAT0)), 110.57      # km per degree


def to_xy(p): return (p[1] * KX, p[0] * KY)
def to_ll(x): return [round(x[1] / KY, 4), round(x[0] / KX, 4)]


def densify(pts):
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b); n = max(1, int(d / STEP_KM))
        out += [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(1, n + 1)]
    return out


def simplify(pts, tol):
    keep = {0, len(pts) - 1}; stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1: continue
        a, b = pts[i], pts[j]; dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) or 1e-9
        k, dm = -1, 0.0
        for m in range(i + 1, j):
            d = abs(dx * (pts[m][1] - a[1]) - dy * (pts[m][0] - a[0])) / L
            if d > dm: k, dm = m, d
        if dm > tol: keep.add(k); stack += [(i, k), (k, j)]
    return [pts[i] for i in sorted(keep)]


def snap_all(paths):
    grid = {}                                   # cell -> list of segments ((x1,y1),(x2,y2))
    def cells(a, b):
        x0, x1 = sorted((a[0], b[0])); y0, y1 = sorted((a[1], b[1]))
        for cx in range(int(x0 // CELL_KM), int(x1 // CELL_KM) + 1):
            for cy in range(int(y0 // CELL_KM), int(y1 // CELL_KM) + 1):
                yield (cx, cy)
    def nearest(p):
        cx, cy = int(p[0] // CELL_KM), int(p[1] // CELL_KM); best, bd = None, TOL_KM
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for a, b in grid.get((cx + dx, cy + dy), ()):
                    vx, vy = b[0] - a[0], b[1] - a[1]; L2 = vx * vx + vy * vy or 1e-12
                    t = max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L2))
                    q = (a[0] + t * vx, a[1] + t * vy); d = math.dist(p, q)
                    if d < bd: best, bd = q, d
        return best
    out, moved = {}, 0
    for k, ll in paths.items():
        pts = densify([to_xy(p) for p in ll])
        short = sum(math.dist(a, b) for a, b in zip(pts, pts[1:])) < SHORT_KM   # a short hop keeps its own line
        snapped = [pts[0]]
        for p in pts[1:-1]:
            q = None if short else nearest(p)
            if q: moved += 1
            snapped.append(q or p)
        snapped.append(pts[-1])
        snapped = simplify(snapped, KEEP_KM)
        for a, b in zip(snapped, snapped[1:]):
            for c in cells(a, b): grid.setdefault(c, []).append((a, b))
        res = [to_ll(p) for p in snapped]
        res[0], res[-1] = ll[0], ll[-1]          # harbours exactly as given
        out[k] = res
    return out, moved


def main():
    f = ROOT / 'ferry-paths.json'
    paths = json.loads(f.read_text())
    out, moved = snap_all(paths)
    f.write_text(json.dumps(out, separators=(',', ':')))
    print(f'snap_ferry_paths: {len(out)} paths, {moved} points moved onto a shared line')


if __name__ == '__main__':
    main()
