# DIO Mini Passive Development Diagnosis

## Grenze
- liest nur die passive Reife-Timeline
- schreibt kein Memory
- beeinflusst keine Handlung
- kein Gate

## Zusammenfassung
- development_stable_carried: families=3 rows=5 reward_sum=5.0 families_list=dio_0ofo,dio_0ps1,dio_1k7y
- development_observation_to_carried: families=2 rows=5 reward_sum=2.0 families_list=dio_1c6b,dio_1d1z
- development_quiet_observation: families=9 rows=11 reward_sum=0.0 families_list=dio_0120,dio_01vz,dio_040y,dio_10dk,dio_143d,dio_14xc,dio_1f9y,dio_1m4n,dio_1mym
- development_negative_open: families=1 rows=1 reward_sum=-1.0 families_list=dio_1d3r

## Familien
- dio_0ofo: stabil getragen; Pfad=moment_carried; Aktionen=LONG; reward_sum=1.000000.
- dio_0ps1: stabil getragen; Pfad=moment_carried; Aktionen=LONG; reward_sum=1.000000.
- dio_1k7y: stabil getragen; Pfad=moment_carried -> moment_carried -> moment_carried; Aktionen=LONG -> LONG -> LONG; reward_sum=3.000000.
- dio_1c6b: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; Pfad=moment_quiet_observed -> moment_quiet_observed -> moment_carried; Aktionen=WAIT -> WAIT -> SHORT; reward_sum=1.000000.
- dio_1d1z: Entwicklung von Beobachtung/Halten zu getragenem Kontakt; Pfad=moment_quiet_observed -> moment_carried; Aktionen=WAIT -> SHORT; reward_sum=1.000000.
- dio_0120: ruhig beobachtet/gehalten; Pfad=moment_quiet_held; Aktionen=WAIT.
- dio_01vz: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT.
- dio_040y: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_10dk: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_143d: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_14xc: ruhig beobachtet/gehalten; Pfad=moment_quiet_held; Aktionen=WAIT.
- dio_1f9y: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed; Aktionen=WAIT.
- dio_1m4n: ruhig beobachtet/gehalten; Pfad=moment_quiet_observed -> moment_quiet_observed; Aktionen=WAIT -> WAIT.
- dio_1mym: ruhig beobachtet/gehalten; Pfad=moment_quiet_held; Aktionen=WAIT.
- dio_1d3r: negative offene Entwicklung; Pfad=moment_open; reward_sum=-1.000000.