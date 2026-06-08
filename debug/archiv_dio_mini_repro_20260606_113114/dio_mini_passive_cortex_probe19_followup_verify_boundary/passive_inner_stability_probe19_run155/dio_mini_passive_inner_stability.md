# DIO Mini Passive Inner Stability

## Stabilitaet

### stable_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 1.384854
- best_reward_sum: 1.384854
- avg_reward: 1.384854
- actions: LONG
- families: dio_0arw

### stable_state / inner_unfinished / observed_potential
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.629146
- avg_reward: 0.000000
- actions: WAIT
- families: dio_00qb

### transition_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 1.036659
- best_reward_sum: 1.036659
- avg_reward: 1.036659
- actions: LONG
- families: dio_0t0v

### start_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 0.894392
- best_reward_sum: 0.894392
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

### transition_state / inner_open_observation / observed_potential
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.094515
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

### transition_state / inner_unfinished / observed_potential
- count: 1
- reward_sum: 0.000000
- best_reward_sum: 0.142483
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1vpi

## Uebergaenge

### same_inner_state
- stability_kind: stable_state
- count: 2
- reward_sum: 1.384854
- positive_contacts: 1
- observed_potentials: 1
- actions: LONG,WAIT
- families: dio_00qb,dio_0arw

### inner_unfinished_to_inner_carried
- stability_kind: transition_state
- count: 1
- reward_sum: 1.036659
- positive_contacts: 1
- observed_potentials: 0
- actions: LONG
- families: dio_0t0v

### timeline_start
- stability_kind: start_state
- count: 1
- reward_sum: 0.894392
- positive_contacts: 1
- observed_potentials: 0
- actions: SHORT
- families: dio_1u7v

### inner_carried_to_inner_open_observation
- stability_kind: transition_state
- count: 1
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 1
- actions: WAIT
- families: dio_14xc

### inner_open_observation_to_inner_unfinished
- stability_kind: transition_state
- count: 1
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 1
- actions: WAIT
- families: dio_1vpi

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel