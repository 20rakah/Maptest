"""World Seed 01 configuration and locked physical constants.

ASSUMPTION labels mark guessed parameters Climate/Geologist may later replace.
"""

from __future__ import annotations

# --- Grid (locked physical scale) ---
# Continent ~2400×1800 km at ~30 km/hex → 80×60 hexes.
HEX_KM = 30
COLS = 80  # q axis extent (west→east), ~2400 km
ROWS = 60  # r axis extent (north→south), ~1800 km
HEX_COUNT = COLS * ROWS  # 4800

# Axial hex ID format: H{q:+03d}{r:+03d}  e.g. H+00+00, H+42-07
ID_FMT = "H{q:+03d}{r:+03d}"

DEFAULT_SEED = 1001  # World Seed 01 default

# CLI knobs (defaults)
DEFAULT_SEA_LEVEL_M = 0.0  # ASSUMPTION: datum = mean sea level meters
DEFAULT_ICE_MULT = 1.0  # residual ice intensity multiplier
DEFAULT_RAINFALL_MULT = 1.0  # precip multiplier

# --- Geology layout (locked history encoded as spatial constraints) ---
# Coordinates in fractional grid space (q/COLS, r/ROWS), 0..1

# Dual-craton suture: mountain spine roughly N–S slightly west of center
SUTURE_Q_FRAC = 0.42  # ASSUMPTION: spine longitude
SUTURE_WIDTH_FRAC = 0.12  # ASSUMPTION: belt half-width in q-fraction

# SE volcanic/island arc
ARC_CENTER = (0.82, 0.78)  # ASSUMPTION
ARC_RADIUS_FRAC = 0.18

# Northern rift
RIFT_R_FRAC = 0.18  # ASSUMPTION: latitude of rift valley
RIFT_WIDTH_FRAC = 0.08

# SW hotspot
HOTSPOT = (0.22, 0.72)  # ASSUMPTION
HOTSPOT_RADIUS_FRAC = 0.10

# Endorheic central-east basin
BASIN_CENTER = (0.62, 0.48)  # ASSUMPTION
BASIN_RADIUS_Q = 0.16
BASIN_RADIUS_R = 0.14

# LGM / residual ice
# ASSUMPTION: ice age ended 1000 yr BP; residual ice on spine + north highlands
ICE_AGE_ENDED_YR_BP = 1000
LGM_NORTH_EDGE_FRAC = 0.35  # ASSUMPTION: LGM ice covered north of this r-frac + spine

# Climate
# ASSUMPTION: continent centered ~35–55°N equivalent; westerlies from west
BASE_LAT_NORTH_DEG = 55.0  # ASSUMPTION: northern edge latitude
BASE_LAT_SOUTH_DEG = 28.0  # ASSUMPTION: southern edge latitude
SEA_LEVEL_TEMP_C = 14.0  # ASSUMPTION: mean annual at sea level mid-continent
LAPSE_RATE_C_PER_M = 0.0065  # ASSUMPTION: Earth-like environmental lapse
BASE_PRECIP_MM = 850.0  # ASSUMPTION: baseline annual precip before orography
OROGRAPHIC_GAIN = 1.8  # ASSUMPTION: windward precip multiplier peak
RAIN_SHADOW_LOSS = 0.35  # ASSUMPTION: leeward precip fraction

# Settlement
EMPTY_CITY_CANDIDATE_FRAC = 0.20  # ASSUMPTION: leave ~20% of city-quality sites empty
# Tier score buckets (raw float score → settle_score string)
TIER_THRESHOLDS = {
    "city-candidate": 7.5,
    "town": 5.5,
    "village": 3.5,
    "farmstead": 1.5,
}
# below farmstead → "none"

SETTLEMENT_TIERS = ("none", "farmstead", "village", "town", "city-candidate")
