# Mini-DIO passive Wiederkehr-/Reifezaehlung Probe20-26

Zweck: Familien werden ueber mehrere kontrollierte Varianten gezaehlt. Diese Karte ist passiv und beschreibt nur Wiederkehr, Variantenfaehigkeit und Zeitfragilitaet.

Keine Handlung, kein Gate, kein Training-Memory.

## Reifezustaende
- `instabil_neuordnend`: 1 Familien, Sinn-Erhalt 0.166667, neue Muster 0.833333
- `sinnnah_variantenfaehig`: 16 Familien, Sinn-Erhalt 0.96875, neue Muster 0.03125
- `zeitfragil_aber_richtungserhaltend`: 1 Familien, Sinn-Erhalt 0.666667, neue Muster 0.333333

## Staerkste Referenzfamilien
- `dio_1ekt`: sinnnah_variantenfaehig, stabil 10/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_05k3`: sinnnah_variantenfaehig, stabil 8/12, Sinn erhalten 0.833333, Zeitfragilitaet 1.0
- `dio_0x52`: sinnnah_variantenfaehig, stabil 6/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_0fvj`: sinnnah_variantenfaehig, stabil 4/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_15gs`: sinnnah_variantenfaehig, stabil 4/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_19mp`: sinnnah_variantenfaehig, stabil 2/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_1ull`: sinnnah_variantenfaehig, stabil 2/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_1hs5`: sinnnah_variantenfaehig, stabil 2/12, Sinn erhalten 0.833333, Zeitfragilitaet 1.0
- `dio_067m`: sinnnah_variantenfaehig, stabil 0/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_0qym`: sinnnah_variantenfaehig, stabil 0/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_1215`: sinnnah_variantenfaehig, stabil 0/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0
- `dio_1aqj`: sinnnah_variantenfaehig, stabil 0/12, Sinn erhalten 1.0, Zeitfragilitaet 1.0

## Interpretation
- `stabil_wiederkehrend`: Familie bleibt ueber mehrere Varianten identisch genug.
- `sinnnah_variantenfaehig`: Familie driftet, aber Bedeutung/Richtung bleibt meist erhalten.
- `zeitfragil_aber_richtungserhaltend`: Temporalvarianz zerlegt die Identitaet, aber die grobe Sinnrichtung bleibt.
- `offen_reifend`: noch keine harte Identitaet, aber auch kein Zerfall.
- `instabil_neuordnend`: zu viel neues Muster oder Richtungskonflikt.

Der wichtige Befund ist nicht Handlung, sondern passive Reife: Mini-DIO kann Familien nach Wiederkehr und Variantenbelastung unterscheiden.

Naechster Schritt: diese Reifezaehlung als getrennte passive Memory-Kandidaten speichern, aber noch nicht vom Runtime-System lesen lassen.
