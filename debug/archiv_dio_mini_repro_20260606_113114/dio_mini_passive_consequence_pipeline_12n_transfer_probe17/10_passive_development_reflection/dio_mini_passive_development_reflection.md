# DIO Mini Passive Development Reflection

- source: debug\dio_mini_passive_consequence_pipeline_12n_transfer_probe17\09_passive_development_diagnosis\dio_mini_passive_development_diagnosis.csv

## Zusammenfassung
- reflection_confirmation_seed: families=2 rows=5 reward_sum=2.0 pressure_max=0.833333 families_list=dio_1c6b,dio_1d1z
- reflection_negative_open: families=1 rows=1 reward_sum=-1.0 pressure_max=0.25 families_list=dio_1d3r
- reflection_quiet_observation: families=9 rows=11 reward_sum=0.0 pressure_max=0.333333 families_list=dio_0120,dio_01vz,dio_040y,dio_10dk,dio_143d,dio_14xc,dio_1f9y,dio_1m4n,dio_1mym
- reflection_trust_seed: families=3 rows=5 reward_sum=5.0 pressure_max=1.0 families_list=dio_0ofo,dio_0ps1,dio_1k7y

## Familien
- dio_1c6b: reflection_confirmation_seed; development=development_observation_to_carried; reward=1.000000; pressure=0.833333
  dio_1c6b: Beobachtung wurde spaeter getragen; Innenlage darf Bestaetigung erinnern. Momente=moment_quiet_observed -> moment_quiet_observed -> moment_carried.
- dio_1d1z: reflection_confirmation_seed; development=development_observation_to_carried; reward=1.000000; pressure=0.775000
  dio_1d1z: Beobachtung wurde spaeter getragen; Innenlage darf Bestaetigung erinnern. Momente=moment_quiet_observed -> moment_carried.
- dio_1d3r: reflection_negative_open; development=development_negative_open; reward=-1.000000; pressure=0.250000
  dio_1d3r: Wiederkehr ist passiv noch offen; Innenlage bleibt lesend.
- dio_0120: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_0120: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_01vz: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.333333
  dio_01vz: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT -> WAIT.
- dio_040y: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_040y: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_10dk: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_10dk: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_143d: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_143d: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_14xc: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_14xc: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_1f9y: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_1f9y: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_1m4n: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.333333
  dio_1m4n: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT -> WAIT.
- dio_1mym: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_1mym: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_0ofo: reflection_trust_seed; development=development_stable_carried; reward=1.000000; pressure=0.800000
  dio_0ofo: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=LONG.
- dio_0ps1: reflection_trust_seed; development=development_stable_carried; reward=1.000000; pressure=0.800000
  dio_0ps1: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=LONG.
- dio_1k7y: reflection_trust_seed; development=development_stable_carried; reward=3.000000; pressure=1.000000
  dio_1k7y: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=LONG -> LONG -> LONG.

## Grenze
- passive Reflexionslesung
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel