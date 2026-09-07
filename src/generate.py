#!/usr/bin/env python3
"""World Seed 01 generator — Climate V1 over Geologist CLEAR package.

Usage:
  python -m src.generate [--seed N] [--sea-level M] [--ice F] [--rainfall F]

If data/geology_hex.csv exists, ingest elev/lithology/glacial/endorheic/resource tags
from Geologist and do NOT overwrite geology_hex.* or geology-owned map PNGs.
Climate owns maps 03–08 and data/climate_hex.*; settlement (09 / hexes settle cols)
is Cartographer packaging still produced by this pipeline for convenience.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import config as C
from src.biosphere import build_resources, build_soil, build_vegetation, food_score
from src.climate import build_climate
from src.export import build_climate_rows, build_rows, write_csv_json
from src.geology import apply_glacial_carving, build_elevation, build_plates_rock
from src.geology_ingest import geology_data_present, load_geology_hex, should_write_geology_maps
from src.hydrology import build_surface_water, build_water_table, residual_ice
from src.render import render_all_layers
from src.settlement import score_settlements
from src.validate import validate_data_dir


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="World Seed 01 continent generator")
    p.add_argument("--seed", type=int, default=C.DEFAULT_SEED, help=f"RNG seed (default {C.DEFAULT_SEED})")
    p.add_argument(
        "--sea-level",
        type=float,
        default=C.DEFAULT_SEA_LEVEL_M,
        help="Sea level offset in meters (raise to flood coasts)",
    )
    p.add_argument(
        "--ice",
        type=float,
        default=C.DEFAULT_ICE_MULT,
        help="Residual ice intensity multiplier (0=none)",
    )
    p.add_argument(
        "--rainfall",
        type=float,
        default=C.DEFAULT_RAINFALL_MULT,
        help="Precipitation multiplier",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT,
        help="Output root (default: world-seed-01 folder)",
    )
    return p.parse_args(argv)


def build_world(args: argparse.Namespace) -> dict:
    data_dir = args.out / "data"
    seed = args.seed

    geo_loaded = None
    if geology_data_present(data_dir):
        print(f"Ingesting Geologist data: {data_dir / 'geology_hex.csv'}")
        geo_loaded = load_geology_hex(data_dir)
        elev = geo_loaded["elev_m"] - args.sea_level
        endorheic = geo_loaded["endorheic"]
        is_ocean = (elev < 0) & ~endorheic
        slope = geo_loaded["slope"]
        rock = geo_loaded["rock"]
        plate = geo_loaded["plate"]
        qf, rf = geo_loaded["qf"], geo_loaded["rf"]
        glacial = geo_loaded["glacial"]
        glacial_scar = geo_loaded.get("glacial_scar")
        geo_res_tag = geo_loaded["geology_resource_tag"]
        geology_source = geo_loaded.get("source", "geology_hex.csv")
    else:
        print("No data/geology_hex.csv — using Cartographer toy geology (locked history constraints)")
        geo = build_plates_rock(seed)
        elev_pack = build_elevation(seed, geo, args.sea_level)
        elev = apply_glacial_carving(elev_pack["elev_m"], seed, args.ice)
        endorheic = geo["basin_dist"] < 1.0
        elev = elev.copy()
        elev[endorheic] = np.maximum(elev[endorheic], 35.0)
        from src.geology import _slope_m_per_km

        slope = _slope_m_per_km(elev)
        rock = geo["rock"]
        plate = geo["plate"]
        qf, rf = geo["qf"], geo["rf"]
        glacial = (rf < C.LGM_NORTH_EDGE_FRAC) | (
            (geo["suture_dist"] < 1.2) & (elev > 800)
        )
        geo_res_tag = None
        glacial_scar = None
        is_ocean = (elev < 0) & ~endorheic
        geology_source = "toy"

    # Ice first so climate can apply melt effects
    ice = residual_ice(elev, qf, rf, args.ice, glacial_mask=glacial)
    climate = build_climate(
        seed,
        elev,
        qf,
        rf,
        args.rainfall,
        endorheic=endorheic,
        glacial_mask=glacial,
        ice=ice,
    )
    surface = build_surface_water(
        seed, elev, climate["precip_mm"], ice, endorheic, is_ocean
    )
    wt = build_water_table(
        elev, climate["precip_mm"], surface, seed, endorheic=endorheic
    )
    soil = build_soil(
        elev,
        slope,
        rock,
        surface["ice"],
        surface["wetland"],
        glacial,
        climate["precip_mm"],
        salt_pan=surface.get("salt_pan"),
        floodplain=surface.get("floodplain"),
    )
    veg = build_vegetation(
        elev,
        climate["temp_c"],
        climate["precip_mm"],
        surface["ice"],
        surface["wetland"],
        surface["river"] | surface["major_river"],
        surface["lake"] | surface.get("inland_sea", np.zeros_like(elev, dtype=bool)),
        soil,
        salt_pan=surface.get("salt_pan"),
        floodplain=surface.get("floodplain"),
        inland_sea=surface.get("inland_sea"),
    )
    res_code, res_tags, climate_resource_tags = build_resources(
        seed,
        rock,
        elev,
        veg,
        surface["water_code"],
        geo_res_tag,
        salt_pan=surface.get("salt_pan"),
        endorheic=endorheic,
    )
    food = food_score(veg, surface["water_code"])
    settle = score_settlements(
        seed,
        elev,
        slope,
        surface["water_code"],
        wt["wt_depth_m"],
        food,
        surface["ice"],
        veg,
    )

    return {
        "geology_source": geology_source,
        "climate_owner": "Climate",
        "elev_m": elev,
        "slope": slope,
        "rock": rock,
        "plate": plate,
        "qf": qf,
        "rf": rf,
        "endorheic": endorheic,
        "glacial": glacial,
        "glacial_scar": glacial_scar,
        **climate,
        **surface,
        **wt,
        "soil": soil,
        "veg": veg,
        "res_code": res_code,
        "res_tags": res_tags,
        "climate_resource_tags": climate_resource_tags,
        "food": food,
        **settle,
        "seed": seed,
        "sea_level": args.sea_level,
        "ice_mult": args.ice,
        "rainfall_mult": args.rainfall,
    }


def run(args: argparse.Namespace) -> int:
    out = args.out
    maps = out / "maps"
    legends = out / "legends"
    data = out / "data"
    maps.mkdir(parents=True, exist_ok=True)
    legends.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)

    # Snapshot geology hashes before run to prove non-overwrite
    geo_csv = data / "geology_hex.csv"
    geo_json = data / "geology_hex.json"
    pre_csv = geo_csv.read_bytes() if geo_csv.is_file() else None
    pre_json = geo_json.read_bytes() if geo_json.is_file() else None

    world = build_world(args)
    write_geo_maps = should_write_geology_maps(data)
    if not write_geo_maps:
        print("Skipping toy plates/elevation map export (Geologist data present)")

    written = render_all_layers(maps, legends, world, write_geology_maps=write_geo_maps)
    rows = build_rows(world)
    write_csv_json(rows, data, stem="hexes")
    climate_rows = build_climate_rows(world)
    write_csv_json(climate_rows, data, stem="climate_hex")

    # Prove geology untouched
    if pre_csv is not None and geo_csv.read_bytes() != pre_csv:
        print("FATAL: geology_hex.csv was modified")
        return 2
    if pre_json is not None and geo_json.read_bytes() != pre_json:
        print("FATAL: geology_hex.json was modified")
        return 2

    meta = out / "data" / "run_meta.txt"
    meta.write_text(
        "\n".join(
            [
                f"seed={args.seed}",
                f"sea_level={args.sea_level}",
                f"ice={args.ice}",
                f"rainfall={args.rainfall}",
                f"grid={C.COLS}x{C.ROWS}",
                f"hex_count={C.HEX_COUNT}",
                f"hex_km={C.HEX_KM}",
                f"geology_source={world['geology_source']}",
                f"climate_owner=Climate",
                f"maps={','.join(written)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    errs = validate_data_dir(data)
    # Also validate climate_hex
    clim_csv = data / "climate_hex.csv"
    if not clim_csv.is_file():
        errs.append("missing climate_hex.csv")
    else:
        import csv as _csv

        with clim_csv.open(newline="", encoding="utf-8") as f:
            crows = list(_csv.DictReader(f))
        if len(crows) != C.HEX_COUNT:
            errs.append(f"climate_hex.csv rows {len(crows)} != {C.HEX_COUNT}")

    if errs:
        print("VALIDATE FAIL:")
        for e in errs:
            print(" -", e)
        return 1
    print(
        f"OK seed={args.seed} hexes={C.HEX_COUNT} maps={len(written)} "
        f"geology={world['geology_source']} climate_owner=Climate"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    return run(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
