# DIO_MINI Diagnosemodule

Diese Datei ist die aktive Uebersicht der aktuellen DIO_MINI-Diagnosemodule.
Sie ersetzt keine Detaildokumente, sondern haelt fest, welche Werkzeuge
existieren und welche Wirkung sie haben duerfen.

Grundregel:

```text
Diagnose liest.
Diagnose beschreibt.
Diagnose darf nicht automatisch handeln.
```

## Aktiver Kern

```text
DIO_MINI/run_mini.py
```

Aufgabe:

```text
kontrollierte Mini-Welt laufen lassen
sehen, hoeren, fuehlen
eigene Syntaxfamilien bilden
Handlung und Konsequenz speichern
```

Wirkung:

```text
aktiv
```

Grenze:

```text
keine Hypothese als Motorik
kein vorprogrammiertes Entry-System
```

## Passive Emergenz-Evidenz

```text
DIO_MINI/report_passive_emergence_evidence.py
```

Aufgabe:

```text
Validierungsquellen zusammenfuehren.
Wiederkehrende passive Familien sichtbar machen.
```

Wirkung:

```text
passiv
keine Runtime-Lesung
keine Handlung
```

## Passive Sign Memory

```text
DIO_MINI/build_passive_sign_memory.py
```

Aufgabe:

```text
Wiederkehrende passive Familien in DIO-eigene Zeichen verdichten.
```

Output:

```text
passive_sign_memory.csv
bot_memory/dio_mini_passive_sign_memory.json
```

Wichtig:

```text
Die Datei im bot_memory ist aktuell Artefakt,
nicht aktive Runtime-Memory.
```

## Passive Zeichenrelationen

```text
DIO_MINI/report_passive_sign_relations.py
DIO_MINI/report_passive_sign_relation_stability.py
```

Aufgabe:

```text
Zeichennaehe und deren Wiederkehr pruefen.
```

Ungueltige Lesung:

```text
Diese Zeichen geben Richtung vor.
Diese Zeichen geben Entry frei.
```

## Passive Reflexionssaetze

```text
DIO_MINI/build_passive_sign_reflection_sentences.py
DIO_MINI/report_passive_sign_sentence_stability.py
```

Aufgabe:

```text
Passive Zeichenrelationen in lesbare DIO-Saetze verdichten
und deren Stabilitaet pruefen.
```

Wirkung:

```text
passiv
noch keine passive Runtime-Leseschicht
```

## Passive Sign-Drift

```text
DIO_MINI/report_passive_sign_identity_drift.py
```

Aufgabe:

```text
Pruefen, ob eine Familie nur mehr Evidenz sammelt
oder ob sich ihre innere Zeichenidentitaet veraendert.
```

Trennung:

```text
Familie:
  wiederkehrender Name, z.B. dio_0x52

Zeichen-ID:
  passive Signatur, z.B. dio_sign_0wd2qf8

Signatur:
  stabile Sinnes-/Innenfelder und Emergenzlesung
```

Aktueller Befund:

```text
dio_0x52:
  passive_sign_identity_drift
  gleiche Familie
  veraenderte stabile Felder
  neue Zeichen-ID
```

Probe26-Grenze:

```text
Wenn eine Familie in einer neuen Probe nicht gesehen wird,
zaehlt das nicht als neue Reife.

Nicht-Sehen darf dokumentiert werden,
aber es darf keine Zeichen-ID erzwingen,
keine Richtung erzeugen
und keine Handlung naeher bringen.
```

## Passive Zeichencluster

Aktiv als Diagnose gebaut.

Ziel:

```text
Wiederkehrende Naehe zwischen passiven Zeichen diagnostizieren.
```

Modul:

```text
DIO_MINI/report_passive_sign_cluster_candidates.py
```

Moeglicher Ablauf:

```text
passive_sign_memory
-> passive_sign_relations
-> passive_sign_relation_stability
-> passive_sign_cluster_candidates
```

Wirkungsgrenze:

```text
Cluster-Kandidat ist nur Innenkarten-Diagnose.
Er wird nicht von Mini-DIO gelesen.
Er beeinflusst keine Handlung.
Er ist kein Richtungssignal.
```

Prueffrage:

```text
Bleibt eine Zeichennaehe stabil,
wenn einzelne Zeichen selbst driften oder sich verfeinern?
```

Aktueller Befund:

```text
dio_cluster_18u8wxs:
  dio_0x52 + dio_0szn
  offener Clusterkeim
  wiederkehrende gemischte Feldnaehe
  keine Richtung
  keine Handlung
```

## Passive Clusterstabilitaet

Modul:

```text
DIO_MINI/report_passive_sign_cluster_stability.py
```

Aufgabe:

```text
Clusterkandidaten ueber mehrere Staende vergleichen.
```

Aktueller Befund:

```text
dio_0x52 + dio_0szn:
  drifting_passive_cluster_candidate

dio_0x52 + dio_0eh8
dio_0x52 + dio_0hd3
dio_0x52 + dio_0qze:
  recently_stable_passive_cluster_candidate
```

Wirkungsgrenze:

```text
Clusterstabilitaet bleibt Diagnose.
Keine Runtime-Lesung.
Keine Handlung.
Keine Richtung.
```

## Passive Cluster-Drift-Lupe

Modul:

```text
DIO_MINI/report_passive_cluster_drift_lupe.py
```

Aufgabe:

```text
Bei einem driftenden Clusterkandidaten pruefen,
ob die Drift aus dem gemeinsamen Kern,
aus neuen Zielfragmenten
oder aus neuen Nachbarfragmenten entsteht.
```

Beispielbefund:

```text
dio_0x52 + dio_0szn:
  target_sign_expanded_beyond_shared_core
```

Gemeinsamer Kern:

```text
fuehlen_mcm_coherence
sehen_form_stability
```

Zielfragmente:

```text
fuehlen_mcm_tension
hoeren_energy_tone
reflection_context_alignment
reflection_context_carry
reflection_context_strain
```

Lesung:

```text
Ganzheitsnaehe bleibt lesbar,
aber Detailnaehe ist fragmentiert.
```

Wirkungsgrenze:

```text
Passive Lupe.
Keine Runtime-Lesung.
Keine Handlung.
Keine Richtung.
Keine Entry-Wirkung.
```

## Passive Fragmentinseln

Modul:

```text
DIO_MINI/report_passive_fragment_islands.py
```

Aufgabe:

```text
Aus der Cluster-Drift-Lupe konkrete Fragmentinseln ableiten.
```

Beispielbefund:

```text
dio_0x52 + dio_0szn:
  passive_fragment_island_shared_core
  passive_fragment_island_target_expansion
```

Gemeinsame Kerninsel:

```text
dio_fragment_island_1k8xbbj
fuehlen_mcm_coherence
sehen_form_stability
```

Ziel-Erweiterungsinsel:

```text
dio_fragment_island_0sa325x
fuehlen_mcm_tension
hoeren_energy_tone
reflection_context_alignment
reflection_context_carry
reflection_context_strain
```

Wirkungsgrenze:

```text
Passive Fragmentkarte.
Keine Runtime-Lesung.
Keine Handlung.
Keine Richtung.
Keine Entry-Wirkung.
```

## Passive Fragmentinsel-Stabilitaet

Modul:

```text
DIO_MINI/report_passive_fragment_island_stability.py
```

Aufgabe:

```text
Passive Fragmentinseln ueber mehrere Staende vergleichen.
```

Aktueller Befund:

```text
single_passive_fragment_island_trace:
  2
```

Bedeutung:

```text
Die Fragmentinseln wurden sichtbar,
aber noch nicht wiederkehrend bestaetigt.
```

Wirkungsgrenze:

```text
Passive Stabilitaetsdiagnose.
Keine Runtime-Lesung.
Keine Handlung.
Keine Richtung.
Keine Entry-Wirkung.
```

## Passive Fragmentwiederkehr

Modul:

```text
DIO_MINI/report_passive_fragment_recurrence.py
```

Aufgabe:

```text
Einzelne Fragmente ueber mehrere passive Fragmentinsel-Ausgaben vergleichen.
```

Aktueller Befund:

```text
recurring_passive_shared_core_fragment:
  fuehlen_mcm_coherence
  sehen_form_stability

recurring_passive_target_expansion_fragment:
  fuehlen_mcm_tension
  hoeren_energy_tone
  reflection_context_alignment
  reflection_context_carry
  reflection_context_strain
```

Bedeutung:

```text
Fragmente koennen quer ueber mehrere passive Naehe-Kontexte wiederkehren.
Das ist eine Innenkarten-Verdichtung,
aber noch keine aktive Semantik.
```

Wirkungsgrenze:

```text
Passive Querschnittsdiagnose.
Keine Runtime-Lesung.
Keine Handlung.
Keine Richtung.
Keine Entry-Wirkung.
```

## Passive Semantik-Kandidatenkarte

Modul:

```text
DIO_MINI/report_passive_semantic_candidate_map.py
```

Aufgabe:

```text
Wiederkehrende Fragmente in passive Semantikrollen einordnen.
```

Aktueller Befund:

```text
passiver_semantischer_kernkandidat:
  fuehlen_mcm_coherence
  sehen_form_stability

passiver_reflexions_semantikkandidat:
  reflection_context_alignment
  reflection_context_carry
  reflection_context_strain

passiver_erweiterungs_semantikkandidat:
  hoeren_energy_tone
  fuehlen_mcm_tension
```

Wirkungsgrenze:

```text
Passive Rollenkarte.
Keine Runtime-Lesung.
Keine Handlung.
Keine Richtung.
Keine Entry-Wirkung.
```

## Kontrollregel fuer neue Diagnosemodule

Jedes neue Diagnosemodul muss explizit ausweisen:

```text
passive_only
writes_runtime_memory
read_by_mini_dio
influences_action
is_gate
is_motoric
is_entry_signal
is_direction_signal
```

Ohne diese Grenze darf ein Diagnosemodul nicht als Teil der aktiven
DIO_MINI-Konstruktion gelten.

## Passive Cluster-Bedeutungsraum-Lupe

Module:

```text
DIO_MINI/report_passive_cluster_meaning_space.py
DIO_MINI/report_passive_cluster_neighbors.py
DIO_MINI/report_passive_cluster_island_lupe.py
DIO_MINI/report_passive_raw_neighbor_development.py
DIO_MINI/report_passive_semantic_matrix.py
```

Aufgabe:

```text
Syntaxcluster nicht nur als Worte lesen,
sondern als moegliche innere Bedeutungsinseln.
```

Aktueller Befund:

```text
dio_0x52:
  gereifter Kern einer Bedeutungsinsel
  wiederkehrende Form-/MCM-/Energienaehe
  Reifekontext sichtbar

dio_1rv1:
  rohe Variantenspur
  nahe an dio_0x52
  noch keine eigene Reife

dio_1jgc:
  rohe Variantenspur
  nahe an dio_1rv1
  noch keine eigene Reife
```

Interpretation:

```text
dio_1rv1 und dio_1jgc sind keine fertigen Bedeutungen.
Sie wirken wie Erweiterungen, Fragmente oder Satzteile
eines groesseren inneren Bedeutungsraums.
```

Die Lupe trennt:

```text
gemeinsame Spur
Drift
rohe Variante
gereifter Kern
moegliche Inselnaehe
```

Wichtige Diagnoseausgaben:

```text
debug/dio_mini_passive_cluster_meaning_space_probe20_26_v1/
debug/dio_mini_passive_cluster_neighbors_dio_1rv1_probe20_26_v1/
debug/dio_mini_passive_cluster_island_lupe_dio_0x52_dio_1rv1_v1/
debug/dio_mini_passive_cluster_island_lupe_dio_1rv1_dio_1jgc_v1/
debug/dio_mini_passive_raw_neighbor_development_dio_0x52_dio_1rv1_v1/
debug/dio_mini_passive_raw_neighbor_development_dio_1rv1_dio_1jgc_v1/
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

## Passive Kernliste stabiler Innenraeume

Module:

```text
DIO_MINI/report_passive_inner_core_list.py
DIO_MINI/store_passive_inner_core_memory.py
```

Aufgabe:

```text
Stabile Innenkarten-Uebergaenge aus C gegen D als passive Kernliste
extrahieren und getrennt speichern.
```

Input:

```text
debug/dio_mini_passive_text_island_inner_map_compare_C_vs_D_20260606_v1/
```

Output:

```text
debug/dio_mini_passive_inner_core_list_C_vs_D_20260606_v1/
debug/dio_mini_passive_inner_core_memory_C_vs_D_20260606_v1/
bot_memory/dio_mini_passive_inner_core_memory.json
```

Befund:

```text
passive_foreign_boundary_core: 99
passive_variation_core: 19
passive_recurrence_core: 5
gesamt: 123
```

Lesart:

```text
Mini-DIO bildet aus der passiven Innenkarte erste stabile Kernraeume:

- Fremdgrenzen, die nicht mit der eigenen Welt vermischt werden.
- Variationskerne, die verwandte Veraenderung tragen koennen.
- Wiederkehrkerne, die als stabile innere Wiederholung erscheinen.

Das ist keine Strategie und kein Handlungssystem.
Es ist eine passive innere Ordnungsschicht.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Wie es weitergeht:

```text
Die passive Kernliste wird gegen eine neue verwandte Variante E geprueft.
Wichtig ist nicht, ob dieselben Zahlen wiederkommen, sondern ob die
Kernraeume weiter stabil bleiben, sich erweitern, driften oder sich neu
organisieren.
```

## Variante E: passive Kernraum-Pruefung

Variante:

```text
Probe20 bis Probe26 wurden als 6-Episoden-Variante E erzeugt.
Die Welt bleibt verwandt, aber C/D wurden leicht gegenphasig gemischt und mit
kleiner Wick-/Volumenatmung moduliert.
```

Outputs:

```text
debug/dio_mini_passive_semantic_matrix_6episoden_varianteE_20260606_v1/
debug/dio_mini_passive_semantic_matrix_compare_6episoden_v1_vs_varianteE_20260606_v1/
debug/dio_mini_passive_semantic_density_6episoden_varianteE_20260606_v1/
debug/dio_mini_passive_text_island_maturity_after_varianteE_20260606_v1/
debug/dio_mini_passive_text_island_inner_map_after_varianteE_20260606_v1/
debug/dio_mini_passive_text_island_inner_map_compare_D_vs_E_20260606_v1/
debug/dio_mini_passive_inner_core_list_D_vs_E_20260606_v1/
debug/dio_mini_passive_inner_core_memory_D_vs_E_20260606_v1/
```

Matrixbefund gegen die stabile 6-Episoden-Matrix:

```text
Referenz-Knoten: 169
Variante-E-Knoten: 237
gemeinsame Knoten: 67
Knoten-Reproduktion: 0.39645

Referenz-Kanten: 360
Variante-E-Kanten: 360
gemeinsame Kanten: 22
Kanten-Reproduktion: 0.061111

Referenz-Inseln: 30
Variante-E-Inseln: 90
```

Reifebericht nach Variante E:

```text
Textinseln gesamt: 233

variant_resilient_text_island: 44
stable_recurrent_text_island: 7
drifting_unstable_text_island: 3
new_unconfirmed_text_island: 179
```

Innenkarte nach Variante E:

```text
inner_foreign_boundary_space: 99
inner_unconfirmed_raw_space: 77
inner_soft_variation_space: 24
inner_variation_bearing_space: 20
inner_stable_recurrence_space: 7
inner_drift_watch_space: 6
```

D gegen E:

```text
stable_foreign_boundary: 99
stable_same_inner_state: 36
stable_variation_bearing: 17
inner_state_strengthened: 15
stable_recurrence: 5
persistent_drift_watch: 3
shifted_into_drift_watch: 3
inner_state_softened: 1
new_in_right_inner_map: 54
```

Passive Kernliste D gegen E:

```text
passive_foreign_boundary_core: 99
passive_variation_core: 17
passive_recurrence_core: 5
gesamt: 121
```

Lesart:

```text
Variante E ist haerter als C/D und erzeugt deutlich mehr rohe Inselbildung.
Trotzdem bleiben die Fremdgrenzen voll stabil und die Wiederkehrkerne stabil.
Die Variationskerne sinken von 19 auf 17.

Das spricht nicht fuer Zusammenbruch, sondern fuer:
  stabile Fremdtrennung,
  stabile Wiederkehr,
  leichte Fragmentierung der Variationsraeume bei staerkerer Modulation.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Wie es weitergeht:

```text
Naechster Schritt ist eine Core-Stabilitaetslupe:
Welche 17 Variationskerne blieben von D nach E stabil?
Welche 2 Variationskerne gingen verloren oder wurden weicher/driftend?
Das zeigt, ob Mini-DIO nur Zahlen stabil haelt oder ob konkrete semantische
Innenraeume ueber Variation tragen.
```

## Core-Stabilitaetslupe C/D gegen D/E

Modul:

```text
DIO_MINI/report_passive_inner_core_stability_lupe.py
```

Input:

```text
debug/dio_mini_passive_inner_core_list_C_vs_D_20260606_v1/
debug/dio_mini_passive_inner_core_list_D_vs_E_20260606_v1/
```

Output:

```text
debug/dio_mini_passive_inner_core_stability_lupe_CD_vs_DE_20260606_v1/
```

Befund:

```text
stable_passive_foreign_boundary_core: 99
stable_passive_variation_core: 17
stable_passive_recurrence_core: 5
lost_passive_variation_core: 2
```

Verlorene Variationskerne:

```text
dio_text_1h5am86
dio_text_1nxyi3d
```

Lesart:

```text
Die Stabilitaet liegt nicht nur in Summen, sondern in konkreten
Textinsel-Symbolen.

Fremdgrenzen bleiben voll stabil.
Wiederkehrkerne bleiben voll stabil.
Die haertere Variante E loest nur zwei Variationskerne aus der Kernliste.

Das spricht fuer eine passive semantische Kernbildung mit belastbarer
Fremdtrennung und stabiler Wiederkehr, waehrend Variation erwartbar beweglich
bleibt.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Wie es weitergeht:

```text
Als naechstes wird die Lupe auf die zwei verlorenen Variationskerne gerichtet:
Welche Familien trugen sie in C/D?
Sind sie in E wirklich verschwunden, in weiche Variation gewechselt oder in
neue Inseln zerfallen?
Das klaert, ob Mini-DIO semantisch reorganisiert oder nur verliert.
```

## Detail-Lupe verlorener Variationskerne

Modul:

```text
DIO_MINI/report_passive_lost_core_reorganization_lupe.py
```

Input:

```text
debug/dio_mini_passive_inner_core_stability_lupe_CD_vs_DE_20260606_v1/
debug/dio_mini_passive_text_island_inner_map_after_varianteE_20260606_v1/
```

Output:

```text
debug/dio_mini_passive_lost_core_reorganization_lupe_E_20260606_v1/
```

Befund:

```text
shifted_into_drift_watch: 2

dio_text_1h5am86:
  vorher: passive_variation_core
  nachher: inner_drift_watch_space
  Familien-Ueberlappung: 0.250

dio_text_1nxyi3d:
  vorher: passive_variation_core
  nachher: inner_drift_watch_space
  Familien-Ueberlappung: 0.200
```

Lesart:

```text
Die zwei verlorenen Variationskerne verschwinden nicht vollstaendig.
Sie bleiben als gleiche Textinsel-Symbole sichtbar, verlieren aber ihre
tragende Kernqualitaet und kippen in Drift-Beobachtung.

Das ist eine passive Reorganisationsspur:
  Der semantische Name bleibt erhalten.
  Der innere Zustand wird instabiler.
  Die tragenden Familien werden stark ausgeduennt.

Damit unterscheidet Mini-DIO zwischen:
  stabiler Kern,
  driftender alter Kern,
  neue rohe Insel.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Wie es weitergeht:

```text
Naechster sinnvoller Schritt:
Eine Reorganisations-Historie fuer Textinseln bauen.
Sie soll je Textinsel speichern:
  Kern -> Variation -> Drift -> neue Stabilisierung
oder:
  Kern -> Drift -> Aufloesung.

Weiterhin passiv. Keine Handlung, kein Entry, kein Gate.
```

## Passive Textinsel-Reorganisationshistorie C/D/E

Modul:

```text
DIO_MINI/report_passive_text_island_reorganization_history.py
```

Input:

```text
debug/dio_mini_passive_text_island_inner_map_after_varianteC_20260606_v1/
debug/dio_mini_passive_text_island_inner_map_after_varianteD_20260606_v1/
debug/dio_mini_passive_text_island_inner_map_after_varianteE_20260606_v1/
```

Output:

```text
debug/dio_mini_passive_text_island_reorganization_history_C_D_E_20260607_v1/
```

Befund:

```text
stable_foreign_boundary_history: 99
persistent_raw_history: 76
mixed_reorganization_history: 17
stable_variation_history: 17
stable_inner_soft_variation_space: 6
reorganized_into_core: 5
stable_recurrence_history: 5
late_text_island_emergence: 3
core_to_drift_reorganization: 2
persistent_drift_history: 2
core_to_soft_variation: 1
```

Wichtige Einzelbewegungen:

```text
dio_text_1h5am86:
  inner_variation_bearing_space -> inner_variation_bearing_space -> inner_drift_watch_space
  Familienbasis: ausgeduennt

