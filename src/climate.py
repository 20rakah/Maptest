"""Layer 3: climate_weather — temperature + precip with orographic / rain shadows.

ASSUMPTION: westerlies; temp falls with latitude and elevation (lapse rate).
"""

from __future__ import annotations

import numpy as np

from . import config as C
from .noise import fbm


def build_climate(
    seed: int,
    elev_m: np.ndarray,
    qf: np.ndarray,
    rf: np.ndarray,
    rainfall_mult: float,
) -> dict[str, np.ndarray]:
    h, w = elev_m.shape
    # Latitude from north edge
    lat = C.BASE_LAT_NORTH_DEG + (C.BASE_LAT_SOUTH_DEG - C.BASE_LAT_NORTH_DEG) * rf

    # Sea-level equivalent temp decreases poleward
    # ASSUMPTION: ~0.5°C per degree latitude from warm south
    temp_sl = C.SEA_LEVEL_TEMP_C + 0.55 * (C.BASE_LAT_SOUTH_DEG + C.BASE_LAT_NORTH_DEG) / 2.0 - 0.55 * lat
    temp_sl += 1.5 * fbm(w, h, seed + 201, octaves=3, base_scale=22.0)

    land = elev_m >= 0
    elev_for_lapse = np.where(land, np.maximum(elev_m, 0.0), 0.0)
    temp_c = temp_sl - C.LAPSE_RATE_C_PER_M * elev_for_lapse

    # Base precip + noise
    precip = C.BASE_PRECIP_MM * (
        0.85 + 0.35 * fbm(w, h, seed + 211, octaves=4, base_scale=18.0)
    )
    # Slightly wetter south / coasts (ASSUMPTION)
    precip *= 0.9 + 0.25 * (1.0 - rf) * 0.3 + 0.2 * (1.0 - np.abs(qf - 0.5) * 0.5)

    # Orographic: westerlies → windward = west face of high terrain
    # Approximate elev gradient eastward
    elev_pad = np.pad(elev_m, ((0, 0), (1, 0)), mode="edge")[:, :-1]
    de_east = elev_m - elev_pad  # positive = rising to the east = windward for westerlies
    windward = np.clip(de_east / 400.0, 0.0, 1.5)
    leeward = np.clip(-de_east / 400.0, 0.0, 1.5)
    # Also use absolute height for general orographic boost on western slopes of spine
    high = np.clip((elev_m - 400.0) / 1200.0, 0, 1) * land.astype(np.float64)

    precip = precip * (1.0 + C.OROGRAPHIC_GAIN * windward * high)
    # Rain shadow east of rises
    precip = precip * (1.0 - (1.0 - C.RAIN_SHADOW_LOSS) * leeward * high)

    # Endorheic interior slightly drier aloft already via shadow; ocean wetter edge
    precip = np.where(land, precip, precip * 1.1)
    precip = np.clip(precip * rainfall_mult, 50.0, 4500.0)

    return {
        "temp_c": temp_c,
        "precip_mm": precip,
        "lat_deg": lat,
        "windward": windward,
        "leeward": leeward,
    }
