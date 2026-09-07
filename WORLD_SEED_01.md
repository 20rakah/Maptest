# World Seed 01 — GM pack

Open this folder (or the [Maptest](https://github.com/20rakah/Maptest) repo). You do **not** need to read Python.

## Start here

| File | What |
|------|------|
| `GAZETTEER.md` | 18 regions (landform, climate, water, food, resources, who lives here, travel catches, hooks) |
| `SETTLEMENTS.md` | City-candidate sites + hooks (`wt_depth_m` well depths) |
| `CLIMATE_CALENDAR.md` | Climate-signed seasons (do not edit lightly) |
| `maps/` | Layer PNGs 01–09 + geology extras |
| `legends/` | Color keys |
| `data/hexes.csv` / `hexes.json` | Master hex table (lockstep with maps) |
| `README.md` | How to change seed / sea level / ice / rainfall |

## Locked inputs

- Geology: `data/geology_hex.csv` — fingerprint `DRAIN_V3_ENDO_939`
- Climate: `data/climate_hex.csv` — rain_shadow (113) ≠ dry_interior (862)
- Settlement tiers only: farmstead / village / town / city-candidate (no borders/kingdoms)

## Hex IDs

`H{q:+03d}{r:+03d}` on an 80×60 grid @ ~30 km/hex. Default seed **1001**.

## Notes

- `water`: surface classes, or `shallow_well` / `spring_line` for groundwater-only sites
- `wt_class` + `wt_depth_m`: Climate source of truth for wells
- Regenerate with `./run.sh` (preserves geology_hex / climate_hex when present)
