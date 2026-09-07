"""Fixes for Referee HOLD on geology package."""
from __future__ import annotations

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
