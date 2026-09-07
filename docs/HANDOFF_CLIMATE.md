# Handoff — Geologist → Climate

**Referee: CLEAR** for Climate on current `data/geology_hex.csv`.

## Files
- `data/geology_hex.csv` / `geology_hex.json` (column `id` = hex id)
- Maps: `01_plates_rock.png`, `02_elevation.png`, `02_slope.png`, `glacial_scars.png`, `endorheic.png`
- Fingerprint: `data/GEOLOGY_REEXPORT.txt` (`DRAIN_V3_ENDO_939`)
- Drainage self-check: `data/DRAINAGE_SELFCHECK.txt`

## Ice extent (LGM)
- North of r-frac 0.35 and high suture spine (elev>800 within suture belt).
- Residual highland ice gone ~1000 yr BP; scars remain (`glacial_scar` tags in CSV; PNG is presence/absence).

## Mountain walls (orography)
- Primary: collision suture near q-frac 0.42
- Secondary: SE arc around (0.82, 0.78)

## Rock types
See `lithology` column / legends.

## Endorheic basin (closed)
- **Use CSV `endorheic=true` mask** (939 hexes, ~28% of land) — floor + high rim + spill catchment (**A19**).
- Centroid (q/COLS, r/ROWS) ≈ **(0.45, 0.51)** — not config BASIN_CENTER (0.62, 0.48).
- Ocean-adjacent: 0; does not steepest-descend to sea.
- Drainage: all non-endorheic land steepest-descends to ocean.

## Counts
- Land 3325/4800; endorheic 939; elev land ~0..2161 m.
