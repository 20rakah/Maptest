# World Seed 01 — Fantasy continent (Cartographer deliverable)

Plain-language packet for GMs. **No kingdoms, borders, or atlas prose** — physical layers + settlement suitability only.

## What's here

| Path | What |
|------|------|
| `maps/` | Layer PNGs (numbered stage order) |
| `legends/` | Matching color-key PNGs + `LEGENDS.md` |
| `data/hexes.csv` / `data/hexes.json` | One row per hex (lockstep with maps) |
| `data/geology_hex.csv` | **Geologist-owned** (optional ingest). Cartographer never overwrites this. |
| `run.sh` | Regenerate from seed |
| `src/` | Python generator |
| `ASSUMPTIONS.md` | Labeled guesses Climate may replace |

## Grid & hex IDs

- Continent scale ~**2400 × 1800 km** at **~30 km/hex** → grid **80 × 60** = **4800** hexes.
- Axial IDs: `H{q:+03d}{r:+03d}` → examples `H+00+00`, `H+42+17`, `H+79+59`.
- Scan order in CSV/JSON: row `r=0…59`, within each row `q=0…79`.
- Same ID is used on every layer and in the hex table.

## Default seed

**World Seed 01 default seed = `1001`.**  
Same seed + same knobs → identical outputs.

## How to regenerate

```bash
cd /workspace/world-seed-01
./run.sh
```

Or with knobs:

```bash
./run.sh --seed 1001 --sea-level 0 --ice 1.0 --rainfall 1.0
# or env:
SEED=1001 SEA_LEVEL=50 ICE=0.5 RAINFALL=1.2 ./run.sh
```

| Knob | Meaning |
|------|---------|
| `--seed` | Deterministic RNG seed |
| `--sea-level` | Meters added to sea datum (positive floods coasts) |
| `--ice` | Residual ice multiplier (`0` = none) |
| `--rainfall` | Precipitation multiplier |

Requires Python 3; `run.sh` creates `.venv` and installs `requirements.txt` (numpy, Pillow).

## Map files (layer order)

1. `01_plates_rock.png` — plates / rock units *(toy Cartographer geology if Geologist file absent)*
2. `02_elevation_slope.png` — elevation with slope darkening
3. `03_climate_weather.png` — temperature + precip (orographic / rain shadows from westerlies)
4. `04_ice_surface_water.png` — residual ice, rivers, lakes, wetlands, endorheic inland sea
5. `05_water_table.png` — relative water-table depth classes
6. `06_soil.png`
7. `07_vegetation.png`
8. `08_resources.png` — follow geology + climate
9. `09_settlement_score.png` — farmstead / village / town / city-candidate / empty

If `data/geology_hex.csv` exists, Cartographer **skips writing** stages 01–02 toy maps and ingests elevation/lithology/glacial/endorheic/geology_resource_tag for climate→settlement.

**Geologist-owned (never overwritten by `./run.sh`):** `data/geology_hex.csv`, `data/geology_hex.json`, and maps `01_plates_rock.png`, `02_elevation.png`, `02_slope.png`, `lithology.png`, `mountain_type.png`, `glacial_scars.png`, `endorheic.png`, `land_ocean.png`.

## Hex table columns

**Required:** `id`, `terrain`, `water`, `food`, `resources`, `settle_score`, `why`  

**Extras:** `q`, `r`, `elev_m`, `slope`, `precip`, `temp_c`, `soil`, `vegetation`, `rock`

`settle_score` is a **tier name** only: `none` | `farmstead` | `village` | `town` | `city-candidate`.  
Some excellent (city-candidate-quality) sites are left **empty on purpose** (~20%).

## Physics rules encoded

- Rivers flow downhill and join
- Orographic rain; temperature falls with latitude and elevation
- Simple glacial carving on spine/north (LGM; ice age ended ~1000 yr BP — ASSUMPTION)
- Dual-craton suture spine, SE arc, northern rift, SW hotspot, endorheic central-east basin
- Resources follow geology; settlements need water + food + route; no borders

## Validate

```bash
./run.sh
# or:
.venv/bin/python -m src.validate data
```

Row count must equal 4800; IDs must match the axial grid.
