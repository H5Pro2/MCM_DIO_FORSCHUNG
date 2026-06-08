# DIO Mini Passive Inner State Timeline

## same_inner_state
- count: 4
- reward_sum: 5.539416
- best_reward_sum: 5.539416
- avg_reward: 1.384854
- actions: LONG
- families: dio_0arw

## inner_unfinished_to_inner_carried
- count: 4
- reward_sum: 4.146636
- best_reward_sum: 4.146636
- avg_reward: 1.036659
- actions: LONG
- families: dio_0t0v

## timeline_start
- count: 4
- reward_sum: 3.577568
- best_reward_sum: 3.577568
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

## inner_carried_to_inner_open_observation
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.378060
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

## inner_cautious_to_inner_unfinished
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 2.516584
- avg_reward: 0.000000
- actions: WAIT
- families: dio_00qb

## inner_open_observation_to_inner_cautious
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 0.569932
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1vpi

# Timeline

## run 149 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 149 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 149 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 149 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand observed_potential_contact.

## run 149 tick 13 dio_00qb
- transition: inner_cautious_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: inner_unfinished; Kontaktzustand observed_potential_contact.

## run 149 tick 14 dio_0t0v
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.036659 / 1.036659
- sentence: dio_0t0v: innen getragen, realer Kontakt LONG, reward=1.036659.

## run 150 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 150 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 150 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 150 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand observed_potential_contact.

## run 150 tick 13 dio_00qb
- transition: inner_cautious_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: held_active_impulse / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: inner_unfinished; Kontaktzustand held_active_impulse.

## run 150 tick 14 dio_0t0v
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.036659 / 1.036659
- sentence: dio_0t0v: innen getragen, realer Kontakt LONG, reward=1.036659.

## run 151 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 151 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 151 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 151 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand observed_potential_contact.

## run 151 tick 13 dio_00qb
- transition: inner_cautious_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: held_active_impulse / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: inner_unfinished; Kontaktzustand held_active_impulse.

## run 151 tick 14 dio_0t0v
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.036659 / 1.036659
- sentence: dio_0t0v: innen getragen, realer Kontakt LONG, reward=1.036659.

## run 152 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 152 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 152 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 152 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_cautious
- inner_state: inner_cautious
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: innen vorsichtig; Kontaktzustand observed_potential_contact.

## run 152 tick 13 dio_00qb
- transition: inner_cautious_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: held_active_impulse / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: inner_unfinished; Kontaktzustand held_active_impulse.

## run 152 tick 14 dio_0t0v
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.036659 / 1.036659
- sentence: dio_0t0v: innen getragen, realer Kontakt LONG, reward=1.036659.

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel