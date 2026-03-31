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

### 3. App starten

```powershell
python main.py
```

Danach im Browser:

```text
http://127.0.0.1:7860
```

### Android-Zugriff im gleichen Netzwerk

Wenn du die App vom Android-Smartphone aus nutzen willst:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_lan.ps1
```

Dann oeffnest du auf dem Smartphone die angezeigte lokale Netzwerkadresse im Browser.

Hinweis:
- Die Startskripte setzen Offline-Betrieb aus dem lokalen Modellcache.
- Neue Modelle sollten deshalb zuerst einmal mit Netzwerkzugang vorgeladen werden.

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
