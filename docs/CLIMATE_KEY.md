# Climate Key — World Seed 01 (for Cartographer)

Climate owns **maps 03–08** and **`data/climate_hex.csv` / `.json`**.  
Geologist owns `geology_hex.*` and geology map PNGs (untouched).  
Cartographer packages **settlement** (map 09, `settle_score` / `why` in `hexes.csv`).

Join key: `id` (`H{q:+03d}{r:+03d}`), grid 80×60, seed 1001, 30 km/hex.

## Layer meanings

| Map | Contents |
|-----|----------|
| 03_climate_weather | Temp (red↔blue) + precip (green). Rain shadows east of suture/arc; dry endorheic interior. |
| 04_ice_surface_water | Ocean, rivers, lakes, **inland_sea** (deep basin floor), **salt_pan** (flat ~589 m sill), wetland, residual ice. |
| 05_water_table | Legacy depth bands; prefer `wt_class` in climate_hex. |
| 06_soil | Rock+climate+slope; includes saline playa on salt pans. |
| 07_vegetation | Biomes from temp/precip/soil/water. |
| 08_resources | Primary paint: timber / pasture / salt / fish / rock-hosted metals etc. |
| 09_settlement_score | **Cartographer packaging** (not Climate narrative). |

## climate_hex columns (minimum)

| Column | Meaning |
|--------|---------|
| temp_c, precip_mm | Mean annual toy climate |
| wind | windward / leeward / open_westerly / calm_interior / ocean_westerly |
| rain_shadow | bool |
| seasonality / season_label | 0–1 index; weak/moderate/strong/maritime |
| water_code / water | 0 none, 1 ocean, 2 river, 3 major_river, 4 lake, 5 inland_sea, 6 wetland, 7 ice, **8 salt_pan** |
| floodplain | bool overlay along rivers |
| wt_class | **shallow_well \| spring_line \| dry \| marsh** (ASSUMPTION C15) |
| soil / vegetation | Label strings |
| climate_resource_tags | Climate belts: `timber\|pasture\|salt_pans\|fisheries` |
| food_proxy / food | Numeric 0–3.5 and rich/good/modest/poor/none |
| endorheic | From Geologist CSV (939 hexes) |

## Endorheic hydrology (read this)

- Mask = CSV `endorheic` **939** hexes (Geology A19 catchment), centroid ~(0.45, 0.51).
- **Inland sea** = deep carved floor (~60–120 m), not the flat sill.
- **Salt pans** = flat ~589 m playa under dry climate — fisheries tags favor coasts + inland sea, salt_pans favor interior.
- Endorheic rivers terminate in basin sinks; they do **not** empty to ocean.

## ASSUMPTION index

See `ASSUMPTIONS_CLIMATE.md` (C1–C22). Guesses are labeled ASSUMPTION in code/docs.
