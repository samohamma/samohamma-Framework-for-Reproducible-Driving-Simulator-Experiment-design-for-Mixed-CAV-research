# -*- coding: utf-8 -*-
from .constants import *
from .geometry import f_main_head, f_exit_anchor

def emit_tlights(prefix, Sx, Sz, *, L_main,
                 onrmp_dfwd=None, onrmp_dlat=+33.0, onrmp_yaw=-DELTA,
                 stngo_frac=STNGO_FRAC_DEFAULT,
                 takeover_back_frac=TAKEOVER_BACK_FRAC_DEFAULT,
                 off_after_exit=OFF_AFTER_EXIT, off_dlat=-10.0, off_yaw=-DELTA):
    if onrmp_dfwd is None:
        onrmp_dfwd = L_START - 110.0

    stngo_dfwd    = f_main_head() + stngo_frac * L_main
    takeover_dfwd = f_main_head() + (1.0 - takeover_back_frac) * L_main
    off_dfwd      = f_exit_anchor(L_main) + L_EXIT + off_after_exit

    x_on , z_on  = Sx + onrmp_dlat, Sz + onrmp_dfwd
    x_stn, z_stn = Sx,               Sz + stngo_dfwd
    x_tko, z_tko = Sx,               Sz + takeover_dfwd
    x_off, z_off = Sx + off_dlat,    Sz + off_dfwd

    nodes = []
    nodes.append(f'''DEF TL_onrmp_{prefix} GenericTrafficLight {{
  translation {x_on:.4f} 0.30 {z_on:.4f}
  rotation 0 1 0 {onrmp_yaw:.4f}
  name "{prefix}TL_onrmp"
  state "red"
  controller "traffic_light_red"
  controllerArgs "2000 0.1 r"
}}''')
    nodes.append(f'''DEF TL_img_StnGo_{prefix} GenericTrafficLight {{
  translation {x_stn:.4f} -5 {z_stn:.4f}
  name "{prefix}TL_img_StnGo"
  state "red"
  controller "traffic_light_red"
  controllerArgs "2000 0.1 r"
}}''')
    nodes.append(f'''DEF TL_img_takeOver_{prefix} GenericTrafficLight {{
  translation {x_tko:.4f} -5 {z_tko:.4f}
  name "{prefix}TL_img_takeOver"
  state "red"
  controller "traffic_light_red"
  controllerArgs "2000 0.1 r"
}}''')
    nodes.append(f'''DEF TL_offrmp_{prefix} GenericTrafficLight {{
  translation {x_off:.4f} 0.50 {z_off:.4f}
  rotation 0 1 0 {off_yaw:.4f}
  name "{prefix}TL_offrmp"
  state "red"
  controller "traffic_light_red"
  controllerArgs "2000 0.1 r"
}}''')
    return "\n".join(nodes), dict(onrmp=(x_on,z_on), stngo=(x_stn,z_stn), takeover=(x_tko,z_tko), offrmp=(x_off,z_off))
