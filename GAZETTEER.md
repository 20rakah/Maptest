# Gazetteer — World Seed 01

## Front matter

| Field | Value |
|---|---|
| World | World Seed 01 |
| Seed | `1001` |
| Grid | 80×60 hexes @ 30 km/hex (~2400×1800 km) |
| Status | **Climate V1 locked** (Referee CLEAR; rain_shadow HOLD cleared) — `DRAIN_V3_ENDO_939` |
| Land / ocean | 3325 land / 1475 ocean |
| Regions | 18 (all land hexes covered) |
| Residual ice | **0** hexes |
| Endorheic (A19) | **939** hexes; centroid ~(0.45, 0.51) |
| rain_shadow | **113** (orographic lee) |
| dry_interior | **862** (closed-basin) |

**Sources:** `data/hexes.csv` (incl. `wt_depth_m`, `shallow_well`/`spring_line`, `rain_shadow`/`dry_interior`), `data/climate_hex.csv`, `docs/SCRIBE_CLIMATE_NOTES.md`, `docs/CLIMATE_KEY.md`, Climate-signed `CLIMATE_CALENDAR.md` (not overwritten), `data/geology_hex.csv`.

**Hard rule:** If map ≠ prose, **stop and flag**. No invented kingdoms/dynasties/pantheons. Working geographic names only. Prefer `geology_hex` lithology. **rain_shadow ≠ dry_interior** (KEY). Cite `wt_depth_m` from data for well-depth hooks — do not invent depths.

**Tour order:** windward/leeward spine flanks → farm belts → coasts → **A19 endorheic salt sill + inland-sea floor** → SE arc & craton → northern rift → SW hotspot.

## West Spine Windward Flank

*id:* `west-spine-windward-flank` · *hexes:* 99 · *bbox:* q 24–28, r 37–59
*Sample hexes:* H+24+59, H+28+37, H+24+53, H+24+46, H+24+58, H+27+37

### Landform
Upland / hills; dominant terrain `farmland` (farmland×46, forest×45, grassland×5, hills×2). Elev mean 469 m (range 91–2161); slope mean 7.7, max 52.5. Lithology (geology_hex): `suture_metamorphic`. Mountain type mode: `collision`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; wet (windward orographic). Mean temp 15.5 °C (range 1.3–20.7); mean precip 944 mm (range 665–2215). Wind mode `open_westerly`; seasonality `weak`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: major_river×1, river×9, spring_line×2, shallow_well×87. Drinkable groundwater on 89 hexes (`shallow_well` / `spring_line`) — **not** waterless. Full water histogram: shallow_well×87, river×9, spring_line×2, major_river×1. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.8 m.

### Food
Dominant food `good` (good×52, rich×46, none×1). Soil mode `loam`; vegetation mode `temperate forest`.

### Resources
Present tags: `timber`×28, `stone`×11, `limestone_karst`×8, `pasture`×5, `fisheries`×3. (`none` on 58 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; windward forest farmers.

### Travel catch
**steep_slope_corridor** — 4 hexes with slope>=8 (max 52.5); travel constrained to lower-slope gaps (e.g. H+28+38, H+27+37, H+27+38, H+28+37) **ford_or_river_crossing** — 10 river hexes (1 major_river); crossings where farmland/settlement meets channel (e.g. H+27+39, H+25+59, H+24+59, H+24+53) **groundwater_dependence** — 89 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+27+37, H+27+38, H+27+40, H+27+41)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+27+39, H+25+59, H+24+59, H+24+53, H+24+48.
2. **Karst sink / disappearing stream hazard** — limestone_karst in resources/geology tags Supporting hexes: H+27+39, H+27+47, H+25+59, H+25+51, H+25+55.

## Northwest Spine Windward Flank

*id:* `northwest-spine-windward-flank` · *hexes:* 61 · *bbox:* q 24–27, r 16–33
*Sample hexes:* H+24+16, H+27+24, H+24+17, H+24+31, H+24+18, H+24+19

### Landform
Upland / hills; dominant terrain `farmland` (farmland×26, forest×22, high_peaks×9, hills×2). Elev mean 572 m (range 155–1971); slope mean 20.9, max 59.0. Lithology (geology_hex): `suture_metamorphic`. Mountain type mode: `collision`. Glacial-scar hexes: 18 (post-LGM scars only; **no residual ice**).

### Climate
Temperate; wet (windward orographic). Mean temp 8.5 °C (range -0.1–13.3); mean precip 1150 mm (range 672–2562). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×1, spring_line×1, shallow_well×33. Drinkable groundwater on 34 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×26 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×33, none×26, spring_line×1, river×1. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.9 m; dry wt_class `wt_depth_m` 8.0–9.5 m.

### Food
Dominant food `rich` (rich×26, good×24, modest×11). Soil mode `loam`; vegetation mode `floodplain farmable`.

### Resources
Present tags: `timber`×18, `limestone_karst`×7, `stone`×6. (`none` on 39 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; windward timber-and-trap bands.

### Travel catch
**steep_slope_corridor** — 20 hexes with slope>=8 (max 59.0); travel constrained to lower-slope gaps (e.g. H+24+33, H+27+23, H+27+26, H+26+26) **ford_or_river_crossing** — 1 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+24+31) **groundwater_dependence** — 34 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+24+16, H+24+17, H+24+18, H+24+19)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+24+31.
2. **Karst sink / disappearing stream hazard** — limestone_karst in resources/geology tags Supporting hexes: H+24+30, H+24+33, H+27+21, H+25+26, H+25+17.

## East Spine Leeward Slopes

*id:* `east-spine-leeward-slopes` · *hexes:* 80 · *bbox:* q 39–42, r 35–59
*Sample hexes:* H+42+42, H+40+50, H+41+38, H+41+35, H+41+36, H+41+37

### Landform
Upland / hills; dominant terrain `grassland` (grassland×53, high_peaks×21, hills×6). Elev mean 742 m (range 108–1989); slope mean 33.5, max 58.7. Lithology (geology_hex): `suture_metamorphic`. Mountain type mode: `collision`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Temperate; dry / rain-shadow lee. Mean temp 13.5 °C (range 3.8–20.1); mean precip 551 mm (range 247–641). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 27 hexes (34%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `none`. Counts: shallow_well×37. Drinkable groundwater on 37 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×43 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: none×43, shallow_well×37. Water-table depth: groundwater hex `wt_depth_m` 6.5–8.0 m; dry wt_class `wt_depth_m` 8.0–16.4 m.

### Food
Dominant food `good` (good×74, modest×5, none×1). Soil mode `loam`; vegetation mode `grassland/pasture`.

### Resources
Present tags: `pasture`×59, `stone`×25, `limestone_karst`×9, `timber`×4, `metals`×1. (`none` on 5 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; well-dependent dryland farmers; lee-side steppe herders / well users; pasture herders.

### Travel catch
**steep_slope_corridor** — 52 hexes with slope>=8 (max 58.7); travel constrained to lower-slope gaps (e.g. H+39+38, H+40+38, H+40+36, H+41+36) **groundwater_dependence** — 37 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+41+38, H+41+39, H+41+40, H+41+41) **rain_shadow_lee** — 27 `rain_shadow` hexes (orographic lee of suture ~q 0.42 and/or SE arc) — water points control routes (e.g. H+41+35, H+39+59, H+39+39, H+39+38)

### Hooks
1. **Lee / rain shadow water-point monopoly** — rain_shadow=true lee east of suture (~q 0.42) and/or SE arc — wells and springs control caravans Supporting hexes: H+41+35, H+39+59, H+39+39, H+39+38, H+40+37.
2. **Failing / deep wells on rain_shadow lee margins** — wt_class=dry with wt_depth_m>=10 m — H+41+54=16.4m, H+40+56=15.4m, H+40+55=15.2m, H+40+41=15.1m, H+39+58=15.1m Supporting hexes: H+41+54, H+40+56, H+40+55, H+40+41, H+39+58.

## Western Farm Belt

*id:* `western-farm-belt` · *hexes:* 99 · *bbox:* q 13–23, r 17–37
*Sample hexes:* H+20+18, H+23+33, H+23+19, H+23+18, H+23+17, H+23+30

### Landform
Upland / hills; dominant terrain `farmland` (farmland×67, grassland×26, forest×5, hills×1). Elev mean 206 m (range 84–724); slope mean 2.6, max 18.7. Lithology (geology_hex): `craton_granite_gneiss`. Mountain type mode: `none`. Glacial-scar hexes: 3 (post-LGM scars only; **no residual ice**).

### Climate
Temperate; moderate. Mean temp 12.1 °C (range 8.9–15.7); mean precip 722 mm (range 637–1184). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: major_river×23, river×10, shallow_well×44. Drinkable groundwater on 44 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×22 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×44, major_river×23, none×22, river×10. Water-table depth: groundwater hex `wt_depth_m` 2.5–8.0 m; dry wt_class `wt_depth_m` 8.0–9.1 m.

### Food
Dominant food `rich` (rich×67, good×32). Soil mode `loam`; vegetation mode `floodplain farmable`.

### Resources
Present tags: `fisheries`×30, `pasture`×26, `stone`×9, `timber`×6, `greenstone_metals`×4. (`none` on 32 hexes.)

### Who would live here
Adaptations the landform supports: river-ford farmers / boat people; well-dependent dryland farmers; pasture herders; pass wardens / highland drovers.

### Travel catch
**steep_slope_corridor** — 6 hexes with slope>=8 (max 18.7); travel constrained to lower-slope gaps (e.g. H+21+33, H+22+33, H+22+32, H+23+31) **ford_or_river_crossing** — 33 river hexes (23 major_river); crossings where farmland/settlement meets channel (e.g. H+23+18, H+23+19, H+23+20, H+23+21) **groundwater_dependence** — 44 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+23+17, H+20+34, H+19+35, H+18+36)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+23+19, H+23+20, H+23+21, H+23+23, H+23+24.
2. **Vacant prime site (excellent but unsettle-scored empty)** — why='excellent site left empty on purpose' Supporting hexes: H+23+18, H+23+22, H+19+30, H+19+29.

## Northwest Farm Belt

*id:* `northwest-farm-belt` · *hexes:* 43 · *bbox:* q 4–11, r 27–38
*Sample hexes:* H+11+38, H+08+32, H+09+36, H+08+28, H+08+27, H+07+29

### Landform
Lowland; dominant terrain `farmland` (farmland×42, grassland×1). Elev mean 101 m (range 82–128); slope mean 0.7, max 1.2. Lithology (geology_hex): `craton_granite_gneiss`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; moderate. Mean temp 14.8 °C (range 13.3–16.1); mean precip 734 mm (range 635–802). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×3, shallow_well×40. Drinkable groundwater on 40 hexes (`shallow_well` / `spring_line`) — **not** waterless. Full water histogram: shallow_well×40, river×3. Water-table depth: groundwater hex `wt_depth_m` 5.8–7.3 m.

### Food
Dominant food `rich` (rich×42, good×1). Soil mode `loam`; vegetation mode `floodplain farmable`.

### Resources
Present tags: `pasture`×1. (`none` on 42 hexes.)

### Who would live here
Adaptations the landform supports: river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**ford_or_river_crossing** — 3 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+08+27, H+10+35, H+09+36) **groundwater_dependence** — 40 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+08+28, H+07+29, H+07+30, H+07+31)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+09+36.
2. **Vacant prime site (excellent but unsettle-scored empty)** — why='excellent site left empty on purpose' Supporting hexes: H+08+27, H+10+35.

## Eastern Riverine Farm Corridors

*id:* `eastern-riverine-farm-corridors` · *hexes:* 143 · *bbox:* q 42–61, r 24–50
*Sample hexes:* H+48+45, H+42+34, H+48+37, H+57+35, H+48+38, H+45+36

### Landform
Lowland; dominant terrain `farmland` (farmland×80, grassland×62, hills×1). Elev mean 110 m (range 92–832); slope mean 4.0, max 22.8. Lithology (geology_hex): `craton_granite_gneiss`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; moderate. Mean temp 15.3 °C (range 9.2–18.1); mean precip 616 mm (range 551–696). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 1 hexes (1%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: major_river×3, river×47, spring_line×18, shallow_well×60. Drinkable groundwater on 78 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×15 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×60, river×47, spring_line×18, none×15, major_river×3. Water-table depth: groundwater hex `wt_depth_m` 2.5–8.0 m; dry wt_class `wt_depth_m` 8.0–12.9 m.

### Food
Dominant food `rich` (rich×80, good×63). Soil mode `loam`; vegetation mode `floodplain farmable`.

### Resources
Present tags: `pasture`×63, `fisheries`×25, `greenstone_metals`×8, `stone`×1. (`none` on 51 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 29 hexes with slope>=8 (max 22.8); travel constrained to lower-slope gaps (e.g. H+43+35, H+44+35, H+45+35, H+45+36) **ford_or_river_crossing** — 50 river hexes (3 major_river); crossings where farmland/settlement meets channel (e.g. H+45+36, H+47+36, H+48+36, H+48+37) **groundwater_dependence** — 78 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+48+38, H+48+39, H+48+41, H+48+43)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+45+36, H+47+36, H+48+36, H+48+37, H+48+42.
2. **Wells and spring-lines control dryland travel** — Drinkable groundwater hexes (`shallow_well`/`spring_line`) amid lee or basin dryness — not waterless Supporting hexes: H+48+38, H+48+39, H+48+41, H+48+43, H+48+44.

## Inner Eastern Farm Corridors

*id:* `inner-eastern-farm-corridors` · *hexes:* 106 · *bbox:* q 38–59, r 16–28
*Sample hexes:* H+50+19, H+38+28, H+46+16, H+59+17, H+44+16, H+45+20

### Landform
Lowland; dominant terrain `farmland` (farmland×62, coast×30, grassland×14). Elev mean 155 m (range 0–663); slope mean 5.7, max 16.5. Lithology (geology_hex): `craton_granite_gneiss`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Temperate; moderate. Mean temp 10.2 °C (range 8.5–11.5); mean precip 725 mm (range 620–761). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×6, spring_line×11, shallow_well×77. Drinkable groundwater on 88 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×12 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×77, none×12, spring_line×11, river×6. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.2 m; dry wt_class `wt_depth_m` 9.4–11.3 m.

### Food
Dominant food `rich` (rich×62, none×30, good×14). Soil mode `loam`; vegetation mode `floodplain farmable`.

### Resources
Present tags: `pasture`×14, `greenstone_metals`×3. (`none` on 90 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 20 hexes with slope>=8 (max 16.5); travel constrained to lower-slope gaps (e.g. H+41+24, H+42+23, H+57+22, H+54+21) **ford_or_river_crossing** — 6 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+45+20, H+43+21, H+43+20, H+43+22) **groundwater_dependence** — 88 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+44+16, H+44+17, H+44+18, H+45+18)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+43+22, H+42+23, H+41+24.
2. **Vacant prime site (excellent but unsettle-scored empty)** — why='excellent site left empty on purpose' Supporting hexes: H+44+18, H+47+16, H+54+16, H+56+16, H+43+18.

## Western Coastal Margin

*id:* `western-coastal-margin` · *hexes:* 400 · *bbox:* q 0–23, r 13–59
*Sample hexes:* H+08+13, H+06+17, H+20+54, H+07+21, H+07+18, H+07+13

### Landform
Lowland; dominant terrain `coast` (coast×280, forest×84, farmland×31, grassland×5). Elev mean 67 m (range 1–135); slope mean 1.4, max 6.7. Lithology (geology_hex): `coastal_sediment`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; moist. Mean temp 15.8 °C (range 9.8–20.7); mean precip 763 mm (range 640–883). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: major_river×35, river×60, spring_line×35, shallow_well×270. Drinkable groundwater on 305 hexes (`shallow_well` / `spring_line`) — **not** waterless. Full water histogram: shallow_well×270, river×60, spring_line×35, major_river×35. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.7 m.

### Food
Dominant food `none` (none×258, good×89, rich×31, modest×22). Soil mode `sandy coastal`; vegetation mode `coastal scrub`.

### Resources
Present tags: `clay`×83, `fisheries`×36, `timber`×35, `pasture`×5, `greenstone_metals`×2. (`none` on 263 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**ford_or_river_crossing** — 95 river hexes (35 major_river); crossings where farmland/settlement meets channel (e.g. H+07+21, H+03+36, H+03+37, H+05+45) **groundwater_dependence** — 305 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+07+13, H+07+14, H+07+15, H+07+16)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+07+21, H+03+37, H+05+45, H+08+49, H+08+44.
2. **Vacant prime site (excellent but unsettle-scored empty)** — why='excellent site left empty on purpose' Supporting hexes: H+18+53, H+22+55, H+21+56, H+23+51.

## Eastern Coastal Margin

*id:* `eastern-coastal-margin` · *hexes:* 159 · *bbox:* q 68–79, r 16–42
*Sample hexes:* H+75+30, H+75+38, H+78+41, H+76+16, H+76+26, H+76+17

### Landform
Lowland; dominant terrain `coast` (coast×155, grassland×4). Elev mean 38 m (range 1–189); slope mean 0.9, max 5.2. Lithology (geology_hex): `coastal_sediment`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Temperate; moderate. Mean temp 13.7 °C (range 10.7–16.3); mean precip 572 mm (range 492–642). Wind mode `open_westerly`; seasonality `strong`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 2 hexes (1%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `none`. Counts: major_river×3, river×20, shallow_well×62. Drinkable groundwater on 62 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×74 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: none×74, shallow_well×62, river×20, major_river×3. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.9 m; dry wt_class `wt_depth_m` 8.0–11.1 m.

### Food
Dominant food `none` (none×152, good×4, modest×3). Soil mode `sandy coastal`; vegetation mode `coastal scrub`.

### Resources
Present tags: `clay`×127, `fisheries`×11, `pasture`×4. (`none` on 30 hexes.)

### Who would live here
Adaptations the landform supports: river-ford farmers / boat people; well-dependent dryland farmers; pasture herders; coastal / river fishers.

### Travel catch
**ford_or_river_crossing** — 23 river hexes (3 major_river); crossings where farmland/settlement meets channel (e.g. H+76+26, H+76+30, H+76+33, H+78+40) **groundwater_dependence** — 62 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+76+16, H+76+17, H+76+27, H+76+28)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+78+41, H+72+34, H+73+33.
2. **Wells and spring-lines control dryland travel** — Drinkable groundwater hexes (`shallow_well`/`spring_line`) amid lee or basin dryness — not waterless Supporting hexes: H+76+16, H+76+17, H+76+27, H+76+28, H+76+29.

## Southern Coastal Margin

*id:* `southern-coastal-margin` · *hexes:* 100 · *bbox:* q 43–63, r 52–59
*Sample hexes:* H+63+57, H+55+54, H+52+52, H+54+58, H+57+58, H+56+57

### Landform
Lowland; dominant terrain `grassland` (grassland×51, farmland×49). Elev mean 168 m (range 146–183); slope mean 1.2, max 8.1. Lithology (geology_hex): `coastal_sediment`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm; dry. Mean temp 19.6 °C (range 18.6–20.6); mean precip 544 mm (range 472–598). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `none`. Counts: major_river×10, river×28, spring_line×2, shallow_well×13. Drinkable groundwater on 15 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×47 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: none×47, river×28, shallow_well×13, major_river×10, spring_line×2. Water-table depth: groundwater hex `wt_depth_m` 2.5–8.0 m; dry wt_class `wt_depth_m` 8.0–9.4 m.

### Food
Dominant food `good` (good×51, rich×49). Soil mode `sandy coastal`; vegetation mode `grassland/pasture`.

### Resources
Present tags: `clay`×74, `pasture`×51, `fisheries`×21. (`none` on 6 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 2 hexes with slope>=8 (max 8.1); travel constrained to lower-slope gaps (e.g. H+57+58, H+56+58) **ford_or_river_crossing** — 38 river hexes (10 major_river); crossings where farmland/settlement meets channel (e.g. H+52+52, H+52+54, H+52+55, H+52+56) **groundwater_dependence** — 15 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+56+57, H+56+58, H+57+58, H+59+57)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+52+52, H+52+54, H+52+55, H+52+58, H+52+59.
2. **Wells and spring-lines control dryland travel** — Drinkable groundwater hexes (`shallow_well`/`spring_line`) amid lee or basin dryness — not waterless Supporting hexes: H+56+57, H+56+58, H+57+58, H+59+57, H+60+57.

## Endorheic Salt Flats (A19 Sill)

*id:* `endorheic-salt-flats` · *hexes:* 765 · *bbox:* q 15–59, r 0–59
*Sample hexes:* H+29+00, H+30+00, H+40+27, H+29+01, H+29+02, H+29+03

### Landform
Closed-basin salt sill / playa; dominant terrain `salt_pan` (salt_pan×708, marsh×55, grassland×2). Elev mean 589 m (range 589–589); slope mean 4.2, max 52.4. Lithology (geology_hex): `basin_sediment`. Mountain type mode: `none`. Glacial-scar hexes: 429 (post-LGM scars only; **no residual ice**).

**A19 sill:** flat playa at ~**589 m** on the large closed catchment (CSV `endorheic=true`, **939** hexes with the inland-sea floor). Centroid ~(0.45, 0.51). Basin dryness here is **`dry_interior`**, not continent-wide rain_shadow. Rivers terminate in the basin — never the ocean.

