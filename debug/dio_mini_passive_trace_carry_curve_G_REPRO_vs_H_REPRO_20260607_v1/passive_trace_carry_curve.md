# Passive Trace Carry Curve

Dieser Bericht beschreibt, wie lange situative emergente Spuren getragen bleiben.

## Grenze

- passiv
- keine Runtime-Lesung
- keine Handlung
- kein Gate
- kein Entry
- keine Richtung

## Familien-Summary

- trace_immediate_or_continuous_kipp: families=46, avg_carry_ratio=0.0, avg_before_first_kipp=0.0, examples=dio_01sj|dio_01w7|dio_03yz|dio_06b8|dio_06gy|dio_095l|dio_09u3|dio_0bm2|dio_0ft4|dio_0g9z|dio_0gmg|dio_0ksa|dio_0l9d|dio_0nrp|dio_0o73|dio_0pni|dio_0q96|dio_0t27|dio_0v3a|dio_0w16|dio_0x52|dio_0xkp|dio_0z2v|dio_108f|dio_140n|dio_14eb|dio_15lu|dio_17ny|dio_19bg|dio_1a1w|dio_1ekr|dio_1f9y|dio_1ffn|dio_1i05|dio_1im7|dio_1jba|dio_1lg2|dio_1mrs|dio_1o2b|dio_1ocs
- trace_fully_carried: families=8, avg_carry_ratio=1.0, avg_before_first_kipp=1.25, examples=dio_0bde|dio_0jx1|dio_0ocv|dio_0rwa|dio_11vr|dio_19b6|dio_1fck|dio_1ndv
- trace_carries_then_kipps: families=3, avg_carry_ratio=0.5, avg_before_first_kipp=1.0, examples=dio_07t9|dio_0p12|dio_1fz7
- trace_kipps_then_recarries: families=3, avg_carry_ratio=0.4, avg_before_first_kipp=0.0, examples=dio_1si6|dio_1ull|dio_1vg2
- trace_mixed_mostly_kipped: families=3, avg_carry_ratio=0.277777778, avg_before_first_kipp=0.0, examples=dio_005q|dio_05ws|dio_1jgc

## Probe-Kurve

- probe20: carry=1/25 ratio=0.04; support_drop=13; direction_flip=0; neuro=9; readiness=2
- probe21: carry=1/17 ratio=0.058823529; support_drop=6; direction_flip=2; neuro=4; readiness=2
- probe22: carry=3/29 ratio=0.103448276; support_drop=12; direction_flip=1; neuro=10; readiness=3
- probe23: carry=7/20 ratio=0.35; support_drop=7; direction_flip=0; neuro=4; readiness=1
- probe24: carry=2/26 ratio=0.076923077; support_drop=7; direction_flip=1; neuro=9; readiness=7
- probe25: carry=4/23 ratio=0.173913043; support_drop=9; direction_flip=0; neuro=7; readiness=2
- probe26: carry=2/21 ratio=0.095238095; support_drop=6; direction_flip=1; neuro=10; readiness=2

## Familien

- dio_07t9: trace_carries_then_kipps; carry=1/2; first_kipp=probe26/probe_neuro_tone_reorganizes; path=probe_no_visible_kipp -> probe_neuro_tone_reorganizes
- dio_0p12: trace_carries_then_kipps; carry=1/2; first_kipp=probe26/probe_neuro_tone_reorganizes; path=probe_no_visible_kipp -> probe_neuro_tone_reorganizes
- dio_1fz7: trace_carries_then_kipps; carry=1/2; first_kipp=probe24/probe_neuro_tone_reorganizes; path=probe_no_visible_kipp -> probe_neuro_tone_reorganizes
- dio_0bde: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0jx1: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0ocv: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0rwa: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_11vr: trace_fully_carried; carry=3/3; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_19b6: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1fck: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1ndv: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_01sj: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe25/probe_lived_support_drop; path=probe_lived_support_drop -> probe_trade_readiness_softens
- dio_01w7: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_neuro_tone_reorganizes
- dio_03yz: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes
- dio_06b8: trace_immediate_or_continuous_kipp; carry=0/7; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes
- dio_06gy: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_trade_readiness_softens -> probe_lived_support_drop
- dio_095l: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_trade_readiness_softens
- dio_09u3: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe24/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes
- dio_0bm2: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_trade_readiness_softens -> probe_neuro_tone_reorganizes
- dio_0ft4: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe25/probe_best_reward_softens; path=probe_best_reward_softens -> probe_lived_support_drop
- dio_0g9z: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe22/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_trade_readiness_softens
- dio_0gmg: trace_immediate_or_continuous_kipp; carry=0/5; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_direction_flip -> probe_direction_flip -> probe_lived_support_drop -> probe_direction_flip
- dio_0ksa: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_0l9d: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe21/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_0nrp: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe21/probe_trade_readiness_softens; path=probe_trade_readiness_softens
- dio_0o73: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_0pni: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_0q96: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_trade_readiness_softens; path=probe_trade_readiness_softens -> probe_lived_support_drop -> probe_trade_readiness_softens
- dio_0t27: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe22/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_direction_flip
- dio_0v3a: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe24/probe_trade_readiness_softens; path=probe_trade_readiness_softens
- dio_0w16: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe21/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_0x52: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_trade_readiness_softens -> probe_lived_support_drop
- dio_0xkp: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe20/probe_trade_readiness_softens; path=probe_trade_readiness_softens
- dio_0z2v: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe22/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes
- dio_108f: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe23/probe_lived_support_drop; path=probe_lived_support_drop
- dio_140n: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe21/probe_lived_support_drop; path=probe_lived_support_drop -> probe_trade_readiness_softens -> probe_trade_readiness_softens
- dio_14eb: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe21/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes
- dio_15lu: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe21/probe_best_reward_softens; path=probe_best_reward_softens -> probe_lived_support_drop
- dio_17ny: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe22/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop -> probe_neuro_tone_reorganizes
- dio_19bg: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_lived_support_drop -> probe_trade_readiness_softens
- dio_1a1w: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe23/probe_lived_support_drop; path=probe_lived_support_drop
- dio_1ekr: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop -> probe_lived_support_drop -> probe_lived_support_drop
- dio_1f9y: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_best_reward_softens -> probe_trade_readiness_softens -> probe_lived_support_drop
- dio_1ffn: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe22/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1i05: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1im7: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_trade_readiness_softens -> probe_trade_readiness_softens
- dio_1jba: trace_immediate_or_continuous_kipp; carry=0/4; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_direction_flip -> probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1lg2: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1mrs: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe24/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop -> probe_neuro_tone_reorganizes
- dio_1o2b: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe23/probe_lived_support_drop; path=probe_lived_support_drop -> probe_lived_support_drop
- dio_1ocs: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe24/probe_trade_readiness_softens; path=probe_trade_readiness_softens
- dio_1pvx: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe21/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1t9x: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe23/probe_trade_readiness_softens; path=probe_trade_readiness_softens
- dio_1vz0: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1wx6: trace_immediate_or_continuous_kipp; carry=0/2; first_kipp=probe23/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_lived_support_drop
- dio_1xfl: trace_immediate_or_continuous_kipp; carry=0/3; first_kipp=probe20/probe_lived_support_drop; path=probe_lived_support_drop -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes
- dio_1ytc: trace_immediate_or_continuous_kipp; carry=0/1; first_kipp=probe21/probe_best_reward_softens; path=probe_best_reward_softens
- dio_1si6: trace_kipps_then_recarries; carry=1/2; first_kipp=probe21/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_no_visible_kipp
- dio_1ull: trace_kipps_then_recarries; carry=1/2; first_kipp=probe25/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_no_visible_kipp
- dio_1vg2: trace_kipps_then_recarries; carry=1/5; first_kipp=probe21/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_no_visible_kipp
- dio_005q: trace_mixed_mostly_kipped; carry=1/4; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes -> probe_no_visible_kipp -> probe_lived_support_drop
- dio_05ws: trace_mixed_mostly_kipped; carry=2/6; first_kipp=probe20/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_no_visible_kipp -> probe_neuro_tone_reorganizes -> probe_no_visible_kipp -> probe_neuro_tone_reorganizes -> probe_neuro_tone_reorganizes
- dio_1jgc: trace_mixed_mostly_kipped; carry=1/4; first_kipp=probe22/probe_neuro_tone_reorganizes; path=probe_neuro_tone_reorganizes -> probe_no_visible_kipp -> probe_lived_support_drop -> probe_neuro_tone_reorganizes
