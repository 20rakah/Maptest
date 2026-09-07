"""Layers 6–8: soil, vegetation, resources (follow geology + climate).

Climate owns soil/vegetation/climate_resource_tags. Geology rock tags may
merge into resource strings but Climate primary belts are climate-driven:
timber, pasture, salt_pans, fisheries (+ geology rock tags where relevant).
"""

from __future__ import annotations

import numpy as np

from .noise import fbm


# Soil codes
SOIL_LABELS = {
    0: "none/ocean",
    1: "rocky/lithosol",
    2: "glacial till",
    3: "mountain thin",
    4: "loam",
    5: "clay basin",
    6: "sandy coastal",
    7: "volcanic andisol",
    8: "arid/skeletal",
    9: "peat/wetland",
    10: "saline playa",
}

# Vegetation codes
VEG_LABELS = {
    0: "none/ocean",
    1: "ice/barren",
    2: "alpine tundra",
    3: "boreal forest",
    4: "temperate forest",
    5: "grassland/pasture",
    6: "shrub/steppe",
    7: "desert scrub",
    8: "wetland/marsh",
    9: "floodplain farmable",
    10: "coastal scrub",
    11: "salt flat sparse",
}

# Resource codes (primary map paint)
RES_LABELS = {
    0: "none",
    1: "timber",
    2: "stone",
    3: "metals",
    4: "obsidian/volcanic",
    5: "salt",
    6: "clay",
    7: "fish",
    8: "peat",
    9: "gems/rare",
    10: "pasture",
}


def build_soil(
    elev_m: np.ndarray,
    slope: np.ndarray,
    rock: np.ndarray,
    ice: np.ndarray,
    wetland: np.ndarray,
    glacial: np.ndarray | None,
    precip_mm: np.ndarray,
    salt_pan: np.ndarray | None = None,
    floodplain: np.ndarray | None = None,
) -> np.ndarray:
    h, w = elev_m.shape
    soil = np.zeros((h, w), dtype=np.int16)
    land = elev_m >= 0
    soil[land] = 4  # default loam
    soil[land & (slope > 25)] = 1
    soil[land & (elev_m > 1500)] = 3
    soil[land & (rock == 7)] = 6
    soil[land & (rock == 6)] = 5  # basin sediment → clay basin
    soil[land & ((rock == 3) | (rock == 5) | (rock == 4))] = 7
    soil[land & (precip_mm < 350)] = 8
    if glacial is not None:
        soil[land & glacial & (elev_m < 1800)] = 2
    if floodplain is not None:
        soil[floodplain & land] = 4  # alluvial loam
    soil[wetland] = 9
    if salt_pan is not None:
        soil[salt_pan] = 10
    soil[ice] = 1
    soil[elev_m < 0] = 0
    return soil


def build_vegetation(
    elev_m: np.ndarray,
    temp_c: np.ndarray,
    precip_mm: np.ndarray,
    ice: np.ndarray,
    wetland: np.ndarray,
    river: np.ndarray,
    lake: np.ndarray,
    soil: np.ndarray,
    salt_pan: np.ndarray | None = None,
    floodplain: np.ndarray | None = None,
    inland_sea: np.ndarray | None = None,
) -> np.ndarray:
    veg = np.zeros(elev_m.shape, dtype=np.int16)
    land = elev_m >= 0
    veg[land] = 6
    veg[land & (temp_c < -2)] = 2
    veg[land & (temp_c >= -2) & (temp_c < 6) & (precip_mm > 500)] = 3
    veg[land & (temp_c >= 6) & (precip_mm >= 700) & (elev_m < 1200)] = 4
    veg[land & (precip_mm >= 400) & (precip_mm < 700) & (temp_c >= 5)] = 5
    veg[land & (precip_mm < 300)] = 7
    veg[land & (elev_m > 2000) & ~ice] = 2
    veg[wetland] = 8
    # farmable floodplain near rivers with good soil/temp
    farm = land & river & (temp_c > 7) & (precip_mm > 500) & ((soil == 4) | (soil == 5)) & (elev_m < 800)
    veg[farm] = 9
    if floodplain is not None:
        veg[floodplain & (temp_c > 6) & (precip_mm > 450) & (soil == 4)] = 9
    # loamy lowlands
    veg[land & (soil == 4) & (temp_c > 8) & (precip_mm > 600) & (elev_m < 500) & (veg == 4)] = 9
    veg[land & (elev_m < 80) & (elev_m >= 0) & (veg != 8)] = 10
    if salt_pan is not None:
        veg[salt_pan] = 11
    veg[ice] = 1
    veg[lake] = 0
    if inland_sea is not None:
        veg[inland_sea] = 0
    veg[elev_m < 0] = 0
    return veg


def build_resources(
    seed: int,
    rock: np.ndarray,
    elev_m: np.ndarray,
    veg: np.ndarray,
    water_code: np.ndarray,
    geology_resource_tag: np.ndarray | None,
    *,
    salt_pan: np.ndarray | None = None,
    endorheic: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (res_code primary, res_tags full, climate_resource_tags Climate-only)."""
    h, w = elev_m.shape
    n = fbm(w, h, seed + 401, octaves=4, base_scale=9.0)
    res = np.zeros((h, w), dtype=np.int16)
    tags = np.empty((h, w), dtype=object)
    tags.fill("")
    climate_tags = np.empty((h, w), dtype=object)
    climate_tags.fill("")

    land = elev_m >= 0
    # Climate belts
    timber = land & ((veg == 3) | (veg == 4)) & (n > -0.15)
    pasture = land & ((veg == 5) | ((veg == 6) & (n > 0.0))) & (elev_m < 1600)
    # Salt pans: interior endorheic flats (ASSUMPTION C17)
    if salt_pan is not None:
        salt = salt_pan.copy()
    else:
        salt = land & (rock == 6) & (n > 0.15) & ((veg == 7) | (veg == 11))
    if endorheic is not None:
        salt = salt | (endorheic & land & (veg == 11))
        salt = salt | (endorheic & land & (rock == 6) & (water_code == 8))
    # Fisheries: ocean coast, major rivers, lakes, inland sea (ASSUMPTION C18)
    fisheries = (
        (water_code == 1)
        | (water_code == 3)
        | (water_code == 4)
        | (water_code == 5)
        | ((water_code == 2) & (n > 0.2))
    )

    # Geology-adjacent (still tagged; Climate merges)
    stone = land & ((rock == 2) | (rock == 1)) & (elev_m > 400) & (n > 0.0)
    metals = land & ((rock == 2) | (rock == 4)) & (n > 0.35)
    volc = land & ((rock == 3) | (rock == 5)) & (n > 0.2)
    clay = land & ((rock == 6) | (rock == 7)) & (n > -0.05) & ~salt
    peat = land & (veg == 8)
    gems = land & (rock == 2) & (n > 0.55)

    # priority paint for map primary code
    res[pasture] = 10
    res[timber] = 1
    res[stone] = 2
    res[clay] = 6
    res[salt] = 5
    res[volc] = 4
    res[metals] = 3
    res[peat] = 8
    res[gems] = 9
    res[fisheries & ~land] = 7
    res[fisheries & land & (res == 0)] = 7
    res[salt] = 5  # salt wins on playa

    for r in range(h):
        for q in range(w):
            cparts = []
            if timber[r, q]:
                cparts.append("timber")
            if pasture[r, q]:
                cparts.append("pasture")
            if salt[r, q]:
                cparts.append("salt_pans")
            if fisheries[r, q]:
                cparts.append("fisheries")
            climate_tags[r, q] = "|".join(cparts) if cparts else ""

            parts = list(cparts)
            if stone[r, q]:
                parts.append("stone")
            if metals[r, q]:
                parts.append("metals")
            if volc[r, q]:
                parts.append("obsidian")
            if clay[r, q]:
                parts.append("clay")
            if peat[r, q]:
                parts.append("peat")
            if gems[r, q]:
                parts.append("gems")
            if geology_resource_tag is not None:
                gt = geology_resource_tag[r, q]
                if gt and str(gt) not in parts:
                    parts.append(str(gt))
            tags[r, q] = "|".join(parts) if parts else ""

    return res, tags, climate_tags


def food_score(veg: np.ndarray, water_code: np.ndarray) -> np.ndarray:
    """Relative food potential 0–3.5 for settlement / CSV (food proxy)."""
    food = np.zeros(veg.shape, dtype=np.float64)
    food[veg == 9] = 3.0  # farmable
    food[veg == 5] = 2.0  # pasture
    food[veg == 4] = 1.5
    food[veg == 3] = 1.0
    food[veg == 8] = 1.2  # marsh forage/fish
    food[veg == 6] = 0.8
    food[veg == 11] = 0.2  # salt flat
    food[(water_code == 3) | (water_code == 4) | (water_code == 5) | (water_code == 1)] += 0.8
    food[water_code == 8] += 0.1  # salt pan: brine shrimp / limited
    return np.clip(food, 0, 3.5)