### Climate
Temperate; arid closed-basin (dry_interior). Mean temp 9.9 °C (range 1.4–17.1); mean precip 442 mm (range 287–654). Wind mode `calm_interior`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 24 hexes (3%). **dry_interior** (closed-basin dryness, not lee orography): 688 hexes (90%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `salt_pan`. Counts: salt_pan×708, wetland×55, endorheic×765. `none`×2 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: salt_pan×708, wetland×55, none×2. Water-table depth: dry wt_class `wt_depth_m` 8.1–13.6 m.

### Food
Dominant food `poor` (poor×708, modest×55, good×2). Soil mode `saline playa`; vegetation mode `salt flat sparse`.

### Resources
Present tags: `evaporite_host`×765, `salt_pans`×708, `peat`×55, `clay`×21, `pasture`×2.

### Who would live here
Adaptations the landform supports: salt-cutters / evaporite caravans; rim herders skirting the brine; waystation keepers on the dry sill edge.

### Travel catch
**steep_slope_corridor** — 111 hexes with slope>=8 (max 52.4); travel constrained to lower-slope gaps (e.g. H+39+36, H+40+35, H+41+34, H+39+37) **salt_pan_crossing** — 708 salt-pan sill hexes (~589 m); saline — not potable; skirt the crust or carry water (e.g. H+29+00, H+29+01, H+29+02, H+29+03) **rain_shadow_lee** — 24 `rain_shadow` hexes (orographic lee of suture ~q 0.42 and/or SE arc) — water points control routes (e.g. H+40+27, H+40+26, H+41+25, H+42+24) **dry_interior_basin** — 688 `dry_interior` hexes (closed-basin precip deficit, NOT rain_shadow) — brine/well logistics (e.g. H+29+00, H+29+01, H+30+07, H+31+08)

### Hooks
1. **Salt pan / evaporite sill gathering** — A19 catchment sill ~589 m: salt_pan + salt_pans resource; dry_interior basin dryness (not rain_shadow) Supporting hexes: H+29+00, H+29+01, H+29+02, H+29+03, H+29+04.
2. **Failing / deep wells on rain_shadow lee margins** — wt_class=dry with wt_depth_m>=10 m — H+27+28=13.6m, H+27+29=13.6m, H+41+34=13.5m, H+28+29=13.5m, H+27+27=13.4m Supporting hexes: H+27+28, H+27+29, H+41+34, H+28+29, H+27+27.

## Endorheic Inland Sea (A19 Floor)

*id:* `endorheic-inland-sea` · *hexes:* 174 · *bbox:* q 40–58, r 23–34
*Sample hexes:* H+49+28, H+58+29, H+45+23, H+45+24, H+45+25, H+45+26

### Landform
Closed-basin deep floor (inland sea); dominant terrain `inland_sea` (inland_sea×174). Elev mean 66 m (range 63–67); slope mean 5.0, max 17.4. Lithology (geology_hex): `basin_sediment`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

**A19 deep floor:** permanent inland sea on the carved basin floor (~60–120 m), with wetland fringe where sill meets water. Same closed catchment as the salt flats (Geology A19 / Climate C10–C12).

### Climate
Temperate; arid closed-basin (dry_interior). Mean temp 13.1 °C (range 11.6–14.8); mean precip 402 mm (range 380–450). Wind mode `calm_interior`; seasonality `strong`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 174 hexes (100%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `inland_sea`. Counts: inland_sea×174, endorheic×174. Full water histogram: inland_sea×174.

### Food
Dominant food `modest` (modest×174). Soil mode `clay basin`; vegetation mode `none/ocean`.

### Resources
Present tags: `fisheries`×174, `evaporite_host`×174, `clay`×29.

### Who would live here
Adaptations the landform supports: lakeshore fishers on the closed sea; fringe reed-cutters / marsh foragers; brine-edge salt traders.

### Travel catch
**steep_slope_corridor** — 50 hexes with slope>=8 (max 17.4); travel constrained to lower-slope gaps (e.g. H+45+23, H+53+23, H+57+31, H+58+29) **endorheic_closed_sea** — Closed A19 drainage; inland_sea=174 wetland=0; rivers terminate here — never the ocean (e.g. H+45+23, H+45+24, H+45+25, H+45+26) **dry_interior_basin** — 174 `dry_interior` hexes (closed-basin precip deficit, NOT rain_shadow) — brine/well logistics (e.g. H+45+23, H+45+24, H+45+25, H+45+26)

### Hooks
1. **Stranded shoreline around endorheic inland sea** — Deep floor inland_sea (~60–120 m) with wetland fringe; closed A19 drainage Supporting hexes: H+45+23, H+45+24, H+45+25, H+45+26, H+45+27.
2. **Closed-basin dry_interior logistics** — dry_interior precip deficit inside endorheic mask — distinct from orographic rain_shadow Supporting hexes: H+45+23, H+45+24, H+45+25, H+45+26, H+45+27.

## Southeast Volcanic Arc

*id:* `southeast-volcanic-arc` · *hexes:* 473 · *bbox:* q 49–77, r 34–56
*Sample hexes:* H+66+34, H+65+46, H+65+39, H+77+41, H+65+56, H+61+36

### Landform
Upland / hills; dominant terrain `grassland` (grassland×263, forest×107, farmland×63, coast×37). Elev mean 490 m (range 1–1114); slope mean 4.2, max 15.6. Lithology (geology_hex): `arc_andesite_volcanic`. Mountain type mode: `arc`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; moderate. Mean temp 14.8 °C (range 11.1–19.6); mean precip 639 mm (range 459–980). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 36 hexes (8%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `none`. Counts: major_river×11, river×31, spring_line×9, shallow_well×167. Drinkable groundwater on 176 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×255 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: none×255, shallow_well×167, river×31, major_river×11, spring_line×9. Water-table depth: groundwater hex `wt_depth_m` 2.5–8.0 m; dry wt_class `wt_depth_m` 8.0–11.3 m.

### Food
Dominant food `good` (good×373, rich×63, none×26, modest×11). Soil mode `volcanic andisol`; vegetation mode `grassland/pasture`.

### Resources
Present tags: `pasture`×263, `obsidian`×115, `timber`×72, `volcanic_host`×30, `fisheries`×18, `greenstone_metals`×3. (`none` on 100 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 31 hexes with slope>=8 (max 15.6); travel constrained to lower-slope gaps (e.g. H+55+48, H+56+47, H+64+56, H+65+56) **ford_or_river_crossing** — 42 river hexes (11 major_river); crossings where farmland/settlement meets channel (e.g. H+61+56, H+65+38, H+65+39, H+65+40) **groundwater_dependence** — 176 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+61+36, H+61+37, H+61+38, H+61+39) **rain_shadow_lee** — 36 `rain_shadow` hexes (orographic lee of suture ~q 0.42 and/or SE arc) — water points control routes (e.g. H+75+51, H+75+50, H+75+49, H+75+48)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+65+39, H+65+40, H+65+41, H+73+42, H+75+41.
2. **Lee / rain shadow water-point monopoly** — rain_shadow=true lee east of suture (~q 0.42) and/or SE arc — wells and springs control caravans Supporting hexes: H+75+51, H+75+50, H+75+49, H+75+48, H+75+47.

## Southeast Craton Plains

*id:* `southeast-craton-plains` · *hexes:* 58 · *bbox:* q 43–51, r 45–53
*Sample hexes:* H+44+46, H+50+49, H+47+52, H+49+45, H+49+46, H+48+47

### Landform
Upland / hills; dominant terrain `grassland` (grassland×42, farmland×12, forest×4). Elev mean 237 m (range 110–574); slope mean 3.8, max 13.4. Lithology (geology_hex): `craton_granite_gneiss`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; moderate. Mean temp 17.4 °C (range 15.3–18.8); mean precip 629 mm (range 541–933). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×4, shallow_well×50. Drinkable groundwater on 50 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×4 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×50, none×4, river×4. Water-table depth: groundwater hex `wt_depth_m` 6.4–8.0 m; dry wt_class `wt_depth_m` 8.1–8.7 m.

### Food
Dominant food `good` (good×46, rich×12). Soil mode `loam`; vegetation mode `grassland/pasture`.

### Resources
Present tags: `pasture`×42, `greenstone_metals`×3, `fisheries`×2, `stone`×1. (`none` on 13 hexes.)

### Who would live here
Adaptations the landform supports: river-ford farmers / boat people; well-dependent dryland farmers; pasture herders; pass wardens / highland drovers.

### Travel catch
**steep_slope_corridor** — 11 hexes with slope>=8 (max 13.4); travel constrained to lower-slope gaps (e.g. H+45+52, H+47+50, H+46+51, H+46+52) **ford_or_river_crossing** — 4 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+47+52, H+47+53, H+48+53, H+49+53) **groundwater_dependence** — 50 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+49+45, H+49+46, H+48+47, H+47+48)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+47+52, H+47+53, H+48+53, H+49+53.
2. **Wells and spring-lines control dryland travel** — Drinkable groundwater hexes (`shallow_well`/`spring_line`) amid lee or basin dryness — not waterless Supporting hexes: H+49+45, H+49+46, H+48+47, H+47+48, H+46+49.

## Northern Rift Corridor

*id:* `northern-rift-corridor` · *hexes:* 204 · *bbox:* q 37–59, r 0–23
*Sample hexes:* H+51+14, H+38+15, H+40+08, H+40+07, H+42+00, H+40+06

### Landform
Upland / hills; dominant terrain `boreal` (boreal×73, coast×49, forest×46, grassland×23). Elev mean 254 m (range 1–865); slope mean 5.7, max 15.6. Lithology (geology_hex): `rift_volcanics`. Mountain type mode: `rift`. Glacial-scar hexes: 157 (post-LGM scars only; **no residual ice**).

### Climate
Cool temperate / boreal-leaning; moderate. Mean temp 6.3 °C (range 1.0–11.0); mean precip 738 mm (range 603–850). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 23 hexes (11%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×4, spring_line×55, shallow_well×114. Drinkable groundwater on 169 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×31 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×114, spring_line×55, none×31, river×4. Water-table depth: groundwater hex `wt_depth_m` 2.5–8.0 m; dry wt_class `wt_depth_m` 8.0–11.2 m.

### Food
Dominant food `modest` (modest×76, good×71, none×49, rich×8). Soil mode `glacial till`; vegetation mode `boreal forest`.

### Resources
Present tags: `timber`×110, `clay`×43, `pasture`×25, `metals`×17, `stone`×17, `volcanic_host`×6, `limestone_karst`×5. (`none` on 39 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 34 hexes with slope>=8 (max 15.6); travel constrained to lower-slope gaps (e.g. H+37+10, H+38+10, H+59+15, H+40+15) **ford_or_river_crossing** — 4 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+42+00, H+43+00, H+41+20, H+41+19) **groundwater_dependence** — 169 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+40+07, H+40+08, H+40+09, H+39+10) **rain_shadow_lee** — 23 `rain_shadow` hexes (orographic lee of suture ~q 0.42 and/or SE arc) — water points control routes (e.g. H+40+06, H+39+15, H+38+15, H+38+14)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+41+20, H+41+19.
2. **Failing / deep wells on rain_shadow lee margins** — wt_class=dry with wt_depth_m>=10 m — H+39+23=11.2m, H+39+22=10.9m, H+39+21=10.6m Supporting hexes: H+39+23, H+39+22, H+39+21.

## Far-North Rift Corridor

*id:* `far-north-rift-corridor` · *hexes:* 123 · *bbox:* q 17–30, r 0–17
*Sample hexes:* H+26+12, H+29+07, H+20+06, H+21+07, H+27+11, H+20+07

### Landform
Upland / hills; dominant terrain `boreal` (boreal×79, forest×16, coast×10, farmland×6). Elev mean 325 m (range 2–1051); slope mean 6.3, max 16.1. Lithology (geology_hex): `rift_volcanics`. Mountain type mode: `rift`. Glacial-scar hexes: 119 (post-LGM scars only; **no residual ice**).

### Climate
Cool temperate / boreal-leaning; wet (windward orographic). Mean temp 5.3 °C (range 0.8–9.2); mean precip 974 mm (range 684–1566). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×21, wetland×2, spring_line×29, shallow_well×71. Drinkable groundwater on 100 hexes (`shallow_well` / `spring_line`) — **not** waterless. Full water histogram: shallow_well×71, spring_line×29, river×21, wetland×2. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.2 m.

### Food
Dominant food `modest` (modest×88, good×19, none×10, rich×6). Soil mode `glacial till`; vegetation mode `boreal forest`.

### Resources
Present tags: `timber`×100, `clay`×33, `metals`×26, `stone`×13, `fisheries`×9, `gems`×8, `pasture`×3, `peat`×2. (`none` on 15 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; windward timber-and-trap bands.

### Travel catch
**steep_slope_corridor** — 36 hexes with slope>=8 (max 16.1); travel constrained to lower-slope gaps (e.g. H+30+11, H+21+07, H+22+06, H+22+07) **ford_or_river_crossing** — 21 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+27+11, H+25+14, H+28+11, H+18+02) **groundwater_dependence** — 100 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+20+06, H+20+07, H+21+07, H+22+06)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+28+11, H+22+04, H+22+01, H+21+01, H+21+00.
2. **Hard-rock metal prospects along suture/greenstone tags** — metals or greenstone_metals in resources Supporting hexes: H+27+09, H+27+10, H+28+08, H+28+07, H+28+09.

