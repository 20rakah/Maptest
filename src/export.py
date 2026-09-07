"""Export master hexes.csv + hexes.json (Cartographer-owned). Lockstep with maps."""

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
    if slope > 30 and elev > 1200:
        return "high_peaks"
    if elev > 1800:
        return "high_mountains"
    if elev > 1000 and slope > 15:
        return "mountains"
    if elev > 600 and slope > 10:
        return "hills"
    return TERRAIN_FROM_VEG.get(veg, "mixed")


def build_rows(world: dict) -> list[dict]:
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
            # food field: short label
            if food >= 2.5:
                food_s = "rich"
            elif food >= 1.5:
                food_s = "good"
            elif food >= 0.8:
                food_s = "modest"
            elif food > 0.2:
                food_s = "poor"
            else:
                food_s = "none"
            rows.append(
                {
                    "id": hid,
                    "terrain": _terrain(veg, elev, wc, slope),
                    "water": water_label,
                    "food": food_s,
                    "resources": res_tag if res_tag else "none",
                    "settle_score": str(world["settle_score"][r, q]),
                    "why": str(world["why"][r, q]),
                    # extras
                    "q": q,
                    "r": r,
                    "elev_m": round(elev, 1),
                    "slope": round(slope, 2),
                    "precip": round(float(world["precip_mm"][r, q]), 1),
                    "temp_c": round(float(world["temp_c"][r, q]), 2),
                    "soil": SOIL_LABELS.get(int(world["soil"][r, q]), ""),
                    "vegetation": VEG_LABELS.get(veg, ""),
                    "rock": ROCK_LABELS.get(int(world["rock"][r, q]), ""),
                }
            )
    return rows


REQUIRED_COLS = ["id", "terrain", "water", "food", "resources", "settle_score", "why"]


def write_csv_json(rows: list[dict], data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    # ensure required first
    ordered = REQUIRED_COLS + [c for c in fieldnames if c not in REQUIRED_COLS]
    csv_path = data_dir / "hexes.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=ordered)
        w.writeheader()
        w.writerows(rows)
    json_path = data_dir / "hexes.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
        f.write("\n")
