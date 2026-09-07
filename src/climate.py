"""Layer 3: climate_weather — temperature, precip, wind, rain shadows, seasons.

ASSUMPTION: westerlies; temp falls with latitude and elevation (lapse rate).
Post-LGM (~1000 yr BP): residual ice melt cools meltwater corridors slightly
and elevates basin/inland humidity near iced highlands (toy).
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
    *,
    endorheic: np.ndarray | None = None,
    glacial_mask: np.ndarray | None = None,
    ice: np.ndarray | None = None,
) -> dict[str, np.ndarray]:
    h, w = elev_m.shape
    # Latitude from north edge
    lat = C.BASE_LAT_NORTH_DEG + (C.BASE_LAT_SOUTH_DEG - C.BASE_LAT_NORTH_DEG) * rf

    # Sea-level equivalent temp decreases poleward
    # ASSUMPTION A7/C1: ~0.55°C per degree latitude from warm south
    temp_sl = C.SEA_LEVEL_TEMP_C + 0.55 * (C.BASE_LAT_SOUTH_DEG + C.BASE_LAT_NORTH_DEG) / 2.0 - 0.55 * lat
    temp_sl += 1.5 * fbm(w, h, seed + 201, octaves=3, base_scale=22.0)

    land = elev_m >= 0
    elev_for_lapse = np.where(land, np.maximum(elev_m, 0.0), 0.0)
    temp_c = temp_sl - C.LAPSE_RATE_C_PER_M * elev_for_lapse

    # Post-LGM residual ice / melt corridors: slight cooling near ice and glacial scars
    # ASSUMPTION C2: ~1000 yr BP deglaciation; meltwater chill ~0.5–1.5°C locally
    if ice is not None:
        temp_c = np.where(ice, np.minimum(temp_c, -2.0), temp_c)
    if glacial_mask is not None and glacial_mask.any():
        melt_cool = glacial_mask.astype(np.float64) * (0.6 + 0.4 * (1.0 - rf))
        temp_c = temp_c - melt_cool

    # Base precip + noise
    precip = C.BASE_PRECIP_MM * (
        0.85 + 0.35 * fbm(w, h, seed + 211, octaves=4, base_scale=18.0)
    )
    # Slightly wetter south / west coasts (ASSUMPTION C3)
    precip *= 0.9 + 0.25 * rf * 0.35 + 0.25 * (1.0 - qf) * 0.45

    # Orographic: westerlies → windward = west face of high terrain
    elev_pad = np.pad(elev_m, ((0, 0), (1, 0)), mode="edge")[:, :-1]
    de_east = elev_m - elev_pad  # positive = rising to the east = windward for westerlies
    windward = np.clip(de_east / 400.0, 0.0, 1.5)
    leeward = np.clip(-de_east / 400.0, 0.0, 1.5)
    high = np.clip((elev_m - 400.0) / 1200.0, 0, 1) * land.astype(np.float64)

    precip = precip * (1.0 + C.OROGRAPHIC_GAIN * windward * high)
    # Rain shadow east of rises
    precip = precip * (1.0 - (1.0 - C.RAIN_SHADOW_LOSS) * leeward * high)

    # Continental interior / large endorheic catchment drier (ASSUMPTION C4)
    # Trust Geologist endorheic mask (~939-hex A19 catchment), not config ellipse.
    if endorheic is not None and endorheic.any():
        precip = np.where(endorheic & land, precip * 0.55, precip)
        # Deep basin floor slightly wetter from closed drainage / melt inflow
        deep = endorheic & land & (elev_m < 200.0)
        precip = np.where(deep, precip * 1.15, precip)

    # Rain-shadow boolean: strong leeward on high terrain OR dry endorheic flat
    rain_shadow = (leeward > 0.35) & (high > 0.25) & land
    if endorheic is not None:
        rain_shadow = rain_shadow | (endorheic & land & (precip < 550))

    # Wind field: prevailing westerlies with local deflection (ASSUMPTION C5)
    # Encode as windward strength 0–1 and discrete wind class string via export.
    wind_strength = np.clip(0.35 + 0.45 * (1.0 - qf) + 0.25 * windward - 0.2 * leeward, 0.05, 1.0)
    wind_strength = np.where(land, wind_strength, wind_strength * 1.15)
    # Classes: windward | open_westerly | leeward | calm_interior
    wind_class = np.full((h, w), "open_westerly", dtype=object)
    wind_class[windward > 0.4] = "windward"
    wind_class[leeward > 0.4] = "leeward"
    if endorheic is not None:
        wind_class[endorheic & land & (windward < 0.25) & (leeward < 0.25)] = "calm_interior"
    wind_class[~land] = "ocean_westerly"

    # Seasonality index 0–1 (higher = more seasonal precip contrast) ASSUMPTION C6
    # Continental + north + rain-shadow → higher seasonality; maritime west coast lower.
    seasonality = (
        0.25
        + 0.35 * np.clip(np.abs(qf - 0.35), 0, 0.5) / 0.5  # away from wet west
        + 0.25 * (1.0 - rf)  # north more seasonal
        + 0.2 * rain_shadow.astype(np.float64)
    )
    seasonality = np.clip(seasonality + 0.08 * fbm(w, h, seed + 221, octaves=2, base_scale=30.0), 0.1, 0.95)
    seasonality = np.where(land, seasonality, 0.2)

    # Simple season labels for Scribe/Cartographer
    season_label = np.full((h, w), "moderate", dtype=object)
    season_label[seasonality >= 0.65] = "strong"
    season_label[seasonality < 0.35] = "weak"
    season_label[~land] = "maritime"

    # Ice-melt humidity bump along glacial corridors (ASSUMPTION C2 continued)
    if glacial_mask is not None and glacial_mask.any():
        precip = precip * (1.0 + 0.08 * glacial_mask.astype(np.float64) * (1.0 - rf))

    precip = np.where(land, precip, precip * 1.1)
    precip = np.clip(precip * rainfall_mult, 50.0, 4500.0)

    return {
        "temp_c": temp_c,
        "precip_mm": precip,
        "lat_deg": lat,
        "windward": windward,
        "leeward": leeward,
        "rain_shadow": rain_shadow,
        "wind_strength": wind_strength,
        "wind_class": wind_class,
        "seasonality": seasonality,
        "season_label": season_label,
    }
