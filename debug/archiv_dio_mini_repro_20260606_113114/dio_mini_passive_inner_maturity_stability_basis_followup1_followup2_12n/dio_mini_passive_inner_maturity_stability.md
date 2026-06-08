# DIO Mini Passive Inner Maturity Stability

## Quellen
- basis: debug\dio_mini_passive_inner_maturity_map_12n_no_future_teacher_probe15_probe16_probe18\dio_mini_passive_inner_maturity_map.csv
- followup1: debug\dio_mini_passive_inner_maturity_map_12n_inner_map_followup_probe15_probe16_probe18\dio_mini_passive_inner_maturity_map.csv
- followup2: debug\dio_mini_passive_inner_maturity_map_12n_inner_map_followup2_probe15_probe16_probe18\dio_mini_passive_inner_maturity_map.csv

## Keim-Stabilitaet
- inner_trust_seed: maps=3 traces=5 families=2 actions=LONG,SHORT state=seed_repeats_across_maps
- inner_carefulness_seed: maps=2 traces=7 families=4 actions=LONG state=seed_repeats_across_maps
- inner_reorganization_seed: maps=1 traces=3 families=3 actions=SHORT state=seed_local_to_one_map

## Familien-Stabilitaet
- dio_14xc:LONG: maps=3 seeds=inner_trust_seed transition=inner_seed_repeats_stably
- dio_173s:SHORT: maps=3 seeds=inner_reorganization_seed,inner_trust_seed transition=inner_seed_reorganizes
- dio_04zi:LONG: maps=2 seeds=inner_carefulness_seed transition=inner_seed_repeats_stably
- dio_1qig:LONG: maps=2 seeds=inner_carefulness_seed transition=inner_seed_repeats_stably
- dio_1w4m:LONG: maps=2 seeds=inner_carefulness_seed transition=inner_seed_repeats_stably

## Grenze
- passive Stabilitaetsdiagnose
- keine Handlung
- kein Trainingsmemory
- kein Gate
- kein Zukunftslehrer