# Mini-DIO Passive Conflict Reflection

- compare_source: `debug\dio_mini_passive_variant_reife_map_compare_probe16_f1_to_f2_from_probe18_12n\dio_mini_passive_variant_reife_map_compare.csv`
- after_map_source: `debug\dio_mini_passive_variant_reife_map_probe16_followup2_from_probe18_12n\dio_mini_passive_variant_reife_map.csv`

## Summary
- burden_reorganized_into_observation: count=1 reward_delta=2.000000 episode_delta=-2 families=dio_1k0r

## Detail
- dio_1k0r:LONG: burden_reorganized_into_observation
  DIO-Syntax: `conflict_reflection|dio_1k0r|LONG|burden_reorganized_into_observation|reward_delta=2.000000|wait_traces=1`
  Lesung: dio_1k0r:LONG war belastet und wird im Folgelauf schwaecher (-3.000000->-1.000000, Episoden 3->1). Dieselbe Familie taucht zusaetzlich als Beobachtung auf. Das ist Reorganisation, keine Sperre.

## Grenze
- passive Konfliktreflexion
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
- Mini-DIO liest diesen Bericht nicht aktiv
