# Mini-DIO Passive Variant Reflection

- source_stability: `debug\dio_mini_passive_variant_stability_probe17_probe14_probe16_from_probe18_12n\dio_mini_passive_variant_stability.json`

## Summary
- burden_is_warning_not_gate: count=1 reward=-1.000000 episodes=1 actions=- variants=probe14_f2,probe16_f2,probe17_f3
- direction_can_be_locally_carried: count=2 reward=12.000000 episodes=12 actions=LONG,SHORT variants=probe14_f2,probe17_f3
- stable_variant_map_with_burden_trace: count=1 reward=12.000000 episodes=34 actions=LONG,SHORT variants=probe14_f2,probe16_f2,probe17_f3
- transfer_is_not_action: count=1 reward=0.000000 episodes=9 actions=- variants=probe14_f2,probe16_f2,probe17_f3

## Detail
- burden_remains_warning_trace: burden_is_warning_not_gate
  DIO-Syntax: `variant_reflection|burden|warning_trace|count=1|reward=-1.000000`
  Lesung: Belastung wird als passive Warnspur lesbar. Sie beschreibt Konsequenz und Reorganisation, keine harte Sperre.
- direction_long_locally_carried: direction_can_be_locally_carried
  DIO-Syntax: `variant_reflection|LONG|locally_carried|variants=probe17_f3|episodes=6|reward=6.000000`
  Lesung: LONG kann in einer passenden Variante lokal getragen sein. Das ist Variantenreife, keine allgemeine Regel.
- direction_short_locally_carried: direction_can_be_locally_carried
  DIO-Syntax: `variant_reflection|SHORT|locally_carried|variants=probe14_f2|episodes=6|reward=6.000000`
  Lesung: SHORT kann in einer passenden Variante lokal getragen sein. Das ist Variantenreife, keine allgemeine Regel.
- stable_variant_map: stable_variant_map_with_burden_trace
  DIO-Syntax: `variant_reflection|stability|same_state=34|burden=1`
  Lesung: Die geprueften Varianten blieben in den Folgelaeufen gleich eingeordnet. Eine Belastungsspur ist sichtbar und bleibt Warnspur, nicht Sperre.
- kinship_remains_observation: transfer_is_not_action
  DIO-Syntax: `variant_reflection|transfer|observation_only|related_traces=9`
  Lesung: Verwandtschaft zu einer alten Reifespur bleibt Wahrnehmung. Sie wird nicht automatisch Handlung.

## Grenze
- passive Reflexion
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
- Mini-DIO liest diesen Bericht nicht aktiv
