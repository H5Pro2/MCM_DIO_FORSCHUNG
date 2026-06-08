# Mini-DIO passive Bedeutungslandkarte Probe25/26

Zweck: Aus dem kontrollierten Variantenvergleich wird eine passive Karte gebaut. Sie beschreibt, ob eine Form-/Feldspur stabil wiedererkannt wird, als Signaturvariante driftet oder als neues praebewusstes Muster erscheint.

Diese Karte ist Diagnose. Sie schreibt kein Training-Memory, wird nicht von Mini-DIO gelesen, beeinflusst keine Handlung und ist kein Gate.

## Semantische Zust?nde
- `feine_signaturverschiebung`: 8 Episoden, gleiche Richtung 1.0, gewichtete Abweichung 0.0143015
- `neues_praebewusstes_muster`: 4 Episoden, gleiche Richtung 1.0, gewichtete Abweichung 0.1098045
- `signaturvariante_gleicher_sinnnaehe`: 14 Episoden, gleiche Richtung 0.857143, gewichtete Abweichung 0.042419214
- `wiedererkennung_stabil`: 10 Episoden, gleiche Richtung 1.0, gewichtete Abweichung 0.0219898

## Passive Rollen
- `ferne_verwandtschaft_mit_gleicher_richtung`: 4 Episoden
- `richtungskonflikt_als_beobachtung`: 2 Episoden
- `stabiler_form_feld_kern`: 10 Episoden
- `verwandte_signatur_mit_gleicher_richtung`: 20 Episoden

## Beispiele
- `dio_04kx -> dio_0ic5` -> `signaturvariante_gleicher_sinnnaehe` / `richtungskonflikt_als_beobachtung` / Delta 0.0367685
- `dio_05k3 -> dio_05k3` -> `wiedererkennung_stabil` / `stabiler_form_feld_kern` / Delta 0.007694
- `dio_067m -> dio_17ao` -> `neues_praebewusstes_muster` / `ferne_verwandtschaft_mit_gleicher_richtung` / Delta 0.1316195
- `dio_0fvj -> dio_1tsz` -> `feine_signaturverschiebung` / `verwandte_signatur_mit_gleicher_richtung` / Delta 0.0060485
- `dio_0qym -> dio_1r1g` -> `signaturvariante_gleicher_sinnnaehe` / `verwandte_signatur_mit_gleicher_richtung` / Delta 0.038951
- `dio_0x52 -> dio_1rv1` -> `feine_signaturverschiebung` / `verwandte_signatur_mit_gleicher_richtung` / Delta 0.014408
- `dio_1215 -> dio_1t1w` -> `signaturvariante_gleicher_sinnnaehe` / `verwandte_signatur_mit_gleicher_richtung` / Delta 0.0780525
- `dio_15gs -> dio_14c1` -> `neues_praebewusstes_muster` / `ferne_verwandtschaft_mit_gleicher_richtung` / Delta 0.0879895
- `dio_19mp -> dio_19mp` -> `wiedererkennung_stabil` / `stabiler_form_feld_kern` / Delta 0.031705
- `dio_1aqj -> dio_1jba` -> `feine_signaturverschiebung` / `verwandte_signatur_mit_gleicher_richtung` / Delta 0.01993
- `dio_1bwy -> dio_0s84` -> `signaturvariante_gleicher_sinnnaehe` / `verwandte_signatur_mit_gleicher_richtung` / Delta 0.0333805
- `dio_1ekt -> dio_1ekt` -> `wiedererkennung_stabil` / `stabiler_form_feld_kern` / Delta 0.040346

## Interpretation
- `wiedererkennung_stabil`: gleiche Familie trotz Variation. Das ist reproduzierte Form-/Feldnaehe.
- `feine_signaturverschiebung`: geringe Sensor-/MCM-Abweichung, aber neue Benennung. Das ist empfindliche Syntaxgrenze.
- `signaturvariante_gleicher_sinnnaehe`: andere Familie, aber gleiche grobe Richtung. Das ist kontrollierte Variantenbildung.
- `neues_praebewusstes_muster`: starke Drift. Das wird nicht als gleiche Spur behandelt.

Naechster Schritt: Diese Karte gegen weitere Varianten pruefen, bevor daraus irgendeine aktive Reflexions- oder Handlungsschicht entstehen darf.
