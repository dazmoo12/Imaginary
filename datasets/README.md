# Datensatzstruktur

## Empfohlene Ordnerstruktur

```text
datasets/
  style_name/
    raw/
    curated/
    captions/
    eval/
    notes.md
```

## Bedeutung

- `raw/`: unbearbeitete Quellbilder
- `curated/`: bereinigte Trainingsbilder
- `captions/`: Prompt- oder Beschriftungsdateien
- `eval/`: kleiner Vergleichssatz fuer Qualitaetspruefung
- `notes.md`: Stilbeschreibung, Herkunft, Besonderheiten

## Empfehlungen

- keine gemischten Stilrichtungen in einem einzelnen Stilordner
- urheberrechtliche Situation vor Verwendung klaeren
- immer einen kleinen Eval-Satz zurueckhalten