## Southwest Hotspot Uplands

*id:* `southwest-hotspot-uplands` · *hexes:* 105 · *bbox:* q 10–25, r 37–48
*Sample hexes:* H+10+44, H+15+43, H+24+44, H+15+37, H+20+48, H+15+38

### Landform
Upland / hills; dominant terrain `forest` (forest×77, farmland×17, coast×7, grassland×4). Elev mean 369 m (range 35–807); slope mean 5.4, max 9.4. Lithology (geology_hex): `hotspot_basalt`. Mountain type mode: `hotspot`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Warm temperate; moist. Mean temp 14.9 °C (range 11.5–18.1); mean precip 804 mm (range 675–1164). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: major_river×2, river×3, shallow_well×75. Drinkable groundwater on 75 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×25 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×75, none×25, river×3, major_river×2. Water-table depth: groundwater hex `wt_depth_m` 6.0–8.0 m; dry wt_class `wt_depth_m` 8.1–9.6 m.

### Food
Dominant food `good` (good×81, rich×17, none×7). Soil mode `volcanic andisol`; vegetation mode `temperate forest`.

### Resources
Present tags: `timber`×45, `pasture`×4, `volcanic_host`×4, `obsidian`×4, `fisheries`×2. (`none` on 52 hexes.)

### Who would live here
Adaptations the landform supports: river-ford farmers / boat people; well-dependent dryland farmers; windward forest farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 12 hexes with slope>=8 (max 9.4); travel constrained to lower-slope gaps (e.g. H+17+45, H+16+46, H+15+43, H+14+44) **ford_or_river_crossing** — 5 river hexes (2 major_river); crossings where farmland/settlement meets channel (e.g. H+20+48, H+24+44, H+24+45, H+25+43) **groundwater_dependence** — 75 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+15+37, H+15+38, H+14+46, H+14+47)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+20+48, H+24+44, H+24+45, H+25+43, H+25+42.
2. **Volcanic-glass / volcanic-host quarries on arc or hotspot rock** — obsidian or volcanic_host in resources Supporting hexes: H+14+46, H+23+41, H+11+44, H+13+41, H+12+43.

