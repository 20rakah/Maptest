"""Geologist geology_hex export for World Seed 01."""
from __future__ import annotations
import csv, json
from pathlib import Path
import numpy as np
from PIL import Image
from . import config as C
from .geology import ROCK_LABELS, apply_glacial_carving, build_elevation, build_plates_rock
from .geo_fix_helpers import enforce_drainage, slope_no_wrap, axial_neighbors
from .ids import qr_to_id
from .noise import fbm
ROOT = Path(__file__).resolve().parents[1]
DATA, MAPS, LEGENDS, DOCS = ROOT/"data", ROOT/"maps", ROOT/"legends", ROOT/"docs"
ROCK_TO_LITH = {0:"oceanic_basalt",1:"craton_granite_gneiss",2:"suture_metamorphic",3:"arc_andesite_volcanic",4:"rift_volcanics",5:"hotspot_basalt",6:"basin_sediment",7:"coastal_sediment"}
PLATE_TO_MOUNTAIN = {0:"none",1:"none",2:"arc",3:"rift",4:"hotspot"}
ASSUMPTIONS = [
"A1: Continent ~2400x1800 km; 30 km/hex; 80x60 grid.",
"A2: ASSUMPTION: config N-S spine simplifies approved NW-SE collision belt.",
"A3: SE oceanic subduction arc active at toy scale.",
"A4: Northern failed/slow rift.",
"A5: SW hotspot track.",
"A6: Westerlies for later orography (Climate owns numbers).",
"A7: LGM ice on spine + northern uplands.",
"A8: Highland ice gone ~800-1200 yr ago (~1000 yr BP).",
"A9: Endorheic central-east basin.",
"A10: Earth-like rock strength.",
"A11: Slope = max axial-neighbour |d elev|/HEX_KM (m/km).",
"A12: glacial_scar tags are toy LGM heuristics.",
"A13: geology_resource_tag rock-hosted only.",
"A14: Seed 1001; sea_level_m=0; ice_mult=1.0.",
"A15: Endorheic floor carved below land sill; ocean-adjacent ellipse cells excluded.",
"A16: Slope uses in-bounds neighbours only (no toroidal wrap).",
"A17: glacial=true iff glacial_scar is not none.",
"A18: Non-endorheic land raise-only ocean spanning-tree so steepest-descent reaches sea (not classical priority-flood).",
"A19: Endorheic CSV mask = closed floor + high rim + spill catchment (~939); drainage tests MUST use this column (not config basin_dist alone). Elev to 0.01 m.",
"A21: basin_sediment lithology only inside endorheic mask; outside remapped to craton_granite_gneiss.",
]

def _lgm_mask(elev, qf, rf):
    spine_d = np.abs(qf - C.SUTURE_Q_FRAC) / C.SUTURE_WIDTH_FRAC
    return (rf < C.LGM_NORTH_EDGE_FRAC) | ((spine_d < 1.2) & (elev > 800))

def _mountain_type(plate, suture_dist):
    h, w = plate.shape
    out = np.empty((h, w), dtype=object)
    for r in range(h):
        for q in range(w):
            mt = PLATE_TO_MOUNTAIN.get(int(plate[r, q]), "none")
            if mt == "none" and suture_dist[r, q] < 1.0:
                mt = "collision"
            out[r, q] = mt
    return out

def _colourise_discrete(arr, palette, scale=8):
    h, w = arr.shape
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    for k, col in palette.items():
        rgb[arr == k] = col
    img = Image.fromarray(rgb, mode="RGB")
    return img.resize((w * scale, h * scale), Image.NEAREST) if scale > 1 else img

def _colourise_float(arr, vmin, vmax, scale=8):
    t = np.clip((arr - vmin) / max(vmax - vmin, 1e-9), 0, 1)
    r = np.clip(2.5 * (t - 0.25), 0, 1)
    g = np.clip(1.5 - 2.0 * np.abs(t - 0.45), 0, 1)
    b = np.clip(1.2 - 2.2 * t, 0, 1)
    rgb = (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)
    img = Image.fromarray(rgb, mode="RGB")
    h, w = arr.shape
    return img.resize((w * scale, h * scale), Image.NEAREST) if scale > 1 else img

def _glacial_scars(elev, elev_pre, slope, qf, rf, land, seed):
    h, w = elev.shape
    lgm = _lgm_mask(elev_pre, qf, rf) & land
    carve = fbm(w, h, seed + 101, octaves=3, base_scale=12.0)
    deepened = (elev_pre - elev) > 40.0
    tags = np.empty((h, w), dtype=object)
    glacial = np.zeros((h, w), dtype=bool)
    for r in range(h):
        for q in range(w):
            if not land[r, q]:
                tags[r, q] = ""
                continue
            parts = []
            if lgm[r, q]:
                if elev[r, q] > 1400 and slope[r, q] > 25:
                    parts.append("hanging_valley")
                if deepened[r, q] and slope[r, q] > 8:
                    parts.append("u_valley")
                if deepened[r, q] and elev[r, q] < 600 and carve[r, q] < -0.2:
                    parts.append("overdeep_basin")
                if elev[r, q] > 900 and slope[r, q] < 8:
                    parts.append("scoured_craton")
                if (qf[r, q] < C.SUTURE_Q_FRAC - 0.05 or rf[r, q] < C.LGM_NORTH_EDGE_FRAC + 0.05) and 200 < elev[r, q] < 900:
                    parts.append("moraine" if carve[r, q] > 0.1 else "outwash")
                if rf[r, q] < 0.12 and elev[r, q] < 150:
                    parts.append("rebound_coast")
            if not parts:
                tags[r, q] = "none"
                glacial[r, q] = False
            else:
                uniq = list(dict.fromkeys(parts))
                tags[r, q] = ";".join(uniq)
                glacial[r, q] = True
    return tags, glacial

def _resource_tag(rock, mountain, endorheic, land, seed):
    rng = np.random.default_rng(seed + 211)
    h, w = rock.shape
    out = np.empty((h, w), dtype=object)
    out.fill("")
    for r in range(h):
        for q in range(w):
            if not land[r, q]:
                continue
            code = int(rock[r, q])
            mt = mountain[r, q]
            if code == 2 and rng.random() < 0.08:
                out[r, q] = "limestone_karst"
            elif code == 1 and rng.random() < 0.04:
                out[r, q] = "greenstone_metals"
            elif endorheic[r, q] and code == 6:
                out[r, q] = "evaporite_host"
            elif mt in ("arc", "hotspot", "rift") and rng.random() < 0.06:
                out[r, q] = "volcanic_host"
    return out

def export(seed=C.DEFAULT_SEED, sea_level_m=C.DEFAULT_SEA_LEVEL_M, ice_mult=C.DEFAULT_ICE_MULT):
    for p in (DATA, MAPS, LEGENDS, DOCS):
        p.mkdir(parents=True, exist_ok=True)
    geo = build_plates_rock(seed)
    elev_pack = build_elevation(seed, geo, sea_level_m)
    elev_pre = elev_pack["elev_m"].copy()
    elev = apply_glacial_carving(elev_pre, seed, ice_mult)
    land = elev >= 0
    ocean = ~land
    elev, endorheic = enforce_drainage(elev, land, ocean, geo["basin_dist"])
    land = elev >= 0
    ocean = ~land
    endorheic = endorheic & land
    for r in range(C.ROWS):
        for q in range(C.COLS):
            if endorheic[r, q] and any(ocean[rr, qq] for qq, rr in axial_neighbors(q, r, C.COLS, C.ROWS)):
                endorheic[r, q] = False
    slope = slope_no_wrap(elev)
    rock = geo["rock"].copy()
    rock[ocean] = 0
    rock[endorheic] = 6
    # Trim basin_sediment outside endorheic (Referee TABLE)
    rock[(~endorheic) & (rock == 6)] = 1  # ASSUMPTION: stray basin fill -> craton family
    mountain = _mountain_type(geo["plate"], geo["suture_dist"]).copy()
    mountain[ocean] = "none"
    mountain[endorheic] = "none"
    scars, glacial = _glacial_scars(elev, elev_pre, slope, geo["qf"], geo["rf"], land, seed)
    resources = _resource_tag(rock, mountain, endorheic, land, seed)
    fields = ["id","q","r","elevation_m","slope","lithology","mountain_type","glacial_scar","glacial","endorheic","geology_resource_tag","plate","land"]
    rows = []
    for r in range(C.ROWS):
        for q in range(C.COLS):
            rows.append({
                "id": qr_to_id(q, r), "q": q, "r": r,
                "elevation_m": round(float(elev[r, q]), 2),
                "slope": round(float(slope[r, q]), 3),
                "lithology": ROCK_TO_LITH.get(int(rock[r, q]), "craton_granite_gneiss"),
                "mountain_type": mountain[r, q],
                "glacial_scar": scars[r, q],
                "glacial": "true" if glacial[r, q] else "false",
                "endorheic": "true" if endorheic[r, q] else "false",
                "geology_resource_tag": resources[r, q],
                "plate": int(geo["plate"][r, q]),
                "land": 1 if land[r, q] else 0,
            })
    with (DATA/"geology_hex.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    meta = {"seed":seed,"cols":C.COLS,"rows":C.ROWS,"hex_km":C.HEX_KM,"sea_level_m":sea_level_m,"ice_mult":ice_mult,"generator":"src/seed_geology_export.py","owner":"Geologist","land_hexes":int(land.sum()),"ocean_hexes":int(ocean.sum()),"endorheic_hexes":int(endorheic.sum()),"elev_land_min":float(elev[land].min()) if land.any() else None,"elev_land_max":float(elev[land].max()) if land.any() else None}
    with (DATA/"geology_hex.json").open("w", encoding="utf-8") as f:
        json.dump({"meta":meta,"assumptions":ASSUMPTIONS,"hexes":rows}, f, indent=2)
    plate_pal = {0:(180,160,120),1:(200,180,140),2:(200,80,60),3:(80,120,200),4:(160,80,160),-1:(20,40,90)}
    _colourise_discrete(np.where(ocean,-1,geo["plate"]), plate_pal).save(MAPS/"01_plates_rock.png")
    elev_vis = elev.copy(); elev_vis[ocean] = -200
    vmax = float(np.percentile(elev[land], 98)) if land.any() else 2000.0
    _colourise_float(elev_vis, -200, vmax).save(MAPS/"02_elevation.png")
    smax = float(np.percentile(slope[land], 95)) if land.any() else 50.0
    _colourise_float(np.where(ocean, 0, slope), 0, smax).save(MAPS/"02_slope.png")
    rock_pal = {0:(20,40,90),1:(190,170,130),2:(120,90,70),3:(200,90,70),4:(90,110,180),5:(150,70,150),6:(210,200,140),7:(230,220,180)}
    _colourise_discrete(rock, rock_pal).save(MAPS/"lithology.png")
    mt_codes = {"none":0,"collision":1,"rift":2,"arc":3,"hotspot":4}
    mt_arr = np.array([[mt_codes.get(mountain[r,q],0) for q in range(C.COLS)] for r in range(C.ROWS)], dtype=np.int16)
    mt_arr[ocean] = -1
    _colourise_discrete(mt_arr, {-1:(20,40,90),0:(200,200,200),1:(100,70,40),2:(70,100,180),3:(200,70,50),4:(160,60,160)}).save(MAPS/"mountain_type.png")
    scar = glacial.astype(np.int16); scar[ocean] = -1
    _colourise_discrete(scar, {-1:(20,40,90),0:(220,220,210),1:(180,220,255)}).save(MAPS/"glacial_scars.png")
    end = endorheic.astype(np.int16); end[ocean] = -1
    _colourise_discrete(end, {-1:(20,40,90),0:(210,210,200),1:(210,180,60)}).save(MAPS/"endorheic.png")
    _colourise_discrete(land.astype(np.int16), {0:(20,40,90),1:(140,170,110)}).save(MAPS/"land_ocean.png")
    (LEGENDS/"01_plates_rock.md").write_text("# 01_plates_rock\n\nWest/East craton, SE arc, northern rift, SW hotspot, ocean.\nASSUMPTION: N-S suture simplifies approved NW-SE spine.\n", encoding="utf-8")
    (LEGENDS/"02_elevation.md").write_text("# 02_elevation\n\nElevation m relative to sea_level_m=0. Glacial carving applied.\n", encoding="utf-8")
    (LEGENDS/"02_slope.md").write_text("# 02_slope\n\nSlope = max in-bounds axial-neighbour |d elev| / 30 km (m per km). No wrap.\n", encoding="utf-8")
    (LEGENDS/"glacial_scars.md").write_text("# glacial_scars\n\nCyan = LGM scars present. CSV: glacial_scar tags + glacial true/false.\n", encoding="utf-8")
    (LEGENDS/"endorheic.md").write_text("# endorheic\n\nGold = closed central-east basin. Grey = exorheic land.\n", encoding="utf-8")
    (LEGENDS/"lithology.md").write_text("# lithology\n\n" + "\n".join(f"- {v}: {ROCK_LABELS.get(k,k)}" for k,v in ROCK_TO_LITH.items()) + "\n", encoding="utf-8")
    (LEGENDS/"mountain_type.md").write_text("# mountain_type\n\nnone | collision | rift | arc | hotspot\n", encoding="utf-8")
    (DOCS/"PHYSICAL_HISTORY.md").write_text("# Physical history V1 (approved)\n\nDual-craton suture; SE arc; northern rift; SW hotspot; western passive margin; central-east endorheic. LGM ice on spine+north. Ice ended ~800-1200 yr ago. No kingdoms.\n", encoding="utf-8")
    (ROOT/"ASSUMPTIONS_GEOLOGY.md").write_text("# Assumptions — Geology\n\n" + "\n".join(f"- {a}" for a in ASSUMPTIONS) + "\n", encoding="utf-8")
    (DOCS/"HANDOFF_CLIMATE.md").write_text(f"# Handoff Geologist to Climate\n\nFiles: data/geology_hex.csv|.json; maps 02_elevation, 02_slope, glacial_scars, endorheic, 01_plates_rock.\nLGM north of r-frac {C.LGM_NORTH_EDGE_FRAC} + high suture. Walls: suture q {C.SUTURE_Q_FRAC}; arc {C.ARC_CENTER}. Endorheic {C.BASIN_CENTER}: {int(endorheic.sum())} hexes. Land {int(land.sum())}/{C.HEX_COUNT}. Elev {meta['elev_land_min']:.0f}..{meta['elev_land_max']:.0f} m.\n", encoding="utf-8")
    print(json.dumps(meta, indent=2))
    return meta

if __name__ == "__main__":
    export()
