# Assumptions — Climate (World Seed 01)

Climate-owned ASSUMPTIONs only. Geology ASSUMPTIONs live in `ASSUMPTIONS_GEOLOGY.md`.

| ID | Topic | Choice | Notes |
|----|--------|--------|-------|
| C1 | Latitude / temp gradient | ~55°N–28°N; ~0.55 °C/°lat; sea-level ref 14 °C | Toy Earth-like mid-latitude belt |
| C2 | Post-LGM timing | Ice age ended ~1000 yr BP; **no residual ice hexes** this run (Geologist glacial scars max elev ~875 m, below cold-ice thresholds); melt chill 0.5–1.5 °C + slight precip bump on glacial scars | Matches Geology A8 “highland ice gone”; scars still climate-active |
| C3 | Moisture pattern | Westerlies; wetter west/south coasts | Orography uses suture ~q 0.42 and SE arc |
| C4 | Endorheic dryness | Endorheic mask ×0.55 precip; deep floor ×1.15 | Uses CSV `endorheic` (939 hexes), **not** config BASIN_CENTER (0.62,0.48). Centroid ~(0.45,0.51) |
| C5 | Wind classes | windward / leeward / open_westerly / calm_interior / ocean_westerly | From elev east-gradient + basin |
| C6 | Seasonality | 0.1–0.95 index → weak/moderate/strong | Higher inland, north, rain-shadow |
| C7 | Lapse rate | 6.5 °C/km | Earth-like |
| C8 | Base precip | 850 mm/yr before orography | Multiplied by `--rainfall` |
| C9 | Orographic / rain-shadow | gain 1.8; leeward retain ~0.35 | Toy |
| C10 | Large-basin hydrology | Deep floor (<~120 m or ≪ sill) = inland_sea; flat sill ~589 m = salt_pan when dry — **not** whole 939 hexes as lake | Scales Geology A19 catchment |
| C11 | River thresholds | accum ≥8 river; ≥28 major | Toy runoff units |
| C12 | Inland sea threshold | elev ≤ sill−50 m or elev < 120 m inside endorheic | Permanent water only on carved floor |
| C13 | Basin fringe wetlands | 1-hex dilate around inland_sea if precip >400 | Seasonal fringe |
| C14 | Floodplain | 1-hex dilate of rivers, elev <900, accum ≥4 | Overlay flag; farmable veg when warm/wet |
| C15 | wt_class mapping | marsh ≤0.8 m or wetland/inland_sea; spring_line ≤2–2.5 m at rivers/coasts/relief; shallow_well 0.8–8 m; else dry | Potable-focused; salt pans forced dry |
| C16 | Playa water table | salt_pan depth clipped 8–40 m | Saline flat ≠ marsh |
| C17 | Salt pans resource | Endorheic salt_pan / veg salt-flat / water_code 8 | Interior basin vs coastal fisheries |
| C18 | Fisheries | ocean, major river, lake, inland_sea (+ some rivers) | Coasts + inland sea |
| C19 | Soil = rock + climate + slope + glacial + time-proxy | Saline playa soil code 10 on salt pans | Toy |
| C20 | Vegetation follows soil+climate | Includes salt flat sparse (11) | No nations invented |
| C21 | Climate resource belts | timber, pasture, salt_pans, fisheries (+ merged geology rock tags in `resources_merged`) | Primary Climate deliverable stops at resources |
| C22 | Settlement score | Still computed for Cartographer packaging (map 09 / hexes.csv) — **Cartographer-owned**, not Climate narrative | Documented ownership split |

**Source of truth:** `data/geology_hex.csv` fingerprint `DRAIN_V3_ENDO_939`. Do not trust stale climate columns in older `hexes.csv` until this Climate run overwrites maps 03–09 / climate tables.
