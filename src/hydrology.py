"""Layers 4–5: ice_surface_water and water_table.

Rivers flow downhill and join. Endorheic A19 catchment (~939 hexes) holds
inland sea on deep floor + salt-pan / playa on flat sill (~589 m) — NOT the
old 197-hex playa model. Residual ice on spine/north after ~1000 yr BP (ASSUMPTION).
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
    """Rivers via steepest-descent accumulation; lakes/inland sea; floodplains.

    Large endorheic catchment (ASSUMPTION C10 / Geology A19):
      - Deep floor (elev << flat sill ~589 m) → inland_sea
      - Flat sill catchment → salt_pan / seasonal playa, not permanent lake
      - Endorheic rivers terminate in basin sinks (never coded as ocean outlet)
    """
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
    runoff = np.where(land & ~ice, np.clip(precip_mm / 800.0, 0.05, 4.0), 0.0)
    # Post-LGM melt bump on formerly glaciated high runoff (ASSUMPTION C2)
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

    # River threshold ASSUMPTION A12 / C11
    river = (accum >= 8.0) & land & ~ice
    major = (accum >= 28.0) & land & ~ice

    # --- Endorheic inland water scaled to ~939-hex catchment ---
    inland_sea = np.zeros((h, w), dtype=np.bool_)
    salt_pan = np.zeros((h, w), dtype=np.bool_)
    lake = pit & land & ~ice & (accum >= 3.0)

    if endorheic is not None and endorheic.any():
        endo_land = endorheic & land
        e_vals = elev_m[endo_land]
        # Flat sill dominates (~589 m); deep floor is the real standing water
        sill = float(np.nanpercentile(e_vals, 60))  # ~588.76
        # Deep permanent water: well below sill (ASSUMPTION C12)
        inland_sea = endo_land & ~ice & (elev_m <= sill - 50.0)
        # Also mark very low absolute floor
        inland_sea = inland_sea | (endo_land & ~ice & (elev_m < 120.0))
        # Local lakes: pits inside endorheic that are not deep sea, with accum
        lake = (lake & ~inland_sea) | (
            pit & endo_land & ~ice & ~inland_sea & (accum >= 5.0) & (elev_m < sill - 5.0)
        )
        # Flat sill / playa: salt pans where arid + flat + not permanent water
        flat_sill = endo_land & ~ice & ~inland_sea & ~lake & (elev_m >= sill - 5.0)
        salt_pan = flat_sill & (precip_mm < 650.0)
        # Do NOT paint entire flat catchment as lake
        lake = lake & ~salt_pan
        # Remove spurious "lakes" that were only flat sill cells
        lake = lake & ~(endo_land & (elev_m >= sill - 5.0) & ~pit)

    # Exorheic lakes stay as pit lakes
    if endorheic is not None:
        lake = lake | (pit & land & ~ice & ~endorheic & (accum >= 3.0))
    lake = lake & ~inland_sea

    # Wetlands: flat + wet near rivers/lakes (not salt pans)
    wet = (
        land
        & ~ice
        & ~lake
        & ~inland_sea
        & ~salt_pan
        & (precip_mm > 900)
        & (elev_m < 250)
        & ((accum > 4) | _dilate(lake | river | inland_sea, 1))
    )
    # Seasonal fringe wetlands around inland sea (ASSUMPTION C13)
    # Carve a 1-hex ring out of salt_pan / dry sill next to permanent water.
    if endorheic is not None and inland_sea.any():
        fringe = _dilate(inland_sea, 1) & endorheic & land & ~inland_sea & ~ice
        wet = wet | fringe
        salt_pan = salt_pan & ~wet

    # Floodplains: low-slope corridor beside rivers (ASSUMPTION C14)
    floodplain = (
        land
        & ~ice
        & ~lake
        & ~inland_sea
        & ~salt_pan
        & ~wet
        & (elev_m < 900)
        & _dilate(river | major, 1)
        & (accum >= 4.0)
    )
    # Prefer gentler cells: exclude very steep via elev local relief proxy later in soil

    # Water class codes for maps/CSV
    # 0=none/dry, 1=coast/ocean, 2=river, 3=major_river, 4=lake,
    # 5=inland_sea, 6=wetland, 7=ice, 8=salt_pan
    water = np.zeros((h, w), dtype=np.int16)
    water[sea_level_is_ocean] = 1
    water[salt_pan] = 8
    water[wet] = 6
    water[floodplain & (water == 0)] = 0  # floodplain is overlay flag, not water_code
    water[river] = 2
    water[major] = 3
    water[lake] = 4
    water[inland_sea] = 5
    water[ice] = 7

    return {
        "accum": accum,
        "river": river,
        "major_river": major,
        "lake": lake,
        "inland_sea": inland_sea,
        "salt_pan": salt_pan,
        "wetland": wet,
        "floodplain": floodplain,
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
    endorheic: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    """Water-table depth + Climate wt_class.

    wt_class (Climate-owned, ASSUMPTION C15):
      marsh       — wetland / emergent / inland-sea fringe / depth ≤ 0.8 m
      spring_line — emergent springs / slope-break shallow (≤ 2 m) near relief
      shallow_well— reachable wells 0.8–8 m
      dry         — deep / arid > 8 m (or ice / ocean n/a → dry for land arid)
    """
    h, w = elev_m.shape
    land = elev_m >= 0
    n = fbm(w, h, seed + 301, octaves=3, base_scale=14.0)
    depth = 12.0 - 8.0 * np.clip(precip_mm / 1200.0, 0, 1.5) + 4.0 * n
    depth += np.clip(elev_m / 800.0, 0, 3) * 3.0
    depth = np.where(surface["river"] | surface["major_river"], np.minimum(depth, 1.5), depth)
    depth = np.where(surface["lake"] | surface.get("inland_sea", False), 0.0, depth)
    depth = np.where(surface["wetland"], np.minimum(depth, 0.8), depth)
    if "salt_pan" in surface:
        # Saline flat: perched or deep depending on precip — treat as deeper unsaturated
        depth = np.where(surface["salt_pan"], np.maximum(depth, 6.0), depth)
    ocean = elev_m < 0
    near = _dilate(ocean, 2) & land
    depth = np.where(near, np.minimum(depth, 2.5), depth)
    depth = np.where(surface["ice"], 99.0, depth)
    depth = np.where(ocean, 0.0, depth)
    # Endorheic flat sill: often dry water table under playa (ASSUMPTION C16)
    if endorheic is not None and "salt_pan" in surface:
        depth = np.where(surface["salt_pan"], np.clip(depth, 8.0, 40.0), depth)
    depth = np.clip(depth, 0.0, 80.0)

    # Legacy numeric code for map 05
    wt_code = np.zeros((h, w), dtype=np.int16)
    wt_code[land & (depth <= 1.0)] = 1
    wt_code[land & (depth > 1.0) & (depth <= 4.0)] = 2
    wt_code[land & (depth > 4.0) & (depth <= 12.0)] = 3
    wt_code[land & (depth > 12.0) & (depth <= 25.0)] = 4
    wt_code[land & (depth > 25.0)] = 5
    wt_code[ocean] = 0
    wt_code[surface["ice"]] = 6

    # Climate wt_class strings
    wt_class = np.full((h, w), "dry", dtype=object)
    wt_class[~land] = "dry"  # ocean: not a well class; keep dry/n/a as dry
    wt_class[surface["ice"]] = "dry"
    shallow = land & ~surface["ice"] & (depth > 0.8) & (depth <= 8.0)
    wt_class[shallow] = "shallow_well"
    # spring_line: very shallow near rivers, coasts, or slope breaks
    spring = land & ~surface["ice"] & (depth <= 2.0) & (
        surface["river"] | surface["major_river"] | near | (elev_m > 400)
    )
    # Prefer spring along mountain fronts: high elev neighbor contrast
    elev_pad_e = np.pad(elev_m, ((0, 0), (0, 1)), mode="edge")[:, 1:]
    elev_pad_w = np.pad(elev_m, ((0, 0), (1, 0)), mode="edge")[:, :-1]
    relief = np.maximum(np.abs(elev_m - elev_pad_e), np.abs(elev_m - elev_pad_w))
    spring = spring | (land & ~surface["ice"] & (depth <= 2.5) & (relief > 80) & (precip_mm > 500))
    wt_class[spring] = "spring_line"
    marsh = land & ~surface["ice"] & (
        surface["wetland"] | (depth <= 0.8) | surface.get("inland_sea", np.zeros_like(land))
    )
    # inland sea surface = marsh-class water table at surface for mapping wells? use marsh
    wt_class[marsh] = "marsh"
    # salt pans stay dry (saline, not potable marsh)
    if "salt_pan" in surface:
        wt_class[surface["salt_pan"]] = "dry"
    wt_class[ocean] = "dry"

    return {"wt_depth_m": depth, "wt_code": wt_code, "wt_class": wt_class}
