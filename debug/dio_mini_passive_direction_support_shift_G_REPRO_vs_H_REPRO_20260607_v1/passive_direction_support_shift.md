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

- same_sensory_field_same_direction_but_reife_kippt: families=41, episode_delta=0.926829268, best_reward_delta=0.024082868, trade_readiness_delta=0.003090002, examples=dio_03yz|dio_05ws|dio_06b8|dio_07t9|dio_095l|dio_09u3|dio_0bde|dio_0g9z|dio_0jx1|dio_0l9d|dio_0nrp|dio_0o73|dio_0ocv|dio_0p12|dio_0pni|dio_0q96|dio_0rwa|dio_0v3a|dio_0xkp|dio_0z2v|dio_11vr|dio_140n|dio_14eb|dio_17ny|dio_19b6|dio_1fck|dio_1ffn|dio_1fz7|dio_1i05|dio_1im7
- direction_support_reorganized: families=8, episode_delta=-1.875, best_reward_delta=-0.002048763, trade_readiness_delta=-0.004211451, examples=dio_005q|dio_0ft4|dio_0ksa|dio_108f|dio_19bg|dio_1a1w|dio_1o2b|dio_1vz0
- same_sensory_field_less_lived_direction_support: families=8, episode_delta=-3.625, best_reward_delta=0.101286528, trade_readiness_delta=-0.011042819, examples=dio_01sj|dio_01w7|dio_06gy|dio_0bm2|dio_0w16|dio_0x52|dio_1ekr|dio_1f9y
- direction_support_flips: families=4, episode_delta=-0.5, best_reward_delta=-0.167828575, trade_readiness_delta=-0.002682263, examples=dio_0gmg|dio_1pvx|dio_1si6|dio_1wx6
- same_sensory_field_direction_reward_weakens: families=2, episode_delta=-1.0, best_reward_delta=-0.58678675, trade_readiness_delta=-0.004874375, examples=dio_0t27|dio_15lu

## Anker

- dio_0gmg: direction_support_flips; best=SHORT->LONG; obs=SHORT->LONG; episodes=12->10; best_reward_delta=-0.2231438; align=near_mcm_field_with_sensory_variation
- dio_1pvx: direction_support_flips; best=LONG->SHORT; obs=LONG->SHORT; episodes=4->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1si6: direction_support_flips; best=LONG->SHORT; obs=LONG->SHORT; episodes=2->4; best_reward_delta=-0.4481705; align=same_sensory_field_visible
- dio_1wx6: direction_support_flips; best=SHORT->LONG; obs=SHORT->LONG; episodes=2->2; best_reward_delta=0.0; align=syntax_survives_but_context_changed
- dio_005q: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=4->6; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_0ft4: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=5->4; best_reward_delta=0.0022604; align=near_mcm_field_with_sensory_variation
- dio_0ksa: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->4; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_108f: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_19bg: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=16->8; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1a1w: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1o2b: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=6->2; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1vz0: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->4; best_reward_delta=-0.0186505; align=near_mcm_field_with_sensory_variation
- dio_0t27: same_sensory_field_direction_reward_weakens; best=SHORT->WAIT; obs=SHORT->-; episodes=4->4; best_reward_delta=-0.2488555; align=same_sensory_field_visible
- dio_15lu: same_sensory_field_direction_reward_weakens; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=-0.924718; align=same_sensory_field_visible
- dio_01sj: same_sensory_field_less_lived_direction_support; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_01w7: same_sensory_field_less_lived_direction_support; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_06gy: same_sensory_field_less_lived_direction_support; best=LONG->LONG; obs=LONG->LONG; episodes=8->2; best_reward_delta=0.59698575; align=same_sensory_field_but_less_lived_support
- dio_0bm2: same_sensory_field_less_lived_direction_support; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->4; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_0w16: same_sensory_field_less_lived_direction_support; best=LONG->LONG; obs=LONG->LONG; episodes=3->2; best_reward_delta=0.167216333; align=same_sensory_field_but_less_lived_support
- dio_0x52: same_sensory_field_less_lived_direction_support; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=8->2; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_1ekr: same_sensory_field_less_lived_direction_support; best=LONG->LONG; obs=LONG->LONG; episodes=9->2; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_1f9y: same_sensory_field_less_lived_direction_support; best=LONG->LONG; obs=LONG->LONG; episodes=7->4; best_reward_delta=0.046090143; align=same_sensory_field_but_less_lived_support
- dio_03yz: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->4; best_reward_delta=0.0141095; align=same_sensory_field_visible
- dio_05ws: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->12; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_06b8: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->14; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_07t9: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_095l: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_09u3: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0bde: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.056686; align=same_sensory_field_visible
- dio_0g9z: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=5->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jx1: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=1->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0l9d: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0nrp: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0o73: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=1->4; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0ocv: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0p12: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=1->4; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0pni: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->4; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0q96: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=8->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0rwa: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0v3a: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0xkp: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0z2v: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=-0.006446; align=same_sensory_field_visible
- dio_11vr: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=6->6; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_140n: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=6->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_14eb: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.153854; align=same_sensory_field_but_reife_kippt
- dio_17ny: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->4; best_reward_delta=0.156416; align=same_sensory_field_visible
- dio_19b6: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1fck: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ffn: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1fz7: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->4; best_reward_delta=0.424535; align=same_sensory_field_visible
- dio_1i05: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1im7: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=8->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1jba: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=5->4; best_reward_delta=-0.0925889; align=same_sensory_field_visible
- dio_1jgc: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=4->6; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1lg2: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1mrs: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=1->4; best_reward_delta=0.304752; align=same_sensory_field_but_reife_kippt
- dio_1ndv: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ocs: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1t9x: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1ull: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1vg2: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->10; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1xfl: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->4; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1ytc: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=-0.02392; align=same_sensory_field_but_reife_kippt
