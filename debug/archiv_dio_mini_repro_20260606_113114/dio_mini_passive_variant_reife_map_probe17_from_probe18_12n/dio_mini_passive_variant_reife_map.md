# Mini-DIO Passive Variant Reife Map

- time_summary_source: `debug\dio_mini_passive_episode_time_map_variant_probe17_from_probe18\dio_mini_passive_episode_time_map_summary.csv`
- transfer_source: `debug\dio_mini_passive_transfer_reife_probe18_to_probe17_12n\dio_mini_passive_transfer_reife.csv`

## Summary
- variant_local_wait_context: count=6 reward=0.000000 episodes=14 avg_transfer_similarity=0.000000 families=dio_0120:WAIT,dio_040y:WAIT,dio_10dk:WAIT,dio_14xc:WAIT,dio_1d1z:WAIT,dio_1f9y:WAIT
- variant_related_observation_trace: count=5 reward=0.000000 episodes=10 avg_transfer_similarity=0.942309 families=dio_13u8:WAIT,dio_143d:WAIT,dio_1c6b:WAIT,dio_1d3r:WAIT,dio_1m4n:WAIT
- variant_self_burden_action_trace: count=2 reward=-2.000000 episodes=2 avg_transfer_similarity=0.782854 families=dio_1d3r:LONG,dio_1mym:LONG
- variant_self_carried_action_trace: count=2 reward=4.000000 episodes=4 avg_transfer_similarity=0.000000 families=dio_0n9e:LONG,dio_1k7y:LONG

## Detail
- dio_0120:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_0120:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_040y:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:1; related=-; similarity=0.000000
  dio_040y:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_10dk:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_10dk:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_14xc:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:1; related=-; similarity=0.000000
  dio_14xc:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_1d1z:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_1d1z:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_1f9y:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_1f9y:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_13u8:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:1; related=dio_02qu; similarity=0.975290
  dio_13u8:WAIT: Die Variante ist verwandt mit dio_02qu (similarity=0.975290), bleibt aber Beobachtung.
- dio_143d:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:2; related=dio_14xc; similarity=0.982861
  dio_143d:WAIT: Die Variante ist verwandt mit dio_14xc (similarity=0.982861), bleibt aber Beobachtung.
- dio_1c6b:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:3; related=dio_1txv; similarity=0.993744
  dio_1c6b:WAIT: Die Variante ist verwandt mit dio_1txv (similarity=0.993744), bleibt aber Beobachtung.
- dio_1d3r:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:2; related=dio_0arw; similarity=0.782854
  dio_1d3r:WAIT: Die Variante ist verwandt mit dio_0arw (similarity=0.782854), bleibt aber Beobachtung.
- dio_1m4n:WAIT: variant_related_observation_trace
  reward=0.000000; outcomes=NO_TRADE:2; related=dio_1vpi; similarity=0.976795
  dio_1m4n:WAIT: Die Variante ist verwandt mit dio_1vpi (similarity=0.976795), bleibt aber Beobachtung.
- dio_1d3r:LONG: variant_self_burden_action_trace
  reward=-1.000000; outcomes=SL:1; related=dio_0arw; similarity=0.782854
  dio_1d3r:LONG: Die Variante belastet diese Handlung aus eigener Konsequenz; reward=-1.000000.
- dio_1mym:LONG: variant_self_burden_action_trace
  reward=-1.000000; outcomes=SL:1; related=-; similarity=0.000000
  dio_1mym:LONG: Die Variante belastet diese Handlung aus eigener Konsequenz; reward=-1.000000.
- dio_0n9e:LONG: variant_self_carried_action_trace
  reward=2.000000; outcomes=TP:2; related=-; similarity=0.000000
  dio_0n9e:LONG: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=2.000000.
- dio_1k7y:LONG: variant_self_carried_action_trace
  reward=2.000000; outcomes=TP:2; related=-; similarity=0.000000
  dio_1k7y:LONG: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=2.000000.

## Grenze
- passive Variantenreife
- lokale Konsequenz und Transfernaehe bleiben getrennt
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