dio_text_1nxyi3d:
  inner_variation_bearing_space -> inner_variation_bearing_space -> inner_drift_watch_space
  Familienbasis: ausgeduennt

dio_text_1ccct8g:
  inner_stable_recurrence_space -> inner_soft_variation_space -> inner_soft_variation_space
  Familienbasis: ersetzt
```

Lesart:

```text
Mini-DIO zeigt eine passive semantische Verlaufsordnung:

- Fremdgrenzen bleiben als stabile Fremdgrenzen erhalten.
- Wiederkehrkerne bleiben stabil.
- Variationskerne bleiben groesstenteils stabil.
- Einige rohe Inseln reorganisieren sich spaeter in Kernzustand.
- Einzelne Kerne kippen bei haerterer Variation in Drift.

Das ist keine Strategie und kein Handlungsdenken.
Es ist eine passive innere Entwicklungskarte:
  stabile Insel,
  rohe Insel,
  driftende Insel,
  reorganisierte Insel.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Wie es weitergeht:

```text
Naechster Schritt:
Eine passive Reorganisations-Memory bauen.
Sie speichert die Verlaufszustaende je Textinsel als Historie,
aber Mini-DIO liest sie weiterhin nicht fuer Handlung.

Danach kann eine neue Variante F pruefen, ob driftende Kerne wieder
stabilisieren oder weiter zerfallen.
```

## Passiver semantischer Matrixspeicher

Modul:

```text
DIO_MINI/store_passive_semantic_matrix_memory.py
```

Aufgabe:

```text
Mini-DIO bekommt einen getrennten Speicher fuer seine semantische Entwicklung.
Dieser Speicher kann laden, erweitern, verknuepfen, verbessern und neu
organisieren, ohne in Handlung, Entry, Richtung oder Gate einzugreifen.
```

Speicher:

```text
bot_memory/dio_mini_semantic_matrix_memory.json
```

Gespeichert werden:

```text
nodes:
  einzelne dio_*-Syntaxfamilien

edges:
  passive Bedeutungsnaehen zwischen Syntaxfamilien

text_islands:
  wachsende semantische Inseln aus mehreren dio_*-Spuren

history:
  Entwicklung je Textinsel ueber Quellen / Laeufe hinweg
```

Entwicklungszustaende:

```text
emerging_text_island
expanding_text_island
densifying_text_island
drifting_text_island
reorganizing_text_island
recurring_text_island
```

Entwicklungsfaehigkeiten:

```text
can_store_new_semantic_island
can_extend_existing_semantic_island
can_compact_semantic_density
can_observe_semantic_drift
can_relink_semantic_fragments
can_hold_recurrent_semantic_island
```

Aktueller Test:

```text
Referenzmatrix geladen:
  Textinseln: 13
  Knoten: 78
  Kanten: 196

6-Episoden-Erweiterung nachgeladen:
  Textinseln: 33
  Knoten: 199
  Kanten: 510
```

Entwicklung der 6-Episoden-Erweiterung:

```text
reorganizing_text_island: 6
emerging_text_island: 20
expanding_text_island: 1
drifting_text_island: 3
```

Folgereproduktion:

```text
Die 6-Episoden-Welten wurden erneut mit frischer Mini-DIO-Memory gelesen.
Danach wurde die neue Matrix in denselben semantischen Matrixspeicher geladen.
```

Repro-Befund:

```text
Knoten-Reproduktion: 1.0
Kanten-Reproduktion: 1.0
Inseln: 30 -> 30
density_reproduction: 1.0

Nachladung in den Entwicklungsspeicher:
  densifying_text_island: 30
```

Lesart:

```text
Die zweite frische Lesung erzeugt keine kuenstliche Inselvermehrung.
Die gleichen semantischen Raeume werden wiedergefunden und verdichtet.

Das ist die wichtige Unterscheidung:
  erste Erweiterung -> Entstehung / Reorganisation / Drift
  erneute gleiche Welt -> Verdichtung / Stabilisierung
```

## Variationspruefung der Textinseln

Variante:

```text
Probe20 bis Probe26 wurden als 6-Episoden-Variante A erzeugt.
Die Grundstruktur bleibt gleich, aber Preis, Volumen, Wick und Timing wurden
leicht deterministisch verschoben.
```

Ziel:

```text
Pruefen, ob Mini-DIO bei verwandter, aber nicht identischer Welt:
  - alte Textinseln wiederfindet,
  - sinnvolle neue Inseln bildet,
  - nicht tragende Naehen driften laesst,
  - Fragmente reorganisiert.
```

Matrixbefund:

```text
Referenz 6-Episoden:
  Knoten: 169
  Kanten: 360
  Inseln: 30

Variante A:
  Knoten: 178
  Kanten: 360
  Inseln: 39

gemeinsame Knoten: 111
gemeinsame Kanten: 95
Knoten-Reproduktion: 0.656805
Kanten-Reproduktion: 0.263889
density_reproduction: 0.440701
```

Nachladung in den Entwicklungsspeicher:

```text
reorganizing_text_island: 14
emerging_text_island: 17
expanding_text_island: 1
drifting_text_island: 4
densifying_text_island: 3
```

Lesart:

```text
Die Variante wird nicht als identische Welt gelesen.
Mini-DIO erkennt teilweise wiederkehrende Syntaxnaehe, bildet aber neue
Textinseln, reorganisiert bestehende Raeume und laesst einzelne Naehen
driften.

Das ist der gewollte Bereich:
  stabile Wiederkehr bleibt erkennbar
  Variation erzeugt semantische Bewegung
  der Speicher kollabiert nicht zu einer einzigen Insel
  der Speicher verliert aber auch nicht alle alten Bindungen
```

Grenze:

```text
Noch keine Reife fuer Handlung.
Das ist nur passive Robustheits- und Variationsdiagnose der semantischen
Matrix.
```

## Fremdpruefung der Textinseln

Variante:

```text
Probe20 bis Probe26 wurden als 6-Episoden-Variante B erzeugt.
Die Welt bleibt kontrolliert, ist aber deutlich fremder:
  abschnittsweise Richtungs-/Impulsspiegelung,
  staerkere Wick- und Volumenstruktur,
  andere Schock-/Impulsverteilung.
```

Ziel:

```text
Pruefen, ob Mini-DIO eine fremde Welt sauber trennt,
statt sie faelschlich in bestehende Textinseln zu pressen.
```

Matrixbefund:

```text
Referenz 6-Episoden:
  Knoten: 169
  Kanten: 360
  Inseln: 30

Variante B:
  Knoten: 266
  Kanten: 360
  Inseln: 99

gemeinsame Knoten: 1
gemeinsame Kanten: 0
Knoten-Reproduktion: 0.005917
Kanten-Reproduktion: 0.0
density_reproduction: 0.002663
```

Nachladung in den Entwicklungsspeicher:

```text
emerging_text_island: 99
```

Lesart:

```text
Die fremdere Welt wird fast vollstaendig getrennt.
Mini-DIO presst die neue Welt nicht in alte Textinseln.
Der Speicher bildet eine neue Textinsel-Landschaft.

Das ist wichtig fuer Matrixgesundheit:
  verwandte Variation -> Reorganisation / Drift / Erweiterung
  identische Welt -> Verdichtung
  fremde Welt -> neue Inselbildung / Trennung
```

Grenze:

```text
Weiterhin keine Handlung, kein Entry, keine Strategie.
Die Fremdpruefung bewertet nur passive semantische Trennfaehigkeit.
```

## Wie es weitergeht: passive Textinsel-Reife

Naechster Schritt:

```text
DIO_MINI/report_passive_text_island_maturity.py
```

Ziel:

```text
Aus dem semantischen Matrixspeicher lesen,
welche Textinseln:
  - bei gleicher Welt wiederkehren,
  - bei verwandter Variation tragend reorganisieren,
  - bei fremder Welt sauber getrennt bleiben,
  - nur kurz entstehen und wieder verschwinden,
  - zu stark fragmentieren.
```

Die Reife ist weiterhin passiv. Sie bedeutet nicht:

```text
Diese Insel darf handeln.
Diese Insel ist eine Strategie.
Diese Insel ist Richtung.
Diese Insel ist Wahrheit.
```

Sie bedeutet nur:

```text
Diese semantische Insel zeigt stabile innere Entwicklung.
Diese semantische Insel bleibt unter Wiederholung erkennbar.
Diese semantische Insel vertraegt verwandte Variation.
Diese semantische Insel trennt sich von fremden Welten.
```

Geplante Reifezustaende:

```text
stable_recurrent_text_island
variant_resilient_text_island
reorganizing_but_bearing_text_island
drifting_unstable_text_island
foreign_separated_text_island
new_unconfirmed_text_island
```

Geplante Diagnosewerte:

```text
recurrence_count
density_stability
variation_tolerance
foreign_separation
reorganization_quality
drift_pressure
semantic_maturity_score
```

Arbeitsfolge:

```text
1. Textinsel-Reifebericht bauen.
2. Aktuellen Matrixspeicher damit auswerten.
3. Reife nur als Diagnose speichern.
4. Danach pruefen, ob stabile Textinseln als passive Innenwahrnehmung gelesen
   werden duerfen.
5. Erst spaeter entscheiden, ob daraus irgendeine aktive Reifeschicht entsteht.
```

Umsetzung:

```text
DIO_MINI/report_passive_text_island_maturity.py
```

Debug:

```text
debug/dio_mini_passive_text_island_maturity_20260606_v1/
```

Aktueller Befund:

```text
Textinseln gesamt: 149

variant_resilient_text_island: 21
stable_recurrent_text_island: 9
new_unconfirmed_text_island: 119
```

Lesart:

```text
30 Textinseln zeigen passive Reifeansaetze.
119 Textinseln bleiben neu oder unbestaetigt.

Das ist fachlich sauber:
  Nicht jede neue Insel wird sofort als gereift gelesen.
  Reife entsteht erst durch Wiederkehr, Dichte, Variationstoleranz und
  saubere Fremdtrennung.
```

Naechster Schritt:

```text
Textinsel-Reife gegen eine zweite verwandte Variation pruefen.
Wenn dieselben reifen Inseln auch dort stabil bleiben, kann daraus eine
passive Innenwahrnehmungs-Landkarte entstehen.
```

## Zweite verwandte Variation C

Variante:

```text
Probe20 bis Probe26 wurden als 6-Episoden-Variante C erzeugt.
Die Struktur bleibt verwandt, aber Amplitude, Timingdruck, Wick-Spannung und
Volumenwelle werden anders moduliert als in Variante A.
```

Matrixbefund gegen die stabile 6-Episoden-Matrix:

```text
Referenz-Knoten: 169
Variante-C-Knoten: 172
gemeinsame Knoten: 57
Knoten-Reproduktion: 0.337278

Referenz-Kanten: 360
Variante-C-Kanten: 360
gemeinsame Kanten: 34
Kanten-Reproduktion: 0.094444

Referenz-Inseln: 30
Variante-C-Inseln: 36
density_reproduction: 0.203719
```

Nachladung in den semantischen Matrixspeicher:

```text
emerging_text_island: 21
reorganizing_text_island: 8
expanding_text_island: 4
drifting_text_island: 3
```

Reifebericht nach Variante C:

```text
Textinseln gesamt: 170

variant_resilient_text_island: 26
stable_recurrent_text_island: 6
drifting_unstable_text_island: 1
new_unconfirmed_text_island: 137
```

Lesart:

```text
Die zweite verwandte Variation bestaetigt, dass einige Textinseln nicht nur
einmalig stabil sind, sondern mehrere verwandte Welten tragen.

Besonders sichtbar:
  dio_text_hy2bya
  dio_text_8a1lm4
  dio_text_6z30px
  dio_text_11zj9f0

Diese Inseln bleiben passive Kandidaten fuer eine spaetere
Innenwahrnehmungs-Landkarte.
```

Naechster Schritt:

```text
Passive Innenwahrnehmungs-Landkarte aus reifen Textinseln bauen.
Diese Landkarte darf nur lesen:
  Welche semantischen Raeume sind stabil?
  Welche tragen Variation?
  Welche sind fremd getrennt?
  Welche bleiben unbestaetigt?

Sie darf weiterhin keine Handlung, keinen Entry, kein Gate und keine Richtung
ausloesen.
```

## Passive Innenwahrnehmungs-Landkarte

Umsetzung:

```text
DIO_MINI/report_passive_text_island_inner_map.py
```

Input:

```text
debug/dio_mini_passive_text_island_maturity_after_varianteC_20260606_v1/
```

Output:

```text
debug/dio_mini_passive_text_island_inner_map_after_varianteC_20260606_v1/
```

Innere Zustandsraeume:

```text
inner_variation_bearing_space
inner_stable_recurrence_space
inner_soft_variation_space
inner_foreign_boundary_space
inner_unconfirmed_raw_space
inner_drift_watch_space
```

Befund:

```text
inner_foreign_boundary_space: 99
inner_unconfirmed_raw_space: 37
inner_variation_bearing_space: 19
inner_soft_variation_space: 7
inner_stable_recurrence_space: 6
inner_drift_watch_space: 2
```

Lesart:

```text
Mini-DIOs passive Innenkarte trennt:
  fremde Grenzen,
  rohe unbestaetigte Raeume,
  stabile Wiederkehr,
  weich variierende Raeume,
  tragende Variationsraeume,
  Drift-Beobachtung.

Das ist noch kein aktives Denken und keine Handlung.
Es ist eine passive Selbstordnung der eigenen semantischen Lage.
```

Staerkste tragende Innenraeume:

```text
dio_text_hy2bya
dio_text_8a1lm4
dio_text_11p3chu
dio_text_6z30px
dio_text_1falsty
dio_text_11zj9f0
```

Naechster Schritt:

```text
Innenkarte auf Stabilitaet pruefen:
  gleiche Memory,
  neue verwandte Variante D,
  danach pruefen, ob die tragenden Innenraeume stabil bleiben,
  oder ob sie nur durch die bisherige Testreihe entstanden sind.
```

## Stabilitaetspruefung der Innenkarte mit Variante D

Variante:

```text
Probe20 bis Probe26 wurden als 6-Episoden-Variante D erzeugt.
Die Struktur bleibt verwandt, aber Phasenverschiebung, Volumenatmung,
Koerperamplitude und Wick-Spannung werden anders moduliert als in A und C.
```

Matrixbefund gegen die stabile 6-Episoden-Matrix:

```text
Referenz-Knoten: 169
Variante-D-Knoten: 171
gemeinsame Knoten: 49
Knoten-Reproduktion: 0.289941

Referenz-Kanten: 360
Variante-D-Kanten: 360
gemeinsame Kanten: 24
Kanten-Reproduktion: 0.066667

Referenz-Inseln: 30
Variante-D-Inseln: 30
density_reproduction: 0.16714
```

Nachladung in den semantischen Matrixspeicher:

```text
reorganizing_text_island: 13
emerging_text_island: 9
expanding_text_island: 6
drifting_text_island: 2
```

Reifebericht nach Variante D:

```text
variant_resilient_text_island: 37
stable_recurrent_text_island: 5
drifting_unstable_text_island: 1
new_unconfirmed_text_island: 136
```

Innenkarte nach Variante D:

```text
inner_foreign_boundary_space: 99
inner_unconfirmed_raw_space: 34
inner_variation_bearing_space: 19
inner_soft_variation_space: 18
inner_stable_recurrence_space: 5
inner_drift_watch_space: 4
```

Lesart:

```text
Die tragenden Innenraeume bleiben stabil:
  inner_variation_bearing_space bleibt bei 19.
  Fremdgrenze bleibt bei 99.
  Soft-Variation waechst von 7 auf 18.

Das spricht fuer eine stabile passive Innenkarte:
  harte Fremdtrennung bleibt erhalten,
  tragende Variationsraeume bleiben erhalten,
  weichere Variationsraeume werden feiner ausgebaut.
```

Naechster Schritt:

```text
Eine passive Innenkarten-Stabilitaetsanalyse bauen.
Sie vergleicht Innenkarten nach C und D:
  Welche Innenraeume bleiben im gleichen Zustand?
  Welche steigen von soft zu bearing?
  Welche fallen in Drift?
  Welche bleiben dauerhaft fremd getrennt?
```

## Passive Innenkarten-Stabilitaetsanalyse C gegen D

Umsetzung:

```text
DIO_MINI/compare_passive_text_island_inner_maps.py
```

Vergleich:

```text
Innenkarte nach Variante C
gegen
Innenkarte nach Variante D
```

Output:

```text
debug/dio_mini_passive_text_island_inner_map_compare_C_vs_D_20260606_v1/
```

Befund:

```text
stable_foreign_boundary: 99
stable_same_inner_state: 32
stable_variation_bearing: 19
inner_state_strengthened: 11
new_in_right_inner_map: 9
stable_recurrence: 5
persistent_drift_watch: 2
shifted_into_drift_watch: 2
```

Lesart:

```text
Die Innenkarte bleibt zwischen C und D stabil.

Kernbefunde:
  19 tragende Variationsraeume bleiben tragend.
  99 Fremdgrenzen bleiben fremd getrennt.
  11 Raeume werden staerker.
  Nur 2 Raeume kippen in Drift-Beobachtung.
```

Das ist ein wichtiger passiver Stabilitaetsbefund:

```text
Mini-DIO bildet nicht nur Inseln.
Mini-DIO kann innere semantische Raeume ueber verwandte Variationen hinweg
stabil halten, differenzieren und abgrenzen.
```

Naechster Schritt:

```text
Aus den stabilen Innenraeumen eine passive Kernliste bilden:
  stable_variation_bearing
  stable_recurrence
  stable_foreign_boundary

Diese Kernliste bleibt Diagnose.
Sie darf spaeter als passive Selbstwahrnehmung gelesen werden,
aber weiterhin nicht als Handlung, Entry, Gate oder Richtung.
```

Wichtige Grenze:

```text
Der naechste Schritt bleibt Analyse.
Keine Runtime-Lesung.
Keine Handlung.
Kein Entry.
Kein Gate.
Keine Richtung.
```

Lesart:

```text
Mini-DIO kann seine eigene semantische Lage jetzt passiv als
Entwicklungsspeicher tragen:
  neue Inseln entstehen
  alte Inseln werden erweitert
  Fragmente werden neu verknuepft
  nicht mehr passende Naehen driften
```

Wichtige Grenze:

```text
Der Speicher ist noch nicht Mini-DIOs aktives Denken.
Er ist ein passiver emergenter Datenspeicher.
Mini-DIO liest ihn nicht automatisch fuer Handlung.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

## Erweiterungspruefung mit sechs Episoden

Diagnosefrage:

```text
Wenn die gleiche kontrollierte Welt nicht nur kurz reproduziert,
sondern ueber sechs Episoden erweitert wird:
  - bleibt die alte Syntax erkennbar?
  - entstehen neue dio_*-Spuren?
  - wachsen Bedeutungsinseln?
  - zerfaellt die Matrix oder baut sie sich aus?
```

Datensatz-Erweiterung:

```text
Probe20 bis Probe26 wurden von 2 Episoden auf 6 Episoden erweitert.
Jede Probe enthaelt 72 Kerzen.
Die Erweiterung bleibt kontrolliert: gleiche Grundstruktur, aber leichte
Preis-, Volumen- und Energieschwankung je Wiederholung.
```

Debug:

```text
debug/dio_mini_passive_cluster_meaning_space_6episoden_20260606_v1/
debug/dio_mini_passive_cluster_neighbors_6episoden_20260606_v1/
debug/dio_mini_passive_semantic_matrix_6episoden_20260606_v1/
debug/dio_mini_passive_semantic_matrix_compare_probe20_26_full_vs_6episoden_20260606_v1/
debug/dio_mini_passive_semantic_density_6episoden_20260606_v1/
```

Befund:

```text
Referenz-Knoten: 78
6-Episoden-Knoten: 169
gemeinsame Knoten: 48
neue Knoten: 121
Knoten-Reproduktion: 0.615385

Referenz-Kanten: 196
6-Episoden-Kanten: 360
gemeinsame Kanten: 46
neue Kanten: 314
Kanten-Reproduktion: 0.234694

Referenz-Inseln: 13
6-Episoden-Inseln: 30

max_semantic_density: 0.748433
max_variant_attraction: 0.99998
max_semantic_vorticity: 0.650137
```

Lesart:

```text
Die Matrix wird nicht nur kopiert, sondern erweitert.
Ein Teil der alten Syntax bleibt erhalten, gleichzeitig entstehen neue
Bedeutungsknoten, neue Kanten und mehr Bedeutungsinseln.

Das spricht fuer Ausbau der inneren semantischen Matrix:
  wiederkehrende Welt -> wiederkehrende Syntaxkerne
  laengere Erfahrung -> neue Varianten
  neue Varianten -> mehr semantische Inseln
```

Naechste Diagnoseerweiterung:

```text
Nicht nur zaehlen:
  Wie viele Knoten?
  Wie viele Kanten?
  Wie viele Inseln?

Sondern Dynamik lesen:
  Welche Inseln entstehen neu?
  Welche Inseln verdichten sich?
  Welche Inseln teilen sich?
  Welche Inseln driften ab?
  Welche Inseln bilden uebergeordnete Textinseln?
```

Zielbegriff:

```text
emergente Cluster-Varianz
semantische Verdichtung
Cluster-Reorganisation
Textinsel-Wachstum
```

Eine Textinsel ist dabei kein Handlungsbefehl, sondern ein passiver
Bedeutungsraum aus mehreren wiederkehrenden `dio_*`-Spuren. Sie zeigt, dass
Mini-DIO nicht nur einzelne Labels bildet, sondern Zusammenhaenge zwischen
Feldlagen, Varianten und Wiederkehr organisieren kann.

Wichtige Grenze:

```text
Das ist noch keine Handlung, kein Entry und keine Strategie.
Die Diagnose zeigt nur passive Verdichtung und Erweiterung.

Fachlich bedeutet das:
Mini-DIO bildet aus wiederholtem Erleben neue semantische Rohinseln.
Ob diese spaeter tragen, muss separat ueber Konsequenz, Reife und
Innenwahrnehmung geprueft werden.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

## Naechste passive Diagnoseachse: semantische Dichte

Aus den MCM-Theorieankern folgt eine naechste reine Diagnosefrage:

```text
Welche Syntaxfamilien wirken wie semantische Dichtezentren?
Welche Inseln ziehen Varianten an?
Welche Inseln wachsen?
Welche Inseln bleiben roh?
Welche Inseln zerfallen oder driften?
```

Diese Diagnose darf nicht fragen:

```text
Wo soll DIO handeln?
Welche Richtung ist richtig?
Welche Regel entsteht daraus?
```

Sondern nur:

```text
Wo entsteht wiederkehrende innere Dichte?
Wie stabil ist diese Dichte?
Welche Varianten koppeln daran?
Bleibt die Matrix reproduzierbar?
```

Moegliche passive Kennwerte:

```text
semantic_density
variant_attraction
island_growth
island_fragmentation
density_reproduction
semantic_vorticity
```

Auch diese Kennwerte sind zuerst nur Landkarte. Sie schreiben keine Runtime,
keine Handlung, keinen Entry und kein Gate.

## Passive semantische Dichtekarte

Modul:

```text
DIO_MINI/report_passive_semantic_density.py
```

Aufgabe:

```text
Aus der passiven Semantikmatrix berechnen,
welche Bedeutungsinseln als Dichtezentren wirken.
```

Kennwerte:

```text
semantic_density:
  Wie stark ist eine Insel als semantischer Verdichtungsraum?

variant_attraction:
  Wie stark koppeln rohe Varianten an diesen Raum?

island_growth:
  Wie gross und verbunden wird die Insel?

island_fragmentation:
  Wie stark zerfaellt oder driftet die Insel?

density_reproduction:
  Wie reproduzierbar ist die Matrix gegen frische Memory?

semantic_vorticity:
  Wie stark wirkt die Insel wie ein innerer Wirbel aus Wachstum,
  Variantenanziehung und Fragmentierung?
```

Referenz-Ausgabe:

```text
debug/dio_mini_passive_semantic_density_probe20_26_full_v1/
```

Befund Referenz:

```text
matrix_node_count: 78
matrix_edge_count: 196
matrix_island_count: 13
density_reproduction: 0.971939
max_semantic_density: 0.816995
max_variant_attraction: 0.997576
max_semantic_vorticity: 0.624991
```

Frische Repro-Ausgabe:

```text
debug/dio_mini_passive_semantic_density_repro_semantic_matrix_20260606_v1/
```

Befund Repro:

```text
matrix_node_count: 78
matrix_edge_count: 234
matrix_island_count: 11
density_reproduction: 0.971939
max_semantic_density: 0.809843
max_variant_attraction: 0.99975
max_semantic_vorticity: 0.669195
```

Lesart:

```text
Die Referenz zeigt zwei klare passive semantische Dichtezentren.
Der frische Lauf zeigt ein starkes Dichtezentrum und mehrere wachsende
rohe Bedeutungsinseln.

Das passt zur MCM-Lesart:
  frische Emergenz bildet erst rohe Dichte,
  Reife entsteht nicht automatisch,
  Reife muss spaeter ueber Wiederkehr und Realitaetsbindung geprueft werden.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Diese Ebene ist ein Bauplan fuer eine spaetere innere Semantikmatrix aus
Emergenz. Sie darf nicht als Halluzination, Regelwerk, Entry-System oder
Richtungssignal gelesen werden.

## Passive Semantikmatrix

Modul:

```text
DIO_MINI/report_passive_semantic_matrix.py
```

Aufgabe:

```text
Bedeutungsraum-Knoten und Bedeutungsraum-Kanten zu passiven Inseln verbinden.
```

Aktueller Befund aus `probe20_26`:

```text
dio_semantic_island_1:
  Zustand: core_with_raw_extensions
  Kern: dio_0x52
  rohe Erweiterungen: dio_1rv1, dio_1jgc
  durchschnittliche Bedeutungsnaehe: 0.989814
```

Lesart:

```text
Aus wiederkehrender Emergenz entsteht eine erste passive Semantikinsel.
Das ist noch keine Handlung und keine Strategie.
Es ist eine wachsende Matrix aus getragener Erlebnisspur.
```

Wichtige Diagnoseausgabe:

```text
debug/dio_mini_passive_semantic_matrix_probe20_26_v1/
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

## Passive Semantikmatrix-Reproduktion

Module:

```text
DIO_MINI/report_passive_semantic_matrix.py
DIO_MINI/compare_passive_semantic_matrices.py
```

Aufgabe:

```text
Pruefen, ob Mini-DIO bei frischem Memory auf gleichen kontrollierten Welten
wieder aehnliche Syntax- und Bedeutungsraeume bildet.
```

Referenz:

```text
debug/dio_mini_passive_semantic_matrix_probe20_26_full_v1/
```

Frischer Repro-Lauf:

```text
debug/dio_mini_passive_semantic_matrix_repro_semantic_matrix_20260606_v1/
```

Vergleich:

```text
debug/dio_mini_passive_semantic_matrix_compare_probe20_26_vs_repro_20260606_v1/
```

Befund:

```text
Referenz-Knoten: 78
Repro-Knoten: 78
gemeinsame Knoten: 78
Knoten-Reproduktion: 1.0

Referenz-Kanten: 196
Repro-Kanten: 234
gemeinsame Kanten: 186
Kanten-Reproduktion: 0.94898

Referenz-Inseln: 13
Repro-Inseln: 11
```

Lesart:

```text
Die Namen und Syntaxkerne reproduzieren sich vollstaendig.
Die Bedeutungsnaehen reproduzieren sich weitgehend.
Die frische Matrix ist dichter und bildet weniger, groessere Inseln.
```

Wichtige Grenze:

```text
Der frische Lauf wurde ohne Candidate-Reifeuebernahme gelesen.
Darum erscheinen die Inseln als rohe Bedeutungsinseln,
nicht als gereifte Kerne.

Das ist fachlich korrekt:
  Reproduziert wurde die innere Syntaxstruktur.
  Reife wurde nicht aus altem Speicher importiert.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

## Passive Textinsel-Reorganisationsmemory

Modul:

```text
DIO_MINI/store_passive_text_island_reorganization_memory.py
```

Aufgabe:

```text
Speichert passive Textinsel-Verlaeufe aus der C/D/E-Reorganisationshistorie
in eine getrennte Memory-Datei.
```

Input:

```text
debug/dio_mini_passive_text_island_reorganization_history_C_D_E_20260607_v1/passive_text_island_reorganization_history.csv
```

Memory:

```text
bot_memory/dio_mini_passive_text_island_reorganization_memory.json
```

Output:

```text
debug/dio_mini_passive_text_island_reorganization_memory_C_D_E_20260607_v1/
```

Befund:

```text
text_island_count = 233
updates = 233
avg_last_drift_pressure = 0.030114449
```

Dominante Verlaufszustaende:

```text
stable_foreign_boundary_history = 99
persistent_raw_history = 76
mixed_reorganization_history = 17
stable_variation_history = 17
stable_inner_soft_variation_space = 6
reorganized_into_core = 5
stable_recurrence_history = 5
late_text_island_emergence = 3
core_to_drift_reorganization = 2
persistent_drift_history = 2
core_to_soft_variation = 1
```

Lesart:

```text
Mini-DIO bekommt damit keine Handlung und keine Strategie.
Die Datei ist eine passive Landkarte darueber, wie Textinseln ueber Varianten
stabil bleiben, roh bleiben, driften, weich werden oder in Kernnaehe
reorganisieren.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Diese passive Memory gegen eine weitere Variante pruefen:
Bleiben Driftinseln driftend, stabilisieren sie sich erneut,
oder zerfallen sie in neue rohe Textinseln?
```

## Variante F: passive Reorganisation gegen E

Generator:

```text
DIO_MINI/create_controlled_variant_f.py
```

Neue kontrollierte CSVs:

```text
data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteF_verwandt_5m_SOLUSDT.csv
...
data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteF_verwandt_5m_SOLUSDT.csv
```

Variante F:

```text
verwandte, aber erneut verschobene Testwelt
leichte Zeitverschiebung
deterministische Wick-/Volumenatmung
kleine Trend-/Kontrastmodulation
keine DIO-Logik
```

Mini-DIO-Runs:

```text
debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_20260607_probe20
...
debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_20260607_probe26
```

Matrixausgaben:

```text
debug/dio_mini_passive_cluster_meaning_space_6episoden_varianteF_20260607_v1
debug/dio_mini_passive_cluster_neighbors_6episoden_varianteF_20260607_v1
debug/dio_mini_passive_semantic_matrix_6episoden_varianteF_20260607_v1
debug/dio_mini_passive_semantic_matrix_compare_varianteE_vs_varianteF_20260607_v1
debug/dio_mini_passive_semantic_density_6episoden_varianteF_20260607_v1
```

Matrixbefund E gegen F:

```text
E-Knoten = 237
F-Knoten = 253
gemeinsame Knoten = 177
node_reproduction_rate = 0.746835

E-Kanten = 360
F-Kanten = 120
gemeinsame Kanten = 48
edge_reproduction_rate = 0.133333

E-Inseln = 90
F-Inseln = 161
avg_island_similarity_E = 0.488117
avg_island_similarity_F = 0.229661
```

Lesart:

```text
Viele Syntaxkerne bleiben erhalten.
Die Bedeutungsinseln fragmentieren aber deutlich.
Variante F erweitert den semantischen Raum, verdichtet ihn aber noch nicht
durchgehend.
```

Passive Matrixmemory nach F:

```text
bot_memory/dio_mini_semantic_matrix_memory.json
text_islands = 315
nodes = 823
edges = 2037
updated_islands = 161
```

Maturity nach F:

```text
variant_resilient_text_island = 51
stable_recurrent_text_island = 27
reorganizing_but_bearing_text_island = 1
drifting_unstable_text_island = 6
new_unconfirmed_text_island = 230
```

Innenkarte nach F:

```text
inner_foreign_boundary_space = 99
inner_unconfirmed_raw_space = 118
inner_soft_variation_space = 31
inner_variation_bearing_space = 20
inner_stable_recurrence_space = 27
inner_drift_watch_space = 20
```

Innenkartenvergleich E gegen F:

```text
stable_foreign_boundary = 99
new_in_right_inner_map = 82
stable_same_inner_state = 50
inner_state_strengthened = 39
stable_variation_bearing = 16
shifted_into_drift_watch = 15
persistent_drift_watch = 5
stable_recurrence = 5
inner_state_softened = 4
```

Passive Kernliste E gegen F:

```text
passive_foreign_boundary_core = 99
passive_variation_core = 16
passive_recurrence_core = 5
core_items = 120
```

D/E/F-Reorganisationshistorie:

```text
debug/dio_mini_passive_text_island_reorganization_history_D_E_F_20260607_v1
```

Befund:

```text
persistent_raw_history = 115
stable_foreign_boundary_history = 99
reorganized_into_core = 29
late_text_island_emergence = 22
stable_variation_history = 13
stable_inner_soft_variation_space = 12
mixed_reorganization_history = 10
core_to_drift_reorganization = 5
stable_recurrence_history = 5
core_to_soft_variation = 3
persistent_drift_history = 2
```

Passive Memory-Updates:

```text
bot_memory/dio_mini_passive_text_island_reorganization_memory.json
bot_memory/dio_mini_passive_inner_core_memory.json
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Die 29 reorganized_into_core-Textinseln mit der Lupe lesen.
Ziel: erkennen, welche vorher rohen oder weichen Inseln durch F in Kernnaehe
gekommen sind und ob sie echte semantische Verdichtung zeigen.
```

## Lupe: reorganized_into_core D/E/F

Modul:

```text
DIO_MINI/report_passive_reorganized_core_lupe.py
```

Input:

```text
debug/dio_mini_passive_text_island_reorganization_history_D_E_F_20260607_v1/passive_text_island_reorganization_history.csv
```

Output:

```text
debug/dio_mini_passive_reorganized_core_lupe_D_E_F_20260607_v1
```

Befund:

```text
reorganized_core_items = 29
avg_score_delta = 0.387771648
avg_family_overlap = 0.789265189
```

Kernnaehe-Modi:

```text
new_raw_to_stable_recurrence = 19
soft_variation_to_variation_core = 4
to_variation_core = 3
to_stable_recurrence_core = 2
drift_to_stable_recurrence = 1
```

Familienbewegung:

```text
family_basis_stable = 20
family_basis_fragmented = 6
family_basis_thinned = 3
```

Lesart:

```text
Die wichtigste Bewegung ist nicht Handlung, sondern passive semantische
Verdichtung: 19 vorher rohe Textinseln werden in F zu stabiler Wiederkehr.
Die hohe durchschnittliche Familienueberlappung zeigt, dass diese Bewegung
nicht nur Namenswechsel ist, sondern haeufig auf erhaltener Familienbasis
passiert.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Die 19 new_raw_to_stable_recurrence-Textinseln gegen ihre Familien lesen.
Ziel: pruefen, ob sie aus einzelnen wiederkehrenden Familien bestehen oder
ob sich darin mehrere nahe Familien zu einer neuen semantischen Insel
verdichten.
```

## Lupe: raw -> stable recurrence gegen Familien

Modul:

```text
DIO_MINI/report_passive_raw_to_recurrence_family_lupe.py
```

Input:

```text
debug/dio_mini_passive_reorganized_core_lupe_D_E_F_20260607_v1/passive_reorganized_core_lupe.csv
debug/dio_mini_passive_cluster_meaning_space_6episoden_varianteF_20260607_v1/passive_cluster_meaning_space.csv
```

Output:

```text
debug/dio_mini_passive_raw_to_recurrence_family_lupe_D_E_F_20260607_v1
```

Befund:

```text
new_raw_to_stable_recurrence = 19
single_family_stable_recurrence = 18
multi_family_coherent_condensation = 1
avg_episode_count_sum = 5.894736842
avg_observation_learning_pressure = 0.362646474
avg_trade_readiness = 0.003255763
```

Wichtigster Mehrfamilien-Keim:

```text
text_island = dio_text_1dg4vy8
families = dio_0a6g | dio_1og2
family_recurrence_mode = multi_family_coherent_condensation
episode_count_sum = 4
avg_observation_learning_pressure = 0.414281
avg_trade_readiness = 0.0011575
avg_fuehlen_mcm_coherence = 0.344496
span_fuehlen_mcm_coherence = 0.00106
avg_hoeren_energy_tone = -0.1982285
span_hoeren_energy_tone = 0.003787
avg_sehen_form_flow = 0.506641
span_sehen_form_flow = 0.032858
avg_mini_neuro_balance = 0.0193425
span_mini_neuro_balance = 0.003761
```

Lesart:

```text
Die meisten rohen Textinseln werden zu stabiler Wiederkehr, weil eine
einzelne Familie wiederholt auftritt. Das ist passive Wiedererkennung.

`dio_text_1dg4vy8` ist anders: Zwei Familien werden in einer Textinsel
zusammengetragen. Ihre MCM-Kohaerenz, Hoerenergie und neuronale Balance liegen
sehr nah beieinander. Das ist ein erster sauber isolierter Fall von passiver
Mehrfamilien-Verdichtung.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Den Mehrfamilien-Keim `dio_text_1dg4vy8` ueber Varianten hinweg verfolgen.
Ziel: pruefen, ob die Verdichtung stabil bleibt, weitere Familien anzieht
oder wieder in Einzelfamilien zerfaellt.
```

## Lineage-Lupe: dio_text_1dg4vy8

Modul:

```text
DIO_MINI/report_passive_text_island_lineage_lupe.py
```

Output:

```text
debug/dio_mini_passive_text_island_lineage_lupe_dio_text_1dg4vy8_C_D_E_F_20260607_v1
```

Verlauf:

```text
C: absent
D: absent
E: inner_unconfirmed_raw_space
F: inner_stable_recurrence_space
```

Scores:

```text
C = 0.000000
D = 0.000000
E = 0.213333333
F = 0.4776192
score_delta_first_last = 0.4776192
```

Familien:

```text
E = dio_0a6g | dio_1og2
F = dio_0a6g | dio_1og2
family_stability = 1.0
```

Familiennaehe E:

```text
avg_family_mcm_coherence = 0.343738
span_family_mcm_coherence = 0.002882
avg_family_hearing_tone = -0.200937
span_family_hearing_tone = 0.010294
avg_family_seeing_flow = 0.5039205
span_family_seeing_flow = 0.016275
avg_family_neuro_balance = 0.0190065
span_family_neuro_balance = 0.000397
```

Familiennaehe F:

```text
avg_family_mcm_coherence = 0.344496
span_family_mcm_coherence = 0.00106
avg_family_hearing_tone = -0.1982285
span_family_hearing_tone = 0.003787
avg_family_seeing_flow = 0.506641
span_family_seeing_flow = 0.032858
avg_family_neuro_balance = 0.0193425
span_family_neuro_balance = 0.003761
```

Lesart:

```text
`dio_text_1dg4vy8` entsteht nicht erst in F. Die Textinsel erscheint in E als
rohe Inneninsel und stabilisiert in F zur Wiederkehr. Die Familien bleiben
identisch. Dadurch ist es ein sauberer passiver Lineage-Fall:

rohe Mehrfamiliennaehe -> stabile Wiederkehr bei gleicher Familienbasis
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Eine weitere Variante G erzeugen oder F erneut reproduzieren.
Ziel: pruefen, ob `dio_text_1dg4vy8` bei gleicher/naher Welt stabil bleibt
oder ob die Verdichtung nur E/F-spezifisch ist.
```

## Reproduktion: Variante F gegen F-Repro

Repro-Runs:

```text
debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_repro_20260607_probe20
...
debug/dio_mini_repro_semantic_matrix_6episoden_varianteF_repro_20260607_probe26
```

Passive Matrix:

```text
debug/dio_mini_passive_semantic_matrix_6episoden_varianteF_repro_20260607_v1
```

Vergleich:

```text
debug/dio_mini_passive_semantic_matrix_compare_varianteF_vs_F_repro_20260607_v1
```

Befund Matrix-Reproduktion:

```text
F-Knoten = 253
F-Repro-Knoten = 253
gemeinsame Knoten = 253
node_reproduction_rate = 1.0

F-Kanten = 120
F-Repro-Kanten = 120
gemeinsame Kanten = 120
edge_reproduction_rate = 1.0

