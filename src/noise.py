"""Deterministic 2D value / fractal noise for World Seed 01."""

from __future__ import annotations

import numpy as np


def _hash2(ix: np.ndarray, iy: np.ndarray, seed: int) -> np.ndarray:
    """Integer hash → float in [0, 1)."""
    n = (ix.astype(np.int64) * 374761393 + iy.astype(np.int64) * 668265263 + seed * 982451653) & 0x7FFFFFFF
    n = (n ^ (n >> 13)) * 1274126177
    n = n & 0x7FFFFFFF
    return (n.astype(np.float64) / 0x7FFFFFFF)


def value_noise(w: int, h: int, scale: float, seed: int) -> np.ndarray:
    """Smooth value noise on a w×h grid; scale = wavelength in cells."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    fx = xx / max(scale, 1e-6)
    fy = yy / max(scale, 1e-6)
    x0 = np.floor(fx).astype(np.int64)
    y0 = np.floor(fy).astype(np.int64)
    x1 = x0 + 1
    y1 = y0 + 1
    sx = fx - x0
    sy = fy - y0
    # smoothstep
    ux = sx * sx * (3.0 - 2.0 * sx)
    uy = sy * sy * (3.0 - 2.0 * sy)
    n00 = _hash2(x0, y0, seed)
    n10 = _hash2(x1, y0, seed)
    n01 = _hash2(x0, y1, seed)
    n11 = _hash2(x1, y1, seed)
    nx0 = n00 * (1 - ux) + n10 * ux
    nx1 = n01 * (1 - ux) + n11 * ux
    return nx0 * (1 - uy) + nx1 * uy


def fbm(w: int, h: int, seed: int, octaves: int = 5, base_scale: float = 24.0) -> np.ndarray:
    """Fractal Brownian motion in roughly [-1, 1]."""
    total = np.zeros((h, w), dtype=np.float64)
    amp = 1.0
    norm = 0.0
    scale = base_scale
    for i in range(octaves):
        total += amp * (value_noise(w, h, scale, seed + i * 97) * 2.0 - 1.0)
        norm += amp
        amp *= 0.5
        scale *= 0.5
    return total / max(norm, 1e-9)


def rng(seed: int) -> np.random.Generator:
    return np.random.default_rng(seed)
