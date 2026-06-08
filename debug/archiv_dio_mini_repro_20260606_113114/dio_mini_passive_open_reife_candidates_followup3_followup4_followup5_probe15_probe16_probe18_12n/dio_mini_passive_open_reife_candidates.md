# Mini-DIO passive offene Reife-Kandidaten

Quelle:

- `debug\dio_mini_passive_time_maturity_join_followup3_followup4_followup5_probe15_probe16_probe18_12n\dio_mini_passive_time_maturity_join.csv`

Grenze:

- Diagnose nur passiv.
- Kein Trainingsmemory.
- Keine Handlung.
- Kein Gate.
- Keine Motorik.

Zusammenfassung:

- open_inner_reife_candidate: count=3 reward=27.0 inner=0
- already_inner_bridged_reference: count=1 reward=9.0 inner=1
- older_open_trace_watch: count=25 reward=9.0 inner=0
- fresh_waiting_context: count=1 reward=0.0 inner=0

Offene Reife-Kandidaten:

- `dio_0arw:LONG` reward=9.0 sources=basis_probe18,followup4_probe18,followup5_probe18 episodes=9
  dio_0arw:LONG: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=basis_probe18,followup4_probe18,followup5_probe18; outcomes=TP:9; reward=9.000000.
- `dio_1txv:SHORT` reward=9.0 sources=basis_probe18,followup4_probe18,followup5_probe18 episodes=9
  dio_1txv:SHORT: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=basis_probe18,followup4_probe18,followup5_probe18; outcomes=TP:9; reward=9.000000.
- `dio_1vpi:SHORT` reward=9.0 sources=basis_probe18,followup4_probe18,followup5_probe18 episodes=9
  dio_1vpi:SHORT: reale frische Tragspur ohne innere Reife. Weiter passiv beobachten; Quellen=basis_probe18,followup4_probe18,followup5_probe18; outcomes=TP:9; reward=9.000000.

Referenzen mit innerer Bruecke:

- `dio_02qu:LONG` via `dio_14xc:LONG` inner=passive_inner_memory_stable reward=9.0

Belastete Beobachtungsspuren:


Fachliche Lesung:

Die offenen Kandidaten sind reale, wiederkehrend getragene Spuren.
Sie werden nicht automatisch zu Handlung oder Reife.
Sie markieren nur, wo Mini-DIO in Folgelaeufen beobachten sollte, ob innere Reife entsteht.
