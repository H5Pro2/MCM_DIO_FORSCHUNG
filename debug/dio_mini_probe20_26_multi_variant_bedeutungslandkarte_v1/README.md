# Mini-DIO Mehrvarianten-Bedeutungslandkarte Probe20-26

Referenz: Probe25. Varianten: Probe20, Probe21, Probe22, Probe23, Probe24, Probe26.

Ziel: Pruefen, ob Mini-DIO ueber mehrere kontrollierte Varianten eine stabile passive Bedeutungsstruktur bildet.

Diese Auswertung ist passiv: kein Training-Memory, keine Handlung, kein Gate.

## Variantenuebersicht
- Probe 20: gleiche Familie 10/36, gleiche Richtung 32/36, avg Delta 0.063817194, States: feine_signaturverschiebung:2;ferne_verwandtschaft_gleicher_richtung:10;neues_praebewusstes_muster:4;signaturvariante_gleicher_sinnnaehe:10;wiedererkennung_stabil:10
- Probe 21: gleiche Familie 6/36, gleiche Richtung 34/36, avg Delta 0.144373444, States: ferne_verwandtschaft_gleicher_richtung:20;neues_praebewusstes_muster:2;signaturvariante_gleicher_sinnnaehe:8;wiedererkennung_stabil:6
- Probe 22: gleiche Familie 10/36, gleiche Richtung 34/36, avg Delta 0.063309528, States: feine_signaturverschiebung:6;ferne_verwandtschaft_gleicher_richtung:8;neues_praebewusstes_muster:2;signaturvariante_gleicher_sinnnaehe:10;wiedererkennung_stabil:10
- Probe 23: gleiche Familie 0/36, gleiche Richtung 28/36, avg Delta 1.09785775, States: ferne_verwandtschaft_gleicher_richtung:26;neues_praebewusstes_muster:8;signaturvariante_gleicher_sinnnaehe:2
- Probe 24: gleiche Familie 2/36, gleiche Richtung 34/36, avg Delta 0.095969944, States: feine_signaturverschiebung:2;ferne_verwandtschaft_gleicher_richtung:16;neues_praebewusstes_muster:2;signaturvariante_gleicher_sinnnaehe:14;wiedererkennung_stabil:2
- Probe 26: gleiche Familie 10/36, gleiche Richtung 34/36, avg Delta 0.03798325, States: feine_signaturverschiebung:8;ferne_verwandtschaft_gleicher_richtung:4;neues_praebewusstes_muster:2;signaturvariante_gleicher_sinnnaehe:12;wiedererkennung_stabil:10

## Zustandsuebersicht
- `feine_signaturverschiebung`: 18 Episoden, gleiche Richtung 1.0, avg Delta 0.014889111
- `ferne_verwandtschaft_gleicher_richtung`: 84 Episoden, gleiche Richtung 1.0, avg Delta 0.473088048
- `neues_praebewusstes_muster`: 20 Episoden, gleiche Richtung 0.0, avg Delta 0.5065636
- `signaturvariante_gleicher_sinnnaehe`: 56 Episoden, gleiche Richtung 1.0, avg Delta 0.044888018
- `wiedererkennung_stabil`: 38 Episoden, gleiche Richtung 1.0, avg Delta 0.038599974

## Befund
Mini-DIO zeigt ueber mehrere Varianten keine reine Auswendigwiederholung. Ein Teil der Familien bleibt stabil, ein Teil driftet fein oder kontrolliert, und nur wenige Episoden werden als neues praebewusstes Muster eingeordnet.

Wichtig ist die Trennung:
- stabile Wiedererkennung: gleiche Familie trotz Variantenreiz.
- feine Signaturverschiebung: neue Benennung bei geringer Sensor-/MCM-Abweichung.
- Signaturvariante gleicher Sinnnaehe: andere Familie, aber gleiche grobe Richtung.
- neues praebewusstes Muster: Drift oder Richtungskonflikt stark genug, um nicht als gleiche Spur zu gelten.

Naechster Schritt: aus dieser Karte keine Handlung ableiten, sondern eine passive Wiederkehr-/Reifezaehlung bauen: Welche Familien bleiben ueber Varianten stabil, welche werden nur Varianten derselben Sinnnaehe?
