# DIO Mini Passive Development Reflection

- source: debug\dio_mini_passive_consequence_pipeline_12n_probe18_landkarte\09_passive_development_diagnosis\dio_mini_passive_development_diagnosis.csv

## Zusammenfassung
- reflection_confirmation_seed: families=2 rows=5 reward_sum=2.0 pressure_max=0.833333 families_list=dio_16yc,dio_1txv
- reflection_negative_open: families=1 rows=1 reward_sum=-1.0 pressure_max=0.25 families_list=dio_0fiy
- reflection_quiet_observation: families=5 rows=5 reward_sum=0.0 pressure_max=0.266667 families_list=dio_0igh,dio_143d,dio_14xc,dio_1g2t,dio_1qwp
- reflection_trust_seed: families=4 rows=8 reward_sum=8.0 pressure_max=1.0 families_list=dio_02qu,dio_0arw,dio_0x1o,dio_1vpi

## Familien
- dio_16yc: reflection_confirmation_seed; development=development_observation_to_carried; reward=1.000000; pressure=0.775000
  dio_16yc: Beobachtung wurde spaeter getragen; Innenlage darf Bestaetigung erinnern. Momente=moment_quiet_observed -> moment_carried.
- dio_1txv: reflection_confirmation_seed; development=development_observation_to_carried; reward=1.000000; pressure=0.833333
  dio_1txv: Beobachtung wurde spaeter getragen; Innenlage darf Bestaetigung erinnern. Momente=moment_quiet_observed -> moment_quiet_observed -> moment_carried.
- dio_0fiy: reflection_negative_open; development=development_negative_open; reward=-1.000000; pressure=0.250000
  dio_0fiy: Wiederkehr ist passiv noch offen; Innenlage bleibt lesend.
- dio_0igh: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_0igh: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_143d: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_143d: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_14xc: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_14xc: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_1g2t: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_1g2t: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_1qwp: reflection_quiet_observation; development=development_quiet_observation; reward=0.000000; pressure=0.266667
  dio_1qwp: Wiederkehr blieb ruhig; Innenlage darf Beobachtung halten. Aktionen=WAIT.
- dio_02qu: reflection_trust_seed; development=development_stable_carried; reward=3.000000; pressure=1.000000
  dio_02qu: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=LONG -> LONG -> LONG.
- dio_0arw: reflection_trust_seed; development=development_stable_carried; reward=1.000000; pressure=0.800000
  dio_0arw: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=LONG.
- dio_0x1o: reflection_trust_seed; development=development_stable_carried; reward=1.000000; pressure=0.800000
  dio_0x1o: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=LONG.
- dio_1vpi: reflection_trust_seed; development=development_stable_carried; reward=3.000000; pressure=1.000000
  dio_1vpi: Wiederkehr wurde getragen; Innenlage darf Vertrauen erinnern. Aktionen=SHORT -> SHORT -> SHORT.

## Grenze
- passive Reflexionslesung
- kein Memory-Schreiben
- keine Motorik
- kein Gate
- keine harte Regel