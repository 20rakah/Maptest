"""Ingest Geologist-owned hex tables when present.

Cartographer toy geology (src/geology.py) runs when data/geology_hex.csv is absent.
When present, we load elevation / lithology / glacial / endorheic / geology_resource_tag
and do NOT overwrite Geologist files (geology_hex.csv/.json or geology map PNGs).

Expected columns (flexible; missing → ASSUMPTION fallbacks documented in ASSUMPTIONS.md):
  id or hex_id (required)
  elev_m or elevation_m
  lithology or rock or rock_unit
  glacial_scar or glacial or glacial_carved (tags / 0/1 / bool-ish)
  endorheic (0/1)
  geology_resource_tag or resource_tag
  slope (optional)
  land (optional)
  mountain_type (optional)
  plate or plate_id (optional)
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from . import config as C
from .ids import qr_to_id

GEOLOGY_CSV = "geology_hex.csv"
GEOLOGY_JSON = "geology_hex.json"

# Map basenames Geologist may own — never overwrite if geology CSV present.
GEOLOGY_OWNED_MAP_STEMS = (
    "plates_rock",
    "01_plates_rock",
    "elevation_slope",
    "02_elevation_slope",
    "02_elevation",
    "02_slope",
    "elevation",
    "slope",
    "geology",
    "lithology",
    "glacial",
    "glacial_scars",
    "endorheic",
    "mountain_type",
    "land_ocean",
)


def geology_csv_path(data_dir: Path) -> Path:
    return data_dir / GEOLOGY_CSV


def geology_data_present(data_dir: Path) -> bool:
    return geology_csv_path(data_dir).is_file()


def _truthy(v: str | None) -> bool:
    if v is None:
        return False
    return str(v).strip().lower() in ("1", "true", "yes", "y", "t")


def _float(row: dict, *keys: str, default: float = 0.0) -> float:
    for k in keys:
        if k in row and row[k] not in (None, ""):
            try:
                return float(row[k])
            except ValueError:
                continue
    return default


def _str(row: dict, *keys: str, default: str = "") -> str:
    for k in keys:
        if k in row and row[k] not in (None, ""):
            return str(row[k]).strip()
    return default


# Exact Geologist lithology strings → rock int codes (geology.ROCK_LABELS)
_LITHO_EXACT = {
    "oceanic_basalt": 0,
    "craton_granite_gneiss": 1,
    "suture_metamorphic": 2,
    "arc_andesite_volcanic": 3,
    "rift_volcanics": 4,
    "hotspot_basalt": 5,
    "basin_sediment": 6,
    "coastal_sediment": 7,
}

# Fuzzy fallback: more-specific tokens BEFORE generic ones (basalt/sediment/volcanic).
_LITHO_FUZZY = (
    ("coastal", 7),
    ("hotspot", 5),
    ("rift", 4),
    ("andesite", 3),
    ("arc", 3),
    ("suture", 2),
    ("metamorphic", 2),
    ("granite", 1),
    ("gneiss", 1),
    ("craton", 1),
    ("basin", 6),
    ("alluvium", 6),
    ("sandstone", 7),
    ("oceanic", 0),
    ("sediment", 6),  # after coastal
    ("volcanic", 3),  # after rift/hotspot
    ("basalt", 0),  # after hotspot/oceanic
)


def lithology_to_rock_code(text: str) -> int:
    t = text.lower().strip().replace(" ", "_").replace("/", "_")
    if t in _LITHO_EXACT:
        return _LITHO_EXACT[t]
    for key, code in _LITHO_FUZZY:
        if key in t:
            return code
    return 1  # ASSUMPTION: unknown → craton granite


def load_geology_hex(data_dir: Path) -> dict[str, np.ndarray] | None:
    """Load Geologist CSV into (ROWS, COLS) arrays keyed like toy geology outputs.

    Returns None if file missing. Raises ValueError on id/grid mismatch.
    """
    path = geology_csv_path(data_dir)
    if not path.is_file():
        return None

    elev = np.full((C.ROWS, C.COLS), np.nan, dtype=np.float64)
    rock = np.full((C.ROWS, C.COLS), 1, dtype=np.int16)
    plate = np.zeros((C.ROWS, C.COLS), dtype=np.int16)
    glacial = np.zeros((C.ROWS, C.COLS), dtype=np.bool_)
    endorheic = np.zeros((C.ROWS, C.COLS), dtype=np.bool_)
    geo_res = np.empty((C.ROWS, C.COLS), dtype=object)
    geo_res.fill("")
    slope = np.full((C.ROWS, C.COLS), np.nan, dtype=np.float64)
    seen = 0

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
        if "id" not in fields and "hex_id" not in fields:
            raise ValueError(f"{path} must have an 'id' or 'hex_id' column")
        for row in reader:
            hid = (row.get("id") or row.get("hex_id") or "").strip()
            # Parse H+qqq+rrr
            if not (hid.startswith("H") and len(hid) >= 7):
                raise ValueError(f"Bad hex id in geology CSV: {hid!r}")
            q = int(hid[1:4])
            r = int(hid[4:7])
            if not (0 <= q < C.COLS and 0 <= r < C.ROWS):
                raise ValueError(f"Hex {hid} out of {C.COLS}x{C.ROWS} grid")
            elev[r, q] = _float(row, "elev_m", "elevation_m", "elevation")
            lith = _str(row, "lithology", "rock", "rock_unit", "lith")
            if lith:
                rock[r, q] = lithology_to_rock_code(lith)
            elif "rock_code" in row and row["rock_code"] not in (None, ""):
                rock[r, q] = int(float(row["rock_code"]))
            plate[r, q] = int(_float(row, "plate", "plate_id", default=0))
            scar = row.get("glacial_scar") or row.get("glacial") or row.get("glacial_carved")
            s = "" if scar is None else str(scar).strip().lower()
            if s in ("", "0", "false", "no", "n", "none", "null"):
                glacial[r, q] = False
            elif s in ("1", "true", "yes", "y", "t"):
                glacial[r, q] = True
            else:
                glacial[r, q] = True  # any non-empty scar tag
            endorheic[r, q] = _truthy(row.get("endorheic"))
            geo_res[r, q] = _str(row, "geology_resource_tag", "resource_tag", "geo_resource")
            if any(k in row and row[k] not in (None, "") for k in ("slope", "slope_m_per_km")):
                slope[r, q] = _float(row, "slope", "slope_m_per_km")
            seen += 1

    if seen != C.HEX_COUNT:
        raise ValueError(
            f"geology_hex.csv has {seen} rows; expected {C.HEX_COUNT} ({C.COLS}x{C.ROWS})"
        )
    if np.isnan(elev).any():
        missing = int(np.isnan(elev).sum())
        raise ValueError(f"geology_hex.csv missing elev_m on {missing} hexes")

    # Fill slope if absent
    if np.isnan(slope).all():
        from .geology import _slope_m_per_km

        slope = _slope_m_per_km(elev)
    else:
        nan_m = np.isnan(slope)
        if nan_m.any():
            from .geology import _slope_m_per_km

            slope = np.where(nan_m, _slope_m_per_km(elev), slope)

    qq, rr = np.meshgrid(np.arange(C.COLS), np.arange(C.ROWS))
    qf = qq.astype(np.float64) / max(C.COLS - 1, 1)
    rf = rr.astype(np.float64) / max(C.ROWS - 1, 1)
    bq, br = C.BASIN_CENTER
    basin_dist = np.sqrt(((qf - bq) / C.BASIN_RADIUS_Q) ** 2 + ((rf - br) / C.BASIN_RADIUS_R) ** 2)
    # Prefer Geologist endorheic flags; else fall back to config basin
    if not endorheic.any():
        endorheic = basin_dist < 1.0

    return {
        "source": "geology_hex.csv",
        "elev_m": elev,
        "slope": slope,
        "rock": rock,
        "plate": plate,
        "glacial": glacial,
        "endorheic": endorheic,
        "geology_resource_tag": geo_res,
        "is_ocean": elev < 0,
        "basin_dist": basin_dist,
        "qf": qf,
        "rf": rf,
        # stubs so toy climate hooks that expect suture_dist etc. still work
        "suture_dist": np.abs(qf - C.SUTURE_Q_FRAC) / C.SUTURE_WIDTH_FRAC,
        "arc_dist": np.ones((C.ROWS, C.COLS)),
        "rift_dist": np.ones((C.ROWS, C.COLS)),
        "hotspot_dist": np.ones((C.ROWS, C.COLS)),
        "land_score": np.where(elev >= 0, 1.0, 0.0),
    }


def should_write_geology_maps(data_dir: Path) -> bool:
    """Cartographer writes toy plates/elevation maps only when Geologist data absent."""
    return not geology_data_present(data_dir)
