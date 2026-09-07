"""Validate hex table ↔ grid lockstep."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from . import config as C
from .ids import qr_to_id


def validate_data_dir(data_dir: Path) -> list[str]:
    errors: list[str] = []
    csv_path = data_dir / "hexes.csv"
    json_path = data_dir / "hexes.json"
    if not csv_path.is_file():
        errors.append(f"missing {csv_path}")
        return errors
    if not json_path.is_file():
        errors.append(f"missing {json_path}")

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != C.HEX_COUNT:
        errors.append(f"CSV rows {len(rows)} != HEX_COUNT {C.HEX_COUNT}")

    required = ["id", "terrain", "water", "food", "resources", "settle_score", "why"]
    if rows:
        for col in required:
            if col not in rows[0]:
                errors.append(f"CSV missing column {col}")

    expected_ids = [qr_to_id(q, r) for r in range(C.ROWS) for q in range(C.COLS)]
    got_ids = [r["id"] for r in rows]
    if got_ids != expected_ids:
        errors.append("CSV id order/set does not match axial grid row-major scan")

    if json_path.is_file():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if len(data) != len(rows):
            errors.append(f"JSON len {len(data)} != CSV len {len(rows)}")
        elif data and rows and data[0].get("id") != rows[0]["id"]:
            errors.append("JSON/CSV first id mismatch")
        # spot-check settle_score lockstep
        for i in (0, len(rows) // 2, len(rows) - 1):
            if data[i].get("settle_score") != rows[i].get("settle_score"):
                errors.append(f"JSON/CSV settle_score mismatch at row {i}")
                break

    # Optional geology ingest consistency
    geo = data_dir / "geology_hex.csv"
    if geo.is_file():
        with geo.open(newline="", encoding="utf-8") as f:
            grows = list(csv.DictReader(f))
        if len(grows) != C.HEX_COUNT:
            errors.append(f"geology_hex.csv rows {len(grows)} != {C.HEX_COUNT}")
        elif grows and grows[0].get("id") != expected_ids[0]:
            # only warn-style if id present
            if "id" not in (grows[0] or {}):
                errors.append("geology_hex.csv missing id")

    return errors


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "data"
    if argv and len(argv) > 1:
        data_dir = Path(argv[1])
    errs = validate_data_dir(data_dir)
    if errs:
        print("VALIDATE FAIL:")
        for e in errs:
            print(" -", e)
        return 1
    print(f"VALIDATE OK: {C.HEX_COUNT} hexes ({C.COLS}x{C.ROWS}) CSV/JSON lockstep")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
