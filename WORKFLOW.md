# Vorgehensdokumentation

## Ziel

Ein lokal gehostetes Open-Source-System aufbauen, das vier Modi in einer gemeinsamen Plattform vereint:

- Text zu Bild
- Bild zu Bild
- Text zu Video
- Bild zu Video

## Arbeitsweise

Die Umsetzung erfolgt nicht als starres Demo, sondern in mehreren Schichten:

1. Anforderungen klaeren
2. geeignete offene Modelle auswaehlen
3. modulare Laufzeitarchitektur aufbauen
4. lokale UI und Inferenzpfade implementieren
5. Hardware- und Betriebsworkflow dokumentieren
6. schrittweise echte Modelltests und Optimierung nachziehen
7. mobile Clients und Fine-Tuning-Schiene vorbereiten

## Bisherige Entscheidungen

### 1. Problem neu zugeschnitten

Ausgangspunkt war eine einzelne SDXL-Bilddemo. Diese war fuer das eigentliche Endziel zu eng, weil:

- sie nur Text zu Bild abdeckte
- keine Videoarchitektur vorsah
- keine austauschbaren Modellprofile besass
- keine saubere Erweiterungsstruktur bot

Deshalb wurde das Projekt auf eine Multi-Modal-Plattform umgestellt.

### 2. Modellstrategie festgelegt

Fuer Bilder:
- `FLUX.2 klein 4B` als offene Hauptbasis
- `FLUX.1 Kontext [dev]` optional fuer staerkeres Editing und Inpainting

Fuer Video:
- `Wan2.1 T2V 1.3B` als Einstieg
- `Wan2.1 T2V 14B` fuer bessere Qualitaet
- `Wan2.1 I2V 14B` fuer Bild-zu-Video

Begruendung:
- Bilder und Videos haben derzeit unterschiedliche Open-Source-Spitzenmodelle
- eine Mischarchitektur ist im lokalen Betrieb realistischer und flexibler
- offene Lizenzen und Hardwarebedarf lassen sich so besser austarieren

### 3. Codebasis modularisiert

Die monolithische Datei wurde in Verantwortungsbereiche geteilt:

- Konfiguration
- Runtime und Pipeline-Loading
- Medienausgabe
- UI

Das dient dazu, kuenftig weitere Modelle, Quantisierungen, APIs und Queueing hinzuzufuegen, ohne die App neu zu schreiben.

### 4. Android-Zielbild festgelegt

Vollstaendige On-Device-Inferenz auf typischen Android-Smartphones ist fuer die Zielmodelle derzeit nicht der realistische Standardweg.

Deshalb ist die strategische Entscheidung:
- Rechner oder Heimserver hostet die Modelle lokal
- Android greift ueber Browser oder spaetere App im lokalen Netz zu
- eine echte Lite-Variante bleibt optional fuer spaeter offen

### 5. Stiltraining eingeplant

Die Produktvision soll nicht bei Standardmodellen stehen bleiben.

Deshalb wird die Architektur offen gehalten fuer:
- eigene Datensaetze
- LoRA-Training oder Adaptertraining
- feste Stilprofile und projektspezifische Parameter

### 6. Filterfreiheit eingeordnet

Ziel ist eine lokale Runtime ohne externe Inhaltsmoderation oder SaaS-Schranken.

Technisch bedeutet das:
- keine Cloud-Moderation im Kernworkflow
- keine verpflichtende Remote-Pruefung
- optionale lokale Schutzmechanismen nur als separate, bewusst schaltbare Schicht

## Umgesetzte Schritte

### Phase A: Basissystem

Erledigt:
- Projekt analysiert
- alte Demo bewertet
- neue Modellstrategie abgeleitet

### Phase B: Softwarearchitektur

Erledigt:
- `imaginary_ai/config.py` fuer Modellprofile
- `imaginary_ai/runtime.py` fuer lazy loading und Inferenz
- `imaginary_ai/ui.py` fuer die vier Hauptmodi
- `main.py` als schlanker Einstiegspunkt
- Lite-Bildprofile fuer aktuelle Hardware und Android-nahe Nutzung

