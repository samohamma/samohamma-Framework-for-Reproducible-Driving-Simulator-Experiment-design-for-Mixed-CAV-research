# -*- coding: utf-8 -*-
import random
from .geometry import lane_x_n, _phys_lane, onramp_local_start, world_from_local
from .constants import *
from .lights import emit_tlights

def _rand_color(rng): return f"{rng.random():.5f} {rng.random():.5f} {rng.random():.5f}"

def _bmw(type_name,name,x,z,color_rgb):
    ctrl = {"surr":"auto_surrounding_merge","sg":"auto_stop_and_go","broken":"auto_broken"}[type_name]
    return f'''BmwX5 {{
  translation {x:.4f} 1.4 {z:.4f}
  color {color_rgb}
  name "{name}"
  controller "{ctrl}"
  supervisor TRUE
  sensorsSlotFront [ Radar {{ minRange 2 maxRange 300 horizontalFieldOfView 0.5 verticalFieldOfView 0.002 }} ]
  sensorsSlotTop [ GPS {{}} Receiver {{}} Emitter {{}} ]
  interior FALSE
  dynamicSpeedDisplay FALSE
  indicatorLevers FALSE
  completeInterior FALSE
}}'''

def _ego_participant(name,Sx,Sz,n_lanes,L_ramp):
    f,l = onramp_local_start(n_lanes,L_ramp)
    x,z = world_from_local(Sx,Sz,f,l)
    return f'''BmwX5Au {{
  translation {x:.4f} 1.38 {z:.4f}
  rotation 0 1 0 {-DELTA:.4f}
  name "{name}"
  controller "auto_ringroad_driver"
  supervisor TRUE
  sensorsSlotTop [ GPS {{}} Receiver {{}} Emitter {{}} ]
  completeInterior FALSE
  innerWindowTransparency 1
}}'''

def emit_vehicles(prefix,Sx,Sz,*,L_main,n_lanes,L_ramp,
                  surr_counts_by_lane, surr_first_gap, surr_spacing,
                  stngo_row_spacing=30.0, stngo_lanes=(1,2,3,4),
                  broken_lane=1, broken_offset=30.0, seed=None,
                  include_participant=True):
    rng = random.Random(seed)
    _, tlpos = emit_tlights(prefix,Sx,Sz,L_main=L_main)
    x_on,z_on   = tlpos['onrmp']
    _,   z_stn  = tlpos['stngo']
    _,   z_tko  = tlpos['takeover']

    nodes = []
    if include_participant:
        nodes.append(_ego_participant("veh-driver",Sx,Sz,n_lanes,L_ramp))

    # Surrounding flow: lanes 1..(n_lanes-1) (keep rightmost empty)
    for lane in range(1, n_lanes):
        count = int(surr_counts_by_lane.get(lane, 0))
        if count <= 0: 
            continue
        phys = _phys_lane(lane, n_lanes)
        x_lane = lane_x_n(Sx, n_lanes, phys)
        for r in range(1, count+1):
            z = z_on - (surr_first_gap + (r-1)*surr_spacing)
            nodes.append(_bmw("surr", f"CAV_Surr_row{r}_Lane{lane}", x_lane, z, _rand_color(rng)))

    # Stop-and-go (avoid rightmost lane)
    for lane in [l for l in stngo_lanes if 1 <= l <= (n_lanes-1)]:
        phys = _phys_lane(lane, n_lanes)
        x_lane = lane_x_n(Sx, n_lanes, phys)
        nodes.append(_bmw("sg", f"CAV_StopnGo_row2_Lane{lane}", x_lane, z_stn,                     _rand_color(rng)))
        nodes.append(_bmw("sg", f"CAV_StopnGo_row1_Lane{lane}", x_lane, z_stn + stngo_row_spacing, _rand_color(rng)))

    # Broken vehicle (avoid rightmost)
    bl = max(1, min(broken_lane, n_lanes-1))
    phys_bl = _phys_lane(bl, n_lanes)
    x_b = lane_x_n(Sx, n_lanes, phys_bl); z_b = z_tko + broken_offset
    nodes.append(_bmw("broken", f"Broken_Surr_row0_Lane{bl}", x_b, z_b, _rand_color(rng)))

    return "\n".join(nodes)