## Western Craton Shield

*id:* `western-craton-shield` · *hexes:* 133 · *bbox:* q 8–21, r 19–37
*Sample hexes:* H+14+22, H+20+32, H+18+19, H+18+20, H+15+22, H+18+21

### Landform
Lowland; dominant terrain `grassland` (grassland×121, farmland×12). Elev mean 137 m (range 81–185); slope mean 0.9, max 9.7. Lithology (geology_hex): `craton_granite_gneiss`. Mountain type mode: `none`. Glacial-scar hexes: 0 (post-LGM scars only; **no residual ice**).

### Climate
Temperate; moderate. Mean temp 13.2 °C (range 10.9–15.8); mean precip 668 mm (range 611–699). Wind mode `open_westerly`; seasonality `moderate`. **rain_shadow** (orographic lee of suture ~q 0.42 and/or SE arc): 0 hexes (0%). **dry_interior** (closed-basin dryness, not lee orography): 0 hexes (0%). Source: Climate V1 (`climate_hex.csv` / signed calendar).

### Water
Dominant water class `shallow_well`. Counts: river×8, spring_line×2, shallow_well×118. Drinkable groundwater on 120 hexes (`shallow_well` / `spring_line`) — **not** waterless. `none`×5 = no surface water and no well/spring class (truly dry for logistics). Full water histogram: shallow_well×118, river×8, none×5, spring_line×2. Water-table depth: groundwater hex `wt_depth_m` 2.5–7.9 m; dry wt_class `wt_depth_m` 8.3–9.0 m.

### Food
Dominant food `good` (good×121, rich×12). Soil mode `loam`; vegetation mode `grassland/pasture`.

### Resources
Present tags: `pasture`×121, `greenstone_metals`×8. (`none` on 12 hexes.)

### Who would live here
Adaptations the landform supports: karst-spring settlement clusters; river-ford farmers / boat people; well-dependent dryland farmers; pasture herders.

### Travel catch
**steep_slope_corridor** — 1 hexes with slope>=8 (max 9.7); travel constrained to lower-slope gaps (e.g. H+21+32) **ford_or_river_crossing** — 8 river hexes (0 major_river); crossings where farmland/settlement meets channel (e.g. H+15+22, H+12+23, H+12+24, H+13+25) **groundwater_dependence** — 120 hexes with drinkable groundwater (`shallow_well`/`spring_line`) — not waterless; dry `none` hexes force routing to known wells/springs (e.g. H+18+19, H+18+20, H+18+21, H+18+22)

### Hooks
1. **Toll ford on farmed river corridor** — River/major_river hexes where settlement scores concentrate Supporting hexes: H+15+22, H+12+23, H+12+24, H+13+25, H+13+26.
2. **Vacant prime site (excellent but unsettle-scored empty)** — why='excellent site left empty on purpose' Supporting hexes: H+13+24.
