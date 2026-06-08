# DIO Mini Passive Reflection Candidate Timeline

## dio_1vpi
- kind: reflection_candidate_cautious_trace
- worlds: probe18_first,probe18_repeat1,probe18_repeat2
- hits: 11
- reward_sum: -1.712415
- best_reward_sum: 1.567313
- inner_state_path: inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious
- contact_state_path: executed_negative_contact -> executed_negative_contact -> executed_negative_contact -> executed_negative_contact -> executed_negative_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact
- question: dio_1vpi: Warum bleibt diese Spur nach Konflikt eher Beobachtung als getragener Kontakt?
- note: dio_1vpi: Vorsichtige Kandidatenspur im Innenverlauf; inner=inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious -> inner_cautious; contact=executed_negative_contact -> executed_negative_contact -> executed_negative_contact -> executed_negative_contact -> executed_negative_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact -> observed_potential_contact; reward=-1.712415; best=1.567313.

## dio_0t0v
- kind: reflection_candidate_reorganized_trace
- worlds: probe18_first,probe18_repeat1,probe18_repeat2
- hits: 7
- reward_sum: 2.909977
- best_reward_sum: 7.256613
- inner_state_path: inner_carried -> inner_carried -> inner_carried -> inner_carried -> inner_carried -> inner_carried -> inner_carried
- contact_state_path: executed_negative_contact -> observed_potential_contact -> observed_potential_contact -> executed_positive_contact -> executed_positive_contact -> executed_positive_contact -> executed_positive_contact
- question: dio_0t0v: Was hat sich zwischen Konflikt und spaeterem Tragen geaendert?
- note: dio_0t0v: Reorganisierte Kandidatenspur im Innenverlauf; inner=inner_carried -> inner_carried -> inner_carried -> inner_carried -> inner_carried -> inner_carried -> inner_carried; contact=executed_negative_contact -> observed_potential_contact -> observed_potential_contact -> executed_positive_contact -> executed_positive_contact -> executed_positive_contact -> executed_positive_contact; reward=2.909977; best=7.256613.

## Grenze
- passiver Kandidaten-Zeitverlauf
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel