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

- same_sensory_field_same_direction_but_reife_kippt: families=53, episode_delta=0.0, best_reward_delta=0.0, trade_readiness_delta=0.0, examples=dio_01sj|dio_01w7|dio_03yz|dio_05ws|dio_06b8|dio_06gy|dio_07t9|dio_095l|dio_09u3|dio_0bde|dio_0bm2|dio_0g9z|dio_0jx1|dio_0l9d|dio_0nrp|dio_0o73|dio_0ocv|dio_0p12|dio_0pni|dio_0q96|dio_0rwa|dio_0t27|dio_0v3a|dio_0w16|dio_0x52|dio_0xkp|dio_0z2v|dio_11vr|dio_140n|dio_14eb
- direction_support_reorganized: families=10, episode_delta=0.0, best_reward_delta=0.0, trade_readiness_delta=0.0, examples=dio_005q|dio_0ft4|dio_0gmg|dio_0ksa|dio_108f|dio_19bg|dio_1a1w|dio_1o2b|dio_1vz0|dio_1wx6

## Anker

- dio_005q: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=38->38; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_0ft4: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=47->47; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_0gmg: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=181->181; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_0ksa: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=52->52; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_108f: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=51->51; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_19bg: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=142->142; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1a1w: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=25->25; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1o2b: direction_support_reorganized; best=LONG->LONG; obs=LONG->LONG; episodes=49->49; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1vz0: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=28->28; best_reward_delta=0.0; align=near_mcm_field_with_sensory_variation
- dio_1wx6: direction_support_reorganized; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=13->13; best_reward_delta=0.0; align=syntax_survives_but_context_changed
- dio_01sj: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=39->39; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_01w7: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=33->33; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_03yz: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=32->32; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_05ws: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=32->32; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_06b8: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=29->29; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_06gy: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=93->93; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_07t9: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=74->74; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_095l: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=41->41; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_09u3: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=34->34; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0bde: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=15->15; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0bm2: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=66->66; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_0g9z: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=86->86; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0jx1: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=10->10; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0l9d: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=11->11; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0nrp: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=13->13; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0o73: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=19->19; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0ocv: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=15->15; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0p12: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=5->5; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0pni: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=24->24; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_0q96: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=137->137; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0rwa: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=21->21; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0t27: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=56->56; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0v3a: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=11->11; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0w16: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=22->22; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_0x52: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=213->213; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_0xkp: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=17->17; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_0z2v: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=18->18; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_11vr: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=37->37; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_140n: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=126->126; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_14eb: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=LONG->LONG; episodes=57->57; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_15lu: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=33->33; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_17ny: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=16->16; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_19b6: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=15->15; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1ekr: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=66->66; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_1f9y: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=71->71; best_reward_delta=0.0; align=same_sensory_field_but_less_lived_support
- dio_1fck: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=11->11; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ffn: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=11->11; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1fz7: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=10->10; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1i05: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=17->17; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1im7: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=38->38; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1jba: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=59->59; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1jgc: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=43->43; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1lg2: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=7->7; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1mrs: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=63->63; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ndv: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=7->7; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
- dio_1ocs: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=15->15; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1pvx: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=11->11; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1si6: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=22->22; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1t9x: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=17->17; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1ull: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=70->70; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1vg2: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=47->47; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1xfl: same_sensory_field_same_direction_but_reife_kippt; best=SHORT->SHORT; obs=SHORT->SHORT; episodes=17->17; best_reward_delta=0.0; align=same_sensory_field_visible
- dio_1ytc: same_sensory_field_same_direction_but_reife_kippt; best=LONG->LONG; obs=LONG->LONG; episodes=13->13; best_reward_delta=0.0; align=same_sensory_field_but_reife_kippt
