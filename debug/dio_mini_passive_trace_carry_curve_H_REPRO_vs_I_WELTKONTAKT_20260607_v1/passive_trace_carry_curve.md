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

- trace_immediate_or_continuous_kipp: families=123, avg_carry_ratio=0.0, avg_before_first_kipp=0.0, examples=dio_005k|dio_01w7|dio_02rt|dio_0325|dio_05cu|dio_06jl|dio_07lp|dio_07mb|dio_07t9|dio_080e|dio_091t|dio_09ow|dio_0avw|dio_0azl|dio_0b2b|dio_0bde|dio_0cxr|dio_0e02|dio_0ehw|dio_0fsp|dio_0ft4|dio_0g2u|dio_0gmg|dio_0haj|dio_0i4h|dio_0ink|dio_0iou|dio_0irs|dio_0j34|dio_0j8d|dio_0k0f|dio_0ksa|dio_0lrt|dio_0m9e|dio_0ngs|dio_0ni1|dio_0nvd|dio_0o73|dio_0ocp|dio_0omt
- trace_fully_carried: families=96, avg_carry_ratio=1.0, avg_before_first_kipp=1.25, examples=dio_00r9|dio_010h|dio_0120|dio_015b|dio_01px|dio_01sj|dio_02y8|dio_05e5|dio_05xk|dio_065c|dio_06gy|dio_09tm|dio_09u3|dio_0a7t|dio_0bm2|dio_0ce4|dio_0e37|dio_0eq2|dio_0g55|dio_0hlx|dio_0icm|dio_0ipe|dio_0jg9|dio_0jgk|dio_0jp7|dio_0jx1|dio_0kae|dio_0kom|dio_0kw1|dio_0l9d|dio_0lf6|dio_0m7s|dio_0nki|dio_0nmw|dio_0nrp|dio_0ocv|dio_0qcz|dio_0qjm|dio_0r90|dio_0rt8
- trace_carries_then_kipps: families=15, avg_carry_ratio=0.473333333, avg_before_first_kipp=1.4, examples=dio_03sc|dio_05ws|dio_06b8|dio_0dos|dio_0eeh|dio_0qfc|dio_0t27|dio_0zq7|dio_16kq|dio_1f9y|dio_1qaq|dio_1qst|dio_1s9i|dio_1si6|dio_1tjm
- trace_kipps_then_recarries: families=9, avg_carry_ratio=0.507407407, avg_before_first_kipp=0.0, examples=dio_07mw|dio_0hl8|dio_0ic6|dio_0r8l|dio_12x0|dio_1dl4|dio_1im7|dio_1jba|dio_1pel
- trace_mixed_mostly_carried: families=3, avg_carry_ratio=0.638888889, avg_before_first_kipp=1.333333333, examples=dio_005q|dio_1gsg|dio_1p8y
- trace_mixed_mostly_kipped: families=1, avg_carry_ratio=0.333333333, avg_before_first_kipp=0.0, examples=dio_1wgb

## Probe-Kurve

- probe20: carry=25/61 ratio=0.409836066; support_drop=7; direction_flip=0; neuro=5; readiness=21
- probe21: carry=31/57 ratio=0.543859649; support_drop=4; direction_flip=0; neuro=0; readiness=15
- probe22: carry=16/62 ratio=0.258064516; support_drop=6; direction_flip=0; neuro=6; readiness=26
- probe23: carry=24/56 ratio=0.428571429; support_drop=2; direction_flip=1; neuro=1; readiness=22
- probe24: carry=25/62 ratio=0.403225806; support_drop=5; direction_flip=0; neuro=3; readiness=20
- probe25: carry=23/56 ratio=0.410714286; support_drop=5; direction_flip=0; neuro=2; readiness=23
- probe26: carry=19/57 ratio=0.333333333; support_drop=4; direction_flip=0; neuro=7; readiness=23

## Familien

- dio_03sc: trace_carries_then_kipps; carry=2/3; first_kipp=probe25/probe_lived_support_drop; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_lived_support_drop
- dio_05ws: trace_carries_then_kipps; carry=2/6; first_kipp=probe22/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_trade_readiness_softens -> probe_trade_readiness_softens -> probe_trade_readiness_softens -> probe_no_visible_kipp -> probe_lived_support_drop
- dio_06b8: trace_carries_then_kipps; carry=2/6; first_kipp=probe22/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_trade_readiness_softens -> probe_trade_readiness_softens -> probe_trade_readiness_softens -> probe_trade_readiness_softens
- dio_0dos: trace_carries_then_kipps; carry=2/3; first_kipp=probe25/probe_lived_support_drop; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_lived_support_drop
- dio_0eeh: trace_carries_then_kipps; carry=3/5; first_kipp=probe24/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp -> probe_trade_readiness_softens -> probe_trade_readiness_softens
- dio_0qfc: trace_carries_then_kipps; carry=1/2; first_kipp=probe26/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_trade_readiness_softens
- dio_0t27: trace_carries_then_kipps; carry=1/2; first_kipp=probe26/probe_best_reward_softens; path=probe_no_visible_kipp -> probe_best_reward_softens
- dio_0zq7: trace_carries_then_kipps; carry=2/4; first_kipp=probe25/probe_lived_support_drop; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_lived_support_drop -> probe_lived_support_drop
- dio_16kq: trace_carries_then_kipps; carry=1/2; first_kipp=probe24/probe_lived_support_drop; path=probe_no_visible_kipp -> probe_lived_support_drop
- dio_1f9y: trace_carries_then_kipps; carry=1/2; first_kipp=probe24/probe_best_reward_softens; path=probe_no_visible_kipp -> probe_best_reward_softens
- dio_1qaq: trace_carries_then_kipps; carry=1/2; first_kipp=probe26/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_trade_readiness_softens
- dio_1qst: trace_carries_then_kipps; carry=1/3; first_kipp=probe22/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_trade_readiness_softens -> probe_trade_readiness_softens
- dio_1s9i: trace_carries_then_kipps; carry=1/3; first_kipp=probe22/probe_best_reward_softens; path=probe_no_visible_kipp -> probe_best_reward_softens -> probe_lived_support_drop
- dio_1si6: trace_carries_then_kipps; carry=1/2; first_kipp=probe23/probe_lived_support_drop; path=probe_no_visible_kipp -> probe_lived_support_drop
- dio_1tjm: trace_carries_then_kipps; carry=1/3; first_kipp=probe23/probe_trade_readiness_softens; path=probe_no_visible_kipp -> probe_trade_readiness_softens -> probe_lived_support_drop
- dio_00r9: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_010h: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0120: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_015b: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_01px: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_01sj: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_02y8: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_05e5: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_05xk: trace_fully_carried; carry=4/4; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_065c: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_06gy: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_09tm: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_09u3: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0a7t: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0bm2: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0ce4: trace_fully_carried; carry=3/3; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0e37: trace_fully_carried; carry=3/3; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0eq2: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0g55: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0hlx: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0icm: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0ipe: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0jg9: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0jgk: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0jp7: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0jx1: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0kae: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0kom: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0kw1: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0l9d: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0lf6: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0m7s: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0nki: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0nmw: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0nrp: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0ocv: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0qcz: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0qjm: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0r90: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0rt8: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0rwa: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0sou: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0trg: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0u61: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0ux0: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0v3a: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0vn1: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0wxw: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0x9y: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_0yco: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_0zoq: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_106t: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_114i: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_11nj: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_11vr: trace_fully_carried; carry=3/3; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_12sg: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_12xx: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_13a8: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_13v0: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_14ai: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_151h: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_15lu: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_16l1: trace_fully_carried; carry=3/3; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_17x0: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_19b6: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_19x7: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1c4a: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1cdk: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_1chc: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1cmt: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1e9s: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1ffn: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1fzx: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_1gad: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1h0p: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1i05: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1ipn: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1j58: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1jgc: trace_fully_carried; carry=3/3; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp -> probe_no_visible_kipp
- dio_1knc: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1lg2: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1ll2: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1mym: trace_fully_carried; carry=2/2; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp -> probe_no_visible_kipp
- dio_1n5f: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
- dio_1nkk: trace_fully_carried; carry=1/1; first_kipp=-/probe_no_visible_kipp; path=probe_no_visible_kipp
