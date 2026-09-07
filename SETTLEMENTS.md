# Settlements — World Seed 01

## How to read settle_score

Tiers are **suitability labels**, not built places. Cartographer packaging on Climate V1 water/food:

| Tier | Land count | Meaning |
|---|---:|---|
| `city-candidate` | 149 | Best water + food + route combo; prime urban sites |
| `town` | 280 | Strong secondary nodes |
| `village` | 1047 | Ordinary agrarian / coastal clusters |
| `farmstead` | 604 | Thin scatter |
| `none` | 1245 | Unsuitable, open water, salt pan, or left empty |

**Water vocab:** `shallow_well` and `spring_line` in the `water` column are **drinkable groundwater** when there is no surface water. Do **not** read them as waterless. Only `water=none` (dry `wt_class`) is truly dry. Salt pans are saline — not potable.

**Well depth:** `wt_depth_m` (metres) sits beside `wt_class`. Use for deep/failing-well hooks on `rain_shadow` or `dry_interior` margins — cite hex id + depth from data, do not invent.

**Climate flags:** `rain_shadow` = orographic lee (suture ~q 0.42 and/or SE arc). `dry_interior` = closed-basin dryness. Do not conflate.

**37 excellent sites left empty on purpose**. Use as ruins, disputed ground, taboo ground, or future growth — not missing data.

No invented settlement names that imply polities. Cite **hex ids** + geographic descriptors only.

## Top corridor: windward farm rivers + groundwater benches

Dense city-candidate spine follows **windward / open-westerly farm belts** where farmland meets `major_river` / `river`, plus benches on `shallow_well` / `spring_line` (groundwater, not arid emptiness).

| id | q | r | terrain | water | wt_depth_m | food | resources | why |
|---|---:|---:|---|---|---:|---|---|---|
| H+20+18 | 20 | 18 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+21+18 | 21 | 18 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+22+18 | 22 | 18 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+19+19 | 19 | 19 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+23+19 | 23 | 19 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+19+20 | 19 | 20 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+23+20 | 23 | 20 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+19+21 | 19 | 21 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+23+21 | 23 | 21 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |
| H+19+22 | 19 | 22 | farmland | major_river | 1.5 | rich | fisheries | fresh water, strong food, route access, major river |

## Deep / failing table on dry margins (from `wt_depth_m`)

Not settlement sites — logistics hazards. Depths copied from hexes.csv.

### rain_shadow lee (orographic), wt_class=dry, depth≥10 m

| id | q | r | wt_depth_m | precip | region |
|---|---:|---:|---:|---:|---|
| H+41+54 | 41 | 54 | 16.4 | 247 | east-spine-leeward-slopes |
| H+40+56 | 40 | 56 | 15.4 | 421 | east-spine-leeward-slopes |
| H+40+55 | 40 | 55 | 15.2 | 443 | east-spine-leeward-slopes |
| H+40+41 | 40 | 41 | 15.1 | 310 | east-spine-leeward-slopes |
| H+39+58 | 39 | 58 | 15.1 | 466 | east-spine-leeward-slopes |
| H+39+57 | 39 | 57 | 15.0 | 484 | east-spine-leeward-slopes |
| H+40+54 | 40 | 54 | 14.9 | 460 | east-spine-leeward-slopes |
| H+40+53 | 40 | 53 | 14.8 | 464 | east-spine-leeward-slopes |

### dry_interior (closed-basin), wt_class=dry, depth≥10 m (sample)

| id | q | r | wt_depth_m | water | region |
|---|---:|---:|---:|---|---|
| H+27+28 | 27 | 28 | 13.6 | salt_pan | endorheic-salt-flats |
| H+27+29 | 27 | 29 | 13.6 | salt_pan | endorheic-salt-flats |
| H+41+34 | 41 | 34 | 13.5 | salt_pan | endorheic-salt-flats |
| H+28+29 | 28 | 29 | 13.5 | salt_pan | endorheic-salt-flats |
| H+27+27 | 27 | 27 | 13.4 | salt_pan | endorheic-salt-flats |
| H+27+30 | 27 | 30 | 13.3 | salt_pan | endorheic-salt-flats |
| H+40+33 | 40 | 33 | 13.3 | salt_pan | endorheic-salt-flats |
| H+28+26 | 28 | 26 | 13.2 | salt_pan | endorheic-salt-flats |

## City-candidate sites (all 149)

Grouped by region. `shallow_well`/`spring_line` = drinkable groundwater. `wt_depth_m` from data. Multi-tag resources use `;` (not `|`) so markdown tables stay aligned — matches master hexes / Maptest.

### West Spine Windward Flank (`west-spine-windward-flank`) — 2 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+24+48 | 24 | 48 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+24+53 | 24 | 53 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |

### Northwest Spine Windward Flank (`northwest-spine-windward-flank`) — 0 city-candidates

*None in this region.*

### East Spine Leeward Slopes (`east-spine-leeward-slopes`) — 0 city-candidates

*None in this region.*

### Western Farm Belt (`western-farm-belt`) — 28 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+13+37 | 13 | 37 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+14+36 | 14 | 36 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+15+35 | 15 | 35 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+16+34 | 16 | 34 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+19+19 | 19 | 19 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+20 | 19 | 20 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+21 | 19 | 21 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+22 | 19 | 22 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+23 | 19 | 23 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+24 | 19 | 24 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+25 | 19 | 25 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+26 | 19 | 26 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+19+27 | 19 | 27 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+19+28 | 19 | 28 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+20+18 | 20 | 18 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+21+18 | 21 | 18 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+22+18 | 22 | 18 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+19 | 23 | 19 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+20 | 23 | 20 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+21 | 23 | 21 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+23 | 23 | 23 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+24 | 23 | 24 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+25 | 23 | 25 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+26 | 23 | 26 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+27 | 23 | 27 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+28 | 23 | 28 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+29 | 23 | 29 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+30 | 23 | 30 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |

### Northwest Farm Belt (`northwest-farm-belt`) — 0 city-candidates

*None in this region.*

### Eastern Riverine Farm Corridors (`eastern-riverine-farm-corridors`) — 36 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+43+46 | 43 | 46 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+43+47 | 43 | 47 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+43+48 | 43 | 48 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+43+49 | 43 | 49 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+44+45 | 44 | 45 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+45+45 | 45 | 45 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+46+45 | 46 | 45 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+47+37 | 47 | 37 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+47+42 | 47 | 42 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+47+46 | 47 | 46 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+48+37 | 48 | 37 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+48+42 | 48 | 42 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+48+45 | 48 | 45 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+49+37 | 49 | 37 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+49+39 | 49 | 39 | farmland | river | 1.5 | rich |  |  | fisheries;greenstone_metals | fresh water, strong food, route access |
| H+49+42 | 49 | 42 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+50+40 | 50 | 40 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+50+42 | 50 | 42 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+51+37 | 51 | 37 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+51+39 | 51 | 39 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+51+41 | 51 | 41 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+52+37 | 52 | 37 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+52+38 | 52 | 38 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+52+39 | 52 | 39 | farmland | river | 1.5 | rich |  |  | greenstone_metals | fresh water, strong food, route access |
| H+52+40 | 52 | 40 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+53+36 | 53 | 36 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+53+37 | 53 | 37 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+53+38 | 53 | 38 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+53+39 | 53 | 39 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+54+36 | 54 | 36 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+54+37 | 54 | 37 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+54+38 | 54 | 38 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+55+36 | 55 | 36 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+55+37 | 55 | 37 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+56+36 | 56 | 36 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+57+35 | 57 | 35 | farmland | spring_line | 2.5 | rich |  |  | none | spring line, strong food, route access |

### Inner Eastern Farm Corridors (`inner-eastern-farm-corridors`) — 0 city-candidates

*None in this region.*

### Western Coastal Margin (`western-coastal-margin`) — 16 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+16+55 | 16 | 55 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+17+54 | 17 | 54 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+49 | 19 | 49 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+19+52 | 19 | 52 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+19+55 | 19 | 55 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+20+51 | 20 | 51 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+20+54 | 20 | 54 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+20+57 | 20 | 57 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+21+50 | 21 | 50 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+21+53 | 21 | 53 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+22+49 | 22 | 49 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+22+52 | 22 | 52 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+22+57 | 22 | 57 | farmland | shallow_well | 2.5 | rich |  |  | clay | shallow well, strong food, route access |
| H+23+47 | 23 | 47 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+48 | 23 | 48 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+23+54 | 23 | 54 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |

### Eastern Coastal Margin (`eastern-coastal-margin`) — 0 city-candidates

*None in this region.*

### Southern Coastal Margin (`southern-coastal-margin`) — 30 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+49+54 | 49 | 54 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+50+54 | 50 | 54 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+50+57 | 50 | 57 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+50+59 | 50 | 59 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+51+54 | 51 | 54 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+51+55 | 51 | 55 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+51+56 | 51 | 56 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+51+57 | 51 | 57 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+51+58 | 51 | 58 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+51+59 | 51 | 59 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+52+52 | 52 | 52 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+52+54 | 52 | 54 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+52+55 | 52 | 55 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+52+58 | 52 | 58 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+52+59 | 52 | 59 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+53+53 | 53 | 53 | farmland | major_river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access, major river |
| H+53+54 | 53 | 54 | farmland | major_river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access, major river |
| H+53+55 | 53 | 55 | farmland | major_river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access, major river |
| H+53+57 | 53 | 57 | farmland | major_river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access, major river |
| H+53+58 | 53 | 58 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+53+59 | 53 | 59 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+54+54 | 54 | 54 | farmland | river | 1.5 | rich |  |  | fisheries;clay | fresh water, strong food, route access |
| H+54+58 | 54 | 58 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+54+59 | 54 | 59 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+55+56 | 55 | 56 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+57+55 | 57 | 55 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+57+56 | 57 | 56 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+58+56 | 58 | 56 | farmland | river | 1.5 | rich |  |  | clay | fresh water, strong food, route access |
| H+58+57 | 58 | 57 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+59+56 | 59 | 56 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |

### Endorheic Salt Flats (A19 Sill) (`endorheic-salt-flats`) — 0 city-candidates

*None in this region.*

### Endorheic Inland Sea (A19 Floor) (`endorheic-inland-sea`) — 0 city-candidates

*None in this region.*

### Southeast Volcanic Arc (`southeast-volcanic-arc`) — 7 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+51+50 | 51 | 50 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+51+51 | 51 | 51 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+55+39 | 55 | 39 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+56+39 | 56 | 39 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+65+39 | 65 | 39 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+65+40 | 65 | 40 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+77+42 | 77 | 42 | farmland | shallow_well | 2.5 | rich | yes |  | obsidian | shallow well, strong food, route access |

### Southeast Craton Plains (`southeast-craton-plains`) — 4 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+47+52 | 47 | 52 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+47+53 | 47 | 53 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |
| H+48+53 | 48 | 53 | farmland | river | 1.5 | rich |  |  | greenstone_metals | fresh water, strong food, route access |
| H+49+53 | 49 | 53 | farmland | river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access |

### Northern Rift Corridor (`northern-rift-corridor`) — 0 city-candidates

*None in this region.*

### Far-North Rift Corridor (`far-north-rift-corridor`) — 0 city-candidates

*None in this region.*

### Southwest Hotspot Uplands (`southwest-hotspot-uplands`) — 2 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+24+44 | 24 | 44 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |
| H+24+45 | 24 | 45 | farmland | major_river | 1.5 | rich |  |  | fisheries | fresh water, strong food, route access, major river |

### Western Craton Shield (`western-craton-shield`) — 8 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+12+23 | 12 | 23 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+12+24 | 12 | 24 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+13+25 | 13 | 25 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+13+26 | 13 | 26 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+13+27 | 13 | 27 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+13+28 | 13 | 28 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |
| H+14+22 | 14 | 22 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+15+22 | 15 | 22 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |

### eastern-eastern-riverine-farm-corridors (`eastern-eastern-riverine-farm-corridors`) — 15 city-candidates

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+45+16 | 45 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+46+16 | 46 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+50+16 | 50 | 16 | farmland | shallow_well | 2.5 | rich |  |  | greenstone_metals | shallow well, strong food, route access |
| H+51+16 | 51 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+52+16 | 52 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+53+16 | 53 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+54+18 | 54 | 18 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+55+16 | 55 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+55+18 | 55 | 18 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+56+18 | 56 | 18 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+57+16 | 57 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+57+18 | 57 | 18 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+58+16 | 58 | 16 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+58+17 | 58 | 17 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |
| H+58+18 | 58 | 18 | farmland | shallow_well | 2.5 | rich |  |  | none | shallow well, strong food, route access |

### western-western-farm-belt (`western-western-farm-belt`) — 1 city-candidate

