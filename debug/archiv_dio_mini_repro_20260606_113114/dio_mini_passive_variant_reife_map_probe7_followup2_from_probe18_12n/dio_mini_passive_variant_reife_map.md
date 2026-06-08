# Mini-DIO Passive Variant Reife Map

- time_summary_source: `debug\dio_mini_passive_episode_time_map_variant_probe7_followup2_from_probe18\dio_mini_passive_episode_time_map_summary.csv`
- transfer_source: `debug\dio_mini_passive_transfer_reife_probe18_to_probe7_followup2_12n\dio_mini_passive_transfer_reife.csv`

## Summary
- variant_local_wait_context: count=3 reward=0.000000 episodes=9 avg_transfer_similarity=0.000000 families=dio_0lyu:WAIT,dio_19i4:WAIT,dio_19p6:WAIT
- variant_self_carried_action_trace: count=3 reward=9.000000 episodes=9 avg_transfer_similarity=0.912391 families=dio_0qrm:SHORT,dio_0u8f:LONG,dio_0x52:SHORT

## Detail
- dio_0lyu:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_0lyu:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_19i4:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_19i4:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_19p6:WAIT: variant_local_wait_context
  reward=0.000000; outcomes=NO_TRADE:3; related=-; similarity=0.000000
  dio_19p6:WAIT: Die Variante bleibt lokaler Wartungs-/Beobachtungskontext.
- dio_0qrm:SHORT: variant_self_carried_action_trace
  reward=3.000000; outcomes=TP:3; related=-; similarity=0.000000
  dio_0qrm:SHORT: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=3.000000.
- dio_0u8f:LONG: variant_self_carried_action_trace
  reward=3.000000; outcomes=TP:3; related=dio_0arw; similarity=0.870421
  dio_0u8f:LONG: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=3.000000.
- dio_0x52:SHORT: variant_self_carried_action_trace
  reward=3.000000; outcomes=TP:3; related=dio_1txv; similarity=0.954361
  dio_0x52:SHORT: Die Variante traegt diese Handlung aus eigener Konsequenz; reward=3.000000.

## Grenze
- passive Variantenreife
- lokale Konsequenz und Transfernaehe bleiben getrennt
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
