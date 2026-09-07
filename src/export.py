"""Export master hexes.csv + climate_hex.csv (Climate-owned) + JSON twins."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from . import config as C
from .biosphere import RES_LABELS, SOIL_LABELS, VEG_LABELS
from .geology import ROCK_LABELS
from .ids import qr_to_id

WATER_LABELS = {
    0: "none",
    1: "ocean",
    2: "river",
    3: "major_river",
    4: "lake",
    5: "inland_sea",
    6: "wetland",
    7: "ice",
    8: "salt_pan",
}

TERRAIN_FROM_VEG = {
    0: "ocean",
    1: "ice_barren",
    2: "alpine",
    3: "boreal",
    4: "forest",
    5: "grassland",
    6: "steppe",
    7: "desert",
    8: "marsh",
    9: "farmland",
    10: "coast",
    11: "salt_flat",
}


def _terrain(veg: int, elev: float, water_code: int, slope: float) -> str:
    if elev < 0:
        return "ocean"
    if water_code == 7:
        return "ice"
    if water_code == 5:
        return "inland_sea"
    if water_code == 4:
        return "lake"
    if water_code == 8:
        return "salt_pan"
    if slope > 30 and elev > 1200:
        return "high_peaks"
    if elev > 1800:
        return "high_mountains"
    if elev > 1000 and slope > 15:
        return "mountains"
    if elev > 600 and slope > 10:
        return "hills"
    return TERRAIN_FROM_VEG.get(veg, "mixed")


def _food_label(food: float) -> str:
    if food >= 2.5:
        return "rich"
    if food >= 1.5:
        return "good"
    if food >= 0.8:
        return "modest"
    if food > 0.2:
        return "poor"
    return "none"


def build_rows(world: dict) -> list[dict]:
    """Cartographer packaging table (hexes.csv) — includes settlement."""
    rows = []
    for r in range(C.ROWS):
        for q in range(C.COLS):
            hid = qr_to_id(q, r)
            veg = int(world["veg"][r, q])
            wc = int(world["water_code"][r, q])
            elev = float(world["elev_m"][r, q])
            slope = float(world["slope"][r, q])
            food = float(world["food"][r, q])
            res_tag = world["res_tags"][r, q] or ""
            water_label = WATER_LABELS.get(wc, "none")
            rows.append(
                {
                    "id": hid,
                    "terrain": _terrain(veg, elev, wc, slope),
                    "water": water_label,
                    "food": _food_label(food),
                    "resources": res_tag if res_tag else "none",
                    "settle_score": str(world["settle_score"][r, q]),
                    "why": str(world["why"][r, q]),
                    "q": q,
                    "r": r,
                    "elev_m": round(elev, 2),
                    "slope": round(slope, 3),
                    "precip": round(float(world["precip_mm"][r, q]), 1),
                    "temp_c": round(float(world["temp_c"][r, q]), 2),
                    "soil": SOIL_LABELS.get(int(world["soil"][r, q]), ""),
                    "vegetation": VEG_LABELS.get(veg, ""),
                    "rock": ROCK_LABELS.get(int(world["rock"][r, q]), ""),
                    "endorheic": bool(world["endorheic"][r, q]),
                    "glacial_scar": (
                        str(world["glacial_scar"][r, q])
                        if world.get("glacial_scar") is not None
                        else ("" if not bool(world["glacial"][r, q]) else "glacial")
                    ),
                    "wt_class": str(world["wt_class"][r, q]),
                    "rain_shadow": bool(world["rain_shadow"][r, q]),
                    "dry_interior": bool(world["dry_interior"][r, q]),
                    "floodplain": bool(world["floodplain"][r, q]),
                }
            )
    return rows


def build_climate_rows(world: dict) -> list[dict]:
    """Climate-owned hex table joinable on id (does NOT include settlement)."""
    rows = []
    for r in range(C.ROWS):
        for q in range(C.COLS):
            hid = qr_to_id(q, r)
            veg = int(world["veg"][r, q])
            wc = int(world["water_code"][r, q])
            food = float(world["food"][r, q])
            wind = world["wind_class"][r, q]
            # windward/leeward convenience
            if wind == "windward":
                wind_side = "windward"
            elif wind == "leeward":
                wind_side = "leeward"
            else:
                wind_side = str(wind)
            rows.append(
                {
                    "id": hid,
                    "q": q,
                    "r": r,
                    "temp_c": round(float(world["temp_c"][r, q]), 2),
                    "precip_mm": round(float(world["precip_mm"][r, q]), 1),
                    "wind": wind_side,
                    "wind_strength": round(float(world["wind_strength"][r, q]), 3),
                    "rain_shadow": bool(world["rain_shadow"][r, q]),
                    "dry_interior": bool(world["dry_interior"][r, q]),
                    "seasonality": round(float(world["seasonality"][r, q]), 3),
                    "season_label": str(world["season_label"][r, q]),
                    "water_code": wc,
                    "water": WATER_LABELS.get(wc, "none"),
                    "river": bool(world["river"][r, q]),
                    "major_river": bool(world["major_river"][r, q]),
                    "lake": bool(world["lake"][r, q]),
                    "inland_sea": bool(world.get("inland_sea", np.zeros((C.ROWS, C.COLS), dtype=bool))[r, q]),
                    "salt_pan": bool(world.get("salt_pan", np.zeros((C.ROWS, C.COLS), dtype=bool))[r, q]),
                    "wetland": bool(world["wetland"][r, q]),
                    "floodplain": bool(world["floodplain"][r, q]),
                    "ice": bool(world["ice"][r, q]),
                    "wt_depth_m": round(float(world["wt_depth_m"][r, q]), 2),
                    "wt_class": str(world["wt_class"][r, q]),
                    "soil": SOIL_LABELS.get(int(world["soil"][r, q]), ""),
                    "soil_code": int(world["soil"][r, q]),
                    "vegetation": VEG_LABELS.get(veg, ""),
                    "veg_code": veg,
                    "climate_resource_tags": world["climate_resource_tags"][r, q] or "",
                    "resources_merged": world["res_tags"][r, q] or "",
                    "food_proxy": round(food, 2),
                    "food": _food_label(food),
                    "endorheic": bool(world["endorheic"][r, q]),
                }
            )
    return rows


REQUIRED_COLS = ["id", "terrain", "water", "food", "resources", "settle_score", "why"]


def write_csv_json(rows: list[dict], data_dir: Path, stem: str = "hexes") -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    if stem == "hexes":
        ordered = REQUIRED_COLS + [c for c in fieldnames if c not in REQUIRED_COLS]
    else:
        ordered = fieldnames
    csv_path = data_dir / f"{stem}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ordered)
        w.writeheader()
        w.writerows(rows)
    json_path = data_dir / f"{stem}.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
        f.write("\n")