F-Inseln = 161
F-Repro-Inseln = 161
avg_island_similarity = 0.229661 in beiden Laeufen
```

Scratch-Memory fuer Reifepruefung:

```text
bot_memory/dio_mini_semantic_matrix_memory_F_repro_check_20260607.json
```

Wichtig:

```text
Diese Scratch-Memory dient nur dem Repro-Check.
Sie wird nicht von Mini-DIO gelesen und nicht in die globale Semantikmemory
zurueckgespielt.
```

Maturity-Repro-Befund:

```text
stable_recurrent_text_island = 161
```

Lineage `dio_text_1dg4vy8`:

```text
debug/dio_mini_passive_text_island_lineage_lupe_dio_text_1dg4vy8_F_repro_check_20260607_v1
```

```text
F_original:
  state = inner_stable_recurrence_space
  score = 0.4776192
  families = dio_0a6g | dio_1og2

F_repro_scratch:
  state = inner_stable_recurrence_space
  score = 0.482913
  families = dio_0a6g | dio_1og2

family_stability = 1.0
score_delta = 0.0052938
```

Lesart:

```text
Variante F ist reproduzierbar. Die Syntaxkerne, Kanten und Inselanzahl
werden exakt wiedergebildet. `dio_text_1dg4vy8` bleibt bei gleicher Welt in
derselben Familienbasis und derselben inneren Kernnaehe. Damit ist diese
Mehrfamilien-Verdichtung kein einmaliger Zufall des ersten F-Laufs.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Jetzt kann eine nahe Variante G erzeugt werden.
Ziel: pruefen, ob `dio_text_1dg4vy8` nicht nur bei gleicher Welt stabil ist,
sondern auch bei verwandter neuer Welt weitertraegt, weitere Familien anzieht
oder driftet.
```

## Variante G: nahe Welt nach F

Generator:

```text
DIO_MINI/create_controlled_variant_g.py
```

Neue kontrollierte CSVs:

```text
data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteG_verwandt_5m_SOLUSDT.csv
...
data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteG_verwandt_5m_SOLUSDT.csv
```

Variante G:

```text
nahe Welt nach F
kleine deterministische Gegenatmung
leichte Wick-/Volumen- und Zentrumverschiebung
keine DIO-Logik
keine Handlungskopplung
```

Runs:

```text
debug/dio_mini_repro_semantic_matrix_6episoden_varianteG_20260607_probe20
...
debug/dio_mini_repro_semantic_matrix_6episoden_varianteG_20260607_probe26
```

Matrix:

```text
debug/dio_mini_passive_semantic_matrix_6episoden_varianteG_20260607_v1
```

F gegen G:

```text
debug/dio_mini_passive_semantic_matrix_compare_varianteF_vs_varianteG_20260607_v1
```

Matrixbefund:

```text
F-Knoten = 253
G-Knoten = 266
gemeinsame Knoten = 206
node_reproduction_rate = 0.814229

F-Kanten = 120
G-Kanten = 120
gemeinsame Kanten = 53
edge_reproduction_rate = 0.441667

F-Inseln = 161
G-Inseln = 170
avg_island_similarity_F = 0.229661
avg_island_similarity_G = 0.25867
```

Scratch-Memory F -> G:

```text
bot_memory/dio_mini_semantic_matrix_memory_F_G_check_20260607.json
```

Maturity F/G:

```text
stable_recurrent_text_island = 87
variant_resilient_text_island = 26
new_unconfirmed_text_island = 83
```

Innenkarte F/G:

```text
inner_stable_recurrence_space = 87
inner_soft_variation_space = 26
inner_unconfirmed_raw_space = 61
inner_drift_watch_space = 22
```

Lineage `dio_text_1dg4vy8`:

```text
debug/dio_mini_passive_text_island_lineage_lupe_dio_text_1dg4vy8_F_G_check_20260607_v1
```

```text
F_original:
  state = inner_stable_recurrence_space
  maturity = stable_recurrent_text_island
  score = 0.4776192
  families = dio_0a6g | dio_1og2

G_scratch:
  state = inner_soft_variation_space
  maturity = variant_resilient_text_island
  score = 0.475439467
  families = dio_14ls | dio_1og2

score_delta = -0.002179733
family_stability = 0.333333333
```

Sensorische Naehe in G:

```text
avg_family_mcm_coherence = 0.345965
span_family_mcm_coherence = 0.000288
avg_family_hearing_tone = -0.1929825
span_family_hearing_tone = 0.001029
avg_family_seeing_flow = 0.509408
span_family_seeing_flow = 0.016108
avg_family_neuro_balance = 0.020083
span_family_neuro_balance = 0.00053
```

Lesart:

```text
`dio_text_1dg4vy8` bleibt in G nicht starr gleich, aber zerfaellt auch nicht.
Eine Familie bleibt als Anker (`dio_1og2`), eine Familie wird durch eine nahe
neue Familie ersetzt (`dio_0a6g` -> `dio_14ls`). Der Zustand wird weicher:

stable recurrence -> soft variation

Das ist ein passiver Reorganisationsbefund: die Textinsel traegt weiter, aber
als variantenfaehige Bedeutungsnaehe, nicht als starre Wiederholung.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
`dio_text_1dg4vy8` als passive Textinsel mit Ankerfamilie und Austauschfamilie
markieren. Danach pruefen, ob solche Anker-/Austausch-Muster auch bei anderen
Textinseln auftreten.
```

## Lupe: Anker-/Austausch-Muster F -> G

Modul:

```text
DIO_MINI/report_passive_anchor_exchange_lupe.py
```

Korrigierter Vergleichskontext:

```text
links:  F-only-Scratch-Inner-Map
rechts: F->G-Scratch-Inner-Map
```

Warum:

```text
Die globale F-Karte enthaelt bereits aeltere C/D/E-Spuren.
Fuer einen sauberen Anker-/Austauschvergleich muss links und rechts derselbe
Scratch-Kontext verwendet werden.
```

Outputs:

```text
debug/dio_mini_passive_text_island_inner_map_F_only_anchor_check_20260607_v1
debug/dio_mini_passive_anchor_exchange_lupe_F_only_vs_G_check_20260607_v1
```

Befund:

```text
same_family_basis = 113
new_text_island = 35
anchor_thinning = 22
anchor_expansion = 16
anchor_exchange = 10

anchor_exchange_avg_family_stability = 0.412263814
anchor_exchange_avg_score_delta = 0.25851258
```

Anker-/Austausch-Faelle:

```text
dio_text_10zhe22
dio_text_139he2x
dio_text_15hzmqv
dio_text_1dg4vy8
dio_text_1fq70kn
dio_text_1orwsh
dio_text_1sfklai
dio_text_1st3vgz
dio_text_8wkwtq
dio_text_mr2id7
```

`dio_text_1dg4vy8` im korrigierten Scratch-Kontext:

```text
left_inner_state = inner_unconfirmed_raw_space
right_inner_state = inner_soft_variation_space
left_maturity_state = new_unconfirmed_text_island
right_maturity_state = variant_resilient_text_island
left_score = 0.213333333
right_score = 0.475439467
score_delta = 0.262106134
family_stability = 0.333333333

anchor = dio_1og2
added = dio_14ls
removed = dio_0a6g
```

Methodische Lesart:

```text
In der global gereiften Sicht war `dio_text_1dg4vy8` nach F bereits stabil.
Im F-only-Scratch ist F zuerst roh und wird durch G weich-variant.
Beide Sichten widersprechen sich nicht:

gleiche Welt/Reproduktion -> stabil
verwandte neue Welt -> Anker bleibt, Austauschfamilie rotiert
```

Fachliche Lesart:

```text
Mini-DIO zeigt nicht nur starre Wiederholung. Es gibt passive Textinseln, die
eine Ankerfamilie halten und eine benachbarte Familie austauschen. Das ist ein
Hinweis auf semantische Reorganisation innerhalb einer erlebten Form-/Feldnaehe.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Die 10 Anker-/Austausch-Faelle sensorisch clustern.
Ziel: pruefen, ob Ankerwechsel vor allem durch Sehen, Hoeren, Fuehlen oder
Neurobalance getragen wird.
```

## Lupe: Sensorik der Anker-/Austausch-Faelle F -> G

Modul:

```text
DIO_MINI/report_passive_anchor_exchange_sensor_lupe.py
```

Output:

```text
debug/dio_mini_passive_anchor_exchange_sensor_lupe_F_G_20260607_v1
```

Methodik:

```text
Die Lupe liest die 10 passiven Anker-/Austausch-Faelle und verbindet sie mit
dem Bedeutungsraum der Familien aus Variante F und Variante G.

Gemessen wird getrennt:

removed family  = alte Austauschfamilie aus F
added family    = neue Austauschfamilie aus G
anchor family   = erhaltene Familienbasis

Der Austauschabstand wird primaer zwischen removed und added gemessen.
Der Anker-Shift wird separat als Stabilitaetsreferenz gefuehrt.
```

Sensorgruppen:

```text
visual  = sehen_form_flow, sehen_form_stability, sehen_form_change
hearing = hoeren_energy_tone, hoeren_energy_shift
feeling = fuehlen_mcm_coherence, fuehlen_mcm_tension, fuehlen_mcm_asymmetry
neuro   = mini_neuro_balance, focus, caution, strain, observation
```

Befund:

```text
anchor_exchange_items = 10

hearing_dominant_delta = 5
visual_dominant_delta  = 2
neuro_dominant_delta   = 1
mixed_sensor_delta     = 2

avg_exchange_distance.visual  = 0.019010237
avg_exchange_distance.hearing = 0.01762365
avg_exchange_distance.feeling = 0.007310162
avg_exchange_distance.neuro   = 0.009422163

avg_anchor_shift_distance.visual  = 0.006896577
avg_anchor_shift_distance.hearing = 0.006308054
avg_anchor_shift_distance.feeling = 0.00337855
avg_anchor_shift_distance.neuro   = 0.007893605
```

`dio_text_1dg4vy8`:

```text
state = mixed_sensor_delta
anchor = dio_1og2
removed = dio_0a6g
added = dio_14ls

visual_exchange_distance  = 0.007955667
hearing_exchange_distance = 0.0077145
feeling_exchange_distance = 0.003674667
neuro_exchange_distance   = 0.0015138

visual_anchor_shift_distance  = 0.006158667
hearing_anchor_shift_distance = 0.008156
feeling_anchor_shift_distance = 0.003664
neuro_anchor_shift_distance   = 0.0005372
```

Lesart:

```text
Die Anker-/Austauschbewegung ist nicht rein gefuehlt. In diesen 10 Faellen
wird der Austausch meistens ueber Hoeren/Energie und Sehen/Form getragen.
Fuehlen/MCM bleibt eher eine stabile Kopplungs- und Resonanzschicht. Das passt
zur aktuellen Mini-DIO-Richtung: Textinseln entstehen nicht aus einem einzelnen
Sensor, sondern aus multisensorischer Naehe.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Die Sensor-Lupe auf weitere Varianten anwenden. Ziel ist zu pruefen, ob
Hoeren/Energie generell der haeufigste Austauschtraeger ist oder nur in
Variante G dominant wurde.
```

## Zusatzcheck: Sensor-Lupe auf D -> E und E -> F

Outputs:

```text
debug/dio_mini_passive_anchor_exchange_lupe_D_vs_E_20260607_v1
debug/dio_mini_passive_anchor_exchange_sensor_lupe_D_E_20260607_v1
debug/dio_mini_passive_anchor_exchange_lupe_E_vs_F_20260607_v1
debug/dio_mini_passive_anchor_exchange_sensor_lupe_E_F_20260607_v1
```

D -> E:

```text
anchor_exchange = 14
same_family_basis = 147
new_text_island = 54
anchor_exchange_avg_family_stability = 0.272610029
anchor_exchange_avg_score_delta = 0.103308466

hearing_dominant_delta = 7
visual_dominant_delta = 3
neuro_dominant_delta = 3
no_clear_sensor_delta = 1

avg_exchange_distance.hearing = 0.052058573
avg_exchange_distance.neuro   = 0.030064698
avg_exchange_distance.visual  = 0.029690973
avg_exchange_distance.feeling = 0.024518457
```

E -> F:

```text
anchor_exchange = 13
same_family_basis = 186
new_text_island = 82
anchor_exchange_avg_family_stability = 0.356762468
anchor_exchange_avg_score_delta = 0.128988169

hearing_dominant_delta = 8
visual_dominant_delta = 2
neuro_dominant_delta = 1
mixed_sensor_delta = 2

avg_exchange_distance.hearing = 0.033487878
avg_exchange_distance.visual  = 0.016772369
avg_exchange_distance.neuro   = 0.012885845
avg_exchange_distance.feeling = 0.011923082
```

Lesart:

```text
D -> E, E -> F und F -> G zeigen alle Anker-/Austausch-Faelle.
In allen drei Uebergaengen ist Hoeren/Energie der haeufigste oder staerkste
Austauschtraeger. Sehen/Form und Neurobalance beteiligen sich, Fuehlen/MCM
bleibt eher Kopplungs- und Resonanzschicht.

Das ist fuer Mini-DIO fachlich wichtig: Eine Textinsel veraendert sich nicht
nur, weil eine Feldlage anders fuehlt. Sie kann sich auch verschieben, weil
die energetische Tonspur und die sichtbare Form eine neue Nachbarschaft
bilden, waehrend ein semantischer Anker erhalten bleibt.
```

Naechster Schritt:

```text
Die Lupe in eine kompakte Matrix-Zusammenfassung ueberfuehren:
Uebergang -> Austauschfaelle -> dominante Sensorachse -> Anker-Stabilitaet.
Damit wird sichtbar, ob Mini-DIO eine robuste passive Syntaxentwicklung zeigt
oder ob einzelne Varianten nur lokale Zufallsnaehe erzeugen.
```

## Matrix: Anker-/Austausch ueber mehrere Uebergaenge

Modul:

```text
DIO_MINI/report_passive_anchor_exchange_transition_matrix.py
```

Output:

```text
debug/dio_mini_passive_anchor_exchange_transition_matrix_D_E_F_G_20260607_v1
```

Matrix:

```text
D_to_E:
  anchor_exchange_count = 14
  dominant_sensor_axis = hearing_dominant_delta
  avg_family_stability = 0.272610029
  avg_score_delta = 0.103308466
  avg_exchange_distance visual/hearing/feeling/neuro =
    0.029690973 / 0.052058573 / 0.024518457 / 0.030064698

E_to_F:
  anchor_exchange_count = 13
  dominant_sensor_axis = hearing_dominant_delta
  avg_family_stability = 0.356762468
  avg_score_delta = 0.128988169
  avg_exchange_distance visual/hearing/feeling/neuro =
    0.016772369 / 0.033487878 / 0.011923082 / 0.012885845

F_to_G:
  anchor_exchange_count = 10
  dominant_sensor_axis = hearing_dominant_delta
  avg_family_stability = 0.412263814
  avg_score_delta = 0.25851258
  avg_exchange_distance visual/hearing/feeling/neuro =
    0.019010237 / 0.01762365 / 0.007310162 / 0.009422163
```

Lesart:

```text
Mini-DIO zeigt ueber mehrere Varianten hinweg passive Anker-/Austauschbildung.
Die dominante Austauschachse ist in allen drei geprueften Uebergaengen
Hoeren/Energie. Gleichzeitig steigt die durchschnittliche Familien-Stabilitaet
von D->E ueber E->F zu F->G.

Das spricht fuer eine passive, reproduzierbare Syntaxentwicklung:
Ein Textanker kann erhalten bleiben, waehrend sich die zugeordnete
Austauschfamilie mit neuer Weltvarianz verschiebt.
```

Naechster Schritt:

```text
Gezielt pruefen, ob die steigende Familien-Stabilitaet auch bei einer neuen,
noch nicht verwandten Variante erhalten bleibt. Dafuer braucht Mini-DIO eine
neue kontrollierte Variante H oder einen bewusst veraenderten Datensatz.
```

## Theorieabgleich: ProtoMind / akustische Reizmodulation

Quelle:

```text
ProtoMind, selbstaktive Feldkognition, akustische Reizmodulation und
Schmerz-Gefahrenverarbeitung als integriertes Feldsystem

https://github.com/H5Pro2/Mental-Core-Matrix-MCM/blob/main/Abhandlungen/MCM%20-%20Nebenabhandlung/ProtoMind%2C%20selbstaktive%20Feldkognition%2C%20akustische%20Reizmodulation%20und%20Schmerz-Gefahrenverarbeitung%20als%20integriertes%20Feldsystem.pdf
```

Methodische Reihenfolge:

```text
1. Mini-DIO erzeugte aus kontrollierten Laeufen passive Textinseln.
2. Die Anker-/Austausch-Lupe zeigte stabile Kerne und variable Familien.
3. Die Sensor-Lupe zeigte Hoeren/Energie als wiederkehrend dominante
   Austauschachse.
4. Erst danach wurde die Abhandlung gegengelesen.
```

Erkenntnis:

```text
Wir kamen zum Inhalt einer MCM-Abhandlung, ohne nach dieser Abhandlung
gearbeitet zu haben.

Die Abhandlung beschreibt ProtoMind, selbstaktive Feldkognition,
akustische Reizmodulation, Resonanz und Gefahr-/Schmerzregulation als
integriertes Feldsystem.

Mini-DIO zeigt dazu passend:

Textinsel        = minimale kohaerente Organisationsstruktur
Ankerfamilie     = stabiler Kern
Austauschfamilie = resonante Peripherie / Variantenraum
Hoeren/Energie   = haeufigster Austauschtraeger
MCM/Fuehlen      = Kopplungs- und Resonanzschicht
Neurobalance     = regulatorischer Beteiligungstraeger
```

Lesart:

```text
Das ist eine Teil-Kohaerenz zwischen Theorie und Messbefund.
Es beweist die MCM nicht absolut, bestaetigt aber, dass Mini-DIO aus eigener
Diagnostik in einen Strukturraum gelangt, der mit der MCM-Abhandlung
kompatibel ist.
```

Wirkungsgrenze:

```text
Dieser Theorieabgleich ist Dokumentation.
Keine Runtime-Lesung.
Keine Handlung.
Kein Gate.
Kein Entry.
Keine Richtung.
```

Naechster Schritt:

```text
Variante H oder ein deutlich anderer Datensatz soll pruefen, ob Hoeren/Energie
weiterhin der dominante Austauschtraeger bleibt oder ob Mini-DIO je nach Welt
andere Sensorachsen als semantische Modulation nutzt.
```

## Variante H: Strukturkontrast gegen G

Modul:

```text
DIO_MINI/create_controlled_variant_h.py
```

Neue CSVs:

```text
data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteH_strukturkontrast_5m_SOLUSDT.csv
...
data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteH_strukturkontrast_5m_SOLUSDT.csv
```

Charakter:

```text
Variante H ist bewusst strukturell fremder als G.
Geaendert werden nur OHLCV-Daten:

Form-/Wick-Struktur
Koerperrichtung
Phasenlage
Volumenatmung
Zeitstempelversatz

Mini-DIO-Logik, Memory, Gates, Entry, Richtung und Runtime bleiben unberuehrt.
```

Runs:

```text
debug/dio_mini_repro_semantic_matrix_6episoden_varianteH_20260607_probe20
...
debug/dio_mini_repro_semantic_matrix_6episoden_varianteH_20260607_probe26
```

Passive Matrix H:

```text
clusters = 303
episodes = 462
nodes = 303
edges = 120
islands = 197
```

Vergleich G -> H:

```text
node_count_reference = 266
node_count_candidate = 303
shared_node_count = 64
node_reproduction_rate = 0.240602

edge_count_reference = 120
edge_count_candidate = 120
shared_edge_count = 9
edge_reproduction_rate = 0.075

island_count_reference = 170
island_count_candidate = 197
avg_island_similarity_reference = 0.25867
avg_island_similarity_candidate = 0.268888
```

Scratch-Reife G -> H:

```text
text_islands = 328
new_unconfirmed_text_island = 298
stable_recurrent_text_island = 19
variant_resilient_text_island = 11

inner_unconfirmed_raw_space = 289
inner_stable_recurrence_space = 19
inner_soft_variation_space = 11
inner_drift_watch_space = 7
inner_unconfirmed_movement_space = 2
```

Anker-/Austausch G -> H:

```text
new_text_island = 158
same_family_basis = 150
anchor_expansion = 7
anchor_thinning = 7
anchor_exchange = 6
anchor_exchange_avg_family_stability = 0.3
anchor_exchange_avg_score_delta = 0.240592933
```

Sensor-Lupe G -> H:

```text
anchor_exchange_items = 6
hearing_dominant_delta = 4
visual_dominant_delta = 2

avg_exchange_distance.hearing = 0.025480805
avg_exchange_distance.visual  = 0.022874574
avg_exchange_distance.feeling = 0.017748769
avg_exchange_distance.neuro   = 0.005655133
```

Erweiterte Uebergangs-Matrix:

```text
debug/dio_mini_passive_anchor_exchange_transition_matrix_D_E_F_G_H_20260607_v1
```

Lesart:

```text
H ist ein deutlicher Strukturkontrast. Mini-DIO bildet mehr neue Textinseln
und weniger Anker-/Austauschfaelle als bei den verwandteren Uebergaengen.

