"""Layer 9: settlement_score — tiers only, no borders/nations.

Tiers: none / farmstead / village / town / city-candidate
Leave ~15–25% of city-candidate-quality sites EMPTY on purpose (seeded).
"""

from __future__ import annotations

import numpy as np

from . import config as C
from .noise import rng


def score_settlements(
    seed: int,
    elev_m: np.ndarray,
    slope: np.ndarray,
    water_code: np.ndarray,
    wt_depth_m: np.ndarray,
    food: np.ndarray,
    ice: np.ndarray,
    veg: np.ndarray,
    wt_class: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    h, w = elev_m.shape
    land = elev_m >= 0
    raw = np.zeros((h, w), dtype=np.float64)

    # Fresh water access
    fresh = np.isin(water_code, (2, 3, 4, 5, 6)) | ((wt_depth_m <= 4.0) & land)
    raw += np.where(fresh, 2.5, 0.0)
    raw += np.where(water_code == 3, 0.8, 0.0)  # major river bonus
    raw += np.where(water_code == 1, 0.6, 0.0)  # coast route/fish (brackish less fresh)

    # Food
    raw += food

    # Route: river / coast / low-slope corridor
    route = (
        np.isin(water_code, (1, 2, 3))
        | ((slope < 8.0) & land & (elev_m < 900))
    )
    raw += np.where(route, 1.5, 0.0)
    raw += np.where((slope < 4.0) & land, 0.5, 0.0)

    # Minuses
    raw -= np.where(slope > 20.0, 2.0, 0.0)
    raw -= np.where(slope > 35.0, 2.0, 0.0)
    raw -= np.where(ice, 5.0, 0.0)
    arid_no_water = land & (food < 0.5) & ~fresh & (water_code == 0)
    raw -= np.where(arid_no_water, 3.0, 0.0)
    raw -= np.where(water_code == 8, 2.5, 0.0)  # salt pan / playa
    deep_marsh = (veg == 8) & (water_code == 6) & (slope < 2)
    raw -= np.where(deep_marsh, 1.5, 0.0)
    raw -= np.where(food < 0.3, 1.5, 0.0)
    raw[elev_m < 0] = -99
    raw[ice] = -99
    # Open water bodies are not settleable hexes (fisheries counted on adjacent coasts/shores)
    open_water = np.isin(water_code, (1, 4, 5))
    raw[open_water] = -99

    # Tier from buckets
    tier = np.empty((h, w), dtype=object)
    tier.fill("none")
    tier[raw >= C.TIER_THRESHOLDS["farmstead"]] = "farmstead"
    tier[raw >= C.TIER_THRESHOLDS["village"]] = "village"
    tier[raw >= C.TIER_THRESHOLDS["town"]] = "town"
    tier[raw >= C.TIER_THRESHOLDS["city-candidate"]] = "city-candidate"
    tier[elev_m < 0] = "none"
    tier[ice] = "none"
    tier[open_water] = "none"

    # Leave ~15–25% of city-candidate-quality sites empty (ASSUMPTION default 20%)
    g = rng(seed + 501)
    city_mask = tier == "city-candidate"
    city_idx = np.argwhere(city_mask)
    n_empty = int(round(len(city_idx) * C.EMPTY_CITY_CANDIDATE_FRAC))
    why = np.empty((h, w), dtype=object)
    why.fill("")

    if n_empty > 0 and len(city_idx) > 0:
        pick = g.choice(len(city_idx), size=min(n_empty, len(city_idx)), replace=False)
        for i in pick:
            r, q = int(city_idx[i][0]), int(city_idx[i][1])
            tier[r, q] = "none"
            why[r, q] = "excellent site left empty on purpose"

    # Reasons for remaining cells
    for r in range(h):
        for q in range(w):
            if why[r, q]:
                continue
            t = tier[r, q]
            if elev_m[r, q] < 0:
                why[r, q] = "ocean"
                continue
            if water_code[r, q] in (4, 5):
                why[r, q] = "open water (lake/inland sea)"
                continue
            if ice[r, q]:
                why[r, q] = "glacial/ice"
                continue
            if t == "none":
                bits = []
                if not fresh[r, q]:
                    bits.append("no reliable fresh water")
                if food[r, q] < 0.5:
                    bits.append("poor food")
                if slope[r, q] > 20:
                    bits.append("too steep")
                if arid_no_water[r, q]:
                    bits.append("arid interior")
                why[r, q] = "; ".join(bits) if bits else "low suitability"
                continue
            parts = []
            if fresh[r, q]:
                # Distinguish surface water vs groundwater (Referee TABLE)
                if int(water_code[r, q]) in (2, 3, 4, 5, 6):
                    parts.append("fresh water")
                elif wt_class is not None:
                    wc = str(wt_class[r, q])
                    if wc == "spring_line":
                        parts.append("spring line")
                    elif wc == "shallow_well":
                        parts.append("shallow well")
                    else:
                        parts.append("groundwater")
                else:
                    parts.append("groundwater")
            if food[r, q] >= 2:
                parts.append("strong food")
            elif food[r, q] >= 1:
                parts.append("adequate food")
            if route[r, q]:
                parts.append("route access")
            if water_code[r, q] == 3:
                parts.append("major river")
            if water_code[r, q] == 1:
                parts.append("coast")
            why[r, q] = ", ".join(parts) if parts else t

    return {
        "raw_score": raw,
        "settle_score": tier,  # tier name as required
        "why": why,
        "fresh": fresh,
        "route": route,
    }
