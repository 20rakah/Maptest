"""Fixes for Referee HOLD on geology package."""
from __future__ import annotations

import heapq

import numpy as np
from . import config as C


def slope_no_wrap(elev: np.ndarray) -> np.ndarray:
    h, w = elev.shape
    pads = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
    max_d = np.zeros_like(elev, dtype=np.float64)
    for r in range(h):
        for q in range(w):
            best = 0.0
            for dq, dr in pads:
                rr, qq = r + dr, q + dq
                if 0 <= rr < h and 0 <= qq < w:
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


def build_endorheic(elev, land, ocean, basin_dist):
    h, w = elev.shape
    cand = (basin_dist < 0.78) & land
    changed = True
    while changed:
        changed = False
        drop = []
        for r in range(h):
            for q in range(w):
                if not cand[r, q]:
                    continue
                for qq, rr in axial_neighbors(q, r, w, h):
                    if ocean[rr, qq]:
                        drop.append((q, r))
                        break
        for q, r in drop:
            if cand[r, q]:
                cand[r, q] = False
                changed = True
    rim = []
    for r in range(h):
        for q in range(w):
            if not cand[r, q]:
                continue
            for qq, rr in axial_neighbors(q, r, w, h):
                if land[rr, qq] and not cand[rr, qq]:
                    rim.append(float(elev[rr, qq]))
    elev_out = elev.copy()
    if not rim or not cand.any():
        return np.zeros_like(land, dtype=bool), elev_out
    sill = min(rim)
    for r in range(h):
        for q in range(w):
            if cand[r, q]:
                # Keep floor above sea level so carve cannot create fake ocean contacts.
                target = sill - 40.0 - 60.0 * max(0.0, 1.0 - float(basin_dist[r, q]))
                target = max(target, 8.0)
                if elev_out[r, q] > target:
                    elev_out[r, q] = target
    endo = cand & (elev_out < (sill - 5.0)) & land
    for r in range(h):
        for q in range(w):
            if not endo[r, q]:
                continue
            for qq, rr in axial_neighbors(q, r, w, h):
                if ocean[rr, qq]:
                    endo[r, q] = False
                    break
    return endo, elev_out



def priority_flood_to_ocean(elev, land, ocean, endorheic):
    """Raise non-endorheic land pits so steepest-descent reaches ocean.

    ASSUMPTION: Priority-flood fill from ocean; intentional endorheic interior skipped
    then re-enforced below its rim. Exterior catchments that would spill into the basin
    are filled toward ocean instead.
    """
    h, w = elev.shape
    out = elev.astype(np.float64).copy()
    filled = np.full((h, w), np.inf, dtype=np.float64)
    visited = np.zeros((h, w), dtype=bool)
    heap = []

    for r in range(h):
        for q in range(w):
            if ocean[r, q]:
                filled[r, q] = out[r, q]
                visited[r, q] = True
                heapq.heappush(heap, (filled[r, q], q, r))

    while heap:
        level, q, r = heapq.heappop(heap)
        if level > filled[r, q] + 1e-9:
            continue
        for qq, rr in axial_neighbors(q, r, w, h):
            if visited[rr, qq]:
                continue
            if endorheic[rr, qq]:
                # Do not flood-fill through the closed basin
                continue
            if not land[rr, qq] and not ocean[rr, qq]:
                continue
            # Pit fill: cannot be lower than the spill path from ocean
            cand = max(float(out[rr, qq]), float(level))
            visited[rr, qq] = True
            filled[rr, qq] = cand
            out[rr, qq] = cand
            heapq.heappush(heap, (cand, qq, rr))

    # Any unvisited non-endorheic land (shouldn't happen if continent connected) — raise to neighbor spill
    for r in range(h):
        for q in range(w):
            if land[r, q] and not endorheic[r, q] and not visited[r, q]:
                # connected via land only; seed from nearest visited land/ocean neighbour max
                neigh = [filled[rr, qq] for qq, rr in axial_neighbors(q, r, w, h) if visited[rr, qq]]
                spill = min(neigh) if neigh else float(out[r, q])
                out[r, q] = max(float(out[r, q]), spill)
                filled[r, q] = out[r, q]
                visited[r, q] = True

    # Re-enforce closed basin: rim from surrounding non-endo land, floor below sill
    rim = []
    for r in range(h):
        for q in range(w):
            if not endorheic[r, q]:
                continue
            for qq, rr in axial_neighbors(q, r, w, h):
                if land[rr, qq] and not endorheic[rr, qq]:
                    rim.append(float(out[rr, qq]))
    if rim and endorheic.any():
        sill = min(rim)
        # Boost rim cells slightly so exterior prefers ocean paths
        for r in range(h):
            for q in range(w):
                if not endorheic[r, q]:
                    continue
                for qq, rr in axial_neighbors(q, r, w, h):
                    if land[rr, qq] and not endorheic[rr, qq]:
                        out[rr, qq] = max(float(out[rr, qq]), sill)
        sill = min(
            float(out[rr, qq])
            for r in range(h)
            for q in range(w)
            if endorheic[r, q]
            for qq, rr in axial_neighbors(q, r, w, h)
            if land[rr, qq] and not endorheic[rr, qq]
        )
        for r in range(h):
            for q in range(w):
                if endorheic[r, q]:
                    target = max(8.0, sill - 50.0)
                    out[r, q] = min(float(out[r, q]), target)
                    if out[r, q] >= sill - 5.0:
                        out[r, q] = sill - 20.0
    return out
