# DIO Mini Passive Inner State Timeline

## same_inner_state
- count: 2
- reward_sum: 1.384854
- best_reward_sum: 2.014000
- avg_reward: 0.692427
- actions: LONG,WAIT
- families: dio_00qb,dio_0arw

## inner_unfinished_to_inner_carried
- count: 1
- reward_sum: 1.036659
- best_reward_sum: 1.036659
- avg_reward: 1.036659
- actions: LONG
- families: dio_0t0v

## timeline_start
- count: 1
- reward_sum: 0.894392
- best_reward_sum: 0.894392
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

## inner_carried_to_inner_open_observation
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.094515
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

## inner_open_observation_to_inner_unfinished
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.142483
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1vpi

# Timeline

## run 155 tick 1 dio_1u7v
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.894392 / 0.894392
- sentence: dio_1u7v: innen getragen, realer Kontakt SHORT, reward=0.894392.

## run 155 tick 6 dio_0arw
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.384854 / 1.384854
- sentence: dio_0arw: innen getragen, realer Kontakt LONG, reward=1.384854.

## run 155 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094515
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 155 tick 12 dio_1vpi
- transition: inner_open_observation_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: held_active_impulse / WAIT
- reward/best: 0.000000 / 0.142483
- sentence: dio_1vpi: inner_unfinished; Kontaktzustand held_active_impulse.

## run 155 tick 13 dio_00qb
- transition: same_inner_state
- inner_state: inner_unfinished
- contact/action: held_active_impulse / WAIT
- reward/best: 0.000000 / 0.629146
- sentence: dio_00qb: inner_unfinished; Kontaktzustand held_active_impulse.

## run 155 tick 14 dio_0t0v
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