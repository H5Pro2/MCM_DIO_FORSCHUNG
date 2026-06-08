# DIO Mini Passive Inner State Timeline

## same_inner_state
- count: 24
- reward_sum: 1.453000
- best_reward_sum: 11.996942
- avg_reward: 0.060542
- actions: LONG,WAIT
- families: dio_0akd,dio_0ofo,dio_10dk,dio_13u8,dio_14xc,dio_1d3r,dio_1f9y,dio_1mym

## inner_open_observation_to_inner_carried
- count: 8
- reward_sum: 1.389869
- best_reward_sum: 6.742395
- avg_reward: 0.173734
- actions: LONG,WAIT
- families: dio_0120,dio_0bmh,dio_0n9e

## inner_unfinished_to_inner_carried
- count: 4
- reward_sum: 1.086760
- best_reward_sum: 4.347040
- avg_reward: 0.271690
- actions: LONG,WAIT
- families: dio_04z7

## timeline_start
- count: 4
- reward_sum: 0.911881
- best_reward_sum: 3.647524
- avg_reward: 0.227970
- actions: SHORT,WAIT
- families: dio_1bwb

## inner_carried_to_inner_open_observation
- count: 12
- reward_sum: 0.000000
- best_reward_sum: 5.573733
- avg_reward: 0.000000
- actions: WAIT
- families: dio_040y,dio_0fzl,dio_0ps1,dio_14xc,dio_1d1z,dio_1f9y

## inner_open_observation_to_inner_unfinished
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 2.780168
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1k7y

# Timeline

## run 133 tick 1 dio_1bwb
- transition: timeline_start
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.911881
- sentence: dio_1bwb: innen getragen, aber in dieser Episode nicht gehandelt.

## run 133 tick 2 dio_1d1z
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.309621
- sentence: dio_1d1z: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 3 dio_10dk
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.196209
- sentence: dio_10dk: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 4 dio_1d3r
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.841340
- sentence: dio_1d3r: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 5 dio_0n9e
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.389869
- sentence: dio_0n9e: innen getragen, aber in dieser Episode nicht gehandelt.

## run 133 tick 6 dio_0ofo
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.453000
- sentence: dio_0ofo: innen getragen, aber in dieser Episode nicht gehandelt.

## run 133 tick 7 dio_0ps1
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.381921
- sentence: dio_0ps1: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 8 dio_0bmh
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.785478
- sentence: dio_0bmh: innen getragen, aber in dieser Episode nicht gehandelt.

## run 133 tick 9 dio_040y
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.275596
- sentence: dio_040y: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 10 dio_1f9y
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.078897
- sentence: dio_1f9y: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 11 dio_14xc
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094628
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 12 dio_1mym
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.175028
- sentence: dio_1mym: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 13 dio_1k7y
- transition: inner_open_observation_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.695042
- sentence: dio_1k7y: inner_unfinished; Kontaktzustand observed_potential_contact.

## run 133 tick 14 dio_04z7
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.086760
- sentence: dio_04z7: innen getragen, aber in dieser Episode nicht gehandelt.

## run 133 tick 15 dio_0akd
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.776339
- sentence: dio_0akd: innen getragen, aber in dieser Episode nicht gehandelt.

## run 133 tick 16 dio_0fzl
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.385437
- sentence: dio_0fzl: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 17 dio_13u8
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.351496
- sentence: dio_13u8: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 133 tick 18 dio_0120
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.333944
- sentence: dio_0120: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 1 dio_1bwb
- transition: timeline_start
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.911881
- sentence: dio_1bwb: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 2 dio_1d1z
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.309621
- sentence: dio_1d1z: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 3 dio_10dk
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.196209
- sentence: dio_10dk: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 4 dio_1d3r
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.841340
- sentence: dio_1d3r: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 5 dio_0n9e
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.389869
- sentence: dio_0n9e: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 6 dio_0ofo
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.453000
- sentence: dio_0ofo: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 7 dio_0ps1
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.381921
- sentence: dio_0ps1: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 8 dio_0bmh
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.785478
- sentence: dio_0bmh: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 9 dio_040y
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.275596
- sentence: dio_040y: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 10 dio_1f9y
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.078897
- sentence: dio_1f9y: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 11 dio_14xc
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094628
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 12 dio_1mym
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.175028
- sentence: dio_1mym: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 13 dio_1k7y
- transition: inner_open_observation_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.695042
- sentence: dio_1k7y: inner_unfinished; Kontaktzustand observed_potential_contact.

## run 134 tick 14 dio_04z7
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.086760
- sentence: dio_04z7: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 15 dio_0akd
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.776339
- sentence: dio_0akd: innen getragen, aber in dieser Episode nicht gehandelt.

## run 134 tick 16 dio_0fzl
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.385437
- sentence: dio_0fzl: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 17 dio_13u8
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.351496
- sentence: dio_13u8: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 134 tick 18 dio_0120
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.333944
- sentence: dio_0120: innen getragen, aber in dieser Episode nicht gehandelt.

## run 135 tick 1 dio_1bwb
- transition: timeline_start
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.911881
- sentence: dio_1bwb: innen getragen, aber in dieser Episode nicht gehandelt.

## run 135 tick 2 dio_1d1z
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.309621
- sentence: dio_1d1z: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 3 dio_10dk
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.196209
- sentence: dio_10dk: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 4 dio_1d3r
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.841340
- sentence: dio_1d3r: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 5 dio_0n9e
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.389869 / 1.389869
- sentence: dio_0n9e: innen getragen, realer Kontakt LONG, reward=1.389869.

## run 135 tick 10 dio_1f9y
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.078897
- sentence: dio_1f9y: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 11 dio_14xc
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094628
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 12 dio_1mym
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.175028
- sentence: dio_1mym: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 13 dio_1k7y
- transition: inner_open_observation_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.695042
- sentence: dio_1k7y: inner_unfinished; Kontaktzustand observed_potential_contact.

## run 135 tick 14 dio_04z7
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 1.086760
- sentence: dio_04z7: innen getragen, aber in dieser Episode nicht gehandelt.

## run 135 tick 15 dio_0akd
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.776339
- sentence: dio_0akd: innen getragen, aber in dieser Episode nicht gehandelt.

## run 135 tick 16 dio_0fzl
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.385437
- sentence: dio_0fzl: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 17 dio_13u8
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.351496
- sentence: dio_13u8: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 135 tick 18 dio_0120
- transition: inner_open_observation_to_inner_carried
- inner_state: inner_carried
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.333944
- sentence: dio_0120: innen getragen, aber in dieser Episode nicht gehandelt.

## run 136 tick 1 dio_1bwb
- transition: timeline_start
- inner_state: inner_carried
- contact/action: executed_positive_contact / SHORT
- reward/best: 0.911881 / 0.911881
- sentence: dio_1bwb: innen getragen, realer Kontakt SHORT, reward=0.911881.

## run 136 tick 6 dio_0ofo
- transition: same_inner_state
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.453000 / 1.453000
- sentence: dio_0ofo: innen getragen, realer Kontakt LONG, reward=1.453000.

## run 136 tick 11 dio_14xc
- transition: inner_carried_to_inner_open_observation
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.094628
- sentence: dio_14xc: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 136 tick 12 dio_1mym
- transition: same_inner_state
- inner_state: inner_open_observation
- contact/action: observed_potential_contact / WAIT
- reward/best: 0.000000 / 0.175028
- sentence: dio_1mym: innen offen beobachtet; Kontaktzustand observed_potential_contact.

## run 136 tick 13 dio_1k7y
- transition: inner_open_observation_to_inner_unfinished
- inner_state: inner_unfinished
- contact/action: held_active_impulse / WAIT
- reward/best: 0.000000 / 0.695042
- sentence: dio_1k7y: inner_unfinished; Kontaktzustand held_active_impulse.

## run 136 tick 14 dio_04z7
- transition: inner_unfinished_to_inner_carried
- inner_state: inner_carried
- contact/action: executed_positive_contact / LONG
- reward/best: 1.086760 / 1.086760
- sentence: dio_04z7: innen getragen, realer Kontakt LONG, reward=1.086760.

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel