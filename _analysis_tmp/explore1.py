import csv
from collections import Counter, defaultdict
import statistics

rows = []
with open("/workspace/world-seed-01/data/hexes.csv") as f:
    for r in csv.DictReader(f):
        r["q"] = int(r["q"]); r["r"] = int(r["r"])
        r["elev_m"] = float(r["elev_m"]); r["slope"] = float(r["slope"])
        r["precip"] = float(r["precip"]); r["temp_c"] = float(r["temp_c"])
        rows.append(r)
print("n", len(rows))
land = [x for x in rows if x["terrain"] != "ocean"]
ocean = [x for x in rows if x["terrain"] == "ocean"]
print("land", len(land), "ocean", len(ocean))
for c in ["terrain","water","food","resources","settle_score","soil","vegetation","rock"]:
    print("---", c)
    print(Counter(x[c] for x in rows).most_common())
print("--- land terrain")
print(Counter(x["terrain"] for x in land).most_common())
print("--- land water")
print(Counter(x["water"] for x in land).most_common())
print("--- land settle")
print(Counter(x["settle_score"] for x in land).most_common())
for c in ["elev_m","temp_c","precip","slope"]:
    vals = [x[c] for x in land]
    print(c, "min", min(vals), "max", max(vals), "mean", round(statistics.mean(vals),2), "med", statistics.median(vals))
