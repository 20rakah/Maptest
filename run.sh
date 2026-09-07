#!/usr/bin/env bash
# Regenerate World Seed 01 from seed (same seed → same outputs).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

# Defaults match World Seed 01; pass-through extra CLI args
SEED="${SEED:-1001}"
SEA="${SEA_LEVEL:-0}"
ICE="${ICE:-1.0}"
RAIN="${RAINFALL:-1.0}"

python -m src.generate --seed "$SEED" --sea-level "$SEA" --ice "$ICE" --rainfall "$RAIN" "$@"
python -m src.validate "$ROOT/data"
echo "Done. Maps in maps/; hex table in data/hexes.csv + data/hexes.json"