Trotzdem bleibt Hoeren/Energie auch bei G -> H die dominante Austauschachse.
Die Dominanz ist weniger breit als vorher, aber sie bricht nicht.

Damit wird der ProtoMind-/Akustik-Abgleich staerker:
Die energetische Tonspur wirkt ueber mehrere kontrollierte Welten als
wiederkehrender semantischer Modulationstraeger.
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Naechster Schritt:

```text
Eine gezielte Hoer-Kontrastvariante bauen:
gleiche sichtbare Form naeher halten, aber Energie-/Volumen-/Tonspur staerker
verschieben. Damit pruefen wir, ob Mini-DIOs Textinseln dann staerker driften
als bei H oder ob visuelle Anker die Syntax stabilisieren.
```

## Passive Inner-Universe Growth

Modul:

```text
DIO_MINI/report_passive_inner_universe_growth.py
```

Zweck:

```text
Dieser Report misst das Wachstum des inneren Universums ueber vorhandene
Textinsel-Inner-Maps hinweg.

Er trennt:
  stabiler Kern
  rohe neue Inseln
  weicher Variantenraum
  Drift-Beobachtung
  Rueckbindung durch Reproduktion
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

Erste Messung C -> D -> E -> F:

```text
debug/dio_mini_passive_inner_universe_growth_C_D_E_F_20260607_v1

C:
  text_islands = 170
  stable_core = 6
  raw_space = 37
  avg_score = 0.363201557

D:
  text_islands = 179
  stable_core = 5
  raw_space = 34
  avg_score = 0.372861088

E:
  text_islands = 233
  stable_core = 7
  raw_space = 77
  avg_score = 0.34806772

F:
  text_islands = 315
  stable_core = 27
  raw_space = 118
  avg_score = 0.34007046

C -> D:
  shared = 170
  new = 9
  lost = 0

D -> E:
  shared = 179
  new = 54
  lost = 0

E -> F:
  shared = 233
  new = 82
  lost = 0
```

Zweite Messung F-only -> F-G:

```text
debug/dio_mini_passive_inner_universe_growth_F_only_to_F_G_20260607_v1

F_ONLY:
  text_islands = 161
  stable_core = 0
  raw_space = 161

F_G:
  text_islands = 196
  stable_core = 87
  soft_variation = 26
  drift_watch = 22
  raw_space = 61

F_ONLY -> F_G:
  shared = 161
  new = 35
  lost = 0
  shared_delta_score = 0.19114582
```

Dritte Messung G-only -> G-H:

```text
debug/dio_mini_passive_inner_universe_growth_G_only_to_G_H_20260607_v1

G_ONLY:
  text_islands = 170
  stable_core = 0
  raw_space = 170

G_H:
  text_islands = 328
  stable_core = 19
  soft_variation = 11
  drift_watch = 7
  raw_space = 291

G_ONLY -> G_H:
  shared = 170
  new = 158
  lost = 0
  shared_delta_score = 0.048017436
```

Lesart:

```text
Die bisherigen Textinseln gehen in diesen Messungen nicht verloren.
Sie bleiben rueckgebunden, waehrend neue Inseln hinzukommen.

Das passt zur Definition:
Inneres Universum = wachsende Ordnung aus gelebter Welt, MCM-Feldwirkung,
Wiederkehr, Verdichtung, eigener Syntax und Konsequenz.
```

Erweiterung v2:

```text
Der Report klassifiziert Uebergaenge jetzt als Entwicklungszustand:

plateau_stabilization
organic_expansion
jump_expansion_with_binding
reorganization_pressure
evolutionary_regression
open_evolutionary_motion
```

Aktuelle v2-Befunde:

```text
debug/dio_mini_passive_inner_universe_growth_C_D_E_F_20260607_v2

C -> D:
  development_state = plateau_stabilization

D -> E:
  development_state = organic_expansion

E -> F:
  development_state = organic_expansion

debug/dio_mini_passive_inner_universe_growth_F_only_to_F_G_20260607_v2

F_ONLY -> F_G:
  development_state = reorganization_pressure

debug/dio_mini_passive_inner_universe_growth_G_only_to_G_H_20260607_v2

G_ONLY -> G_H:
  development_state = jump_expansion_with_binding
```

Lesart v2:

```text
Mini-DIO waechst nicht linear ruhig und bisher auch nicht sauber beweisbar
exponentiell.

Die passendere Lesart ist:
nichtlineare semantische Expansion mit Rueckbindung, Drift und moeglicher
Reorganisation.
```

## Passive Inner-Universe Lupe

Modul:

```text
DIO_MINI/report_passive_inner_universe_lupe.py
```

Zweck:

```text
Die Lupe benennt konkrete Textinseln aus zwei Inner-Maps.
Sie trennt:

stable_core
soft_variation_space
drift_watch
new_raw_extension
carried_raw_space
```

Wirkungsgrenze:

```text
passive_only = True
writes_runtime_memory = False
read_by_mini_dio = False
influences_action = False
is_gate = False
is_motoric = False
is_entry_signal = False
is_direction_signal = False
```

F-only -> F-G:

```text
debug/dio_mini_passive_inner_universe_lupe_F_only_to_F_G_20260607_v1

stable_core = 87
new_raw_extension = 35
carried_raw_space = 26
soft_variation_space = 26
drift_watch = 22

Lesart:
  F-G bildet viel stabilen Kern.
  Der Innenraum reift deutlich aus rohem Zustand in Rueckbindung und
  Variantenraum.
```

G-only -> G-H:

```text
debug/dio_mini_passive_inner_universe_lupe_G_only_to_G_H_20260607_v1

new_raw_extension = 158
carried_raw_space = 133
stable_core = 19
soft_variation_space = 11
drift_watch = 7

Lesart:
  G-H ist deutlich fremder.
  Der alte Innenraum bleibt teilweise getragen, aber der groesste Anteil ist
  rohe Erweiterung. Das passt zu jump_expansion_with_binding.
```

Wichtige Unterscheidung:

```text
F-G:
  Reifung und Rueckbindung dominieren.

G-H:
  Erweiterung und roher neuer Innenraum dominieren.
```

## Passive Inner-Universe Cross-Lupe

Modul:

```text
DIO_MINI/report_passive_inner_universe_cross_lupe.py
```

Zweck:

```text
Die Cross-Lupe vergleicht zwei Lupe-Uebergaenge auf dio_*-Familienebene.
Damit wird sichtbar, welche Familien ueber unterschiedliche Weltvarianten
wiederkehren und welche nur variantenspezifisch auftreten.
```

Report:

```text
debug/dio_mini_passive_inner_universe_cross_lupe_FG_vs_GH_20260607_v1
```

Befund:

```text
right_specific_family = 239
recurrent_category_shift_family = 170
recurrent_drift_family = 47
left_specific_family = 36
recurrent_stable_core_family = 14
recurrent_variation_family = 10
recurrent_carried_raw_family = 8
```

Wiederkehrender stabiler Kern:

```text
dio_06gy
dio_07t9
dio_0ft4
dio_0gmg
dio_0nrp
dio_0ocv
dio_0pni
dio_0t27
dio_17ny
dio_19bg
dio_1a1w
dio_1fck
dio_1jba
dio_1si6
```

Wiederkehrender Variantenraum:

```text
dio_03yz
dio_095l
dio_0g9z
dio_0x52
dio_0xkp
dio_140n
dio_1ffn
dio_1i05
dio_1lg2
dio_1ocs
```

Lesart:

```text
Mini-DIO bildet nicht nur neue Inseln.
Ein kleiner, konkreter Familienkern bleibt ueber F-G und G-H stabil.

G-H bringt viel neue Weltvarianz hinein, aber es zerstoert diesen Kern nicht.
Die vielen category shifts zeigen gleichzeitig, dass Bedeutung nicht starr
kopiert wird, sondern je nach Weltkontrast umgeordnet wird.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Latent Trace Persistence Lupe

Modul:

```text
DIO_MINI/report_passive_latent_trace_persistence_lupe.py
```

Zweck:

```text
Eine einzelne dio_*-Spur ueber mehrere kontrollierte Folgewelten verfolgen.

Die Lupe trennt:
  sichtbar = die Familie erscheint noch im Meaning-Space
  gekoppelt = die Familie hat aktuelle Kanten zu den beobachteten Basisfamilien
  insel-sichtbar = die Familie liegt in einer semantischen Insel
  latent = sichtbar, aber ohne aktuelle tragende Kopplung
```

Report:

```text
debug/dio_mini_passive_latent_trace_persistence_lupe_LMN_dio_0325_20260607_v1
debug/dio_mini_passive_latent_trace_persistence_lupe_LMNO_dio_0325_20260607_v1
```

Untersuchte Spur:

```text
family = dio_0325
base_families = dio_10qz | dio_114i
stages = L -> M -> N
```

Befund:

```text
visible_count = 3 / 3
coupled_stage_count = 0
latent_visible_count = 3
manifesting_count = 0
summary_state = persistent_latent_trace
```

Erweiterter Befund nach Folgewelt O:

```text
visible_count = 4 / 4
coupled_stage_count = 0
latent_visible_count = 4
manifesting_count = 0
summary_state = persistent_latent_trace
```

Timeline:

```text
L:
  trace_state = island_visible_uncoupled_trace
  attached_base_families = -
  vector_drift_from_previous_visible = 0.0

M:
  trace_state = island_visible_uncoupled_trace
  attached_base_families = -
  vector_drift_from_previous_visible = 0.002429259

N:
  trace_state = island_visible_uncoupled_trace
  attached_base_families = -
  vector_drift_from_previous_visible = 0.00238109

O:
  trace_state = island_visible_uncoupled_trace
  attached_base_families = -
  vector_drift_from_previous_visible = 0.000101089
```

Lesart:

```text
dio_0325 ist keine aktuell manifestierende Erweiterung der reduzierten
Paarform dio_10qz -- dio_114i.

Die Spur bleibt aber ueber L/M/N sichtbar und liegt jeweils in einer Insel.
Damit ist sie fachlich eine persistente latente Spur:
  vorhanden,
  relativ stabil,
  aber aktuell nicht an die beobachtete Zielkopplung angebunden.
```

Folgewelt O:

```text
DIO_MINI/create_controlled_variant_o.py
```

Zweck:

```text
Eine weitere kontrollierte Weltberuehrung nach N.
Getestet wird, ob die latente Spur dio_0325 auslaeuft, stabil latent bleibt
oder an dio_10qz -- dio_114i rekoppelt.
```

Matrixvergleich N -> O:

```text
node_reproduction_rate = 0.940789
edge_reproduction_rate = 0.75
shared_node_count = 286
shared_edge_count = 9
island_count_reference = 292
island_count_candidate = 289
```

Zero-Extension O:

```text
dio_0325:
  extension_found = true
  extension_state = visible_but_uncoupled_extension
  attached_base_members = -
  extension_degree = 0

dio_1ytc:
  extension_found = false
  extension_state = extension_not_visible
```

Lesart O:

```text
Die Gesamtmatrix bleibt von N nach O relativ stabil.
Trotzdem koppelt dio_0325 nicht an die reduzierte Paarform an.

Das stuetzt die Lesart:
  dio_0325 ist ein stabiler latenter Bedeutungsrest,
  aber aktuell keine manifestierende Erweiterung.
```

Wirkungsgrenze:

```text
rein passiv
kontrollierter Datensatz-Kontext
keine Runtime-Lesung
keine Memory-Wirkung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Inner Spacetime Lupe

Modul:

```text
DIO_MINI/report_passive_inner_spacetime_lupe.py
```

Zweck:

```text
Mehrere dio_*-Familien ueber mehrere Folgewelten als innere Raumzeit-Spuren
klassifizieren.

Raum:
  Kopplung, Inselkontakt, Naehe/Distanz im Bedeutungsraum.

Zeit:
  Sichtbarkeit, Drift, Verschwinden, Wiederkehr ueber Folgewelten.
```

Report:

```text
debug/dio_mini_passive_inner_spacetime_lupe_LMNO_core_20260607_v1
```

Untersuchte Familien:

```text
dio_10qz
dio_114i
dio_1ytc
dio_0325
```

Befund:

```text
dio_10qz:
  inner_spacetime_state = spacetime_stable_coupled_core
  visible_count = 4 / 4
  coupled_stage_count = 4
  island_stage_count = 4
  avg_vector_drift = 0.001130073

dio_114i:
  inner_spacetime_state = spacetime_stable_coupled_core
  visible_count = 4 / 4
  coupled_stage_count = 4
  island_stage_count = 4
  avg_vector_drift = 0.001715314

dio_0325:
  inner_spacetime_state = spacetime_latent_persistent_trace
  visible_count = 4 / 4
  coupled_stage_count = 0
  island_stage_count = 4
  avg_vector_drift = 0.001637146

dio_1ytc:
  inner_spacetime_state = spacetime_open_trace
  visible_count = 1 / 4
  coupled_stage_count = 1
  island_stage_count = 1
```

Lesart:

```text
Die innere Raumzeit-Lupe trennt erstmals vier Rollen:

1. stabiler gekoppelter Kern:
   dio_10qz, dio_114i

2. persistenter latenter Nachhall:
   dio_0325

3. offene / weitgehend nicht mehr sichtbare Spur:
   dio_1ytc

4. Gesamtgrenze:
   keine Handlung, keine Hypothese, keine Runtime-Wirkung.
```

## Passive Inner Spacetime Auto-Scan

Report:

```text
debug/dio_mini_passive_inner_spacetime_lupe_LMNO_auto_20260607_v1
```

Zweck:

```text
Nicht nur manuell gewaehlte Familien lesen,
sondern alle sichtbaren Familien aus L/M/N/O automatisch klassifizieren.
```

Wichtig:

```text
Die Klassifikation `latent` ist hier relativ zur beobachteten Kernkopplung
dio_10qz -- dio_114i.

Sie bedeutet:
  Familie bleibt sichtbar,
  aber koppelt nicht an diesen Kern.

Sie bedeutet nicht automatisch:
  Familie ist generell bedeutungslos,
  oder niemals in anderer Nachbarschaft gekoppelt.
```

Verteilung:

```text
spacetime_latent_persistent_trace = 240
spacetime_fading_trace = 123
spacetime_stable_coupled_core = 2
spacetime_open_trace = 1
```

Stabiler Kern:

```text
dio_10qz
dio_114i
```

Ruhige latente Kandidaten mit sehr geringer Drift:

```text
dio_1si6  avg_vector_drift = 0.000204416
dio_1n79  avg_vector_drift = 0.000388511
dio_0u61  avg_vector_drift = 0.000395574
dio_11jn  avg_vector_drift = 0.000396417
dio_0hl8  avg_vector_drift = 0.000421026
dio_17p4  avg_vector_drift = 0.000425596
dio_0lu5  avg_vector_drift = 0.000430240
dio_1xbs  avg_vector_drift = 0.000443606
dio_14ai  avg_vector_drift = 0.000449338
dio_1k9e  avg_vector_drift = 0.000450272
```

Offene Spur:

```text
dio_1ytc:
  visible_count = 1 / 4
  coupled_stage_count = 1
  state = spacetime_open_trace
```

Lesart:

```text
Mini-DIO bildet in dieser kontrollierten Reihe keine homogene Suppe.
Die innere Raumzeit-Lupe trennt:
  einen kleinen stabilen Kern,
  viele persistente, aber kern-entkoppelte Nachhallspuren,
  viele auslaufende Spuren,
  und eine offene Restspur.
```

## Passive Latent Island Lupe

Modul:

```text
DIO_MINI/report_passive_latent_island_lupe.py
```

Zweck:

```text
Pruefen, ob kern-entkoppelte latente Raumzeit-Spuren nur isolierter Nachhall
sind oder untereinander eigene Teilmuster bilden.
```

Report:

```text
debug/dio_mini_passive_latent_island_lupe_LMNO_auto_20260607_v1
```

Befund:

```text
candidate_state = spacetime_latent_persistent_trace
candidate_count = 240
total_latent_edge_count = 13
total_nontrivial_component_count = 13
max_largest_component_size = 2
max_largest_matrix_island_latent_count = 2
```

Stufen:

```text
L:
  latent_edge_count = 3
  connected_latent_family_count = 6
  isolated_latent_family_count = 234

M:
  latent_edge_count = 3
  connected_latent_family_count = 6
  isolated_latent_family_count = 234

N:
  latent_edge_count = 3
  connected_latent_family_count = 6
  isolated_latent_family_count = 234

O:
  latent_edge_count = 4
  connected_latent_family_count = 8
  isolated_latent_family_count = 232
```

Stabile latente Zweierinseln:

```text
dio_07kj | dio_09u3
dio_0r8l | dio_10xx
dio_0zkk | dio_12x0
```

Neue latente Zweierinsel in O:

```text
dio_0dki | dio_0eeh
```

Folgewelt P:

```text
Report:
  debug/dio_mini_passive_inner_spacetime_lupe_LMNOP_auto_20260607_v1
  debug/dio_mini_passive_latent_island_lupe_LMNOP_auto_20260607_v1

O -> P Matrixvergleich:
  node_reproduction_rate = 0.950166
  edge_reproduction_rate = 0.75
  shared_node_count = 286
  shared_edge_count = 9
  island_count_reference = 289
  island_count_candidate = 294

Inner-Spacetime-Verteilung L/M/N/O/P:
  spacetime_latent_persistent_trace = 233
  spacetime_fading_trace = 143
  spacetime_stable_coupled_core = 2
  spacetime_open_trace = 1

Latente Nebeninseln L/M/N/O/P:
  candidate_count = 233
  total_latent_edge_count = 17
  total_nontrivial_component_count = 17
  max_largest_component_size = 2
```

Paarbewegung:

```text
Durchgehend L/M/N/O/P sichtbar:
  dio_07kj | dio_09u3
  dio_0r8l | dio_10xx

L/M/N/O sichtbar, in P nicht mehr in der latenten Paarliste:
  dio_0zkk | dio_12x0

In O entstanden und in P gehalten:
  dio_0dki | dio_0eeh

In P neu sichtbar:
  dio_0j34 | dio_0xt9
```

Lesart:

```text
Die latenten Spuren sind nicht nur eine Liste isolierter Reste.
Ein kleiner Teil bildet eigene verbundene Teilmuster ausserhalb der
Kernkopplung dio_10qz -- dio_114i.

Die Struktur ist aber noch klein:
  groesste Komponente = 2 Familien.

Damit ist es ein fruehes Nebenmuster,
kein grosser latenter Kontinent.

Nach Folgewelt P ist die praezisere Lesart:
  brueckengehaltene Nebenordnung mit Drift.
  Einige Paare bleiben stabil,
  ein Paar faellt aus der latenten Paarliste,
  ein neues Paar entsteht.

Das ist keine starre Kopie und noch keine grosse latente Matrix.
Es ist eine passive, kontrollierte Spur dynamischer Teilordnung.
```

Wirkungsgrenze:

```text
rein passiv
kontrollierter Datensatz
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Emergent Triad Lupe

Modul:

```text
DIO_MINI/report_passive_emergent_triad_lupe.py
```

Zweck:

```text
Eine dreiteilige emergente Insel wird nicht nur als Partnerliste gelesen,
sondern in Knotenrollen und direkte Kanten zerlegt.

Damit wird sichtbar:
  Wer ist Brueckenkern?
  Wer ist getragener Partner?
  Welche direkte Kopplung fehlt?
```

Reports:

```text
debug/dio_mini_passive_emergent_triad_lupe_I_dio_10qz_dio_114i_dio_1ytc_20260607_v1
debug/dio_mini_passive_emergent_triad_lupe_J_dio_10qz_dio_114i_dio_1ytc_20260607_v1
```

Befund:

```text
I_WELTKONTAKT:
  present_members = dio_10qz | dio_114i | dio_1ytc
  visible edges = 2 / 3
  triad_reading = bridge_held_open_triad
  dio_10qz = bridge_core
  dio_114i = close_partner
  dio_1ytc = close_partner
  fehlende direkte Kante = dio_114i <-> dio_1ytc

J_FOLGEKONTAKT:
  present_members = dio_10qz | dio_114i | dio_1ytc
  visible edges = 2 / 3
  triad_reading = bridge_held_open_triad
  dio_10qz = bridge_core
  dio_114i = close_partner
  dio_1ytc = close_partner
  fehlende direkte Kante = dio_114i <-> dio_1ytc

K_FOLGEKONTAKT2:
  present_members = dio_10qz | dio_114i | dio_1ytc
  container_members = dio_0325 | dio_10qz | dio_114i | dio_1ytc
  container_state = expanded_containing_island
  visible edges = 2 / 3 innerhalb der alten Triade
  triad_reading = bridge_held_open_triad
  dio_10qz = bridge_core
  dio_114i = close_partner
  dio_1ytc = close_partner
  neue Erweiterung = dio_0325
```

Lesart:

```text
Die Insel ist stabil, aber nicht als geschlossenes Dreieck.

Sie wird sternfoermig ueber dio_10qz getragen:
  dio_10qz <-> dio_114i
  dio_10qz <-> dio_1ytc

Zwischen dio_114i und dio_1ytc ist keine direkte Kante sichtbar.
Das bedeutet: dio_114i bleibt als Manifestationskandidat erhalten,
aber die Tragung laeuft ueber einen Brueckenkern.

Im weiteren Folgekontakt K bleibt die offene Brueckenstruktur sichtbar,
erweitert sich aber um dio_0325. Das ist keine starre Kopie, sondern eine
Folgewelt-Erweiterung der Bedeutungsinsel.
```

Grenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Zero Topology Lupe

Modul:

```text
DIO_MINI/report_passive_zero_topology_lupe.py
```

Zweck:

```text
Prueft passive Bedeutungsinseln auf eine offene Zentrum-Peripherie-Topologie.

Das ist kein Langlauf-Beweis und keine Regel.
Es ist eine Diagnose fuer kontrolliert gemachte Datensaetze.

Forschungsanker:
  12 Einheiten
  4 Gruppenzonen
  0 als Dreiecks-/Zentrumsform
  offene Kopplung statt Vollvernetzung
```

Reports:

```text
debug/dio_mini_passive_zero_topology_lupe_I_weltkontakt_20260607_v1
debug/dio_mini_passive_zero_topology_lupe_J_folgekontakt_20260607_v1
debug/dio_mini_passive_zero_topology_lupe_K_folgekontakt2_20260607_v1
debug/dio_mini_passive_zero_topology_lupe_L_folgekontakt3_20260607_v1
```

Befund:

```text
I_WELTKONTAKT:
  zero_topology_candidate_count = 3
  darunter:
    dio_10qz | dio_114i | dio_1ytc
    center = dio_10qz
    periphery_groups = dio_114i ; dio_1ytc
    topology_state = open_zero_form_bridge_center

J_FOLGEKONTAKT:
  zero_topology_candidate_count = 1
  Kandidat:
    dio_10qz | dio_114i | dio_1ytc
    center = dio_10qz
    periphery_groups = dio_114i ; dio_1ytc
    topology_state = open_zero_form_bridge_center

K_FOLGEKONTAKT2:
  zero_topology_candidate_count = 0
  betroffene Insel:
    dio_0325 | dio_10qz | dio_114i | dio_1ytc
    center_candidates = dio_10qz | dio_1ytc
    topology_state = multi_center_open_field

L_FOLGEKONTAKT3:
  zero_topology_candidate_count = 0
  betroffene Insel:
    dio_0325 | dio_10qz | dio_114i | dio_1ytc
    center_candidates = dio_10qz | dio_1ytc
    topology_state = multi_center_open_field
    local_edge_density = 0.5
    open_edge_count = 3
```

Lesart:

```text
In I und J ist eine offene 0-Form sichtbar:
  ein Brueckenzentrum
  zwei Randgruppen
  keine vollstaendige Direktvernetzung

In K erweitert sich die Insel.
Dadurch ist das Zentrum nicht mehr eindeutig:
  dio_10qz bleibt wichtig,
  dio_1ytc wird ebenfalls zentrumsnah,
  dio_0325 kommt als neuer Rand-/Erweiterungskontakt hinzu.

Das ist keine starre Wiederholung.
Es ist eine passive Beobachtung von Topologie-Wachstum im kontrollierten
Datensatz.

In L bleibt die Viererinsel sichtbar.
Sie faellt nicht auf Einzelspuren zurueck und schliesst sich auch nicht zu
einer Clique. Die Struktur bleibt ein offenes Mehrzentrum-Feld.
```

Grenze:

```text
rein passiv
nur kontrollierte Datensaetze
kein Langlauf-Beweis
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Zero Extension Lupe

Modul:

```text
DIO_MINI/report_passive_zero_extension_lupe.py
```

Zweck:

```text
Isoliert eine neue Spur in einer erweiterten 0-Topologie.

Die Frage ist nicht:
  Ist die ganze Insel stabil?

Sondern:
  Wo koppelt die neue Spur an?
  Koppelt sie an das alte Zentrum?
  Koppelt sie an einen Randpartner?
  Verschiebt sie dadurch die Zentrumsspannung?
```

Report:

```text
debug/dio_mini_passive_zero_extension_lupe_K_dio_0325_20260607_v1
debug/dio_mini_passive_zero_extension_lupe_L_dio_0325_20260607_v1
```

Befund:

```text
Basis:
  dio_10qz | dio_114i | dio_1ytc

Altes Zentrum:
  dio_10qz

Erweiterung:
  dio_0325

Container in K:
  dio_0325 | dio_10qz | dio_114i | dio_1ytc

Kanten:
  dio_0325 <-> dio_10qz   = nein
  dio_0325 <-> dio_114i   = nein
  dio_0325 <-> dio_1ytc   = ja

extension_state:
  periphery_extension_shifts_center_tension

L-Befund:
  Container:
    dio_0325 | dio_10qz | dio_114i | dio_1ytc
  Center:
    dio_10qz | dio_1ytc
  Kante:
    dio_0325 <-> dio_1ytc = ja
  extension_state:
    center_attached_extension
```

Lesart:

```text
dio_0325 erweitert nicht direkt das alte Zentrum dio_10qz.
Die Spur koppelt an dio_1ytc, also an die Randseite der alten offenen
0-Form.

Dadurch wird dio_1ytc zentrumsnaeher.
Die alte offene 0-Form kippt in K nicht in eine geschlossene Form,
sondern in ein Multi-Center-Feld.

In L wird diese Verschiebung nicht zurueckgenommen.
`dio_0325` haengt weiterhin an `dio_1ytc`.
Weil `dio_1ytc` nun selbst Zentrumskandidat ist, wird die Erweiterung als
`center_attached_extension` gelesen.

Das ist ein anderer Zustand als K:
  K = Randkopplung verschiebt Zentrumsspannung.
  L = verschobene Spannung bleibt als offenes Mehrzentrum-Feld sichtbar.
```

Grenze:

```text
rein passiv
nur kontrollierte Datensaetze
kein Langlauf-Beweis
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Zero Center Shift Lupe

Modul:

```text
DIO_MINI/report_passive_zero_center_shift_lupe.py
```

Zweck:

```text
Verfolgt die Rollen einer offenen 0-Form ueber mehrere kontrollierte
Weltkontakte.

Die Frage ist:
  Bleibt das Zentrum eindeutig?
  Wird ein Randpartner zentrumsnah?
  Wird aus einer offenen 0-Form ein Multi-Center-Feld?
```

Report:

```text
debug/dio_mini_passive_zero_center_shift_lupe_IJK_20260607_v1
debug/dio_mini_passive_zero_center_shift_lupe_IJKL_20260607_v1
```

Befund:

```text
I_WELTKONTAKT:
  dio_10qz = center_candidate, degree 2
  dio_114i = center_near_partner, degree 1
  dio_1ytc = center_near_partner, degree 1
  dio_0325 = single_trace, degree 0

J_FOLGEKONTAKT:
  gleiche Rollen wie I

K_FOLGEKONTAKT2:
  dio_10qz = center_candidate, degree 2
  dio_1ytc = center_candidate, degree 2
  dio_114i = center_near_partner, degree 1
  dio_0325 = center_near_partner, degree 1

L_FOLGEKONTAKT3:
  dio_10qz = center_candidate, degree 2
  dio_1ytc = center_candidate, degree 2
  dio_114i = center_near_partner, degree 1
  dio_0325 = center_near_partner, degree 1
```

Lesart:

```text
dio_1ytc verschiebt sich in K vom zentrumsnahen Randpartner zum zweiten
Zentrumskandidaten.

dio_0325 verschiebt sich von Einzelspur zu zentrumsnahem Partner, weil es
an dio_1ytc koppelt.

Damit ist die K-Erweiterung kein einfacher Zusatz am Rand, sondern eine
Verschiebung der Zentrumsspannung:
  vorher: dio_10qz als eindeutiger Brueckenkern
  nachher: dio_10qz und dio_1ytc als zwei zentrumsnahe Pole

L bestaetigt diese Rollen im kontrollierten Folgekontakt:
  dio_10qz bleibt Zentrumskandidat,
  dio_1ytc bleibt zweiter Zentrumskandidat,
  dio_114i bleibt zentrumsnaher Partner,
  dio_0325 bleibt zentrumsnaher Erweiterungspartner.

Damit ist die Viererinsel keine einmalige K-Ausweitung, sondern eine
stabile offene Mehrzentrum-Struktur ueber K -> L.
```

Grenze:

```text
rein passiv
nur kontrollierte Datensaetze
kein Langlauf-Beweis
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Viererinsel-Lupe L

Modul:

```text
DIO_MINI/report_passive_emergent_triad_lupe.py
```

Hinweis:

```text
Der Modulname stammt aus der Triadenphase.
Fachlich wurde hier eine Viererinsel zerlegt.
```

Report:

```text
debug/dio_mini_passive_emergent_triad_lupe_L_dio_0325_dio_10qz_dio_114i_dio_1ytc_20260607_v1
```

Befund:

```text
members:
  dio_0325 | dio_10qz | dio_114i | dio_1ytc

visible_edge_count:
  3 / 6

triad_reading:
  partial_coupling_triad

semantic_density:
  0.759971

variant_attraction:
  0.839968

island_growth:
  0.999990

island_fragmentation:
  0.000081

semantic_vorticity:
  0.672804
```

Sichtbare Kanten:

```text
dio_0325 <-> dio_1ytc
dio_10qz <-> dio_114i
dio_10qz <-> dio_1ytc
```

Fehlende Kanten:

```text
dio_0325 <-> dio_10qz
dio_0325 <-> dio_114i
dio_114i <-> dio_1ytc
```

Lesart:

```text
L ist keine geschlossene Vierer-Clique.
L ist auch kein Zerfall in Einzelspuren.

Die Struktur ist eine offene Mehrzentrum-Kopplung:
  dio_10qz koppelt dio_114i und dio_1ytc,
  dio_1ytc koppelt dio_10qz und dio_0325,
  dio_114i und dio_0325 bleiben indirekt getragen.

Damit entsteht eine brueckenartige Bedeutungsform:
  dio_114i -- dio_10qz -- dio_1ytc -- dio_0325

Das passt zur MCM-Lesart:
  stabile Rollennaehe ohne Vollvernetzung.
```

Grenze:

```text
rein passiv
nur kontrollierte Datensaetze
kein Langlauf-Beweis
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Folgewelt M: Trennung der Viererinsel

Generator:

```text
DIO_MINI/create_controlled_variant_m.py
```

Reports:

```text
debug/dio_mini_passive_semantic_matrix_compare_L_FOLGEKONTAKT3_vs_varianteM_folgekontakt4_20260607_v1
debug/dio_mini_passive_zero_topology_lupe_M_folgekontakt4_20260607_v1
debug/dio_mini_passive_zero_center_shift_lupe_IJKLM_20260607_v1
debug/dio_mini_passive_emergent_triad_lupe_M_dio_0325_dio_10qz_dio_114i_dio_1ytc_20260607_v1
debug/dio_mini_passive_zero_extension_lupe_M_dio_0325_20260607_v1
debug/dio_mini_passive_bridge_separation_lupe_L_to_M_target_20260607_v1
```

Globaler Vergleich L -> M:

```text
node_reproduction_rate = 0.890728
edge_reproduction_rate = 0.333333
shared_node_count = 269
shared_edge_count = 4
island_count_reference = 290
island_count_candidate = 294
```

Lesart global:

```text
Viele Familien bleiben sichtbar.
Die Kanten/Nachbarschaften werden aber deutlich umorganisiert.
Das ist keine reine Kopie der L-Welt.
```

Zielinsel-Befund M:

```text
requested:
  dio_0325 | dio_10qz | dio_114i | dio_1ytc

present:
  dio_0325 | dio_10qz | dio_114i

visible_edge_count:
  1 / 3

sichtbare Kante:
  dio_10qz <-> dio_114i

nicht sichtbar:
  dio_0325 <-> dio_10qz
  dio_0325 <-> dio_114i
  dio_0325 <-> dio_1ytc
  dio_10qz <-> dio_1ytc
  dio_114i <-> dio_1ytc

dio_1ytc:
  in dieser Zielstruktur nicht sichtbar
```

Extension-Befund M:

```text
extension_family:
  dio_0325

extension_state:
  visible_but_uncoupled_extension

extension_reading:
  Spur ist sichtbar, aber ohne Kante zur Basisinsel.
```

Center-Shift-Befund I -> J -> K -> L -> M:

```text
dio_10qz:
  bleibt sichtbar, aber Kopplungsgrad faellt.

dio_114i:
  wird in M selbst Zentrumskandidat der reduzierten Paarform.

dio_1ytc:
  verliert die sichtbare Tragung in dieser Zielstruktur.

dio_0325:
  bleibt sichtbar, aber entkoppelt von der Basisinsel.
```

Wichtige Abgrenzung:

```text
M enthaelt wieder eine open_zero_form_bridge_center,
aber diese gehoert nicht zur alten Zielinsel.

Die alte Zielinsel wird nicht als Viererform weitergetragen.
Sie reduziert sich auf die Paarbindung dio_10qz <-> dio_114i,
waehrend dio_0325 als sichtbare, aber entkoppelte Spur weiterbesteht.
```

MCM-Lesart:

```text
Das ist ein kontrollierter Hinweis auf situationsbedingte Emergenz.

L:
  offene Mehrzentrum-Bruecke wird getragen.

M:
  dieselbe Bruecke wird von der Folgewelt nicht mehr voll getragen.
  Ein Teil bleibt als Paarform,
  ein Teil bleibt als entkoppelte Spur.

Damit wird sichtbar:
  Manifestation ist nicht nur Auftauchen,
  sondern auch Weitergetragenwerden durch Weltkontakt.
```

## Passive Bridge Separation Lupe

Modul:

```text
DIO_MINI/report_passive_bridge_separation_lupe.py
```

Zweck:

```text
Vergleicht eine ausgewaehlte Brueckenstruktur zwischen zwei kontrollierten
Stufen.

Die Lupe trennt:
  bleibt eine Familie sichtbar?
  bleibt eine Kante sichtbar?
  wird eine Familie sichtbar, aber entkoppelt?
  faellt eine Familie aus der Zielstruktur?
```

Report:

```text
debug/dio_mini_passive_bridge_separation_lupe_L_to_M_target_20260607_v1
```

Befund L -> M:

```text
family_transition_counts:
  family_carried: 1
  family_not_carried: 1
  family_visible_but_decoupled: 2

edge_transition_counts:
  edge_carried: 1
  edge_lost: 2
  edge_absent: 3
```

Familien:

```text
dio_114i:
  family_carried
  edge_carried_count = 1

dio_10qz:
  family_visible_but_decoupled
  edge_carried_count = 1
  edge_lost_count = 1

dio_0325:
  family_visible_but_decoupled
  edge_lost_count = 1

dio_1ytc:
  family_not_carried
  edge_lost_count = 2
```

Kanten:

```text
getragen:
  dio_10qz <-> dio_114i

verloren:
  dio_0325 <-> dio_1ytc
  dio_10qz <-> dio_1ytc

weiterhin abwesend:
  dio_0325 <-> dio_10qz
  dio_0325 <-> dio_114i
  dio_114i <-> dio_1ytc
```

Lesart:

```text
Die Trennung entsteht nicht durch einen grossen Einzelwertbruch.
Die Einzelspuren bleiben teils sehr nahe.

Der Bruch liegt in der relationalen Kopplung:
  dio_1ytc wird in M nicht mehr getragen.
  Dadurch verliert dio_0325 seine Bruecke zur Zielinsel.
  dio_10qz bleibt nur noch mit dio_114i gekoppelt.

Das ist eine saubere Diagnose fuer:
  Familie sichtbar != Familie gekoppelt.
```

Grenze:

```text
rein passiv
nur kontrollierte Datensaetze
kein Langlauf-Beweis
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Folgewelt N: Rueckkopplungsprobe fuer dio_0325

Generator:

```text
DIO_MINI/create_controlled_variant_n.py
```

Zweck:

```text
Gezielte passive Folgewelt nach M.

Die Frage ist:
  bleibt dio_0325 isoliert?
  koppelt dio_0325 an dio_114i?
  findet dio_0325 zurueck zu dio_1ytc?
  stabilisiert sich die reduzierte Paarform dio_10qz <-> dio_114i?
```

Reports:

```text
debug/dio_mini_passive_semantic_matrix_compare_M_FOLGEKONTAKT4_vs_varianteN_folgekontakt5_20260607_v1
debug/dio_mini_passive_bridge_separation_lupe_M_to_N_target_20260607_v1
debug/dio_mini_passive_zero_extension_lupe_N_dio_0325_20260607_v1
debug/dio_mini_passive_zero_center_shift_lupe_IJKLMN_20260607_v1
debug/dio_mini_passive_emergent_triad_lupe_N_dio_0325_dio_10qz_dio_114i_dio_1ytc_20260607_v1
```

Globaler Vergleich M -> N:

```text
node_reproduction_rate = 0.921569
edge_reproduction_rate = 0.666667
shared_node_count = 282
shared_edge_count = 8
island_count_reference = 294
island_count_candidate = 292
```

Bridge-Separation-Befund M -> N:

```text
family_transition_counts:
  family_carried: 3
  family_absent: 1

edge_transition_counts:
  edge_carried: 1
  edge_absent: 5
```

Zielstruktur:

```text
sichtbar:
  dio_0325
  dio_10qz
  dio_114i

nicht sichtbar:
  dio_1ytc

getragen:
  dio_10qz <-> dio_114i

nicht gekoppelt:
  dio_0325 <-> dio_10qz
  dio_0325 <-> dio_114i
  dio_0325 <-> dio_1ytc
  dio_10qz <-> dio_1ytc
  dio_114i <-> dio_1ytc
```

Extension-Befund:

```text
dio_0325:
  extension_state = visible_but_uncoupled_extension
  bleibt sichtbar,
  koppelt aber nicht zur Basisinsel zurueck.
```

Center-Shift-Befund bis N:

```text
dio_10qz:
  bleibt Zentrumskandidat, aber mit reduziertem Kopplungsgrad.

dio_114i:
  wird vom Randpartner zum Zentrumskandidaten der reduzierten Paarform.

dio_1ytc:
  verliert Tragung und bleibt in N abwesend.

dio_0325:
  bleibt Einzelspur ohne Kante.
```

MCM-Lesart:

```text
N stabilisiert nicht die alte Viererbruecke.
N stabilisiert die reduzierte Paarform:
  dio_10qz <-> dio_114i

dio_0325 bleibt als Spur erhalten, aber ohne relationale Tragung.
Das spricht fuer eine entkoppelte Erinnerungs-/Spurform,
nicht fuer eine erneute Manifestation.
```

Grenze:

```text
rein passiv
nur kontrollierte Datensaetze
kein Langlauf-Beweis
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Emergent Candidate Lupe

Modul:

```text
DIO_MINI/report_passive_emergent_candidate_lupe.py
```

Aufgabe:

```text
Ausgewaehlte emergente Kandidaten werden pro Stage gelesen:
  Sensor-/MCM-Vektordrift
  Feld-Drift
  Sehen/Hoeren-Drift
  Neuroton
  Zeitlage
  Inselpraesenz
  Kopplungspartner
```

Aktueller Report:

```text
debug/dio_mini_passive_emergent_candidate_lupe_G_REPRO_H_REPRO_I_WELTKONTAKT_20260607_v1
```

Befund:

```text
dio_005q:
  isolierte Variation
  staerkere Drift aus Sehen/Hoeren
  keine Kopplung

dio_1wx6:
  starke isolierte Variation
  Drift in Feld und Sensorik
  Neuroton wechselt von observation_tone zu focus_tone
  keine Kopplung

dio_114i:
  Reorganisationsspur
  koppelt in I_WELTKONTAKT mit dio_10qz und dio_1ytc

dio_0scd:
  Reorganisationsspur
  koppelt in I_WELTKONTAKT mit dio_0axn und dio_122f
```

Lesart:

```text
Es gibt zwei unterschiedliche emergente Bewegungen:

1. Isolierte Variation:
   Die Spur bleibt allein, aber ihr innerer Vektor bewegt sich.

2. Reorganisation:
   Die Spur erscheint erst spaeter und koppelt dann mit anderen Inseln.

Damit wird die eigentliche Emergenz nicht als stabile Wiederholung gelesen,
sondern als Bewegung, Kopplung und moegliche Verdichtung.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Emergent Partner Lupe

Modul:

```text
DIO_MINI/report_passive_emergent_partner_lupe.py
```

Aufgabe:

```text
Die Partner-Lupe liest emergente Reorganisationsspuren genauer.

Sie prueft:
  War die Spur vorher sichtbar, aber isoliert?
  Bildet sie im spaeteren Weltkontakt eine gemeinsame Insel?
  Welche Partner entstehen?
  Wie eng liegen die Partner in Ganzbedeutung, Sensorik, MCM-Feld
  und Neuroton zusammen?
```

Aktueller Report:

```text
debug/dio_mini_passive_emergent_partner_lupe_H_REPRO_I_WELTKONTAKT_20260607_v1
```

Befund:

```text
dio_114i:
  H_REPRO: sichtbar, aber nicht gekoppelt
  I_WELTKONTAKT: koppelt mit dio_10qz und dio_1ytc
  avg_whole_distance = 0.008542394
  avg_sensory_distance = 0.014158917
  avg_mcm_distance = 0.010337658
  avg_neuro_distance = 0.002865573

dio_0scd:
  H_REPRO: sichtbar, aber nicht gekoppelt
  I_WELTKONTAKT: koppelt mit dio_0axn und dio_122f
  avg_whole_distance = 0.013329276
  avg_sensory_distance = 0.024295865
  avg_mcm_distance = 0.012350938
  avg_neuro_distance = 0.001092902
```

Lesart:

```text
Beide Spuren sind keine reinen Wiederholungen.

Sie waren vorher als eigene Spur vorhanden,
blieben zuerst ohne gemeinsame Insel,
und fanden erst im neuen Weltkontakt eine eng verwandte Nachbarschaft.

Das ist eine passive Reorganisationsspur:
  bestehende innere Spur
  + neuer Weltkontakt
  -> neue semantische Kopplung
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Emergent Island Growth Lupe

Modul:

```text
DIO_MINI/report_passive_emergent_island_growth_lupe.py
```

Aufgabe:

```text
Die Island-Growth-Lupe liest eine emergente Spur ueber mehrere Stages:
  sichtbar oder nicht sichtbar
  isoliert oder gekoppelt
  Partnerbildung
  semantische Dichte
  Inselwachstum
  Fragmentierung
  Vorticity

Damit wird geprueft, ob eine Spur nur aufploppt,
oder ob sie unter neuem Weltkontakt zu einer Bedeutungsinsel verdichtet.
```

Aktueller Report:

```text
debug/dio_mini_passive_emergent_island_growth_lupe_H_REPRO_I_WELTKONTAKT_20260607_v1
```

Befund:

```text
dio_114i:
  H_REPRO: visible_isolated
  I_WELTKONTAKT: coupled_density_center
  Partner: dio_10qz | dio_1ytc
  semantic_density: 0.080000 -> 0.793305
  island_growth: 0.306667 -> 0.999985
  fragmentation: 1.000000 -> 0.000053

dio_0scd:
  H_REPRO: visible_isolated
  I_WELTKONTAKT: coupled_density_center
  Partner: dio_0axn | dio_122f
  semantic_density: 0.080000 -> 0.793304
  island_growth: 0.306667 -> 0.999984
  fragmentation: 1.000000 -> 0.000054
```

Lesart:

```text
Beide Spuren waren vorher eigene, fragmentierte Einzelspuren.
Unter neuem Weltkontakt wurden sie nicht geloescht,
sondern fanden zwei passende Partner und verdichteten zu
semantischen Dichtezentren.

Das ist eine staerkere passive Emergenzspur als reine Wiederholung:
  isolierter Keim
  -> Weltkontakt
  -> Partnerbildung
  -> Dichtezentrum
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Manifestations-Test I -> J

Folgewelt:

```text
DIO_MINI/create_controlled_variant_j.py
```

Aufgabe:

```text
Variante J ist ein zweiter deterministischer Weltkontakt nach I.
Sie prueft, ob in I entstandene Dichtezentren bei weiterem Weltkontakt:
  stabil bleiben,
  kippen,
  verschwinden,
  oder sich neu organisieren.
```

Reports:

```text
debug/dio_mini_passive_semantic_matrix_compare_I_WELTKONTAKT_vs_varianteJ_folgekontakt_20260607_v1
debug/dio_mini_passive_emergent_island_growth_lupe_I_WELTKONTAKT_J_FOLGEKONTAKT_20260607_v1
```

Matrix-Befund:

```text
node_reproduction_rate: 0.761290
edge_reproduction_rate: 0.416667

Lesart:
  Viele Knoten bleiben sichtbar.
  Deutlich weniger Kanten bleiben gleich.
  Das spricht fuer weiterlaufende Reorganisation,
  nicht fuer starre Kopie.
```

Kandidaten-Befund:

```text
dio_114i:
  I: coupled_density_center
  J: coupled_density_center
  Partner bleiben: dio_10qz | dio_1ytc
  semantic_density bleibt 0.793305
  Lesart: stabiler Manifestationskandidat.

dio_0scd:
  I: coupled_density_center
  J: not_visible
  semantic_density 0.793304 -> 0.000000
  Lesart: Dichtezentrum wird im Folgekontakt nicht mehr getragen.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

Pipeline-Anschluss:

```text
DIO_MINI/run_passive_inner_universe_repro_pipeline.py

Schalter:
  --build-carry-separator
  --carry-separator-reference dio_11vr

Voraussetzung:
  --carry-followup-candidates muss gesetzt sein,
  damit zuerst ein Follow-Up-Result entsteht.
```

## Passive Emergent Lifecycle

Modul:

```text
DIO_MINI/report_passive_emergent_lifecycle.py
```

Aufgabe:

```text
Der Report trennt realitaetsbezogene Ordnung von eigentlicher Emergenz.

Realitaetsbezogene Ordnung:
  wiederholte aehnliche Weltlage erzeugt wiederholte innere Ordnung.

Eigentliche Emergenz:
  Aufploppen, Drift, Variation, Kopplung, Teilung, Verdichtung.

Manifestation:
  emergente Bewegung wird ueber Weltkontakt stabil genug getragen.
```

Wichtige Trennung:

```text
island_presence:
  Spur ist als Insel oder isolierte Spur sichtbar.

island_contact:
  Spur koppelt an andere Inseln/Familien.

Damit wird eine isolierte stabile Ordnung nicht faelschlich als
Verschmelzung gelesen.
```

Aktueller Report:

```text
debug/dio_mini_passive_emergent_lifecycle_G_REPRO_H_REPRO_I_WELTKONTAKT_20260607_v1
```

Befund:

```text
Familien gesamt: 566

sporadic_popup: 297
reality_bound_manifestation_candidate: 118
reality_order_trace: 66
recurring_soft_order_trace: 72
isolated_emergent_variation_candidate: 4
isolated_emergent_variation_trace: 3
emergent_split_drift_trace: 4
emergent_reorganization_trace: 2
```

Lesart:

```text
dio_11vr ist kein Hauptbeispiel fuer eigentliche Emergenz,
sondern fuer realitaetsgebundene Ordnung:
  stabile Wiederkehr,
  sehr geringe Variation,
  mehrfach getragen.

Interessanter fuer eigentliche Emergenz sind:
  dio_005q
  dio_1wx6
  dio_0lrt
  dio_1xka

Diese Spuren zeigen isolierte Variation mit Manifestationsdruck,
aber noch keine Verschmelzung mit anderen Inseln.

Reorganisationsspuren:
  dio_114i
  dio_0scd

Hier wirken Kopplung und Teilung gleichzeitig.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Carry Separator

Modul:

```text
DIO_MINI/report_passive_carry_separator.py
```

Aufgabe:

```text
Stabile Tragespur gegen schwache Keime trennen.

Der Report vergleicht eine Referenzfamilie mit Follow-Up-Kandidaten und
trennt:
  stable_carried_trace
  weak_single_contact_keim
  kipped_under_world_contact
  not_reproduced
  unclear_or_mixed_separator
```

Wichtig:

```text
Ein Carry-Ratio von 1.0 reicht nicht aus.

Wenn eine Spur nur in einer Probe sichtbar und getragen ist, bleibt sie ein
Keim. Reife entsteht erst durch wiederholten getragenen Weltkontakt.
```

Aktueller Lauf:

```text
debug/dio_mini_passive_carry_separator_dio_11vr_H_REPRO_vs_I_WELTKONTAKT_20260607_v1
```

Befund:

```text
Referenz:
  dio_11vr
  visible = 3
  carried = 3
  carry_ratio = 1.0
  text_island = dio_text_38zk5e

Kandidaten:
  weak_single_contact_keim = 4
  kipped_under_world_contact = 2
  not_reproduced = 1
```

Lesart:

```text
dio_11vr ist derzeit die stabilere Vergleichsspur.

dio_0ocv, dio_0rwa, dio_19b6 und dio_0jx1 sind sichtbar und getragen,
aber noch ohne Tragedauer.

dio_1ndv und dio_0bde kippen unter Folgeweltkontakt.
dio_1fck erscheint im Folgeweltkontakt nicht erneut.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Carry Follow-Up Result

Modul:

```text
DIO_MINI/report_passive_carry_followup_result.py
```

Selfcheck-Report:

```text
debug/dio_mini_passive_carry_followup_result_selfcheck_dio_11vr_G_REPRO_vs_H_REPRO_20260607_v1
```

Zweck:

```text
Eine spätere Weltvariante kann gegen die Follow-Up-Kandidaten gelegt werden.

Das Modul bewertet pro Kandidat:
  matured_to_multi_probe_carried
  still_single_probe_carried
  partial_carry_with_kipp
  kipped_in_followup
  candidate_not_visible_in_followup
```

Selfcheck:

```text
Mit demselben G_REPRO/H_REPRO-Kontrast bleiben alle 7 Kandidaten:
  still_single_probe_carried

Das ist korrekt, weil noch kein neuer Weltkontakt vorliegt.
```

Lesart:

```text
Der nächste echte Test ist nicht mehr die Kandidatenbildung,
sondern eine neue kontrollierte Weltvariante.

Erst danach kann bewertet werden:
  Keim reift,
  Keim kippt,
  Keim bleibt kurz,
  Keim verschwindet.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Variante I - Weltkontakt-Folgeprüfung

Generator:

```text
DIO_MINI/create_controlled_variant_i.py
```

Daten:

```text
data/kontrolliert_sensor_relation_probe20_emergenz_richtungsvarianz_6episoden_varianteI_weltkontakt_5m_SOLUSDT.csv
...
data/kontrolliert_sensor_relation_probe26_emergenz_signaturdrift_6episoden_varianteI_weltkontakt_5m_SOLUSDT.csv
```

Zweck:

```text
Variante I ist eine nahe Weltkontakt-Fortsetzung nach H.
Sie soll prüfen, ob schwache Ein-Proben-Träger bei weiterer Weltzeit reifen,
kippen oder nur situativ sichtbar bleiben.

Geändert wird nur OHLCV.
Mini-DIO-Logik, Memory-Wirkung, Gates, Entries und Richtung bleiben unberührt.
```

Basislauf:

```text
Variante I / weltkontakt
Probes 20..26
runs = 2
Episoden = 916
Trades = 0
passiv
```

Reports:

```text
debug/dio_mini_passive_direction_support_shift_H_REPRO_vs_I_WELTKONTAKT_20260607_v1
debug/dio_mini_passive_temporal_kipp_points_H_REPRO_vs_I_WELTKONTAKT_20260607_v1
debug/dio_mini_passive_trace_carry_curve_H_REPRO_vs_I_WELTKONTAKT_20260607_v1
debug/dio_mini_passive_carry_contrast_H_REPRO_vs_I_WELTKONTAKT_20260607_v1
debug/dio_mini_passive_carry_followup_result_dio_11vr_H_REPRO_vs_I_WELTKONTAKT_20260607_v1
```

Befund H -> I:

```text
Direction-Support:
  families = 247
  same_sensory_field_same_direction_but_reife_kippt = 242
  direction_support_reorganized = 3
  same_sensory_field_direction_reward_weakens = 1
  direction_support_not_visible_right = 1

Temporal-Kipp:
  family_no_visible_temporal_kipp = 96
  family_trade_readiness_softens = 86
  family_loses_lived_support = 30
  family_best_reward_softens = 28
  family_neuro_temporal_reorganizes = 6
  family_has_direction_flip = 1

Tragekurve:
  trace_fully_carried = 96
  trace_immediate_or_continuous_kipp = 123
  trace_carries_then_kipps = 15
  trace_kipps_then_recarries = 9
  trace_mixed_mostly_carried = 3
  trace_mixed_mostly_kipped = 1
```

Kandidaten aus G/H gegen H/I:

```text
still_single_probe_carried:
  dio_0ocv
  dio_0rwa
  dio_19b6
  dio_0jx1

kipped_in_followup:
  dio_1ndv
  dio_0bde

candidate_not_visible_in_followup:
  dio_1fck
```

Stabile Referenz:

```text
dio_11vr bleibt erneut multi_probe_carried_trace:
  visible = 3
  carried = 3
  carry_ratio = 1.0
  text = dio_text_38zk5e -> dio_text_38zk5e
```

Lesart:

```text
Variante I bestätigt eine wichtige Trennung:
  Keimnähe reicht nicht.
  Manche Keime bleiben Ein-Proben-Träger.
  Manche kippen.
  Manche erscheinen nicht mehr.
  dio_11vr bleibt dagegen wiederholt getragen.

Damit wird dio_11vr als stabilere emergente Tragespur stärker,
während die schwachen Kandidaten noch keine Reife zeigen.
```

## Passive Carry Follow-Up Candidates

Modul:

```text
DIO_MINI/report_passive_carry_followup_candidates.py
```

Report:

```text
debug/dio_mini_passive_carry_followup_candidates_dio_11vr_G_REPRO_vs_H_REPRO_20260607_v1
```

Zweck:

```text
Ein-Proben-Träger aus dem Trageprofil werden isoliert.
Sie sind noch keine stabile Reife, aber mögliche Keime.

Die Frage lautet:
  Werden sie bei mehr Weltkontakt zu Mehr-Proben-Trägern?
  Kippen sie?
  Oder bleiben sie kurze situative Aufleuchtungen?
```

Befund:

```text
Kandidaten = 7

high:
  dio_0ocv
  dio_1fck

medium:
  dio_0rwa
  dio_1ndv
  dio_19b6
  dio_0bde

low:
  dio_0jx1
```

Lesart:

```text
dio_0ocv und dio_1fck sind die nächsten schwachen Träger.
Sie sind nahe an dio_11vr, aber noch ohne ausreichende Tragedauer.

Das ist ein guter passiver Prüfpunkt für die nächste kontrollierte Variante.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Carry Profile

Modul:

```text
DIO_MINI/report_passive_carry_profile.py
```

Report:

```text
debug/dio_mini_passive_carry_profile_dio_11vr_G_REPRO_vs_H_REPRO_20260607_v1
```

Zweck:

```text
Eine stabile Referenzspur wird mit ähnlichen und kippenden Spuren verglichen.

Referenz:
  dio_11vr
  multi_probe_carried_trace
  trace_fully_carried
  sichtbar in 3 Proben
  getragen in 3 Proben
  Textinsel dio_text_38zk5e
```

Befund:

```text
Die nächsten ähnlichen Gegenlagen sind überwiegend Ein-Proben-Träger.
Sie sehen der Referenz nahe, haben aber noch keine Tragedauer.

Beispiel:
  dio_0ocv
  weak_carried_like_reference_needs_more_world_contact

Kippende Gegenlagen wie dio_0v3a liegen nicht zwingend durch Sensorik
weit weg, sondern durch fehlende Tragedauer.
```

Lesart:

```text
Das stabile Profil ist nicht nur:
  "ähnliche Form",
sondern:
  "ähnliche Form/Feldlage über Weltkontakt gehalten".

Damit wird Tragedauer als eigener Reifefaktor sichtbar.
Ein einzelner getragener Kontakt ist noch kein stabiler Zustand.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Carry Contrast

Modul:

```text
DIO_MINI/report_passive_carry_contrast.py
```

Report:

```text
debug/dio_mini_passive_carry_contrast_G_REPRO_vs_H_REPRO_20260607_v1
```

Zweck:

```text
Getragene situative Spuren werden gegen sofort oder dauerhaft kippende
Spuren gestellt.

Damit wird geprüft, ob stabile Tragung nur Sichtbarkeit ist oder ob sie
eine eigene Sensor-/Feld-/Zeitqualität besitzt.
```

Befund:

```text
families = 63

immediate_or_continuous_kipp_trace = 46
single_probe_carried_trace = 7
carries_then_kipps_trace = 3
kipps_then_recarries_trace = 3
mixed_or_unclear_trace = 3
multi_probe_carried_trace = 1
```

Stärkster bisheriger Kandidat:

```text
dio_11vr

trace = multi_probe_carried_trace
visible_probes = 3
carried_probes = 3
carry_ratio = 1.0
text_island = dio_text_38zk5e -> dio_text_38zk5e
sensory_field_distance = 0.004459482
mcm_coherence_delta = -0.000271
mcm_tension_delta = 0.000839
mcm_asymmetry_delta = 0.006474
lived_support_drop_count = 0
neuro_tone_reorganizes_count = 0
```

Kontrast:

```text
dio_0x52
  bleibt syntaktisch sichtbar,
  kippt aber in allen sichtbaren Proben.
  Hauptbruch: Verlust gelebter Stützung.

dio_1lg2
  bleibt syntaktisch sichtbar,
  kippt aber ebenfalls.
  Hauptbruch: Neuro-/Ton-Umordnung und danach Stützungsverlust.
```

Lesart:

```text
Niedrige Sensor-Feld-Distanz allein reicht nicht.

Stabile Tragung zeigt sich erst, wenn:
  die Form/Feld-Nähe wiederkehrt,
  die Textinsel erhalten bleibt,
  die gelebte Stützung nicht abfällt,
  die neurotonale Lage nicht reorganisiert,
  und die Spur über mehrere Proben getragen bleibt.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Trace Carry Curve

Modul:

```text
DIO_MINI/report_passive_trace_carry_curve.py
```

Report:

```text
debug/dio_mini_passive_trace_carry_curve_G_REPRO_vs_H_REPRO_20260607_v1
```

Ziel:

```text
Aus den zeitlichen Kipp-Punkten eine passive Tragekurve bilden:
Wie lange bleibt eine situative Spur getragen, bevor sie kippt?
```

Befund:

```text
Familien: 63
Proben: 7

trace_immediate_or_continuous_kipp: 46
trace_fully_carried: 8
trace_carries_then_kipps: 3
trace_kipps_then_recarries: 3
trace_mixed_mostly_kipped: 3
```

Probe-Kurve:

```text
probe20: carry_ratio = 0.040000000
probe21: carry_ratio = 0.058823529
probe22: carry_ratio = 0.103448276
probe23: carry_ratio = 0.350000000
probe24: carry_ratio = 0.076923077
probe25: carry_ratio = 0.173913043
probe26: carry_ratio = 0.095238095
```

Konkrete Anker:

```text
dio_0x52:
  trace_immediate_or_continuous_kipp
  sichtbar in 4 Proben
  getragen in 0 Proben
  erster Kipp-Punkt: probe20 / probe_lived_support_drop
  dominanter Kippzustand: probe_lived_support_drop

dio_1lg2:
  trace_immediate_or_continuous_kipp
  sichtbar in 2 Proben
  getragen in 0 Proben
  erster Kipp-Punkt: probe20 / probe_neuro_tone_reorganizes
  danach: probe_lived_support_drop

dio_11vr:
  trace_fully_carried
  sichtbar in 3 Proben
  getragen in 3 Proben
  Textinsel bleibt dio_text_38zk5e
```

Lesart:

```text
Die meisten situationsbedingten Spuren sind noch nicht dauerhaft getragen.
Sie erscheinen als Syntax/Familie, kippen aber sofort oder durchgehend.

Ein kleiner Teil bleibt getragen.
Das ist der interessantere Kandidat fuer stabile situative Ordnung.
```

Wichtige Einschraenkung:

```text
trace_fully_carried ist staerker, wenn die Familie ueber mehrere Proben
sichtbar bleibt.

Eine einzelne getragene Probe ist kein starker Reifebeweis.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Temporal Kipp Points

Modul:

```text
DIO_MINI/report_passive_temporal_kipp_points.py
```

Report:

```text
debug/dio_mini_passive_temporal_kipp_points_G_REPRO_vs_H_REPRO_20260607_v1
```

Ziel:

```text
Zeitlich markieren, wo eine situative emergente Spur zuerst kippt.

Geprueft wird pro Familie und Probe:
  Richtungsflip
  Beobachtungsrichtungsflip
  Verlust gelebter Episodenstuetzung
  Abschwaechung hypothetischer Weltbelohnung
  Abschwaechung Trade-Readiness
  Neuroton- oder Zeitstatus-Umordnung
```

Befund G_REPRO -> H_REPRO:

```text
Familien: 63
Probe-Detailzeilen: 161

family_loses_lived_support: 39
family_no_visible_temporal_kipp: 8
family_neuro_temporal_reorganizes: 7
family_trade_readiness_softens: 5
family_has_direction_flip: 3
family_best_reward_softens: 1
```

Konkrete Anker:

```text
dio_0x52:
  Familie kippt ueber Verlust gelebter Stuetzung.
  erster Kipp-Punkt: probe20 / probe_lived_support_drop
  Pfad:
    lived_support_drop
    lived_support_drop
    trade_readiness_softens
    lived_support_drop

dio_1lg2:
  Familie kippt ebenfalls in Richtung Verlust gelebter Stuetzung,
  beginnt aber mit Neuroton-Umordnung.
  erster Kipp-Punkt: probe20 / probe_neuro_tone_reorganizes
  danach: probe_lived_support_drop
```

Lesart:

```text
Der haeufigste Kippmechanismus ist nicht Richtungsflip.

Viel haeufiger verliert eine Spur gelebte Stuetzung:
  sie bleibt als Syntax sichtbar,
  sie kann Sinnesnaehe behalten,
  sie kann Richtung behalten,
  aber sie wird nicht mehr breit genug von der Welt getragen.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Diagnose: Situationsbedingter Emergenter Gedanke

Diagnoseziel:

```text
Festhalten, dass eine Syntax-/Familien-/Textinselspur als situativer
emergenter Gedanke auftreten kann.

Diese Spur ist nicht programmiert.
Sie entsteht aus Wahrnehmung, Feldlage, Zeitkontakt und Weltreaktion.
```

Beobachteter Zusammenhang:

```text
Ein emergenter Gedanke bleibt sichtbar,
wird aber von der Aussenwelt nicht immer stabil genug getragen.

Damit wird er zu situativen Daten:
  nicht Regel
  nicht Gate
  nicht Entry
  nicht Richtung
  sondern beobachtbare innere Ordnung im Kontext
```

Diagnosefragen:

```text
Kehrt die Spur in aehnlicher Sinnes-/Feldlage wieder?
Bleibt ihre Richtung sichtbar?
Kippt Reife trotz gleicher Richtung?
Faellt gelebte Stuetzung ab?
Entsteht daraus neue Insel, Drift oder Verdichtung?
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Direction Support Shift

Modul:

```text
DIO_MINI/report_passive_direction_support_shift.py
```

Report:

```text
debug/dio_mini_passive_direction_support_shift_G_REPRO_vs_H_REPRO_20260607_v1
```

Ziel:

```text
Pruefen, ob Reife kippt, weil die hypothetisch beste Richtung,
die Beobachtungsrichtung oder die Weltstuetzung nicht mehr gleich tragen.

Das bleibt Diagnose:
  keine Handlung
  kein Entry
  kein Richtungssignal
```

Befund G_REPRO -> H_REPRO ueber Probe20 bis Probe26:

```text
Familien: 63

same_sensory_field_same_direction_but_reife_kippt: 41
same_sensory_field_less_lived_direction_support: 8
direction_support_reorganized: 8
direction_support_flips: 4
same_sensory_field_direction_reward_weakens: 2
```

Konkrete Anker:

```text
dio_0x52:
  Richtung bleibt SHORT -> SHORT
  Beobachtungsrichtung bleibt SHORT -> SHORT
  best_reward_training bleibt 1.0 -> 1.0
  Episoden fallen 8 -> 2
  trade_readiness faellt 0.025963375 -> 0.0037115
  Zustand: same_sensory_field_less_lived_direction_support

dio_1lg2:
  Richtung bleibt SHORT -> SHORT
  Beobachtungsrichtung bleibt SHORT -> SHORT
  best_reward_training bleibt 1.0 -> 1.0
  Episoden bleiben 2 -> 2
  Zustand: same_sensory_field_same_direction_but_reife_kippt
```

Lesart:

```text
Die Reife kippt nicht nur, wenn die Richtung flippt.

Bei vielen Familien bleibt die gleiche beste Richtung sichtbar.
Trotzdem kippt die Reife.

Das spricht fuer:
  gleiche Sinnesnaehe,
  gleiche Richtungsahnung,
  aber nicht genug gelebte Integration oder Bestaetigungsbreite.
```

Interpretation:

```text
Ein emergenter Gedanke kann zur Welt noch aehnlich passen,
aber seine Ordnung wird nicht mehr stabil getragen.

Das ist naeher an:
  "Ich sehe/erahne noch dieselbe Richtung,
   aber die Aussenwelt traegt meine innere Ordnung nicht ausreichend."

Nicht:
  "Die Richtung war einfach falsch."
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Shift Sensory-Field Alignment

Modul:

```text
DIO_MINI/report_passive_shift_sensory_field_alignment.py
```

Pipeline-Anbindung:

```text
DIO_MINI/run_passive_inner_universe_repro_pipeline.py
```

Report:

```text
debug/dio_mini_passive_shift_sensory_field_alignment_G_REPRO_vs_H_REPRO_20260607_v1
```

Ziel:

```text
Die Reife-Kippungen gegen Sehen, Hoeren und Fuehlen legen.

Frage:
  Bleibt die Syntax, weil eine aehnliche Sinnes-/Feldlage vorliegt?
  Oder bleibt sie nur als roher Name ohne tragenden Zusammenhang?
```

Befund G_REPRO -> H_REPRO:

```text
Familien: 63

same_sensory_field_visible: 34
same_sensory_field_but_reife_kippt: 11
same_sensory_field_but_less_lived_support: 8
near_mcm_field_with_sensory_variation: 9
syntax_survives_but_context_changed: 1
```

Konkrete Anker:

```text
dio_0x52:
  gleiche Textinsel: dio_text_1456g6j
  Episoden: 8 -> 2
  sensory_field_distance = 0.007631226
  MCM-Kohaerenz: 0.979900 -> 0.981866
  Zustand: same_sensory_field_but_less_lived_support

dio_1lg2:
  gleiche Textinsel: dio_text_13ycr5k
  Episoden: 2 -> 2
  sensory_field_distance = 0.011317391
  MCM-Kohaerenz: 0.970369 -> 0.980784
  Zustand: same_sensory_field_but_reife_kippt
```

Lesart:

```text
Die Wahrnehmungsnaehe bleibt in vielen Faellen erhalten.
Die Reife kippt trotzdem.

Damit liegt der Bruch nicht primaer im Sehen/Hoeren/Fuehlen,
sondern in der getragenen Bestaetigung:
  gleiche oder nahe Sinneslage,
  hohe MCM-Kohaerenz,
  aber weniger gelebte Stuetzung oder rohe Reife.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Syntax-Maturity Shift

Modul:

```text
DIO_MINI/report_passive_syntax_maturity_shift.py
```

Pipeline-Anbindung:

```text
DIO_MINI/run_passive_inner_universe_repro_pipeline.py
```

Report:

```text
debug/dio_mini_passive_syntax_maturity_shift_G_REPRO_vs_H_REPRO_20260607_v1
```

Ziel:

```text
Pruefen, ob Syntax/Familie erhalten bleibt,
waehrend die innere Reife kippt.
```

Befund G_REPRO -> H_REPRO:

```text
verglichene Anker: 63
syntax_survives_reife_kippt: 63
Textinsel-Anker: 56
Familien-Anker: 7
avg_score_delta: -0.276772486
avg_rawness_delta: +0.276772486
```

Konkrete Anker:

```text
dio_0x52:
  dio_text_1456g6j bleibt gleich
  inner_stable_recurrence_space -> inner_unconfirmed_raw_space
  score_delta = -0.276666666

dio_1lg2:
  dio_text_13ycr5k bleibt gleich
  inner_stable_recurrence_space -> inner_unconfirmed_raw_space
  score_delta = -0.276666666
```

Lesart:

```text
Die Syntaxspur kann reproduzierbar bleiben,
ohne dass ihre Reife erhalten bleibt.

Das ist wichtig:
  Name/Syntax ist nicht automatisch Bedeutung.
  Hohe MCM-Kohaerenz ist nicht automatisch Reife.
  Wiedererkennbarkeit ist nicht automatisch Tragfaehigkeit.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```

## Passive Inner-Universe Repro Pipeline

Modul:

```text
DIO_MINI/run_passive_inner_universe_repro_pipeline.py
```

Zweck:

```text
Kontrollierte Varianten F/G/H reproduzierbar durch dieselbe passive
Diagnosekette schicken:

1. Mini-DIO-Runs fuer Probe20 bis Probe26
2. passiver Meaning-Space
3. passive Nachbarschaften
4. passive Semantic Matrix
5. passive Semantic Density
6. diagnostische Semantic-Matrix-Memory
7. Textinsel-Reife
8. Textinsel-Innenkarte
9. optional Matrix-/Innenkartenvergleich
10. optional Family-Bridge-Lineage
```

Wirkungsgrenze:

```text
Das Modul ist Diagnose-Orchestrierung.
Es baut keine Handlung.
Es setzt kein Gate.
Es erzeugt kein Entry-Signal.
Es erzeugt kein Richtungssignal.
Die erzeugte Semantic-Matrix-Memory bleibt passiv.
```

Beispiel:

```text
python -m DIO_MINI.run_passive_inner_universe_repro_pipeline ^
  --variant F ^
  --tag repro_check ^
  --date-tag 20260607_probe ^
  --runs 2 ^
  --reset-memory ^
  --family dio_0x52 ^
  --family dio_1lg2 ^
  --compare-inner-map debug\dio_mini_passive_text_island_inner_map_after_varianteF_20260607_v1\passive_text_island_inner_map.csv ^
  --compare-matrix debug\dio_mini_passive_semantic_matrix_6episoden_varianteF_20260607_v1 ^
  --compare-label F_ORIGINAL
```

## G-Repro gegen F-Repro

Report:

```text
debug/dio_mini_passive_family_bridge_lineage_varianteG_repro_check_20260607_v1
```

Befund:

```text
F_REPRO / dio_0x52:
  Textinsel = dio_text_1456g6j
  Zustand = inner_stable_recurrence_space
  Score = 0.476246133

G_REPRO / dio_0x52:
  Textinsel = dio_text_1456g6j
  Zustand = inner_stable_recurrence_space
  Score = 0.483333333

G_REPRO / dio_1lg2:
  Textinsel = dio_text_13ycr5k
  Zustand = inner_stable_recurrence_space
  Score = 0.483333333
```

Matrix-Vergleich F_REPRO -> G_REPRO:

```text
node_count_reference = 253
node_count_candidate = 277
shared_node_count = 207
node_reproduction_rate = 0.818182

edge_count_reference = 120
edge_count_candidate = 12
shared_edge_count = 1
edge_reproduction_rate = 0.008333

island_count_reference = 161
island_count_candidate = 265
```

Innenkartenvergleich:

```text
stable_recurrence = 105
new_in_right_inner_map = 160
missing_in_right_inner_map = 56
```

Lesart:

```text
dio_0x52 reproduziert sich in G_REPRO stabiler als erwartet:
gleiche Textinsel, gleicher Innenraum, leicht hoeherer Score.

dio_1lg2 erscheint ebenfalls wieder, aber nicht als Bruecke auf derselben
Textinsel. Es bildet eine eigene stabile Textinsel.

Damit ist die Bruecke dio_0x52 | dio_1lg2 nicht bestaetigt.
Bestaetigt ist:
  - starke Wiederkehr auf Familien-/Wortebene
  - klare Reorganisation auf Kanten-/Beziehungsebene
  - Aufspaltung in getrennte stabile Inseln statt gemeinsamer Verdichtung
```

## H-Repro als Strukturkontrast

Report:

```text
debug/dio_mini_passive_family_bridge_lineage_varianteH_repro_check_20260607_v1
```

Befund:

```text
G_REPRO / dio_0x52:
  Textinsel = dio_text_1456g6j
  Zustand = inner_stable_recurrence_space
  Score = 0.483333333

H_REPRO / dio_0x52:
  Textinsel = dio_text_1456g6j
  Zustand = inner_unconfirmed_raw_space
  Score = 0.206666667

G_REPRO / dio_1lg2:
  Textinsel = dio_text_13ycr5k
  Zustand = inner_stable_recurrence_space
  Score = 0.483333333

H_REPRO / dio_1lg2:
  Textinsel = dio_text_13ycr5k
  Zustand = inner_unconfirmed_raw_space
  Score = 0.206666667
```

Matrix-Vergleich G_REPRO -> H_REPRO:

```text
node_count_reference = 277
node_count_candidate = 300
shared_node_count = 63
node_reproduction_rate = 0.227437

edge_count_reference = 12
edge_count_candidate = 12
shared_edge_count = 0
edge_reproduction_rate = 0.0

island_count_reference = 265
island_count_candidate = 288
```

Innenkartenvergleich:

```text
inner_state_softened = 56
missing_in_right_inner_map = 209
new_in_right_inner_map = 232
```

Kantenbefund fuer `dio_0x52` und `dio_1lg2`:

```text
G_REPRO:
  keine direkte Matrix-/Neighbor-Kante zu dio_0x52 oder dio_1lg2

H_REPRO:
  keine direkte Matrix-/Neighbor-Kante zu dio_0x52 oder dio_1lg2
```

Node-Befund:

```text
G_REPRO / dio_0x52:
  episodes = 8
  mcm_coherence = 0.979900
  matrix_node_state = recurring_raw_semantic_trace

G_REPRO / dio_1lg2:
  episodes = 2
  mcm_coherence = 0.970369
  matrix_node_state = raw_semantic_trace

H_REPRO / dio_0x52:
  episodes = 2
  mcm_coherence = 0.981866
  matrix_node_state = raw_semantic_trace

H_REPRO / dio_1lg2:
  episodes = 2
  mcm_coherence = 0.980784
  matrix_node_state = raw_semantic_trace
```

Lesart:

```text
H bestaetigt den Strukturkontrast:
Die Syntaxnamen bleiben sichtbar, aber die Reife faellt in den rohen Raum.
Die MCM-Kohaerenz bleibt hoch, aber Beziehungskanten tragen nicht.

Damit ist der Unterschied wichtig:
  Wort/Wiederkehr bleibt.
  Beziehung/Reife kollabiert unter fremderer Struktur.
```

## Passive Inner-Core Anchor Lupe

Modul:

```text
DIO_MINI/report_passive_inner_core_anchor_lupe.py
```

Zweck:

```text
Die Anchor-Lupe prueft, ob wiederkehrende Familien tiefe Anker oder nur
stabile Einzelformen sind.
```

Report:

```text
debug/dio_mini_passive_inner_core_anchor_lupe_FG_vs_GH_20260607_v1
```

Befund:

```text
category_shift_anchor = 170
drift_sensitive_anchor = 47
exact_single_form_anchor = 14
variant_bridge_anchor = 10
```

Lesart:

```text
Die 14 stabilen Kernfamilien sind exact_single_form_anchor:
  gleiche Familie
  gleiche Textinsel
  stable_core -> stable_core
  sehr kleine Score-Abweichung

Das ist stabile Realitaetsbindung, aber noch flach.

Tiefe Anker wuerden mehrere Textinseln, Varianten oder Reorganisation tragen.
Diese Tiefe zeigt sich eher bei den 10 variant_bridge_anchor, weil dort die
Familie stabil bleibt, aber die Textinsel wechselt.
```

Wichtiger Befund:

```text
Stabiler Kern != automatisch tiefer Kern.

Ein stabiler Einzelform-Anker ist reproduzierbar.
Ein tiefer Anker muss zusaetzlich Varianten tragen koennen.
```

## Passive Variant Bridge Lupe

Modul:

```text
DIO_MINI/report_passive_variant_bridge_lupe.py
```

Zweck:

```text
Die Variant-Bridge-Lupe gruppiert `variant_bridge_anchor` nach
Textinsel-Uebergang.

Sie zeigt, ob mehrere Familien denselben semantischen Wechsel tragen.
```

Report:

```text
debug/dio_mini_passive_variant_bridge_lupe_FG_vs_GH_20260607_v1
```

Befund:

```text
shared_variant_bridge:
  dio_text_15hzmqv -> dio_text_jwkf1a
  families = dio_095l | dio_0g9z | dio_0xkp | dio_1ocs
  avg_delta = -0.052447867

strengthening_variant_bridge:
  dio_text_1456g6j -> dio_text_1ne15hk
  families = dio_0x52 | dio_1lg2
  avg_delta = 0.079008733

thin_variant_bridge:
  dio_text_mr2id7 -> dio_text_zle8sl
  families = dio_1ffn | dio_1i05
  avg_delta = -0.011845333

single_strengthening_bridge:
  dio_text_1kx4hnb -> dio_text_19a4wib
  family = dio_140n

single_strengthening_bridge:
  dio_text_1o8gs8u -> dio_text_1xd64od
  family = dio_03yz
```

Lesart:

```text
Die interessanteste Bruecke ist aktuell:
  dio_0x52 | dio_1lg2

Sie traegt denselben Textinselwechsel und verstaerkt sich dabei.
Das ist kein Beweis fuer tiefe Semantik, aber ein staerkerer Kandidat als
ein exact_single_form_anchor.
```

## Passive Family Bridge Lineage

Modul:

```text
DIO_MINI/report_passive_family_bridge_lineage.py
```

Zweck:

```text
Ausgewaehlte dio_*-Familien ueber mehrere passive Inner-Maps verfolgen.
Damit wird sichtbar, ob eine Familie nur lokal vorkommt oder ueber mehrere
Weltvarianten driftet, reift, verschwindet, wiederkehrt oder Textinseln
wechselt.
```

Report:

```text
debug/dio_mini_passive_family_bridge_lineage_dio_0x52_dio_1lg2_20260607_v1
```

Befund `dio_0x52`:

```text
C:
  dio_text_cmxrx4
  score = 0.6272642
  state = inner_variation_bearing_space

D:
  dio_text_cmxrx4
  score = 0.658346867

E:
  dio_text_cmxrx4
  score = 0.673354733

F:
  dio_text_cmxrx4
  score = 0.572545067
  state = inner_drift_watch_space

F_G:
  dio_text_1456g6j
  score = 0.393777267
  state = inner_soft_variation_space

G_H:
  dio_text_1ne15hk
  score = 0.472786
  state = inner_soft_variation_space
```

Befund `dio_1lg2`:

```text
F_G:
  dio_text_1456g6j
  score = 0.393777267

G_H:
  dio_text_1ne15hk
  score = 0.472786
```

Lesart:

```text
dio_0x52 ist kein kurzer Einmalanker.

Die Familie:
  bleibt von C bis H sichtbar,
  reift C -> E,
  kippt in F in Drift,
  wechselt danach Textinsel,
  koppelt in F-G mit dio_1lg2,
  und staerkt sich in G-H gemeinsam mit dio_1lg2.

Das ist ein staerkerer Kandidat fuer semantische Beweglichkeit als eine
exakte Einzelform-Wiederholung.
```

## Passive Family Bridge Repro Check

Report:

```text
debug/dio_mini_passive_family_bridge_lineage_dio_0x52_dio_1lg2_F_vs_F_repro_20260607_v1
```

Befund:

```text
F / dio_0x52:
  Textinsel = dio_text_cmxrx4
  Zustand = inner_drift_watch_space
  Score = 0.572545067

F_REPRO / dio_0x52:
  Textinsel = dio_text_1456g6j
  Zustand = inner_stable_recurrence_space
  Score = 0.476246133

dio_1lg2:
  in diesem F-Repro-Schnitt nicht sichtbar
```

Lesart:

```text
dio_0x52 reproduziert sich als Familie, aber nicht als identische
Textinsel-Kopie.

Die Familie wechselt von einer Drift-Beobachtung in eine stabilere
Wiederkehr. Das ist fachlich naeher an organischer Bedeutungsumordnung als
an mechanischem Kopieren.

dio_1lg2 bleibt fuer diesen Repro-Schnitt offen. Die spaetere Bruecke
dio_0x52 | dio_1lg2 ist damit noch nicht als voll reproduziert bewertet,
sondern als Kandidat fuer weitere kontrollierte Varianten.
```

Wirkungsgrenze:

```text
rein passiv
keine Runtime-Lesung
keine Handlung
kein Gate
kein Entry-Signal
kein Richtungssignal
```
