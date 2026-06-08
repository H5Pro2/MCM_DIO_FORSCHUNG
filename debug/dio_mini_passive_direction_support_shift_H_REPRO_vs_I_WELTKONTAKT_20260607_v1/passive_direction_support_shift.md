# Passive Direction Support Shift

Dieser Bericht prueft, ob eine gekippte Syntax mit veraenderter Richtungsstuetzung zusammenhaengt.

## Grenze

- passiv
- keine Runtime-Lesung
- keine Handlung
- kein Gate
- kein Entry
- keine Richtung

## Summary

- same_sensory_field_same_direction_but_reife_kippt: families=242, episode_delta=-0.024793388, best_reward_delta=0.002537062, trade_readiness_delta=-0.00021188, examples=dio_005k|dio_005q|dio_00r9|dio_010h|dio_0120|dio_015b|dio_01px|dio_01sj|dio_01w7|dio_02rt|dio_02y8|dio_0325|dio_03sc|dio_05cu|dio_05e5|dio_05ws|dio_05xk|dio_065c|dio_06b8|dio_06gy|dio_06jl|dio_07lp|dio_07mb|dio_07mw|dio_07t9|dio_080e|dio_091t|dio_09ow|dio_09tm|dio_09u3
- direction_support_reorganized: families=3, episode_delta=-2.0, best_reward_delta=0.051708833, trade_readiness_delta=-0.005149639, examples=dio_0lrt|dio_14ud|dio_1xka
- direction_support_not_visible_right: families=1, episode_delta=0.0, best_reward_delta=-3.5e-05, trade_readiness_delta=-2.5e-06, examples=dio_0t27
- same_sensory_field_direction_reward_weakens: families=1, episode_delta=-2.0, best_reward_delta=-0.4373715, trade_readiness_delta=-0.0015215, examples=dio_1si6

## Anker

- dio_0t27: direction_support_not_visible_right; best=WAIT->WAIT; obs=-->-; episodes=4->4; best_reward_delta=-3.5e-05; align=same_sensory_field_visible
- dio_0lrt: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=6->4; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_14ud: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->2; best_reward_delta=0.411032; align=near_mcm_field_with_sensory_variation
- dio_1xka: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->4; best_reward_delta=-0.2559055; align=near_mcm_field_with_sensory_variation
- dio_1si6: same_sensory_field_direction_reward_weakens; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->2; best_reward_delta=-0.4373715; align=same_sensory_field_visible
- dio_005k: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_005q: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=6->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_00r9: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_010h: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0120: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_015b: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_01px: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_01sj: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_01w7: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_02rt: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=6->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_02y8: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0325: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=-0.001072; align=same_sensory_field_visible
- dio_03sc: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_05cu: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=-0.00285; align=same_sensory_field_visible
- dio_05e5: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_05ws: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=12->10; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_05xk: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=8->8; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_065c: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.506757; align=same_sensory_field_visible
- dio_06b8: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=14->14; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_06gy: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_06jl: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_07lp: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=-0.001956; align=same_sensory_field_visible
- dio_07mb: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_07mw: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->8; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_07t9: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_080e: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=-0.003401; align=same_sensory_field_visible
- dio_091t: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_09ow: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_09tm: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_09u3: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0a7t: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0avw: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0azl: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0b2b: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=-0.000188; align=same_sensory_field_visible
- dio_0bde: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=-0.008695; align=same_sensory_field_visible
- dio_0bm2: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ce4: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0cxr: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0dos: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=6->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0e02: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=-0.01152; align=same_sensory_field_visible
- dio_0e37: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0eeh: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=12->16; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ehw: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0eq2: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0fsp: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ft4: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->4; best_reward_delta=-0.007988; align=same_sensory_field_visible
- dio_0g2u: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=6->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0g55: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0gmg: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=10->10; best_reward_delta=-0.002008; align=same_sensory_field_visible
- dio_0haj: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0hl8: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0hlx: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0i4h: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ic6: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=6->8; best_reward_delta=0.180232667; align=same_sensory_field_visible
- dio_0icm: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ink: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=-0.001784; align=same_sensory_field_visible
- dio_0iou: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ipe: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0irs: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0j34: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0j8d: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jg9: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jgk: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jp7: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jx1: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0k0f: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0kae: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0kom: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ksa: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0kw1: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0l9d: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0lf6: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0m7s: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0m9e: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ngs: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ni1: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0nki: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0013; align=same_sensory_field_visible
- dio_0nmw: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0nrp: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0nvd: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->4; best_reward_delta=-0.06338; align=same_sensory_field_visible
- dio_0o73: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ocp: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ocv: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0omt: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0pni: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
