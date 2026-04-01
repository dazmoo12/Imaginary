# Imaginary Local Media AI

Dieses Projekt entwickelt sich von einer einzelnen Bilddemo zu einer lokal gehosteten Open-Source-Media-KI weiter.

Zielbild:
- Text zu Bild
- Bild zu Bild
- Text zu Video
- Bild zu Video

Die aktuelle Basis ist modular aufgebaut, damit wir Modelle, Hardwareprofile und Workflows schrittweise erweitern koennen.

## Neue Produktziele

Zusatzanforderungen, die jetzt in die Architektur aufgenommen sind:

- Android-Nutzung:
  - primaer als mobiler Client gegen den lokal gehosteten Rechner
  - optional spaeter als echte Lite-Variante mit kleineren Modellen
- Datensatzgestuetzte Stilsteuerung:
  - Vorbereitung fuer LoRA-/Style-Finetuning und projektspezifische Parameter
- Keine externe Moderation:
  - keine Cloud-Pruefung oder SaaS-Filter in der App-Schicht
  - lokale optionale Sicherheitslogik bleibt bewusst getrennt von der Kernpipeline

## Architekturentscheidung

Stand 31.03.2026 ist fuer dieses Vorhaben eine zweigeteilte Open-Source-Strategie sinnvoll:

- Bilder:
  - `FLUX.2 klein 4B` als offene Hauptbasis mit Apache-2.0-Lizenz
  - optional `FLUX.1 Kontext [dev]` fuer staerkeres instruktionbasiertes Editing und Inpainting
- Video:
  - `Wan2.1 T2V 1.3B` als lokal realistische Einstiegsversion
  - `Wan2.1 T2V 14B` fuer hoehere Qualitaet
  - `Wan2.1 I2V 14B 480P/720P` fuer Bild-zu-Video
  - `1080P` als klar gekennzeichnetes HD-Zielprofil ueber 720P plus Upscaling

Warum diese Aufteilung:
- Bild- und Video-Modelle haben derzeit unterschiedliche Sweet Spots.
- Ein einziges lokales Open-Source-Modell fuer alles ist noch kein sauberer Kompromiss aus Qualitaet, Lizenz und Hardwarebedarf.
- Mit dieser Architektur koennen wir eine gemeinsame lokale App betreiben und spaeter einzelne Teile austauschen.

## Aktueller Umsetzungsstand

Bereits umgesetzt:
- modulare Python-Struktur statt Ein-Datei-Demo
- Gradio-Oberflaeche mit vier Modi
- lazy loading fuer Pipelines
- Ausgabepfad fuer Videos
- Modellprofile mit Lizenz- und VRAM-Hinweisen
- Android-tauglicher Zugriffspfad ueber LAN-Startskript vorgesehen
- Projektpfade fuer Datensaetze und Fine-Tuning vorbereitet
- lokale CUDA-Laufzeit fuer `GTX 1080 8GB` erfolgreich eingerichtet
- `SDXL Turbo Lite` erfolgreich fuer Text-zu-Bild und Bild-zu-Bild lokal getestet
- `Wan2.1 T2V 1.3B` erfolgreich als kleiner lokaler Text-zu-Video-Smoke-Test ausgefuehrt
- Startskripte laufen im Offline-/Cache-Modus fuer den fertigen lokalen Betrieb
- Offline-Runtime fuer den App-eigenen Text-zu-Video-Pfad erfolgreich verifiziert
- schwere `I2V 14B`-Profile sind fuer `GTX 1080 8GB` derzeit als `Heavy/Experimentell` einzuordnen

Noch nicht voll validiert:
- echter Download aller grossen Modelle
- Volltest der Video-Inferenz
- Performance-Tuning pro GPU-Klasse
- schwere FLUX- und Wan-Profile auf `8 GB VRAM`
- Bild-zu-Video auf dieser Hardware

## Projektstruktur

- [main.py](C:/Users/Mo/Projects/Imaginary/main.py): Startpunkt der lokalen App
- [imaginary_ai/config.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/config.py): Modell- und Taskkonfiguration
- [imaginary_ai/runtime.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/runtime.py): Pipeline-Management und Inferenzlogik
- [imaginary_ai/ui.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/ui.py): Gradio-Oberflaeche
- [imaginary_ai/media.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/media.py): Medien-Ausgabeordner
- [WORKFLOW.md](C:/Users/Mo/Projects/Imaginary/WORKFLOW.md): detaillierte Dokumentation des Vorgehens
- [TRAINING.md](C:/Users/Mo/Projects/Imaginary/TRAINING.md): Datensatz- und Fine-Tuning-Workflow
- [datasets/README.md](C:/Users/Mo/Projects/Imaginary/datasets/README.md): erwartete Datensatzstruktur
- [scripts/start_local.ps1](C:/Users/Mo/Projects/Imaginary/scripts/start_local.ps1): lokaler Start nur fuer den Rechner selbst
- [scripts/start_lan.ps1](C:/Users/Mo/Projects/Imaginary/scripts/start_lan.ps1): LAN-Start fuer Android-Zugriff per Browser

## Setup

### 1. Python-Umgebung

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Danach GPU-Profil passend zur Karte installieren:

```powershell
# Fuer GTX 1080 / Pascal
uv pip install --python .venv\Scripts\python.exe -r requirements-gpu-pascal-cu126.txt --index-url https://download.pytorch.org/whl/cu126

# Fuer modernere NVIDIA-Karten
uv pip install --python .venv\Scripts\python.exe -r requirements-gpu-modern-cu128.txt --index-url https://download.pytorch.org/whl/cu128
```

### 2. Hugging Face Auth bei Bedarf

```powershell
$env:HF_TOKEN="dein_token"
```

Oder dauerhaft projektlokal:

```text
.env
```

Beispiel:

```text
HF_TOKEN=hf_your_token_here
```

Eine Vorlage liegt in [.env.example](C:/Users/Mo/Projects/Imaginary/.env.example).

### 3. App starten

```powershell
python main.py
```

Danach im Browser:

```text
http://127.0.0.1:7860
```

### Einfacher Windows-Start ohne PowerShell-Aktivierung

Per Doppelklick oder in `cmd`:

```text
start-local.cmd
```

Fuer Android/LAN:

```text
start-lan.cmd
```

Benutzerfreundliche Launcher fuer den Alltag:

```text
Imaginary Local AI.cmd
Imaginary LAN AI.cmd
```

Diese Dateien:
- starten die App
- oeffnen automatisch den Browser
- nutzen auf diesem Geraet bevorzugt die privaten Starter mit lokal hinterlegtem Token, falls vorhanden

Die Oberfläche bietet bereits:
- ein einfaches Prompt-Feld fuer `Text zu Bild`
- Drag & Drop fuer Bilder bei `Bild zu Bild` und `Bild zu Video`
- Modellwahl pro Modus direkt in der UI

### Android-Zugriff im gleichen Netzwerk

## Welche Datei starte ich?

Fuer den normalen Alltag auf diesem privaten Geraet:
- [Imaginary Local AI.cmd](C:/Users/Mo/Projects/Imaginary/Imaginary%20Local%20AI.cmd)

Fuer Zugriff vom Android-Smartphone im gleichen Netzwerk:
- [Imaginary LAN AI.cmd](C:/Users/Mo/Projects/Imaginary/Imaginary%20LAN%20AI.cmd)

Technischer Hintergrund:
- beide Launcher starten die Gradio-App
- beide oeffnen den Browser automatisch
- gerechnet wird immer auf deinem PC, nicht auf dem Smartphone
- das Smartphone ist in diesem Setup nur Browser-Client, Fernbedienung und Anzeige

Wenn du die App vom Android-Smartphone aus nutzen willst:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_lan.ps1
```

Dann oeffnest du auf dem Smartphone die angezeigte lokale Netzwerkadresse im Browser.

Hinweis:
- Die Startskripte setzen Offline-Betrieb aus dem lokalen Modellcache.
- Neue Modelle sollten deshalb zuerst einmal mit Netzwerkzugang vorgeladen werden.
- Wenn eine `.env` im Projekt liegt, laden die Startskripte `HF_TOKEN` automatisch daraus.

## Hardware-Einordnung

Praktisch sinnvolle Startstufen:

- 12 bis 16 GB VRAM:
  - stark fuer Bild
  - eingeschraenkt fuer kleine bis mittlere Video-Workflows
- 24 GB VRAM:
  - deutlich besser fuer offene Video-Modelle
  - sinnvoll fuer `Wan2.1 14B`
- darunter:
  - Bilder oft noch machbar
  - Video eher nur mit kleineren Profilen, Offloading und Geduld

Spezifisch fuer die aktuell erkannte Hardware:
- `GTX 1080 8GB` ist fuer schwere FLUX- und Wan-Profile knapp
- deshalb ist ein stufenweiser Ausbau mit kleineren Profilen, CPU-Offloading und klaren Mobil-/Desktop-Rollen sinnvoll
- `SDXL Turbo Lite` ist auf dieser Hardware bereits erfolgreich end-to-end bestaetigt
- `Wan2.1 T2V 1.3B` laeuft als reduzierter Smoke-Test lokal, ist aber deutlich langsamer als die Bildpfade
- fuer die App sind konservative Video-Defaults gesetzt: 4 Schritte, 9 Frames, 8 FPS

Praktische Einstufung fuer diese Karte:
- `SDXL Turbo Lite`: gut geeignet
- `FLUX.2 klein 4B`: moeglich, aber deutlich schwerer
- `Wan2.1 T2V 1.3B`: machbar als kleiner lokaler Videopfad
- `Wan2.1 I2V 14B`: eher Heavy/Experimentell statt alltagstauglicher Standard

## Modelle in der UI

### Text zu Bild

- `SDXL Turbo Lite`
  - schnellster lokaler Bildpfad
  - gut fuer schnelle Entwuerfe, Tests und alltaegliche Nutzung auf deiner `GTX 1080 8GB`
- `FLUX.2 klein 4B`
  - qualitativ staerkeres offenes Bildmodell
  - langsamer und schwerer als `SDXL Turbo Lite`

### Bild zu Bild

- `SDXL Turbo Lite`
  - schnellster Bildbearbeitungs-Pfad fuer dein aktuelles System
  - gut fuer Stilvarianten und grobe Umdeutungen vorhandener Bilder
- `FLUX.2 klein 4B`
  - staerkere offene Qualitaetsoption fuer Bildbearbeitung
  - braucht deutlich mehr Ressourcen
- `FLUX.1 Kontext [dev]`
  - besonders fuer instruktionbasierte Bearbeitung gedacht
  - gut, wenn du ein Bild sehr gezielt nach Textanweisung veraendern willst
- `FLUX.1 Kontext Inpaint [dev]`
  - wie `FLUX.1 Kontext`, aber zusaetzlich fuer gezielte Teilbereiche per Maske
  - sinnvoll fuer Austausch, Retusche und Inpainting

### Text zu Video

- `Wan2.1 T2V 1.3B`
  - kleinstes und praktischstes Video-Modell in diesem Projekt
  - dein sinnvoller Startpunkt fuer lokale Videotests
- `Wan2.1 T2V 14B [Heavy]`
  - deutlich groesser und qualitativ staerker
  - fuer staerkere GPUs gedacht
- `Wan2.1 T2V 14B 1080P via Upscaling [Heavy]`
  - erzeugt intern niedriger und skaliert auf HD hoch
  - klar als Upscaling-Profil gedacht, nicht als native 1080p-Generierung

### Bild zu Video

- `Wan2.1 I2V 14B 480P [Heavy/Experimentell]`
  - kreativ starker, aber schwerer Bild-zu-Video-Pfad
  - auf deiner Hardware eher Test- oder Spezialfall
- `Wan2.1 I2V 14B 720P [Heavy/Experimentell]`
  - noch anspruchsvoller
  - aktuell nicht als Alltagspfad gedacht
- `Wan2.1 I2V 14B 1080P via Upscaling [Heavy/Experimentell]`
  - HD-Ausgabe ueber Upscaling
  - ebenfalls klar als Heavy-/Experimentell-Profil gedacht

Faustregel fuer die Auswahl:
- `Lite` oder kleine Modelle fuer Alltag, schnelle Versuche und haeufige Nutzung
- `Heavy` fuer kreative Einzelprojekte, mehr Wartezeit und bessere Hardware
- `Experimentell` bedeutet: technisch moeglich, aber auf deiner aktuellen GPU nicht als bequemer Standard zu erwarten

## Modellunterschiede in der Praxis

### Bildmodelle

- `SDXL Turbo Lite`
  - schnellster und leichtester Pfad im Projekt
  - gut fuer Entwuerfe, Android-Lite-Ideen und erste lokale Tests
  - schwacher bei Praezision und komplexen Bearbeitungen als die FLUX-Modelle

- `FLUX.2 klein 4B`
  - moderneres offenes Bildmodell
  - besser fuer hochwertige Text-zu-Bild- und Bild-zu-Bild-Ergebnisse
  - schwerer als `SDXL Turbo Lite`

- `FLUX.1 Kontext [dev]`
  - staerker bei instruktionbasierten Aenderungen und Inpainting
  - gut fuer gezielte Bildbearbeitung
  - schwerer und zudem non-commercial lizenziert

### Videomodelle

- `Wan2.1 T2V 1.3B`
  - kleinstes sinnvolles offenes Video-Modell in unserem Stack
  - daher unser aktueller realistischer Einstieg fuer deine Hardware
  - trotzdem viel schwerer und langsamer als Bildmodelle

- `Wan2.1 T2V 14B`
  - deutlich groesser und qualitativ staerker
  - gedacht fuer groessere GPUs
  - auf deiner Karte eher kein Standardworkflow

- `Wan2.1 I2V 14B`
  - Bild-zu-Video ist zusaetzlich schwerer als Text-zu-Video, weil zum Prompt noch das Eingabebild konsistent verarbeitet werden muss
  - das Modell ist gross und speicherhungrig
  - deshalb auf `GTX 1080 8GB` eher experimentell

## Bedeutung der UI-Parameter

### Allgemeine Parameter

- `Modell`
  - waehlt das konkrete KI-Modell fuer den jeweiligen Modus aus
  - bestimmt vor allem Qualitaet, Geschwindigkeit und Hardwarebedarf

- `Prompt`
  - deine Textanweisung an das Modell
  - beschreibt Motiv, Stil, Licht, Stimmung, Kameraeindruck oder Aenderungswunsch

- `Seed`
  - Startwert fuer den Zufall
  - gleicher Seed plus gleiche Einstellungen ergibt meist sehr aehnliche Ergebnisse
  - anderer Seed erzeugt Varianten

### Bild-Parameter

- `Inference Steps`
  - Anzahl der Rechenschritte pro Bild
  - mehr Schritte koennen sauberere Ergebnisse bringen, kosten aber Zeit

- `Guidance`
  - wie stark sich das Modell an deinen Prompt haelt
  - hoeher bedeutet meist strengere Prompt-Treue
  - zu hoch kann Ergebnisse aber unnatuerlich wirken lassen

- `Strength`
  - nur fuer Bearbeitungsmodi mit Ausgangsbild relevant
  - bestimmt, wie stark das Originalbild veraendert wird
  - niedrig = nah am Original
  - hoch = staerkere Umgestaltung

- `Ausgangsbild`
  - das per Drag & Drop geladene Bild
  - dient bei `Bild zu Bild` und `Bild zu Video` als Grundlage

- `Maske`
  - nur fuer Inpainting-Modelle relevant
  - markiert gezielt die Bildbereiche, die veraendert werden sollen

### Video-Parameter

- `Frames`
  - Anzahl der erzeugten Einzelbilder des Clips
  - mehr Frames bedeuten meist laengere oder etwas fluessigere Videos, aber deutlich mehr Rechenzeit

- `FPS`
  - Wiedergabegeschwindigkeit in Bildern pro Sekunde
  - hoehere FPS wirken fluessiger
  - bei gleicher Framezahl wird der Clip dadurch kuerzer

Praktische Lesart fuer dein System:
- `Inference Steps` = Qualitaet gegen Zeit
- `Guidance` = Prompt-Treue
- `Strength` = Eingriff ins Ausgangsbild
- `Frames` = Hauptkostentreiber bei Video
- `FPS` = Wiedergabegeschwindigkeit
- `Seed` = Variantenregler

## Warum Video so viel laenger dauert als Bild

Das ist leider normal.

Bei Bildmodellen entsteht genau ein Bild.
Bei Videomodellen muessen dagegen viele Frames erzeugt und zeitlich konsistent gehalten werden.

Das bedeutet praktisch:
- mehr Rechenschritte
- mehr Speicherbedarf
- mehr Daten beim ersten Download
- laengeres Laden grosser Gewichte
- zusaetzliche Verarbeitung bei Bild-zu-Video

Deshalb fuehlen sich selbst kleine Video-Tests oft unverhaeltnismaessig langsam an, besonders auf aelteren 8-GB-Karten.

## Android-Strategie

Fuer dieses Projekt ist die sinnvollste Android-Loesung nicht native Vollinferenz auf dem Smartphone, sondern:

1. Desktop oder Heimserver rechnet lokal
2. Android fungiert als mobiler Client im Browser
3. spaeter optional eine Lite-Variante mit kleineren Modellen oder abgespeckten Features

Warum:
- moderne offene Video- und starke Bildmodelle sind fuer typische Smartphone-Specs zu schwer
- Browser- oder App-Client gegen einen lokalen Host behaelt trotzdem den voll lokalen Betrieb

## Stiltraining und individuelle Parameter

Das Projekt bleibt bewusst offen fuer spaeteres Nachtrainieren:

- Stilsteuerung ueber LoRA statt Vollfinetuning
- eigene Datensaetze pro Stil, Produktfamilie oder Markenlook
- spaeter auch projektinterne Presets und Parameterprofile

Details und Datensatzstruktur stehen in [TRAINING.md](C:/Users/Mo/Projects/Imaginary/TRAINING.md) und [datasets/README.md](C:/Users/Mo/Projects/Imaginary/datasets/README.md).

## Moderation und Filter

Diese App ist als lokale Runtime ohne externe Cloud-Moderation ausgelegt.

Konkret:
- keine SaaS-Filterung in der App-Schicht
- keine automatische Weiterleitung an externe Moderationsdienste
- optionale lokale Schutzlogik waere spaeter separat und explizit aktivierbar

Wichtig:
- lokal und filterarm bedeutet nicht fuer rechtswidrige Nutzung gedacht
- die Verantwortung bleibt beim Betreiber

## Videoaufloesung

Mehr als 480p ist mit Open Source grundsaetzlich moeglich.

Praktisch relevante Wege:
- native 720p-Generierung mit `Wan2.1 T2V 14B` oder `Wan2.1 I2V 14B 720P`
- 720p-Generierung plus anschliessendes Upscaling auf `1080P`
- 480p-Generierung plus anschliessendes Open-Source-Upscaling
- spaeter optional Frame-Interpolation und Nachschaerfung

Fuer einen stabilen lokalen Start ist 480p oft sinnvoller. Danach skaliert man auf 720p und fuer HD-Lieferung auf 1080p hoch, sobald Hardware und Workflow stabil sind.

## Naechste sinnvolle Schritte

- erste Bildpipelines lokal verifizieren
- kleines Text-zu-Video-Profil validieren
- danach 720p-Video und Upscaling als zweite Stufe aktivieren
- mobilen LAN-Zugriff am Android-Geraet pruefen
- Datensatz-Workflow fuer spaetere LoRA-Trainings vorbereiten

## Bereits validierte Smoke-Tests

- Text zu Bild:
  - [outputs/sdxl-turbo-smoke-test.png](C:/Users/Mo/Projects/Imaginary/outputs/sdxl-turbo-smoke-test.png)
- Bild zu Bild:
  - [outputs/sdxl-turbo-i2i-smoke-test.png](C:/Users/Mo/Projects/Imaginary/outputs/sdxl-turbo-i2i-smoke-test.png)
- Text zu Video:
  - [outputs/wan-t2v-smoke-test.mp4](C:/Users/Mo/Projects/Imaginary/outputs/wan-t2v-smoke-test.mp4)
  - [outputs/wan-t2v-1-3b-45.mp4](C:/Users/Mo/Projects/Imaginary/outputs/wan-t2v-1-3b-45.mp4)
