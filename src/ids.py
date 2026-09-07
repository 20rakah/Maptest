"""Stable axial hex IDs used everywhere (maps, CSV, JSON)."""

from __future__ import annotations

from .config import COLS, ID_FMT, ROWS


def qr_to_id(q: int, r: int) -> str:
    return ID_FMT.format(q=q, r=r)


def id_to_qr(hid: str) -> tuple[int, int]:
    # H+qqq+rrr or H+qqq-rrr etc.
    assert hid.startswith("H") and len(hid) == 7
    q = int(hid[1:4])
    r = int(hid[4:7])
    return q, r


def all_hex_ids() -> list[tuple[str, int, int]]:
    """Row-major: r from 0..ROWS-1, q from 0..COLS-1."""
    out = []
    for r in range(ROWS):
        for q in range(COLS):
            out.append((qr_to_id(q, r), q, r))
    return out
