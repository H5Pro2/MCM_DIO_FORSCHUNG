# Mini-DIO Passive Reorganization Follow-up

- awareness: `debug\dio_mini_passive_conflict_stability_inner_awareness_probe16_probe7_from_probe18_12n`

## Summary
- reorganization_family_not_seen: count=2 families=dio_19i4,dio_1k0r sources=probe16_f3,probe7_f3 wait=0 action=0
- reorganization_quiet_wait_continues: count=2 families=dio_19i4,dio_1k0r sources=probe16_f3,probe7_f3 wait=2 action=0

## Detail
- probe16_f3 dio_19i4:SHORT -> reorganization_family_not_seen (action=0, wait=0)
  DIO-Syntax: `reorganization_followup|dio_19i4|SHORT|reorganization_family_not_seen|source=probe16_f3|action=0|wait=0`
- probe16_f3 dio_1k0r:LONG -> reorganization_quiet_wait_continues (action=0, wait=1)
  DIO-Syntax: `reorganization_followup|dio_1k0r|LONG|reorganization_quiet_wait_continues|source=probe16_f3|action=0|wait=1`
- probe7_f3 dio_19i4:SHORT -> reorganization_quiet_wait_continues (action=0, wait=1)
  DIO-Syntax: `reorganization_followup|dio_19i4|SHORT|reorganization_quiet_wait_continues|source=probe7_f3|action=0|wait=1`
- probe7_f3 dio_1k0r:LONG -> reorganization_family_not_seen (action=0, wait=0)
  DIO-Syntax: `reorganization_followup|dio_1k0r|LONG|reorganization_family_not_seen|source=probe7_f3|action=0|wait=0`

## Grenze
- passiver Follow-up-Leser
- keine Handlung
- kein Gate
- keine Motorik
- kein Trainingsmemory
- Mini-DIO liest diesen Bericht nicht aktiv
