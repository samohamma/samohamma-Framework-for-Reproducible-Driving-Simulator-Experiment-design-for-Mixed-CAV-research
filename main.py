# -*- coding: utf-8 -*-
import os, sys

# path setup
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
WORLDS_DIR = os.path.join(THIS_DIR, "worlds")
os.makedirs(WORLDS_DIR, exist_ok=True)

if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)

from GenereateExperiment import make_roads, build_world

# ---- user config ----
N = 2
n_lanes = 5
L_mid   = 700.0
L_ramp  = [1000.0, 800.0]
L_main  = 12300.0

N1, N2, N3, N4, N5 = 12, 10, 6, 1, 0
surr_counts = {1:N1, 2:N2, 3:N3, 4:N4, 5:N5}
# ---------------------

roads = make_roads(
    N,
    n_lanes=n_lanes,
    L_mid=L_mid,
    L_ramp=L_ramp,
    L_main=L_main,
    surr_counts_rr1=surr_counts,
)

world_text = build_world(road_cfgs=roads)

out_path = os.path.join(WORLDS_DIR, "ExperimentDesign.wbt")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(world_text)

print(f"Wrote {out_path}")