| id | q | r | terrain | water | wt_depth_m | food | rain_shadow | dry_interior | resources | why |
|---|---:|---:|---|---|---:|---|---|---|---|---|
| H+09+36 | 9 | 36 | farmland | river | 1.5 | rich |  |  | none | fresh water, strong food, route access |

## Empty-but-excellent sites

| id | q | r | region | terrain | water | wt_depth_m | food | why |
|---|---:|---:|---|---|---|---:|---|---|
| H+47+16 | 47 | 16 | inner-eastern-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+54+16 | 54 | 16 | inner-eastern-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+56+16 | 56 | 16 | inner-eastern-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+23+18 | 23 | 18 | western-farm-belt | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+43+18 | 43 | 18 | inner-eastern-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+44+18 | 44 | 18 | inner-eastern-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+44+21 | 44 | 21 | inner-eastern-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+23+22 | 23 | 22 | western-farm-belt | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+13+24 | 13 | 24 | western-craton-shield | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+08+27 | 8 | 27 | northwest-farm-belt | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+19+29 | 19 | 29 | western-farm-belt | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+19+30 | 19 | 30 | western-farm-belt | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+59+32 | 59 | 32 | eastern-riverine-farm-corridors | farmland | shallow_well | 2.5 | rich | excellent site left empty on purpose |
| H+10+35 | 10 | 35 | northwest-farm-belt | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+52+36 | 52 | 36 | eastern-riverine-farm-corridors | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+50+37 | 50 | 37 | eastern-riverine-farm-corridors | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+56+38 | 56 | 38 | southeast-volcanic-arc | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+65+38 | 65 | 38 | southeast-volcanic-arc | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+50+39 | 50 | 39 | eastern-riverine-farm-corridors | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+48+40 | 48 | 40 | eastern-riverine-farm-corridors | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+49+40 | 49 | 40 | eastern-riverine-farm-corridors | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+51+40 | 51 | 40 | eastern-riverine-farm-corridors | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+47+45 | 47 | 45 | eastern-riverine-farm-corridors | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+24+46 | 24 | 46 | west-spine-windward-flank | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+24+50 | 24 | 50 | west-spine-windward-flank | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+23+51 | 23 | 51 | western-coastal-margin | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+53+52 | 53 | 52 | southern-coastal-margin | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+18+53 | 18 | 53 | western-coastal-margin | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+22+55 | 22 | 55 | western-coastal-margin | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+54+55 | 54 | 55 | southern-coastal-margin | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+56+55 | 56 | 55 | southern-coastal-margin | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+21+56 | 21 | 56 | western-coastal-margin | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+52+56 | 52 | 56 | southern-coastal-margin | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+53+56 | 53 | 56 | southern-coastal-margin | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |
| H+61+56 | 61 | 56 | southeast-volcanic-arc | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+52+57 | 52 | 57 | southern-coastal-margin | farmland | river | 1.5 | rich | excellent site left empty on purpose |
| H+54+57 | 54 | 57 | southern-coastal-margin | farmland | major_river | 1.5 | rich | excellent site left empty on purpose |

## Town-tier counts by region

### West Spine Windward Flank — 8 town-tier hexes in region

### Northwest Spine Windward Flank — 1 town-tier hexes in region

### East Spine Leeward Slopes — 0 town-tier hexes in region

### Western Farm Belt — 2 town-tier hexes in region

### Northwest Farm Belt — 0 town-tier hexes in region

### Eastern Riverine Farm Corridors — 20 town-tier hexes in region

### Inner Eastern Farm Corridors — 23 town-tier hexes in region

### Western Coastal Margin — 73 town-tier hexes in region

### Eastern Coastal Margin — 3 town-tier hexes in region

### Southern Coastal Margin — 9 town-tier hexes in region

### Endorheic Salt Flats (A19 Sill) — 0 town-tier hexes in region

### Endorheic Inland Sea (A19 Floor) — 0 town-tier hexes in region

### Southeast Volcanic Arc — 52 town-tier hexes in region

### Southeast Craton Plains — 0 town-tier hexes in region

### Northern Rift Corridor — 50 town-tier hexes in region

### Far-North Rift Corridor — 30 town-tier hexes in region

### Southwest Hotspot Uplands — 3 town-tier hexes in region

### Western Craton Shield — 6 town-tier hexes in region
