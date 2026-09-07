# Legends — World Seed 01

Color keys match `maps/*.png`. Legend PNGs sit beside this file.

## Hex ID scheme
Axial coordinates: `H{q:+03d}{r:+03d}` example `H+00+00` … grid **80×60** (4800 hexes), ~30 km/hex.

## 01–02 Geology maps
Owned by Geologist when `data/geology_hex.csv` is present — see their map PNGs.

## Ownership
- **Climate** owns maps 03–08 and `data/climate_hex.csv|.json`.
- **Cartographer** packages settlement map 09 / settle columns in `hexes.csv`.
- **Geologist** owns geology maps + `geology_hex.*` (never overwritten here).

## 03 climate_weather (Climate)
See `03_climate_weather_legend.png`.

## 04 ice_surface_water (Climate)
See `04_ice_surface_water_legend.png`.

## 05 water_table (Climate)
See `05_water_table_legend.png`.

## 06 soil (Climate)
See `06_soil_legend.png`.

## 07 vegetation (Climate)
See `07_vegetation_legend.png`.

## 08 resources (Climate)
See `08_resources_legend.png`.

## 09 settlement_score (Cartographer packaging)
See `09_settlement_score_legend.png`.
