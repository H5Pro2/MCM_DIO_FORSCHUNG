# DIO Mini Passive Inner Stability

## Stabilitaet

### stable_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 1.453000
- best_reward_sum: 1.453000
- avg_reward: 1.453000
- actions: LONG
- families: dio_0ofo

### stable_state / inner_carried / observed_potential
- count: 5
- reward_sum: 0.000000
- best_reward_sum: 5.235017
- avg_reward: 0.000000
- actions: WAIT
- families: dio_0akd,dio_0ofo

### stable_state / inner_open_observation / observed_potential
- count: 18
- reward_sum: 0.000000
- best_reward_sum: 5.308925
- avg_reward: 0.000000
- actions: WAIT
- families: dio_10dk,dio_13u8,dio_14xc,dio_1d3r,dio_1f9y,dio_1mym

### transition_state / inner_carried / positive_real_contact
- count: 2
- reward_sum: 2.476629
- best_reward_sum: 2.476629
- avg_reward: 1.238314
- actions: LONG
- families: dio_04z7,dio_0n9e

### start_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 0.911881
- best_reward_sum: 0.911881
- avg_reward: 0.911881
- actions: SHORT
- families: dio_1bwb

### start_state / inner_carried / observed_potential
- count: 3
- reward_sum: 0.000000
- best_reward_sum: 2.735643
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1bwb

### transition_state / inner_carried / observed_potential
- count: 10
- reward_sum: 0.000000
- best_reward_sum: 8.612806
- avg_reward: 0.000000
- actions: WAIT
- families: dio_0120,dio_04z7,dio_0bmh,dio_0n9e

### transition_state / inner_open_observation / observed_potential
- count: 12
- reward_sum: 0.000000
- best_reward_sum: 5.573733
- avg_reward: 0.000000
- actions: WAIT
- families: dio_040y,dio_0fzl,dio_0ps1,dio_14xc,dio_1d1z,dio_1f9y

### transition_state / inner_unfinished / observed_potential
- count: 4
- reward_sum: 0.000000
- best_reward_sum: 2.780168
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1k7y

## Uebergaenge

### same_inner_state
- stability_kind: stable_state
- count: 24
- reward_sum: 1.453000
- positive_contacts: 1
- observed_potentials: 23
- actions: LONG,WAIT
- families: dio_0akd,dio_0ofo,dio_10dk,dio_13u8,dio_14xc,dio_1d3r,dio_1f9y,dio_1mym

### inner_open_observation_to_inner_carried
- stability_kind: transition_state
- count: 8
- reward_sum: 1.389869
- positive_contacts: 1
- observed_potentials: 7
- actions: LONG,WAIT
- families: dio_0120,dio_0bmh,dio_0n9e

### inner_unfinished_to_inner_carried
- stability_kind: transition_state
- count: 4
- reward_sum: 1.086760
- positive_contacts: 1
- observed_potentials: 3
- actions: LONG,WAIT
- families: dio_04z7

### timeline_start
- stability_kind: start_state
- count: 4
- reward_sum: 0.911881
- positive_contacts: 1
- observed_potentials: 3
- actions: SHORT,WAIT
- families: dio_1bwb

### inner_carried_to_inner_open_observation
- stability_kind: transition_state
- count: 12
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 12
- actions: WAIT
- families: dio_040y,dio_0fzl,dio_0ps1,dio_14xc,dio_1d1z,dio_1f9y

### inner_open_observation_to_inner_unfinished
- stability_kind: transition_state
- count: 4
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 4
- actions: WAIT
- families: dio_1k7y

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel