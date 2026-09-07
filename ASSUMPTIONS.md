# ASSUMPTIONS — World Seed 01 (Cartographer)

Guessed constants Climate / Geologist may later replace. All are labeled **ASSUMPTION** in `src/config.py` and related modules.

| ID | Topic | Value / choice | Notes |
|----|--------|----------------|-------|
| A1 | Ice age end | 1000 yr BP | Locked window was 800–1200; pick midpoint |
| A2 | Grid | 80×60 hexes @ 30 km | From ~2400×1800 km continent |
| A3 | Default seed | 1001 | World Seed 01 |
| A4 | Spine longitude | q-fraction 0.42 | Dual-craton suture placement |
| A5 | SE arc / SW hotspot / rift / basin centers | see `config.py` | Spatial encoding of locked history |
| A6 | Latitude band | ~55°N–28°N | Earth-like westerlies belt |
| A7 | Sea-level temp | 14 °C mid-ref | Before lapse |
| A8 | Lapse rate | 6.5 °C/km | Earth-like |
| A9 | Base precip | 850 mm/yr | Before orography |
| A10 | Orographic gain / rain-shadow loss | 1.8 / 0.35 | Toy |
| A11 | Empty city-candidate fraction | 20% | Within 15–25% band |
| A12 | River accumulation thresholds | 8 / 28 | Toy runoff units |
| A13 | Map cells | 8×8 px/hex square grid | Not true hex geometry; GM-readable |
| A14 | Unknown lithology on ingest | → craton granite code | If Geologist string unmatched |
| A15 | Settlement tier thresholds | 1.5 / 3.5 / 5.5 / 7.5 | Raw score buckets |

When `data/geology_hex.csv` is present, elevation/lithology/glacial/endorheic/geology_resource_tag come from Geologist; climate-orography still uses Cartographer ASSUMPTION parameters unless Climate replaces them later.
