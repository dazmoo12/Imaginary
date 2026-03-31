# Training und Datensaetze

## Ziel

Dieses Projekt soll spaeter nicht nur Standardmodelle verwenden, sondern auch eigene Stilpraegungen aufnehmen koennen.

Die bevorzugte Richtung dafuer ist:
- LoRA-Training
- Adapter statt Vollfinetuning
- getrennte Datensaetze pro Stil oder Projekt

## Warum LoRA statt Vollfinetuning

- deutlich geringerer Speicherbedarf
- schneller iterierbar
- besser fuer mehrere Stilrichtungen parallel
- einfacher als modulare Zusatzgewichte verteilbar

## Geplanter Workflow

1. Datensatz pro Stil oder Anwendungsfall sammeln
2. Bilder kuratieren und beschriften
3. Trainingssatz und Evaluationssatz trennen
4. LoRA auf geeignetem Basismodell trainieren
5. LoRA lokal in die Generierungspipeline laden
6. Stiltreue und Nebenwirkungen vergleichen

## Empfohlene Datensatzstruktur

Siehe auch [datasets/README.md](C:/Users/Mo/Projects/Imaginary/datasets/README.md).

Grundidee:
- ein Ordner pro Stil
- Rohdaten getrennt von kuratierten Bildern
- Prompts, Metadaten und Bewertung getrennt mitfuehren

## Wichtige Regeln fuer gute Stil-Datensaetze

- lieber 30 bis 200 gute Bilder als viele schwache
- moeglichst konsistente Stilabsicht
- unterschiedliche Motive, aber stabile Formsprache
- schlechte, verrauschte oder widerspruechliche Bilder aussortieren

## Projektstatus

Aktuell vorbereitet:
- Datensatzordner
- Beispielkonfigurationen fuer spaetere Trainingsprofile

Noch nicht implementiert:
- vollstaendige Trainingsskripte
- LoRA-Loader in der UI
- automatisierte Evaluationsstrecke
