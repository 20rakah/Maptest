"""Layer 1–2 toy plates/rock + elevation/slope (locked physical history).

TOY FALLBACK for packaging when Geologist data is absent.
If data/geology_hex.csv exists, use src/geology_ingest.py instead and do NOT
overwrite Geologist-owned geology_hex.csv/.json or geology map PNGs.
"""

from __future__ import annotations

import numpy as np

from . import config as C
from .noise import fbm, value_noise


def _grid_fracs() -> tuple[np.ndarray, np.ndarray]:
    """Return q_frac, r_frac shaped (ROWS, COLS) in [0,1]."""
    qq, rr = np.meshgrid(np.arange(C.COLS), np.arange(C.ROWS))
    qf = qq.astype(np.float64) / max(C.COLS - 1, 1)
    rf = rr.astype(np.float64) / max(C.ROWS - 1, 1)
    return qf, rf


def build_plates_rock(seed: int) -> dict[str, np.ndarray]:
    """Tectonic / rock units constrained by Geologist lock.

    Returns dict with plate_id, rock codes, distance fields, qf/rf.
    """
    h, w = C.ROWS, C.COLS
    qf, rf = _grid_fracs()
    n = fbm(w, h, seed + 11, octaves=4, base_scale=20.0)

    plate = np.zeros((h, w), dtype=np.int16)
    suture = C.SUTURE_Q_FRAC + 0.03 * n
    plate[qf >= suture] = 1
    aq, ar = C.ARC_CENTER
    dist_arc = np.sqrt(((qf - aq) / C.ARC_RADIUS_FRAC) ** 2 + ((rf - ar) / C.ARC_RADIUS_FRAC) ** 2)
    plate[dist_arc < 1.0] = 2
    rift_d = np.abs(rf - C.RIFT_R_FRAC) / C.RIFT_WIDTH_FRAC
    plate[(rift_d < 1.0) & (qf > 0.25) & (qf < 0.75)] = 3
    hq, hr = C.HOTSPOT
    dist_hs = np.sqrt(((qf - hq) / C.HOTSPOT_RADIUS_FRAC) ** 2 + ((rf - hr) / C.HOTSPOT_RADIUS_FRAC) ** 2)
    plate[dist_hs < 1.0] = 4

    rock = np.full((h, w), 1, dtype=np.int16)
    rock[plate == 1] = 1
    sut_d = np.abs(qf - C.SUTURE_Q_FRAC) / C.SUTURE_WIDTH_FRAC
    rock[sut_d < 1.0] = 2
    rock[plate == 2] = 3
    rock[plate == 3] = 4
    rock[plate == 4] = 5
    bq, br = C.BASIN_CENTER
    dist_b = np.sqrt(((qf - bq) / C.BASIN_RADIUS_Q) ** 2 + ((rf - br) / C.BASIN_RADIUS_R) ** 2)
    rock[dist_b < 1.0] = 6

    return {
        "plate": plate,
        "rock": rock,
        "suture_dist": sut_d,
        "arc_dist": dist_arc,
        "rift_dist": rift_d,
        "hotspot_dist": dist_hs,
        "basin_dist": dist_b,
        "qf": qf,
        "rf": rf,
    }


PLATE_LABELS = {
    0: "West craton",
    1: "East craton",
    2: "SE volcanic arc",
    3: "Northern rift",
    4: "SW hotspot",
}

ROCK_LABELS = {
    0: "Oceanic basalt",
    1: "Craton granite/gneiss",
    2: "Suture metamorphic",
    3: "Arc andesite/volcanic",
    4: "Rift volcanics",
    5: "Hotspot basalt",
    6: "Basin sediment",
    7: "Coastal sediment",
}


def build_elevation(seed: int, geo: dict, sea_level_m: float) -> dict[str, np.ndarray]:
    """Elevation (m) and slope. ASSUMPTION: continent shelf around edges."""
    h, w = C.ROWS, C.COLS
    qf, rf = geo["qf"], geo["rf"]
    base = fbm(w, h, seed + 31, octaves=6, base_scale=28.0)
    detail = fbm(w, h, seed + 47, octaves=4, base_scale=10.0)

    cx, cy = 0.50, 0.50
    oval = np.sqrt(((qf - cx) / 0.52) ** 2 + ((rf - cy) / 0.50) ** 2)
    coast_n = fbm(w, h, seed + 59, octaves=3, base_scale=16.0)
    land_score = 1.20 - oval + 0.12 * coast_n

    elev = 80.0 + 220.0 * base + 80.0 * detail

    sut = geo["suture_dist"]
    spine = np.clip(1.0 - sut, 0, 1) ** 1.4
    elev += spine * (1800.0 + 400.0 * value_noise(w, h, 8.0, seed + 71))

    arc = np.clip(1.0 - geo["arc_dist"], 0, 1)
    elev += arc * (900.0 + 600.0 * value_noise(w, h, 5.0, seed + 83))
    land_score = np.maximum(land_score, arc * 0.9)

    rift = np.clip(1.0 - geo["rift_dist"], 0, 1)
    elev -= rift * 350.0
    elev += np.clip(1.0 - np.abs(geo["rift_dist"] - 1.1), 0, 1) * 200.0 * (
        (qf > 0.25) & (qf < 0.75)
    ).astype(np.float64)

    hs = np.clip(1.0 - geo["hotspot_dist"], 0, 1) ** 1.2
    elev += hs * (1100.0 + 300.0 * value_noise(w, h, 6.0, seed + 97))

    basin = np.clip(1.0 - geo["basin_dist"], 0, 1) ** 1.1
    elev -= basin * 450.0
    in_basin = geo["basin_dist"] < 1.0
    elev = np.where(in_basin, np.maximum(elev, 40.0 + 60.0 * (1.0 - basin)), elev)

    elev = np.where(land_score > 0.12, elev, -80.0 + 40.0 * base - 200.0 * (0.12 - land_score))

    near_shore = (land_score > 0.12) & (land_score < 0.35)
    geo["rock"] = geo["rock"].copy()
    geo["rock"][near_shore & (geo["rock"] == 1)] = 7

    elev_adj = elev - sea_level_m
    slope = _slope_m_per_km(elev_adj)

    return {
        "elev_m": elev_adj,
        "elev_raw_m": elev,
        "slope": slope,
        "land_score": land_score,
        "is_ocean": elev_adj < 0,
    }


def _slope_m_per_km(elev: np.ndarray) -> np.ndarray:
    """Approximate slope magnitude using axial neighbors."""
    h, w = elev.shape
    pads = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
    max_d = np.zeros_like(elev)
    for dq, dr in pads:
        shifted = np.roll(np.roll(elev, -dr, axis=0), -dq, axis=1)
        d = np.abs(shifted - elev) / C.HEX_KM
        max_d = np.maximum(max_d, d)
    max_d[0, :] *= 0.5
    max_d[-1, :] *= 0.5
    max_d[:, 0] *= 0.5
    max_d[:, -1] *= 0.5
    return max_d


def apply_glacial_carving(elev: np.ndarray, seed: int, ice_mult: float) -> np.ndarray:
    """Simple LGM elev edits. ASSUMPTION: ice age ended 1000 yr BP."""
    h, w = elev.shape
    qf, rf = _grid_fracs()
    out = elev.copy()
    spine_d = np.abs(qf - C.SUTURE_Q_FRAC) / C.SUTURE_WIDTH_FRAC
    lgm = (rf < C.LGM_NORTH_EDGE_FRAC) | ((spine_d < 1.2) & (elev > 800))
    carve = fbm(w, h, seed + 101, octaves=3, base_scale=12.0)
    trough = (carve < -0.15).astype(np.float64) * lgm.astype(np.float64)
    out -= trough * (120.0 + 80.0 * (-carve)) * ice_mult
    out[lgm & (elev > 1200)] -= 40.0 * ice_mult
    return out
