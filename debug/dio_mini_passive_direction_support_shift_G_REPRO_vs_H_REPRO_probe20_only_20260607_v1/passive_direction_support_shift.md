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

- direction_support_not_visible_right: families=39, episode_delta=-0.051282051, best_reward_delta=-0.025641026, trade_readiness_delta=-9.9936e-05, examples=dio_01sj|dio_07t9|dio_09u3|dio_0bde|dio_0ft4|dio_0g9z|dio_0jx1|dio_0ksa|dio_0l9d|dio_0nrp|dio_0ocv|dio_0p12|dio_0rwa|dio_0t27|dio_0v3a|dio_0w16|dio_0z2v|dio_108f|dio_140n|dio_14eb|dio_15lu|dio_17ny|dio_19b6|dio_1a1w|dio_1fck|dio_1ffn|dio_1fz7|dio_1jgc|dio_1mrs|dio_1ndv
- same_sensory_field_direction_reward_weakens: families=11, episode_delta=-2.363636364, best_reward_delta=-0.837916227, trade_readiness_delta=-0.003499136, examples=dio_01w7|dio_03yz|dio_06gy|dio_095l|dio_0bm2|dio_0x52|dio_1ekr|dio_1f9y|dio_1im7|dio_1jba|dio_1xfl
- direction_support_reorganized: families=10, episode_delta=1.8, best_reward_delta=0.75508235, trade_readiness_delta=0.00194995, examples=dio_005q|dio_05ws|dio_06b8|dio_0gmg|dio_0o73|dio_0pni|dio_19bg|dio_1i05|dio_1lg2|dio_1vz0
- same_sensory_field_same_direction_but_reife_kippt: families=3, episode_delta=0.0, best_reward_delta=0.0, trade_readiness_delta=-4.833e-06, examples=dio_0q96|dio_0xkp|dio_11vr

## Anker

- dio_01sj: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_07t9: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_09u3: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0bde: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ft4: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_0g9z: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jx1: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ksa: direction_support_not_visible_right; best=SHORT->-; obs=SHORT->-; episodes=2->0; best_reward_delta=-1.0; align=near_mcm_field_with_sensory_variation
- dio_0l9d: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0nrp: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0ocv: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0p12: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0rwa: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0t27: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0v3a: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0w16: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_0z2v: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_108f: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_140n: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_14eb: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_15lu: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_17ny: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_19b6: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1a1w: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1fck: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ffn: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1fz7: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1jgc: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1mrs: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ndv: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1o2b: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1ocs: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1pvx: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1si6: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1t9x: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1ull: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1vg2: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1wx6: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=syntax_survives_but_context_changed
- dio_1ytc: direction_support_not_visible_right; best=-->-; obs=-->-; episodes=0->0; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_005q: direction_support_reorganized; best=-->LONG; obs=-->LONG; episodes=0->2; best_reward_delta=1.0; align=near_mcm_field_with_sensory_variation
- dio_05ws: direction_support_reorganized; best=-->LONG; obs=-->LONG; episodes=0->2; best_reward_delta=1.0; align=same_sensory_field_but_reife_kippt
- dio_06b8: direction_support_reorganized; best=-->LONG; obs=-->LONG; episodes=0->2; best_reward_delta=1.0; align=same_sensory_field_visible
- dio_0gmg: direction_support_reorganized; best=-->LONG; obs=-->LONG; episodes=0->2; best_reward_delta=0.093284; align=near_mcm_field_with_sensory_variation
- dio_0o73: direction_support_reorganized; best=-->LONG; obs=-->LONG; episodes=0->2; best_reward_delta=1.0; align=same_sensory_field_but_reife_kippt
- dio_0pni: direction_support_reorganized; best=-->SHORT; obs=-->SHORT; episodes=0->2; best_reward_delta=1.0; align=same_sensory_field_but_reife_kippt
- dio_19bg: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=4->2; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1i05: direction_support_reorganized; best=-->SHORT; obs=-->SHORT; episodes=0->2; best_reward_delta=1.0; align=same_sensory_field_visible
- dio_1lg2: direction_support_reorganized; best=-->SHORT; obs=-->SHORT; episodes=0->2; best_reward_delta=1.0; align=same_sensory_field_but_reife_kippt
- dio_1vz0: direction_support_reorganized; best=-->SHORT; obs=-->SHORT; episodes=0->4; best_reward_delta=0.4575395; align=near_mcm_field_with_sensory_variation
- dio_01w7: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_but_less_lived_support
- dio_03yz: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=2->0; best_reward_delta=-0.484461; align=same_sensory_field_visible
- dio_06gy: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=4->0; best_reward_delta=-0.4295875; align=same_sensory_field_but_less_lived_support
- dio_095l: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_visible
- dio_0bm2: same_sensory_field_direction_reward_weakens; best=SHORT->-; obs=SHORT->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_but_less_lived_support
- dio_0x52: same_sensory_field_direction_reward_weakens; best=SHORT->-; obs=SHORT->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_but_less_lived_support
- dio_1ekr: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_but_less_lived_support
- dio_1f9y: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=2->0; best_reward_delta=-0.30303; align=same_sensory_field_but_less_lived_support
- dio_1im7: same_sensory_field_direction_reward_weakens; best=SHORT->-; obs=SHORT->-; episodes=4->0; best_reward_delta=-1.0; align=same_sensory_field_visible
- dio_1jba: same_sensory_field_direction_reward_weakens; best=LONG->-; obs=LONG->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_visible
- dio_1xfl: same_sensory_field_direction_reward_weakens; best=SHORT->-; obs=SHORT->-; episodes=2->0; best_reward_delta=-1.0; align=same_sensory_field_visible
- dio_0q96: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0xkp: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_11vr: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=2->2; best_reward_delta=0.0; align=same_sensory_field_visible
