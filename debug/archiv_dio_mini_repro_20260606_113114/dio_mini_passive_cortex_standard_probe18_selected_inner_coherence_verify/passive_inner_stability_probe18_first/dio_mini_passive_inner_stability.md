# DIO Mini Passive Inner Stability

## Stabilitaet

### stable_state / inner_unknown / positive_real_contact
- count: 3
- reward_sum: 2.455651
- best_reward_sum: 2.455651
- avg_reward: 0.818550
- actions: LONG
- families: dio_0120,dio_0bmh,dio_0ems

### stable_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 1.384854
- best_reward_sum: 1.384854
- avg_reward: 1.384854
- actions: LONG
- families: dio_0arw

### stable_state / inner_unknown / observed_potential
- count: 15
- reward_sum: 0.000000
- best_reward_sum: 7.916502
- avg_reward: 0.000000
- actions: WAIT
- families: dio_00qb,dio_0120,dio_0bmh,dio_0ems,dio_0fiy,dio_0igh,dio_1g2t,dio_1qwp

### start_state / inner_carried / positive_real_contact
- count: 1
- reward_sum: 0.894392
- best_reward_sum: 0.894392
- avg_reward: 0.894392
- actions: SHORT
- families: dio_1u7v

### start_state / inner_carried / observed_potential
- count: 3
- reward_sum: 0.000000
- best_reward_sum: 2.683176
- avg_reward: 0.000000
- actions: WAIT
- families: dio_1u7v

### transition_state / inner_carried / observed_potential
- count: 2
- reward_sum: 0.000000
- best_reward_sum: 2.769708
- avg_reward: 0.000000
- actions: WAIT
- families: dio_0arw

### transition_state / inner_open_observation / observed_potential
- count: 3
- reward_sum: 0.000000
- best_reward_sum: 0.283545
- avg_reward: 0.000000
- actions: WAIT
- families: dio_14xc

### transition_state / inner_unknown / observed_potential
- count: 8
- reward_sum: 0.000000
- best_reward_sum: 4.806848
- avg_reward: 0.000000
- actions: WAIT
- families: dio_02qu,dio_0x1o,dio_16yc

### transition_state / inner_cautious / negative_real_contact
- count: 3
- reward_sum: -1.027449
- best_reward_sum: 0.427449
- avg_reward: -0.342483
- actions: SHORT
- families: dio_1vpi

### transition_state / inner_carried / negative_real_contact
- count: 1
- reward_sum: -1.236659
- best_reward_sum: 1.036659
- avg_reward: -1.236659
- actions: SHORT
- families: dio_0t0v

## Uebergaenge

### same_inner_state
- stability_kind: stable_state
- count: 19
- reward_sum: 3.840505
- positive_contacts: 4
- observed_potentials: 15
- actions: LONG,WAIT
- families: dio_00qb,dio_0120,dio_0arw,dio_0bmh,dio_0ems,dio_0fiy,dio_0igh,dio_1g2t,dio_1qwp

### timeline_start
- stability_kind: start_state
- count: 4
- reward_sum: 0.894392
- positive_contacts: 1
- observed_potentials: 3
- actions: SHORT,WAIT
- families: dio_1u7v

### inner_carried_to_inner_open_observation
- stability_kind: transition_state
- count: 1
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 1
- actions: WAIT
- families: dio_14xc

### inner_carried_to_inner_unknown
- stability_kind: transition_state
- count: 5
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 5
- actions: WAIT
- families: dio_0x1o,dio_16yc

### inner_cautious_to_inner_unknown
- stability_kind: transition_state
- count: 3
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 3
- actions: WAIT
- families: dio_02qu

### inner_unknown_to_inner_open_observation
- stability_kind: transition_state
- count: 2
- reward_sum: 0.000000
- positive_contacts: 0
- observed_potentials: 2
- actions: WAIT
- families: dio_14xc

### inner_open_observation_to_inner_cautious
- stability_kind: transition_state
- count: 3
- reward_sum: -1.027449
- positive_contacts: 0
- observed_potentials: 0
- actions: SHORT
- families: dio_1vpi

### inner_unknown_to_inner_carried
- stability_kind: transition_state
- count: 3
- reward_sum: -1.236659
- positive_contacts: 0
- observed_potentials: 2
- actions: SHORT,WAIT
- families: dio_0arw,dio_0t0v

## Grenze
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel