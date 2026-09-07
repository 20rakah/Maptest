# Climate Calendar — World Seed 01

> **STATUS: Climate V1 signed** (`DRAIN_V3_ENDO_939`, seed 1001).
>
> Numbers below are from current `data/climate_hex.csv` after Climate regen.  
> **Climate numbers are source of truth.** Scribe owns GM-voice polish of this calendar; do not invent countries.
>
> Region narrative notes: `docs/SCRIBE_CLIMATE_NOTES.md` (natural regions only).

## Continent snapshot (land)

| Metric | Value |
|--------|------:|
| Land hexes | 3325 |
| Mean temp °C | 12.6 |
| Mean precip mm/yr | 637 |
| rain_shadow (orographic lee) | 113 |
| dry_interior (closed-basin) | 862 |
| Endorheic (Geologist) | 939 |

## Latitude bands

**ASSUMPTION C1:** continent ~**55°N–28°N** (r=0 → ~55°N, r=59 → ~28°N, linear).

| r band | Approx latitude | Land hexes | Mean temp_c | Mean precip mm |
|--------|-----------------|----------:|----------:|---------------:|
| 0–10 | ~53°N | 312 | 4.3 | 732 |
| 10–20 | ~48°N | 353 | 8.3 | 692 |
| 20–30 | ~44°N | 635 | 11.2 | 613 |
| 30–40 | ~39°N | 741 | 13.5 | 606 |
| 40–50 | ~35°N | 745 | 14.7 | 654 |
| 50–60 | ~30°N | 539 | 17.6 | 590 |

Pattern from data: temperature rises and mean precip generally falls toward the south (higher r). Northern rows cooler; orography and basin dryness dominate local precip.

## Wet west / lee east of suture spine (~q 0.42)

| Flank | q window | Land hexes | Mean precip mm |
|-------|----------|----------:|---------------:|
| West of spine (orographic windward) | 24–32 | 526 | 756 |
| East of spine (rain-shadow lee) | 34–42 | 528 | 470 |

Westerlies lift on the suture spine (~q-fraction **0.42**) → wetter west flank; lee-side drying east of the crest.  
**`rain_shadow`** = orographic lee of suture and/or SE arc only (includes **exorheic** lee). Counts this run: rain_shadow=113 (exorheic lee=89, endorheic overlap=24 — a **subset**, not the whole 939-hex endorheic mask).

### SE arc (windward wet / lee dry)

| Arc flank | Land hexes | Mean precip mm | rain_shadow |
|-----------|----------:|---------------:|------------:|
| West of arc center (windward) | 334 | 684 | 0 |
| East of arc center (lee) | 219 | 549 | 38 |

ASSUMPTION C9 barrier fields: SE arc lee is east-side drying under westerlies (not inverted local-gradient).

## Endorheic: dry_interior vs inland_sea vs salt_pan

Geologist mask `endorheic` = **939** hexes (`DRAIN_V3_ENDO_939`). Climate does **not** treat the whole mask as rain_shadow.

| Class | Meaning | Count (this run) |
|-------|---------|-----------------:|
| dry_interior | `endorheic & land & precip < 550` — closed-basin dryness (ASSUMPTION **C23** / C4); **not** lee orography | 862 |
| inland_sea | Deep carved basin floor permanent water | 174 |
| salt_pan | Flat ~589 m sill playa | 708 |
| calm_interior wind | Endorheic flats without strong windward/leeward | 832 |
| calm_interior ∩ rain_shadow | Must stay ~0 (basin calm ≠ lee-shadow) | 0 |
| calm_interior ∩ dry_interior | Expected dry closed-basin interiors | 784 |

**rain_shadow ≠ dry_interior.** Lee of suture/arc is orographic; dry_interior is intentional endorheic precip deficit.

## Seasonal table (late-medieval Earth-like, ~28–55°N)

**ASSUMPTION (toy):** illustrative seasons for GM prep. Labels from `season_label` / `seasonality` on land this run: {np.str_('moderate'): 2327, np.str_('strong'): 807, np.str_('weak'): 191}. Absolute storm tracks / growing-degree days not locked.

| Season | Rough months (ASSUMPTION) | What GMs should expect |
|--------|---------------------------|------------------------|
| Deep winter | ~Dec–Feb | North (r≲15) near/below freezing; spine highlands cold; west lowlands milder/wetter. Residual ice hexes = 0 this run (C2). |
| Spring thaw / sowing | ~Mar–May | Mid-flank thaw; **ASSUMPTION** flood pulse on major_river corridors; wetlands/inland-sea fringe wettest. |
| High summer | ~Jun–Aug | Warm south (r≥50); **rain_shadow** lee + **dry_interior** basin driest — water-point travel; salt_pan brine. |
| Harvest / autumn rains | ~Sep–Nov | **ASSUMPTION** westerly storm track renews west-flank precip; early snow on high suture passes. |

Land `season_label` is weak/moderate/strong from seasonality index (C6); ocean = maritime.

## Region notes (do not invent countries)

Point Scribe to **`docs/SCRIBE_CLIMATE_NOTES.md`** for natural-region climate / food / adaptation one-liners.  
This calendar does **not** list kingdoms, borders, or country names.

## Ownership

| Owner | Owns |
|-------|------|
| Climate | Maps 03–08, `climate_hex.*`, precip/temp/wind/`rain_shadow`/`dry_interior`/water-table/soil/veg/climate resources, **this calendar's numbers** |
| Geologist | `geology_hex.*`, geology maps (untouched this run) |
| Scribe | GM voice polish of calendar prose; region notes file |
| Cartographer | Settlement packaging (map 09 / settle columns) |

Fingerprint: Geology `DRAIN_V3_ENDO_939` + Climate V1 barrier orography (C9) + dry_interior (C23).
