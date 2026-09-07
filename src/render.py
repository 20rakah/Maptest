"""Render layer PNGs and legend PNGs / LEGENDS.md. Hex colors must match data."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import config as C
from .geology import PLATE_LABELS, ROCK_LABELS
from .biosphere import RES_LABELS, SOIL_LABELS, VEG_LABELS

# Pixel size per hex (flat visual grid — not true hex geometry; ASSUMPTION for GM readability)
CELL = 8


def _font(size: int = 14):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _rgb_array(h: int, w: int) -> np.ndarray:
    return np.zeros((h, w, 3), dtype=np.uint8)


def _save_rgb(path: Path, rgb: np.ndarray) -> None:
    # Upscale by CELL for readability
    img = Image.fromarray(rgb, mode="RGB")
    img = img.resize((rgb.shape[1] * CELL, rgb.shape[0] * CELL), Image.NEAREST)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _legend_png(path: Path, title: str, entries: list[tuple[tuple[int, int, int], str]]) -> None:
    row_h = 28
    width = 420
    height = 40 + row_h * len(entries)
    img = Image.new("RGB", (width, height), (250, 250, 248))
    draw = ImageDraw.Draw(img)
    font = _font(14)
    title_font = _font(16)
    draw.text((12, 8), title, fill=(20, 20, 20), font=title_font)
    y = 36
    for color, label in entries:
        draw.rectangle([12, y, 36, y + 20], fill=color, outline=(0, 0, 0))
        draw.text((48, y + 2), label, fill=(20, 20, 20), font=font)
        y += row_h
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def _colorize_codes(codes: np.ndarray, palette: dict[int, tuple[int, int, int]]) -> np.ndarray:
    h, w = codes.shape
    rgb = _rgb_array(h, w)
    for k, col in palette.items():
        m = codes == k
        rgb[m] = col
    return rgb


def _elev_colors(elev: np.ndarray) -> np.ndarray:
    h, w = elev.shape
    rgb = _rgb_array(h, w)
    ocean = elev < 0
    rgb[ocean] = (20, 60, 120)
    land = ~ocean
    e = elev.copy()
    e[ocean] = 0
    # green low → brown → white high
    t = np.clip(e / 2500.0, 0, 1)
    rgb[land, 0] = (40 + 180 * t[land]).astype(np.uint8)
    rgb[land, 1] = (120 - 40 * t[land]).astype(np.uint8)
    rgb[land, 2] = (50 + 100 * t[land]).astype(np.uint8)
    rgb[land & (e > 2000)] = (235, 240, 245)
    return rgb


WATER_PALETTE = {
    0: (210, 190, 150),  # dry land
    1: (30, 90, 160),  # ocean
    2: (70, 150, 220),  # river
    3: (20, 80, 200),  # major river
    4: (50, 140, 180),  # lake
    5: (40, 110, 150),  # inland sea
    6: (90, 140, 100),  # wetland
    7: (230, 240, 255),  # ice
}

WT_PALETTE = {
    0: (20, 60, 120),
    1: (80, 180, 220),
    2: (120, 200, 160),
    3: (180, 200, 100),
    4: (200, 160, 80),
    5: (160, 100, 60),
    6: (230, 240, 255),
}

SETTLE_PALETTE = {
    "none": (40, 40, 40),
    "farmstead": (180, 200, 120),
    "village": (220, 180, 80),
    "town": (220, 120, 60),
    "city-candidate": (200, 40, 40),
    "ocean": (20, 50, 90),
}

PLATE_PALETTE = {
    0: (180, 160, 120),
    1: (160, 150, 100),
    2: (200, 80, 80),
    3: (120, 80, 140),
    4: (220, 140, 60),
}

ROCK_PALETTE = {
    0: (60, 60, 80),
    1: (190, 180, 150),
    2: (120, 100, 90),
    3: (180, 70, 70),
    4: (140, 60, 120),
    5: (200, 110, 50),
    6: (210, 200, 140),
    7: (230, 210, 160),
}


def render_all_layers(
    out_maps: Path,
    out_legends: Path,
    world: dict,
    write_geology_maps: bool,
) -> list[str]:
    """Write PNGs; return list of map filenames written."""
    written: list[str] = []
    elev = world["elev_m"]
    slope = world["slope"]

    if write_geology_maps:
        # Combined plates_rock: rock colors with plate outline cue
        rock_rgb = _colorize_codes(world["rock"], ROCK_PALETTE)
        rock_rgb[elev < 0] = (20, 40, 80)
        name = "01_plates_rock.png"
        _save_rgb(out_maps / name, rock_rgb)
        written.append(name)
        _legend_png(
            out_legends / "01_plates_rock_legend.png",
            "Plates / Rock",
            [(ROCK_PALETTE[k], ROCK_LABELS[k]) for k in sorted(ROCK_LABELS)],
        )

        # elevation + slope side encoding: elev color, darken by slope
        elev_rgb = _elev_colors(elev)
        s = np.clip(slope / 40.0, 0, 1)
        elev_rgb = (elev_rgb.astype(np.float64) * (1.0 - 0.45 * s[..., None])).astype(np.uint8)
        name = "02_elevation_slope.png"
        _save_rgb(out_maps / name, elev_rgb)
        written.append(name)
        _legend_png(
            out_legends / "02_elevation_slope_legend.png",
            "Elevation / Slope",
            [
                ((20, 60, 120), "Ocean (<0 m)"),
                ((40, 120, 50), "Lowland"),
                ((160, 100, 50), "Upland / hills"),
                ((200, 180, 140), "High mountains"),
                ((235, 240, 245), "Very high / ice-prone"),
                ((80, 80, 80), "Darker = steeper slope"),
            ],
        )
    else:
        # Still write elev-derived climate bases; geology maps left to Geologist
        pass

    # 03 climate: temp as red-blue, precip as overlay green intensity → split two-channel viz
    temp = world["temp_c"]
    precip = world["precip_mm"]
    h, w = temp.shape
    clim = _rgb_array(h, w)
    tnorm = np.clip((temp + 5) / 30.0, 0, 1)
    pnorm = np.clip(precip / 2000.0, 0, 1)
    clim[..., 0] = (30 + 200 * tnorm).astype(np.uint8)
    clim[..., 1] = (40 + 180 * pnorm).astype(np.uint8)
    clim[..., 2] = (180 - 120 * tnorm).astype(np.uint8)
    clim[elev < 0] = (20, 50, 100)
    name = "03_climate_weather.png"
    _save_rgb(out_maps / name, clim)
    written.append(name)
    _legend_png(
        out_legends / "03_climate_weather_legend.png",
        "Climate (temp + precip)",
        [
            ((30, 40, 180), "Cold / dry-leaning (blue)"),
            ((230, 100, 60), "Warm (more red)"),
            ((100, 220, 100), "Wet (more green)"),
            ((20, 50, 100), "Ocean"),
        ],
    )

    # 04 ice + surface water
    name = "04_ice_surface_water.png"
    _save_rgb(out_maps / name, _colorize_codes(world["water_code"], WATER_PALETTE))
    written.append(name)
    _legend_png(
        out_legends / "04_ice_surface_water_legend.png",
        "Ice / Surface Water",
        [
            (WATER_PALETTE[0], "Dry land"),
            (WATER_PALETTE[1], "Ocean"),
            (WATER_PALETTE[2], "River"),
            (WATER_PALETTE[3], "Major river"),
            (WATER_PALETTE[4], "Lake"),
            (WATER_PALETTE[5], "Inland sea (endorheic)"),
            (WATER_PALETTE[6], "Wetland"),
            (WATER_PALETTE[7], "Residual ice"),
        ],
    )

    # 05 water table
    name = "05_water_table.png"
    _save_rgb(out_maps / name, _colorize_codes(world["wt_code"], WT_PALETTE))
    written.append(name)
    _legend_png(
        out_legends / "05_water_table_legend.png",
        "Water Table",
        [
            (WT_PALETTE[0], "Ocean"),
            (WT_PALETTE[1], "Emergent / spring (≤1 m)"),
            (WT_PALETTE[2], "Shallow (1–4 m)"),
            (WT_PALETTE[3], "Moderate (4–12 m)"),
            (WT_PALETTE[4], "Deep (12–25 m)"),
            (WT_PALETTE[5], "Arid-deep (>25 m)"),
            (WT_PALETTE[6], "Ice"),
        ],
    )

    # 06 soil
    soil_pal = {
        0: (20, 40, 80),
        1: (120, 110, 100),
        2: (180, 180, 170),
        3: (140, 120, 90),
        4: (120, 90, 50),
        5: (100, 80, 60),
        6: (210, 190, 130),
        7: (90, 70, 50),
        8: (190, 160, 100),
        9: (60, 80, 50),
    }
    name = "06_soil.png"
    _save_rgb(out_maps / name, _colorize_codes(world["soil"], soil_pal))
    written.append(name)
    _legend_png(
        out_legends / "06_soil_legend.png",
        "Soil",
        [(soil_pal[k], SOIL_LABELS[k]) for k in sorted(SOIL_LABELS)],
    )

    # 07 vegetation
    veg_pal = {
        0: (20, 40, 80),
        1: (230, 240, 255),
        2: (180, 200, 180),
        3: (40, 100, 60),
        4: (30, 140, 50),
        5: (160, 190, 70),
        6: (170, 150, 70),
        7: (200, 170, 110),
        8: (70, 110, 80),
        9: (120, 160, 40),
        10: (150, 170, 90),
    }
    name = "07_vegetation.png"
    _save_rgb(out_maps / name, _colorize_codes(world["veg"], veg_pal))
    written.append(name)
    _legend_png(
        out_legends / "07_vegetation_legend.png",
        "Vegetation",
        [(veg_pal[k], VEG_LABELS[k]) for k in sorted(VEG_LABELS)],
    )

    # 08 resources
    res_pal = {
        0: (50, 50, 50),
        1: (40, 120, 40),
        2: (140, 140, 140),
        3: (180, 120, 40),
        4: (100, 40, 100),
        5: (240, 240, 220),
        6: (160, 100, 70),
        7: (40, 100, 180),
        8: (80, 70, 40),
        9: (200, 40, 160),
    }
    res_rgb = _colorize_codes(world["res_code"], res_pal)
    res_rgb[elev < 0] = (20, 40, 80)
    name = "08_resources.png"
    _save_rgb(out_maps / name, res_rgb)
    written.append(name)
    _legend_png(
        out_legends / "08_resources_legend.png",
        "Resources (primary)",
        [(res_pal[k], RES_LABELS[k]) for k in sorted(RES_LABELS)],
    )

    # 09 settlement
    settle = world["settle_score"]
    srgb = _rgb_array(h, w)
    for r in range(h):
        for q in range(w):
            if elev[r, q] < 0:
                srgb[r, q] = SETTLE_PALETTE["ocean"]
            else:
                srgb[r, q] = SETTLE_PALETTE.get(settle[r, q], SETTLE_PALETTE["none"])
    name = "09_settlement_score.png"
    _save_rgb(out_maps / name, srgb)
    written.append(name)
    _legend_png(
        out_legends / "09_settlement_score_legend.png",
        "Settlement tiers (no borders)",
        [
            (SETTLE_PALETTE["ocean"], "Ocean"),
            (SETTLE_PALETTE["none"], "Empty / none"),
            (SETTLE_PALETTE["farmstead"], "Farmstead"),
            (SETTLE_PALETTE["village"], "Village"),
            (SETTLE_PALETTE["town"], "Town"),
            (SETTLE_PALETTE["city-candidate"], "City-candidate"),
        ],
    )

    _write_legends_md(out_legends, write_geology_maps)
    return written


def _write_legends_md(out_legends: Path, write_geology_maps: bool) -> None:
    lines = [
        "# Legends — World Seed 01",
        "",
        "Color keys match `maps/*.png`. Legend PNGs sit beside this file.",
        "",
        "## Hex ID scheme",
        f"Axial coordinates: `{C.ID_FMT}` example `H+00+00` … grid **{C.COLS}×{C.ROWS}** "
        f"({C.HEX_COUNT} hexes), ~{C.HEX_KM} km/hex.",
        "",
    ]
    if write_geology_maps:
        lines += ["## 01 plates_rock", "See `01_plates_rock_legend.png` (toy Cartographer geology).", ""]
        lines += ["## 02 elevation_slope", "See `02_elevation_slope_legend.png`.", ""]
    else:
        lines += [
            "## 01–02 Geology maps",
            "Owned by Geologist when `data/geology_hex.csv` is present — see their map PNGs.",
            "",
        ]
    for i, title in [
        (3, "climate_weather"),
        (4, "ice_surface_water"),
        (5, "water_table"),
        (6, "soil"),
        (7, "vegetation"),
        (8, "resources"),
        (9, "settlement_score"),
    ]:
        lines += [f"## {i:02d} {title}", f"See `{i:02d}_{title}_legend.png`.", ""]
    (out_legends / "LEGENDS.md").write_text("\n".join(lines), encoding="utf-8")
