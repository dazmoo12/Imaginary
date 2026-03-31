# Uebergabeprotokoll

## Projektstand

Das Projekt wurde von einer einfachen Bilddemo zu einer lokalen Open-Source-Media-KI weiterentwickelt.

Aktuell vorhanden:
- Text zu Bild
- Bild zu Bild
- Text zu Video
- Bild zu Video als Architekturpfad
- Android-Zugriff ueber lokalen Browser/LAN-Host
- Vorbereitung fuer Datensaetze und spaeteres LoRA-/Style-Finetuning

## Real validiert

Auf der vorhandenen Hardware wurden erfolgreich getestet:

- `SDXL Turbo Lite` Text-zu-Bild
- `SDXL Turbo Lite` Bild-zu-Bild
- `Wan2.1 T2V 1.3B` als reduzierter Text-zu-Video-Smoke-Test
- App-Runtime im Offline-/Cache-Modus fuer den lokalen Betrieb

## Hardwarebasis

Erkannt und eingerichtet:
- NVIDIA GeForce GTX 1080
- 8 GB VRAM
- Python 3.13
- CUDA-faehiges `torch 2.6.0+cu126`

## Wichtige Dateien

- [README.md](C:/Users/Mo/Projects/Imaginary/README.md): Hauptanleitung
- [WORKFLOW.md](C:/Users/Mo/Projects/Imaginary/WORKFLOW.md): Vorgehen und Architekturentscheidungen
- [TRAINING.md](C:/Users/Mo/Projects/Imaginary/TRAINING.md): Datensatz- und Fine-Tuning-Richtung
- [main.py](C:/Users/Mo/Projects/Imaginary/main.py): App-Einstiegspunkt
- [imaginary_ai/config.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/config.py): Modelle und Defaults
- [imaginary_ai/runtime.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/runtime.py): Laden und Inferenz
- [imaginary_ai/ui.py](C:/Users/Mo/Projects/Imaginary/imaginary_ai/ui.py): Gradio-Oberflaeche
- [scripts/start_local.ps1](C:/Users/Mo/Projects/Imaginary/scripts/start_local.ps1): lokaler Offline-Start
- [scripts/start_lan.ps1](C:/Users/Mo/Projects/Imaginary/scripts/start_lan.ps1): Android/LAN-Start

## So probierst du es aus

### Lokal am Rechner

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_local.ps1
```

Oder einfacher per Doppelklick:

```text
start-local.cmd
```

Danach im Browser:

```text
http://127.0.0.1:7860
```

### Vom Android-Smartphone

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_lan.ps1
```

Oder einfacher per Doppelklick:

```text
start-lan.cmd
```

Dann die angezeigte `http://<deine-ip>:7860`-Adresse auf dem Smartphone im gleichen WLAN oeffnen.

## Bereits erzeugte Smoke-Test-Dateien

- [outputs/sdxl-turbo-smoke-test.png](C:/Users/Mo/Projects/Imaginary/outputs/sdxl-turbo-smoke-test.png)
- [outputs/sdxl-turbo-i2i-smoke-test.png](C:/Users/Mo/Projects/Imaginary/outputs/sdxl-turbo-i2i-smoke-test.png)
- [outputs/wan-t2v-smoke-test.mp4](C:/Users/Mo/Projects/Imaginary/outputs/wan-t2v-smoke-test.mp4)
- [outputs/wan-t2v-1-3b-45.mp4](C:/Users/Mo/Projects/Imaginary/outputs/wan-t2v-1-3b-45.mp4)

## Noch offen

- Bild-zu-Video auf der aktuellen Hardware
- groessere FLUX-/Wan-Profile
- REST-API oder nativer Android-Client
- echter LoRA-Trainingslauf
- sauberes GitHub-Remote fuer spaetere Weiterarbeit

## GitHub-Status

Lokal kann ein sauberer Git-Stand erstellt werden.

Fuer den finalen Push auf GitHub fehlt aktuell mindestens eines davon:
- ein bestehendes leeres Ziel-Repository
- oder `gh` plus authentifizierter GitHub-CLI-Zugang
- oder ein anderer Repo-Erstellpfad
