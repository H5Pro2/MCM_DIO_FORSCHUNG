# DIO Mini Passive Inner State Timeline

## same_inner_state
- count: 19
- reward_sum: 3.840505
- best_reward_sum: 11.757007
- avg_reward: 0.202132
- actions: LONG,WAIT
- families: dio_00qb,dio_0120,dio_0arw,dio_0bmh,dio_0ems,dio_0fiy,dio_0igh,dio_1g2t,dio_1qwp

## timeline_start
- count: 4
- reward_sum: 0.894392
- best_reward_sum: 3.577568
- avg_reward: 0.223598
- actions: SHORT,WAIT
- families: dio_1u7v

## inner_carried_to_inner_open_observation
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.094515
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

## inner_carried_to_inner_unknown
- count: 5
- reward_sum: 0.000000
- best_reward_sum: 3.704528
- avg_reward: 0.000000
- actions: WAIT
- families: dio_0x1o,dio_16yc

## inner_cautious_to_inner_unknown
- count: 3
- reward_sum: 0.000000
- best_reward_sum: 1.102320
- avg_reward: 0.000000
- actions: WAIT
- families: dio_02qu

## inner_unknown_to_inner_open_observation
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 0.189030
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

## inner_open_observation_to_inner_cautious
- count: 3
- reward_sum: -1.027449
- best_reward_sum: 0.427449
- avg_reward: -0.342483
- actions: SHORT
- families: dio_1vpi

## inner_unknown_to_inner_carried
- count: 3
- reward_sum: -1.236659
- best_reward_sum: 3.806367
- avg_reward: -0.412220
- actions: SHORT,WAIT
- families: dio_0arw,dio_0t0v

# Timeline

## run 141 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.894392
- sentence: dio_1u7v: innen getragen, aber in dieser Episode nicht gehandelt.

## run 141 tick 2 dio_16yc
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.325504
- sentence: dio_16yc: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 3 dio_1g2t
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.146451
- sentence: dio_1g2t: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 4 dio_0fiy
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.757407
- sentence: dio_0fiy: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 5 dio_0ems
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.304587
- sentence: dio_0ems: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 6 dio_0arw
- transition: inner_unknown_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.384854
- sentence: dio_0arw: innen getragen, aber in dieser Episode nicht gehandelt.

## run 141 tick 7 dio_0x1o
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.364008
- sentence: dio_0x1o: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 8 dio_0bmh
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.817371
- sentence: dio_0bmh: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 9 dio_0igh
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.324337
- sentence: dio_0igh: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 10 dio_1qwp
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.078757
- sentence: dio_1qwp: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 11 dio_14xc
- transition: inner_unknown_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 141 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: executed_negative_contact / SHORT
- reward/best: -0.342483 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand executed_negative_contact.

## run 141 tick 17 dio_02qu
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.367440
- sentence: dio_02qu: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 141 tick 18 dio_0120
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.333693
- sentence: dio_0120: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.894392
- sentence: dio_1u7v: innen getragen, aber in dieser Episode nicht gehandelt.

## run 142 tick 2 dio_16yc
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.325504
- sentence: dio_16yc: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 3 dio_1g2t
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.146451
- sentence: dio_1g2t: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 4 dio_0fiy
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.757407
- sentence: dio_0fiy: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 5 dio_0ems
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.304587
- sentence: dio_0ems: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 6 dio_0arw
- transition: inner_unknown_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.384854
- sentence: dio_0arw: innen getragen, aber in dieser Episode nicht gehandelt.

## run 142 tick 7 dio_0x1o
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.364008
- sentence: dio_0x1o: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 8 dio_0bmh
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 0.817371 / 0.817371
- sentence: dio_0bmh: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## run 142 tick 13 dio_00qb
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 142 tick 14 dio_0t0v
- transition: inner_unknown_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_negative_contact / SHORT
- reward/best: -1.236659 / 1.036659
- sentence: dio_0t0v: innen getragen, realer Kontakt SHORT, reward=-1.236659.

## run 143 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.894392
- sentence: dio_1u7v: innen getragen, aber in dieser Episode nicht gehandelt.

## run 143 tick 2 dio_16yc
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.325504
- sentence: dio_16yc: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 143 tick 3 dio_1g2t
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.146451
- sentence: dio_1g2t: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 143 tick 4 dio_0fiy
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.757407
- sentence: dio_0fiy: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 143 tick 5 dio_0ems
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 1.304587 / 1.304587
- sentence: dio_0ems: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## run 143 tick 10 dio_1qwp
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.078757
- sentence: dio_1qwp: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 143 tick 11 dio_14xc
- transition: inner_unknown_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 143 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: executed_negative_contact / SHORT
- reward/best: -0.342483 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand executed_negative_contact.

## run 143 tick 17 dio_02qu
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.367440
- sentence: dio_02qu: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 143 tick 18 dio_0120
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.333693
- sentence: dio_0120: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 144 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 144 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 144 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 144 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: executed_negative_contact / SHORT
- reward/best: -0.342483 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand executed_negative_contact.

## run 144 tick 17 dio_02qu
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.367440
- sentence: dio_02qu: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 144 tick 18 dio_0120
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 0.333693 / 0.333693
- sentence: dio_0120: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel