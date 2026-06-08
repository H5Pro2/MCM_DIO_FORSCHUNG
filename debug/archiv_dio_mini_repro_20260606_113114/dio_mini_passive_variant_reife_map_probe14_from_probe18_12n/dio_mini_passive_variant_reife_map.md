# Mini-DIO Passive Variant Reife Map

- time_summary_source: `debug\dio_mini_passive_episode_time_map_variant_probe14_from_probe18\dio_mini_passive_episode_time_map_summary.csv`
- transfer_source: `debug\dio_mini_passive_transfer_reife_probe18_to_probe14_12n\dio_mini_passive_transfer_reife.csv`

## Summary
- variant_local_wait_context: count=6 reward=0.000000 episodes=18 avg_transfer_similarity=0.000000 families=dio_0989:WAIT,dio_0b66:WAIT,dio_0gmg:WAIT,dio_0qze:WAIT,dio_1guc:WAIT,dio_1t1w:WAIT
- variant_related_observation_trace: count=2 reward=0.000000 episodes=6 avg_transfer_similarity=0.933014 families=dio_173s:WAIT,dio_1rv1:WAIT
- variant_self_carried_action_trace: count=2 reward=6.000000 episodes=6 avg_transfer_similarity=0.966012 families=dio_0hd3:SHORT,dio_0szn:SHORT

## Detail
- dio_0989:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_0989:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_0b66:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_0b66:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_0gmg:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_0gmg:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_0qze:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_0qze:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_1guc:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_1guc:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_1t1w:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_1t1w:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_173s:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:3; related=dio_0arw; similarity=0.909548
  dio_173s:WAIT: Die Variante ist verwandt mit dio_0arw (similarity=0.909548), bleibt aber Beobachtung.
- dio_1rv1:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:3; related=dio_1txv; similarity=0.956480
  dio_1rv1:WAIT: Die Variante ist verwandt mit dio_1txv (similarity=0.956480), bleibt aber Beobachtung.
- dio_0hd3:SHORT: variant_self_carried_action_trace
  reward=3.000000; outcomes=TP:3; related=dio_14xc; similarity=0.966012
  dio_0hd3:SHORT: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=3.000000.
- dio_0szn:SHORT: variant_self_carried_action_trace
  reward=3.000000; outcomes=TP:3; related=-; similarity=0.000000
  dio_0szn:SHORT: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=3.000000.

## Grenze
- passive Variantenreife
- lokale Konsequenz und Transfernaehe bleiben getrennt
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
