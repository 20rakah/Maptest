"""Drainage-safe elevation fixes for Referee HOLD."""
from __future__ import annotations

from collections import deque

import numpy as np

from . import config as C


def slope_no_wrap(elev: np.ndarray) -> np.ndarray:
    h, w = elev.shape
    max_d = np.zeros_like(elev, dtype=np.float64)
    for r in range(h):
        for q in range(w):
            best = 0.0
            for qq, rr in axial_neighbors(q, r, w, h):
                d = abs(float(elev[rr, qq]) - float(elev[r, q])) / C.HEX_KM
                if d > best:
                    best = d
            max_d[r, q] = best
    return max_d


def axial_neighbors(q, r, cols, rows):
    for dq, dr in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)):
        qq, rr = q + dq, r + dr
        if 0 <= qq < cols and 0 <= rr < rows:
            yield qq, rr


def _steepest(elev, q, r):
    best = None
    be = float(elev[r, q])
    h, w = elev.shape
    for qq, rr in axial_neighbors(q, r, w, h):
        ev = float(elev[rr, qq])
        if ev < be - 1e-9:
            be = ev
            best = (qq, rr)
    return best


def enforce_ocean_drainage(raw_elev, land, ocean, blocked=None):
    """Raise-only spanning tree from ocean so every reached land cell drains to sea."""
    h, w = raw_elev.shape
    if blocked is None:
        blocked = np.zeros((h, w), dtype=bool)
    parent = np.full((h, w, 2), -1, dtype=np.int32)
    order = []
    dq = deque()
    visited = ocean.copy()
    for r in range(h):
        for q in range(w):
            if ocean[r, q]:
                dq.append((q, r))
    while dq:
        q, r = dq.popleft()
        for qq, rr in axial_neighbors(q, r, w, h):
            if visited[rr, qq] or not land[rr, qq] or blocked[rr, qq]:
                continue
            visited[rr, qq] = True
            parent[rr, qq] = (q, r)
            order.append((qq, rr))
            dq.append((qq, rr))
    out = raw_elev.astype(np.float64).copy()
    for qq, rr in order:
        pq, pr = int(parent[rr, qq, 0]), int(parent[rr, qq, 1])
        parent_e = 0.0 if ocean[pr, pq] else float(out[pr, pq])
        if out[rr, qq] <= parent_e:
            out[rr, qq] = parent_e + 0.5
    reached = visited & land & ~blocked
    return out, reached


def build_endorheic_seed(elev, land, ocean, basin_dist):
    """Inland basin seed; no ocean adjacency."""
    h, w = elev.shape
    cand = (basin_dist < 0.72) & land
    changed = True
    while changed:
        changed = False
        drop = []
        for r in range(h):
            for q in range(w):
                if not cand[r, q]:
                    continue
                if any(ocean[rr, qq] for qq, rr in axial_neighbors(q, r, w, h)):
                    drop.append((q, r))
        for q, r in drop:
            if cand[r, q]:
                cand[r, q] = False
                changed = True
    return cand


