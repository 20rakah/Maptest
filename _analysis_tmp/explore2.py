import csv
from collections import Counter, defaultdict
import statistics

rows=[]
with open("/workspace/world-seed-01/data/hexes.csv") as f:
    for r in csv.DictReader(f):
        r["q"]=int(r["q"]); r["r"]=int(r["r"])
        for k in ("elev_m","slope","precip","temp_c"): r[k]=float(r[k])
        rows.append(r)
by_id={x["id"]:x for x in rows}
land=[x for x in rows if x["terrain"]!="ocean"]

# Rock spatial extents
for rock in sorted(set(x["rock"] for x in land)):
    xs=[x for x in land if x["rock"]==rock]
    qs=[x["q"] for x in xs]; rs=[x["r"] for x in xs]
    print(f"{rock}: n={len(xs)} q={min(qs)}-{max(qs)} r={min(rs)}-{max(rs)} elev={min(x[\"elev_m\"] for x in xs):.0f}-{max(x[\"elev_m\"] for x in xs):.0f}")

# Inland sea / lake / ice locations
for t in ["inland_sea","lake","ice","marsh","high_mountains","mountains","alpine","steppe"]:
    xs=[x for x in land if x["terrain"]==t]
    if not xs: continue
    qs=[x["q"] for x in xs]; rs=[x["r"] for x in xs]
    print(f"terrain {t}: n={len(xs)} q={min(qs)}-{max(qs)} r={min(rs)}-{max(rs)}")

# Water inland_sea
for w in ["inland_sea","ice","major_river","wetland"]:
    xs=[x for x in land if x["water"]==w]
    if not xs: continue
    qs=[x["q"] for x in xs]; rs=[x["r"] for x in xs]
    print(f"water {w}: n={len(xs)} q={min(qs)}-{max(qs)} r={min(rs)}-{max(rs)}")

# City candidates
cities=sorted([x for x in land if x["settle_score"]=="city-candidate"], key=lambda x:-{"rich":3,"good":2,"modest":1,"none":0}[x["food"]])
print("city-candidates", len(cities))
for x in cities[:15]:
    print(x["id"], "q",x["q"],"r",x["r"], "elev",x["elev_m"], x["terrain"], x["water"], x["food"], x["resources"], x["why"][:80])

# Empty with good why?
empty=[x for x in land if x["settle_score"]=="none"]
print("empty sample whys:")
print(Counter(x["why"] for x in empty).most_common(20))

# precip by q band on land
for lo,hi in [(0,20),(20,30),(30,40),(40,50),(50,65),(65,80)]:
    xs=[x for x in land if lo<=x["q"]<hi]
    if not xs: continue
    print(f"q {lo}-{hi}: n={len(xs)} precip mean={statistics.mean(x[\"precip\"] for x in xs):.0f} temp={statistics.mean(x[\"temp_c\"] for x in xs):.1f}")

# temp by r band
for lo,hi in [(0,10),(10,20),(20,30),(30,40),(40,50),(50,60)]:
    xs=[x for x in land if lo<=x["r"]<hi]
    if not xs: continue
    print(f"r {lo}-{hi}: n={len(xs)} temp mean={statistics.mean(x[\"temp_c\"] for x in xs):.1f} precip={statistics.mean(x[\"precip\"] for x in xs):.0f}")