### Phase C: Dokumentation

Erledigt:
- README neu strukturiert
- dieses Vorgehensdokument angelegt
- mobile und Fine-Tuning-Pfade dokumentiert

### Phase D: Erste reale Validierung

Erledigt:
- Python-3.13-Laufzeit fuer die GPU eingerichtet
- CUDA-kompatibles PyTorch fuer `GTX 1080` installiert
- `SDXL Turbo Lite` als Text-zu-Bild real getestet
- `SDXL Turbo Lite` als Bild-zu-Bild real getestet
- `Wan2.1 T2V 1.3B` als reduzierter Text-zu-Video-Smoke-Test real getestet
- Offline-/Cache-Betrieb in Runtime und Startskripte eingebaut
- Offline-Runtime des app-eigenen T2V-Pfads erfolgreich verifiziert

## Offene technische Arbeit

### 1. Lokale Modellvalidierung

Noch offen:
- echte Paketinstallation
- Download der gewaehlten Modelle
- Test der vier Modi auf der vorhandenen Hardware

Teilweise erledigt:
- Bild-Lite-Pfade erfolgreich getestet
- kleiner T2V-Pfad erfolgreich getestet
- groessere Video- und I2V-Pfade noch offen
- I2V 14B auf aktueller Hardware vorlaeufig als Heavy/Experimentell eingeordnet

### 2. Performanceprofile

Geplant:
- Profile fuer 12 GB, 16 GB und 24 GB VRAM
- Offloading- und Quantisierungsoptionen
- schnellere Presets fuer Entwurf vs. Qualitaet

### 3. Produktionsreife

Geplant:
- REST-API
- Job-Queue
- Presets fuer Anwendungsfaelle
- strukturierte Output-Metadaten
- optional Upscaling- und Postprocessing-Stufe
- optional nativer Android-Client statt Browserzugriff

### 4. Datensatz- und Stiltraining

Geplant:
- Datensatzablage pro Stil oder Projekt
- Trainingskonfigurationen fuer LoRA
- Evaluationssatz fuer Stiltreue
- Versionierung der Trainingsartefakte

## Empfohlener Betriebsworkflow

### Stufe 1: Bildfunktionen stabilisieren

- Python-Umgebung einrichten
- `FLUX.2 klein 4B` lokal testen
- danach `FLUX.1 Kontext` fuer Editing pruefen

### Stufe 2: kleines Video-Profil aktivieren

- `Wan2.1 T2V 1.3B` bei 480p testen
- Laufzeiten, VRAM und Stabilitaet messen

### Stufe 3: schweres Video-Profil erweitern

- `Wan2.1 T2V 14B`
- `Wan2.1 I2V 14B 480P` oder `720P`

### Stufe 4: Nachbearbeitung

- Open-Source-Upscaling fuer Videos
- optional Frame-Interpolation
- optionale Stil- oder Qualitaets-Presets

### Stufe 5: Mobile Nutzung

- LAN-Start fuer Browserzugriff am Android-Geraet
- spaeter optional REST-API oder nativer Client

## Antwort auf die Skalierungsfrage

Ja, mehr als 480p ist mit Open Source moeglich.

Praktische Optionen:
- native 720p-Modelle einsetzen
- 720p erzeugen und danach auf 1080p hochskalieren
- 480p erzeugen und danach hochskalieren
- 1080p als Delivery-Profil eher mehrstufig denken als als erste Ausbaustufe

Wichtig fuer das fertige Produkt:
- 1080p-Profile muessen in UI und Ergebnisanzeige explizit als `Upscaling` markiert sein
- native und hochskalierte Ausgabe duerfen nicht sprachlich vermischt werden

Die wirtschaftlich und technisch sinnvollste Reihenfolge fuer ein lokales Projekt ist fast immer:

1. zuerst 480p stabil
2. dann 720p nativ
3. danach 1080p als HD-Zielprofil
