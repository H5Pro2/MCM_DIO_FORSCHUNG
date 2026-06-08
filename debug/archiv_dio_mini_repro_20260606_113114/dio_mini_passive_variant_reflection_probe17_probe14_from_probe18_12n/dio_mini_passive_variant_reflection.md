# Mini-DIO Passive Variant Reflection

- source_stability: `debug\dio_mini_passive_variant_stability_probe17_probe14_from_probe18_12n\dio_mini_passive_variant_stability.json`

## Summary
- direction_can_be_locally_carried: count=2 reward=12.000000 episodes=12 actions=LONG,SHORT variants=probe14_f2,probe17_f3
- stable_variant_map_without_burden: count=1 reward=12.000000 episodes=20 actions=LONG,SHORT variants=probe14_f2,probe17_f3
- transfer_is_not_action: count=1 reward=0.000000 episodes=6 actions=- variants=probe14_f2,probe17_f3

## Detail
- direction_long_locally_carried: direction_can_be_locally_carried
  DIO-Syntax: `variant_reflection|LONG|locally_carried|variants=probe17_f3|episodes=6|reward=6.000000`
  Lesung: LONG kann in einer passenden Variante lokal getragen sein. Das ist Variantenreife, keine allgemeine Regel.
- direction_short_locally_carried: direction_can_be_locally_carried
  DIO-Syntax: `variant_reflection|SHORT|locally_carried|variants=probe14_f2|episodes=6|reward=6.000000`
  Lesung: SHORT kann in einer passenden Variante lokal getragen sein. Das ist Variantenreife, keine allgemeine Regel.
- stable_without_burden: stable_variant_map_without_burden
  DIO-Syntax: `variant_reflection|stability|same_state=20|burden=0`
  Lesung: Die geprüften Varianten blieben in den Folgeläufen gleich eingeordnet. Belastete stabile Handlungen wurden nicht sichtbar.
- kinship_remains_observation: transfer_is_not_action
  DIO-Syntax: `variant_reflection|transfer|observation_only|related_traces=6`
  Lesung: Verwandtschaft zu einer alten Reifespur bleibt Wahrnehmung. Sie wird nicht automatisch Handlung.

## Grenze
- passive Reflexion
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
- Mini-DIO liest diesen Bericht nicht aktiv