def enforce_drainage(elev, land, ocean, basin_dist):
    """1) Make all land drain to ocean. 2) Insert closed basin with rim above exterior."""
    # Step 1: continent drains to ocean
    out, _ = enforce_ocean_drainage(elev, land, ocean, blocked=None)
    h, w = out.shape
    endo = build_endorheic_seed(out, land, ocean, basin_dist)
    if not endo.any():
        return out, endo

    # Exterior neighbours of the seed define the rim height
    ext_adj = []
    for r in range(h):
        for q in range(w):
            if not endo[r, q]:
                continue
            for qq, rr in axial_neighbors(q, r, w, h):
                if land[rr, qq] and not endo[rr, qq]:
                    ext_adj.append(float(out[rr, qq]))
    if not ext_adj:
        return out, np.zeros_like(endo)

    rim_h = max(ext_adj) + 10.0
    floor_h = max(8.0, min(ext_adj) - 30.0)
    if floor_h >= rim_h - 5.0:
        floor_h = rim_h - 25.0

    # Build 1-hex rim ring (also endorheic) from cells adjacent to floor
    rim = np.zeros((h, w), dtype=bool)
    for r in range(h):
        for q in range(w):
            if land[r, q] and not endo[r, q] and not ocean[r, q]:
                if any(endo[rr, qq] for qq, rr in axial_neighbors(q, r, w, h)):
                    rim[r, q] = True
    # Avoid ocean-touching rim/floor
    for r in range(h):
        for q in range(w):
            if (endo[r, q] or rim[r, q]) and any(ocean[rr, qq] for qq, rr in axial_neighbors(q, r, w, h)):
                endo[r, q] = False
                rim[r, q] = False

    for r in range(h):
        for q in range(w):
            if rim[r, q]:
                out[r, q] = max(float(out[r, q]), rim_h)
            if endo[r, q]:
                # slight inward dish using basin_dist
                out[r, q] = floor_h + 5.0 * float(basin_dist[r, q])

    endo = endo | rim

    # Re-drain exterior with basin+rim blocked; preserves rim/floor after
    drained, reached = enforce_ocean_drainage(out, land, ocean, blocked=endo)
    # Keep exterior drained elev; restore endo heights
    for r in range(h):
        for q in range(w):
            if endo[r, q]:
                if rim[r, q]:
                    out[r, q] = max(float(drained[r, q]), rim_h)
                else:
                    out[r, q] = floor_h + 5.0 * float(basin_dist[r, q])
            else:
                out[r, q] = drained[r, q]

    # Unreached land behind basin joins endo as floor
    behind = land & ~reached & ~endo & ~ocean
    endo = endo | behind
    for r in range(h):
        for q in range(w):
            if behind[r, q]:
                out[r, q] = floor_h + 5.0 * float(basin_dist[r, q])
            if endo[r, q] and any(ocean[rr, qq] for qq, rr in axial_neighbors(q, r, w, h)):
                endo[r, q] = False
                if out[r, q] <= 0:
                    out[r, q] = 0.5

    # Final guarantee: no exterior spill into endo; no exterior pits
    for _ in range(200):
        changed = False
        for r in range(h):
            for q in range(w):
                if not land[r, q] or endo[r, q]:
                    continue
                nxt = _steepest(out, q, r)
                if nxt and endo[nxt[1], nxt[0]]:
                    endo[r, q] = True
                    out[r, q] = rim_h
                    changed = True
                elif nxt is None:
                    opts = [
                        (float(out[rr, qq]), qq, rr)
                        for qq, rr in axial_neighbors(q, r, w, h)
                        if not endo[rr, qq]
                    ]
                    if opts:
                        e, qq, rr = min(opts)
                        pe = 0.0 if ocean[rr, qq] else e
                        out[r, q] = pe + 0.5
                        changed = True
                    else:
                        # only neighbours are endo/ocean-blocked — join basin
                        endo[r, q] = True
                        out[r, q] = rim_h
                        changed = True
        if not changed:
            break

    # Break remaining flats / single pits on exterior with ocean-distance nudge
    from collections import deque
    dist = np.full((h, w), np.inf)
    dq = deque()
    for r in range(h):
        for q in range(w):
            if ocean[r, q]:
                dist[r, q] = 0.0
                dq.append((q, r))
    while dq:
        q, r = dq.popleft()
        for qq, rr in axial_neighbors(q, r, w, h):
            if not np.isfinite(dist[rr, qq]) and land[rr, qq] and not endo[rr, qq]:
                dist[rr, qq] = dist[r, q] + 1.0
                dq.append((qq, rr))
    qq, rr = np.meshgrid(np.arange(w), np.arange(h))
    mask = land & ~endo & np.isfinite(dist)
    out = out.astype(np.float64)
    out[mask] = out[mask] + 0.01 * dist[mask] + 1e-4 * (qq[mask] + 1) + 1e-6 * (rr[mask] + 1)
    # Raise any leftover exterior local minima
    for r in range(h):
        for q in range(w):
            if not land[r, q] or endo[r, q]:
                continue
            if _steepest(out, q, r) is None:
                opts = [
                    (float(out[rr, qq]), qq, rr)
                    for qq, rr in axial_neighbors(q, r, w, h)
                    if not endo[rr, qq]
                ]
                if opts:
                    e, qq, rr = min(opts)
                    pe = 0.0 if ocean[rr, qq] else e
                    out[r, q] = pe + 0.5
                else:
                    endo[r, q] = True

    # Absorb any remaining exterior whose steepest path enters endo
    for _ in range(20):
        added = 0
        for r in range(h):
            for q in range(w):
                if not land[r, q] or endo[r, q]:
                    continue
                seen = set()
                cur = (q, r)
                enters = False
                for __ in range(h * w + 5):
                    if cur in seen:
                        break
                    seen.add(cur)
                    cq, cr = cur
                    if ocean[cr, cq]:
                        break
                    if endo[cr, cq]:
                        enters = True
                        break
                    nxt = _steepest(out, cq, cr)
                    if nxt is None:
                        break
                    cur = nxt
                if enters:
                    endo[r, q] = True
                    out[r, q] = rim_h
                    added += 1
        if added == 0:
            break

    return out, endo
