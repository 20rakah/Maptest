# Scribe notes — Climate / water / food (World Seed 01)

Natural regions only (no country names). Stats from Climate V1 layers over Geologist `DRAIN_V3_ENDO_939`. Peoples mentioned only as adaptation cues.

**Continent climate snapshot (land):** precip ~320–2830 mm/yr (median ~640); temp ~−0.1–20.7 °C (median ~13.1). Westerlies; rain-shadow / interior dryness strong on the closed basin (~939 hexes). Post-LGM ~1000 yr BP: highland ice gone; glacial scars still slightly cooler/wetter. Residual ice map hexes = 0 this run.

---

## 1. Western windward coasts & plains
Moister mid-latitude west (precip often ~700–900+). Grassland/pasture and floodplain farmable corridors along rivers; pockets of temperate forest inland of the shore. Water table commonly `shallow_well` / `spring_line`. **Food:** good pasture + river floodplain farming. **Adaptations:** fishing villages on the open west, herders on grass, farms on floodplains.

## 2. NW highlands / cold forest belt
Cooler (often ~6–9 °C), timber-rich temperate + boreal forest. Springs common on relief. **Food:** modest forest forage + timber culture; poorer grain than south. **Adaptations:** woodcraft, upland herding, meltwater streams from scarred valleys.

## 3. Northern rift / far-north uplands
Short cool season, coastal scrub and boreal patches, strong seasonality. Glacial scars mark former ice. **Food:** lean; fisheries where coasts open. **Adaptations:** seasonal mobility, reliance on fish and cold-hardy pasture.

## 4. Suture spine (collision wall, ~q 0.42)
Orographic precip peaks on western flanks; leeward east dries. Mixed grassland and temperate forest; some timber. Steeper slopes → thinner soils, spring lines on mountain fronts. **Food:** pasture + timber; farms in river notches. **Adaptations:** highland herders; pass communities controlling windward/leeward trade.

## 5. Suture north (cold forest wall)
Boreal/temperate timber belt, cooler temps (~6 °C). High `timber` tags. **Food:** forest-modest. **Adaptations:** logging/hunting cultures tied to scarred valleys.

## 6. Eastern lee plains
Rain-shadow leaning, coastal scrub / steppe-to-scrub mosaics, fewer major rivers. Water table mixed dry/shallow_well. **Food:** poorer than west; pasture pockets. **Adaptations:** sparse herding, wells, avoidance of basin brine.

## 7. Central exorheic lowlands (between spine and basin rim)
River-fed floodplain farmable strips and coastal-scrub margins; springs along channels. **Food:** good along rivers. **Adaptations:** river farming belts feeding traffic around—but not into—the closed basin.

## 8. Endorheic salt flats (flat sill ~589 m, ~765 hexes)
Large arid playa: `salt_pan` water class, `salt flat sparse` veg, `wt_class=dry`, `salt_pans` resource belt. Precip often ~320–500 mm. **Not** a small playa—full A19 catchment sill. **Food:** very poor (brine). **Adaptations:** salt harvesting caravans; no dense farming; routes skim the rim.

## 9. Endorheic inland sea (deep floor ~60–120 m, ~174 hexes)
Permanent closed water with marsh-class water table and `fisheries`. Fringing wetlands where sill meets water. Rivers from the catchment terminate here—**never** the ocean. **Food:** inland fish/brine-edge forage. **Adaptations:** lakeshore fishers; contrast with surrounding salt crust.

## 10. SE volcanic arc lands
Warmer (~15 °C), extensive grassland/pasture, some floodplain farms in valleys. Rock-hosted volcanic resources merge with climate pasture belts. **Food:** strong pasture. **Adaptations:** herders on volcanic soils; ash-plain grazing.

## 11. SW hotspot / warm coast
Warmest land (~17 °C), coastal scrub + temperate forest, major rivers to ocean, spring lines near coast. Timber + pasture + coastal fisheries. **Food:** good mixed. **Adaptations:** coastal fishers and forest farms.

## 12. Southern lowlands
Warm (~18 °C), grassland and floodplain farmable with more rivers toward southern seas. **Food:** rich relative to interior. **Adaptations:** dense farming belts facing open ocean trade.

## 13. Open oceans (N/E/S/W shelves)
`fisheries` dominant; no land soils. Northern seas colder. **Adaptations:** maritime peoples on facing coasts only (Climate does not place settlements).

---

## Cross-cutting water / food rules of thumb
- **Drinkable wells:** `shallow_well` / `spring_line` common outside basin; basin sill is `dry` (saline).
- **Marsh:** mainly inland-sea floor/fringe — not a continent-wide swamp.
- **Timber belt:** NW highlands + suture north + SW forest patches.
- **Pasture belt:** SE arc, southern/western grass, suture flanks.
- **Salt vs fish:** salt_pans = interior sill; fisheries = oceans + inland sea + major rivers.

Ownership: Climate layers only. Nations/borders out of scope. Settlement scores in `hexes.csv` / map 09 are Cartographer packaging.
