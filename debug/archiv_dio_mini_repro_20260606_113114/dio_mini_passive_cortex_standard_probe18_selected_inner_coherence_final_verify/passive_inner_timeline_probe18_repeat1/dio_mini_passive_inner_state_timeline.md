# DIO Mini Passive Inner State Timeline

## same_inner_state
- count: 6
- reward_sum: 6.206802
- best_reward_sum: 6.206802
- avg_reward: 1.034467
- actions: LONG
- families: dio_0120,dio_0arw

## timeline_start
- count: 4
- reward_sum: 3.577568
- best_reward_sum: 3.577568
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

## inner_carried_to_inner_unknown
- count: 2
- reward_sum: 1.551314
- best_reward_sum: 1.551314
- avg_reward: 0.775657
- actions: LONG
- families: dio_0akd

## inner_carried_to_inner_open_observation
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.378060
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

## inner_cautious_to_inner_unknown
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 1.993172
- avg_reward: 0.000000
- actions: WAIT
- families: dio_00qb,dio_02qu

## inner_unknown_to_inner_carried
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 2.073318
- avg_reward: 0.000000
- actions: WAIT
- families: dio_0t0v

## inner_open_observation_to_inner_cautious
- count: 4
- reward_sum: -0.684966
- best_reward_sum: 0.569932
- avg_reward: -0.171241
- actions: SHORT,WAIT
- families: dio_1vpi

# Timeline

## run 145 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 145 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 145 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 145 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: executed_negative_contact / SHORT
- reward/best: -0.342483 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand executed_negative_contact.

## run 145 tick 17 dio_02qu
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.367440
- sentence: dio_02qu: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 145 tick 18 dio_0120
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 0.333693 / 0.333693
- sentence: dio_0120: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## run 146 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 146 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 146 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 146 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: executed_negative_contact / SHORT
- reward/best: -0.342483 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand executed_negative_contact.

## run 146 tick 17 dio_02qu
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.367440
- sentence: dio_02qu: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 146 tick 18 dio_0120
- transition: same_inner_state
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 0.333693 / 0.333693
- sentence: dio_0120: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## run 147 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 147 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 147 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 147 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand observed_potential_contact.

## run 147 tick 13 dio_00qb
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 147 tick 14 dio_0t0v
- transition: inner_unknown_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.036659
- sentence: dio_0t0v: innen getragen, aber in dieser Episode nicht gehandelt.

## run 147 tick 15 dio_0akd
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 0.775657 / 0.775657
- sentence: dio_0akd: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## run 148 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 148 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 148 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 148 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand observed_potential_contact.

## run 148 tick 13 dio_00qb
- transition: inner_cautious_to_inner_unknown
- inner_state: inner_unknown
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: keine passive Innenlage zugeordnet; Kontaktzustand observed_potential_contact.

## run 148 tick 14 dio_0t0v
- transition: inner_unknown_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.036659
- sentence: dio_0t0v: innen getragen, aber in dieser Episode nicht gehandelt.

## run 148 tick 15 dio_0akd
- transition: inner_carried_to_inner_unknown
- inner_state: inner_unknown
- contact/action: executed_positive_contact / LONG
- reward/best: 0.775657 / 0.775657
- sentence: dio_0akd: keine passive Innenlage zugeordnet; Kontaktzustand executed_positive_contact.

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel