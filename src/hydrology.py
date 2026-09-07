"""Layers 4–5: ice_surface_water and water_table.

Rivers flow downhill and join. Endorheic basin holds inland sea/lake.
Residual ice on spine/north after ~1000 yr BP deglaciation (ASSUMPTION).
"""

from __future__ import annotations

import numpy as np

from . import config as C
from .noise import fbm


def residual_ice(
    elev_m: np.ndarray,
    qf: np.ndarray,
    rf: np.ndarray,
    ice_mult: float,
    glacial_mask: np.ndarray | None = None,
) -> np.ndarray:
    """Boolean residual ice. Prefer Geologist glacial mask for extent cue."""
    spine = np.abs(qf - C.SUTURE_Q_FRAC) / C.SUTURE_WIDTH_FRAC
    cold_high = (elev_m > (2200.0 / max(ice_mult, 0.25))) & (spine < 1.3)
    north_high = (rf < 0.28) & (elev_m > (1600.0 / max(ice_mult, 0.25)))
    ice = cold_high | north_high
    if glacial_mask is not None and glacial_mask.any():
        # residual ice only where formerly glaciated AND still high/cold
        ice = ice & glacial_mask
    if ice_mult <= 0:
        ice = np.zeros_like(ice)
    return ice & (elev_m >= 0)


def build_surface_water(
    seed: int,
    elev_m: np.ndarray,
    precip_mm: np.ndarray,
    ice: np.ndarray,
    endorheic: np.ndarray,
    sea_level_is_ocean: np.ndarray,
) -> dict[str, np.ndarray]:
    """Rivers via steepest-descent accumulation; lakes in sinks / endorheic basin."""
    h, w = elev_m.shape
    land = ~sea_level_is_ocean

    # Flow direction: 6 axial neighbors, pick lowest elev
    nbrs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
    flow_dq = np.zeros((h, w), dtype=np.int8)
    flow_dr = np.zeros((h, w), dtype=np.int8)
    pit = np.zeros((h, w), dtype=np.bool_)

    for r in range(h):
        for q in range(w):
            if not land[r, q] or ice[r, q]:
                continue
            best = elev_m[r, q]
            bdq = bdq_r = 0
            found = False
            for dq, dr in nbrs:
                nq, nr = q + dq, r + dr
                if 0 <= nq < w and 0 <= nr < h:
                    if elev_m[nr, nq] < best - 0.01:
                        best = elev_m[nr, nq]
                        bdq, bdq_r = dq, dr
                        found = True
            if found:
                flow_dq[r, q] = bdq
                flow_dr[r, q] = bdq_r
            else:
                pit[r, q] = True

    # Upstream accumulation order: process high → low
    order = np.argsort(-elev_m.ravel())
    accum = np.zeros((h, w), dtype=np.float64)
    # runoff proxy
    runoff = np.where(land & ~ice, np.clip(precip_mm / 800.0, 0.05, 4.0), 0.0)
    accum += runoff

    for idx in order:
        r, q = divmod(int(idx), w)
        if not land[r, q] or ice[r, q]:
            continue
        dq, dr = int(flow_dq[r, q]), int(flow_dr[r, q])
        if dq == 0 and dr == 0:
            continue
        nq, nr = q + dq, r + dr
        if 0 <= nq < w and 0 <= nr < h and land[nr, nq]:
            accum[nr, nq] += accum[r, q]

    # River threshold ASSUMPTION
    river = (accum >= 8.0) & land & ~ice
    # Major river
    major = (accum >= 28.0) & land & ~ice

    # Lakes: pits with enough accum, plus endorheic basin floor
    lake = pit & land & ~ice & (accum >= 3.0)
    # Inland sea in endorheic low area
    if endorheic is not None:
        basin_low = endorheic & land & (elev_m < np.nanpercentile(elev_m[endorheic & land], 35))
        lake = lake | basin_low
        # drown lowest basin cells as inland sea
        if basin_low.any():
            thr = np.nanpercentile(elev_m[endorheic & land], 25)
            inland_sea = endorheic & land & (elev_m <= thr) & ~ice
            lake = lake | inland_sea

    # Wetlands: flat + wet near rivers/lakes
    wet = land & ~ice & ~lake & (precip_mm > 900) & (elev_m < 200) & (
        (accum > 4) | _dilate(lake | river, 1)
    )

    # Water class codes for maps/CSV
    # 0=none/dry, 1=coast/ocean, 2=river, 3=major_river, 4=lake, 5=inland_sea, 6=wetland, 7=ice
    water = np.zeros((h, w), dtype=np.int16)
    water[sea_level_is_ocean] = 1
    water[wet] = 6
    water[river] = 2
    water[major] = 3
    water[lake] = 4
    # inland sea: endorheic lakes that are larger cluster — mark deep basin lakes as 5
    if endorheic is not None:
        water[lake & endorheic & (elev_m < np.nanmedian(elev_m[lake & endorheic]) if (lake & endorheic).any() else 0)] = 5
    water[ice] = 7

    return {
        "accum": accum,
        "river": river,
        "major_river": major,
        "lake": lake,
        "wetland": wet,
        "ice": ice,
        "water_code": water,
        "flow_dq": flow_dq,
        "flow_dr": flow_dr,
        "pit": pit,
    }


def _dilate(mask: np.ndarray, steps: int = 1) -> np.ndarray:
    out = mask.copy()
    nbrs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]
    h, w = mask.shape
    for _ in range(steps):
        nxt = out.copy()
        for dq, dr in nbrs:
            rolled = np.roll(np.roll(out, dr, axis=0), dq, axis=1)
            # avoid wrap: clear edges after roll
            nxt |= rolled
        nxt[0, :] = out[0, :]
        nxt[-1, :] = out[-1, :]
        nxt[:, 0] = out[:, 0]
        nxt[:, -1] = out[:, -1]
        out = nxt
    return out


def build_water_table(
    elev_m: np.ndarray,
    precip_mm: np.ndarray,
    surface: dict[str, np.ndarray],
    seed: int,
) -> dict[str, np.ndarray]:
    """Relative water-table depth (m below surface). Lower = wetter / shallower WT.

    ASSUMPTION: WT rises near rivers/lakes/coast and with precip; deep under arid highs.
    """
    h, w = elev_m.shape
    land = elev_m >= 0
    n = fbm(w, h, seed + 301, octaves=3, base_scale=14.0)
    # depth below ground (positive = deeper unsaturated)
    depth = 12.0 - 8.0 * np.clip(precip_mm / 1200.0, 0, 1.5) + 4.0 * n
    depth += np.clip(elev_m / 800.0, 0, 3) * 3.0
    depth = np.where(surface["river"] | surface["major_river"], np.minimum(depth, 1.5), depth)
    depth = np.where(surface["lake"], 0.0, depth)
    depth = np.where(surface["wetland"], np.minimum(depth, 0.8), depth)
    # coastal shallow
    ocean = elev_m < 0
    near = _dilate(ocean, 2) & land
    depth = np.where(near, np.minimum(depth, 2.5), depth)
    depth = np.where(surface["ice"], 99.0, depth)  # frozen / irrelevant
    depth = np.where(ocean, 0.0, depth)
    depth = np.clip(depth, 0.0, 80.0)

    # class: 0 ocean, 1 emergent/spring, 2 shallow, 3 moderate, 4 deep, 5 arid-deep, 6 ice
    wt_code = np.zeros((h, w), dtype=np.int16)
    wt_code[land & (depth <= 1.0)] = 1
    wt_code[land & (depth > 1.0) & (depth <= 4.0)] = 2
    wt_code[land & (depth > 4.0) & (depth <= 12.0)] = 3
    wt_code[land & (depth > 12.0) & (depth <= 25.0)] = 4
    wt_code[land & (depth > 25.0)] = 5
    wt_code[ocean] = 0
    wt_code[surface["ice"]] = 6

    return {"wt_depth_m": depth, "wt_code": wt_code}
