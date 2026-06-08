# Mini-DIO passive offene Reife-Kandidaten

Quelle:

- `debug\dio_mini_passive_time_maturity_join_basis_followup1_followup2_followup3_12n\dio_mini_passive_time_maturity_join.csv`

Grenze:

- Diagnose nur passiv.
- Kein Trainingsmemory.
- Keine Handlung.
- Kein Gate.
- Keine Motorik.

Zusammenfassung:

- open_inner_reife_candidate: count=4 reward=45.0 inner=0
- already_inner_bridged_reference: count=2 reward=24.0 inner=2
- fresh_waiting_context: count=25 reward=0.0 inner=0
- older_open_trace_watch: count=3 reward=0.0 inner=0
- burden_reife_watch: count=2 reward=-7.0 inner=0

Offene Reife-Kandidaten:

- `dio_0arw:LONG` reward=12.0 sources=basis,followup1,followup2,followup3 episodes=12
  dio_0arw:LONG: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=basis,followup1,followup2,followup3; outcomes=TP:12; reward=12.000000.
- `dio_1txv:SHORT` reward=12.0 sources=basis,followup1,followup2,followup3 episodes=12
  dio_1txv:SHORT: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=basis,followup1,followup2,followup3; outcomes=TP:12; reward=12.000000.
- `dio_1vpi:SHORT` reward=12.0 sources=basis,followup1,followup2,followup3 episodes=12
  dio_1vpi:SHORT: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=basis,followup1,followup2,followup3; outcomes=TP:12; reward=12.000000.
- `dio_0u1i:SHORT` reward=9.0 sources=followup1,followup2,followup3 episodes=9
  dio_0u1i:SHORT: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=followup1,followup2,followup3; outcomes=TP:9; reward=9.000000.

Referenzen mit innerer Bruecke:

- `dio_02qu:LONG` via `dio_14xc:LONG` inner=passive_inner_memory_stable reward=12.0
- `dio_1g18:SHORT` via `dio_173s:SHORT` inner=passive_inner_memory_reorganizing reward=12.0

Belastete Beobachtungsspuren:

- `dio_1k0r:LONG` reward=-4.0 sources=basis,followup1
- `dio_0x52:SHORT` reward=-3.0 sources=basis

Fachliche Lesung:

Die offenen Kandidaten sind reale, wiederkehrend getragene Spuren.
Sie werden nicht automatisch zu Handlung oder Reife.
Sie markieren nur, wo Mini-DIO in Folgelaeufen beobachten sollte, ob innere Reife entsteht.
