# 🎙️ Kev.FunASR v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Lizenz-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Plattform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/Datenschutz-100%25lokal-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/Abhängigkeiten-3pipPakete-success" alt="Deps">
</p>

<p align="center">
  <b>Echtzeit-Spracherkennung, sofort einsatzbereit.</b><br>
  Eine einzige Python-Datei. Keine Cloud. Alle Funktionen inklusive.
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <a href="README_zh.md">🇨🇳 中文</a> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <b>🇩🇪 Deutsch</b> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="Kev.FunASR UI — dark tech theme">
</p>

---

## Warum Kev.FunASR?

Echtzeit-Transkriptionstools fallen in zwei Kategorien:

| | Cloud-APIs | Desktop-Apps | **Kev.FunASR** |
|---|---|---|---|
| Datenschutz | ❌ Audio wird an Server gesendet | ✅ Lokal | ✅ **100% lokal, kein Netzwerk** |
| Kosten | ❌ Preis pro Minute | 💰 Einmalkauf | 🆓 **Für immer kostenlos** |
| Latenz | ⚠️ 1-3 Sekunden | ✅ Echtzeit | ✅ **SSE Push, <100ms** |
| Sprachen | ✅ 50+ | ⚠️ Begrenzt | ✅ **Auto-Erkennung 20+ Sprachen** |
| Untertitelexport | ⚠️ Zusätzliches Tool nötig | ⚠️ Festes Format | ✅ **Ein-Klick SRT** |
| Audioaufnahme | ❌ Nein | ✅ Ja | ✅ **Toggle für WAV-Speicherung** |
| KI-Zusammenfassung | ⚠️ API-Zusatzkosten | ❌ Selten | ✅ **Integriert (Ollama)** |
| Anpassung | ❌ Closed Source | ❌ Closed Source | ✅ **Vollständiger Code, 20 Themes** |
| Bereitstellung | N/A | Installer | 🚀 **Einzelne `.py`-Datei** |

**Die perfekte Balance:** Profi-Funktionen einer Cloud-API + Datenschutz einer lokalen App + eine modifizierbare Python-Datei.

---

## ✨ Funktionen

### 🎤 Echtzeit-Spracherkennung
Sprechen → Text erscheint sofort. Basierend auf **Alibaba SenseVoiceSmall** + VAD + Satzzeichen-Modell. Automatische Spracherkennung oder Festlegung auf eine Sprache.

### ⚡ SSE Echtzeit-Push
Kein Polling. Kein Neuladen. **Server-Sent Events** senden Text mit <100ms Latenz an den Browser.

### 📥 SRT-Untertitelexport
Ein Klick (oder Taste `S`) lädt eine standardmäßige `.srt`-Datei herunter. Direkt in Premiere, DaVinci Resolve usw. verwendbar.

### 🎙️ WAV-Audioaufnahme
Aufnahme einschalten → gesamtes Mikrofon-Audio wird als `.wav` auf dem Desktop gespeichert. Ausschalten → Header repariert, Datei bereit.

### 🧠 KI-Zusammenfassung (Ollama)
Wenn [Ollama](https://ollama.com) läuft, generiert die KI automatisch:
- **Mindmap** — visueller Themenbaum
- **Kernpunkte** — strukturierte Liste
- **Zitate** — beste wörtliche Aussagen

### 🌍 Echtzeit-Übersetzung
Sprache A transkribiert → sofort in Sprache B übersetzt. 20+ Sprachen verfügbar.

### 🎨 20 Themes
Nicht nur Dark Mode. **20 kuratierte Themes** — Cyber Green, Neon Night, Midnight Ink, Minimal White, Warm Paper und mehr.

---

## 🚀 Schnellstart

```bash
pip install funasr deep-translator numpy
# Optional: Ollama für KI-Zusammenfassung installieren
brew install ollama && ollama pull qwen2.5:14b
python3 funasr_live.py
open http://localhost:8765
```

Erster Start lädt ca. 400 MB ASR-Modelle herunter (für folgende Starts gecacht).

---

## ⌨️ Tastenkürzel

| Taste | Aktion |
|-------|--------|
| `Space` | Pause/Fortsetzen |
| `S` | SRT herunterladen |
| `R` | Aufnahme ein/aus |
| `1-4` | Tab wechseln |

---

## 📡 API

| Endpunkt | Beschreibung |
|----------|-------------|
| `/events` | SSE-Stream (Echtzeit) |
| `/api` | Letztes Ergebnis (Polling) |
| `/config` | Konfiguration & Status |
| `/download/srt` | SRT-Untertitel herunterladen |
| `/toggle_pause` | Mikrofon ein/aus |
| `/toggle_record` | Aufnahme ein/aus |
| `/set_lang?mode=de` | Sprache festlegen |
| `/set_translate?target=en` | Übersetzungsziel |

---

## 🔧 Konfiguration

`CONFIG` am Anfang von `funasr_live.py` bearbeiten:

```python
CONFIG = {
    "port": 8765,
    "chunk_seconds": 1.5,
    "sample_rate": 16000,
    "rms_threshold": 0.003,
    "bt_hfp_helper": True,
    "translate_enabled": True,
    "translate_target": "en",
}
```

---

## 🎯 Anwendungsfälle

| Szenario | Nutzen |
|----------|--------|
| Besprechungsnotizen | Aufnehmen + KI-Zusammenfassung + SRT |
| Content-Erstellung | Skripte diktieren |
| Sprachenlernen | Sprechen + Echtzeit-Übersetzung |
| Barrierefreiheit | Live-Untertitel für Präsentationen |
| Interviews | WAV aufnehmen + Transkription mit Zeitstempeln |
| Video-Untertitelung | SRT direkt generieren |
| Live-Streaming | UI als Untertitel-Overlay einbetten |

---

## 📦 Abhängigkeiten

```text
funasr >= 1.3.0
deep-translator >= 1.11
numpy >= 1.24
```

Kein Node.js, Docker oder CUDA. Nur Python + pip.

---

## 📄 Lizenz

MIT — freie Nutzung, Modifikation und kommerzielle Nutzung erlaubt.

---

<p align="center">
  <sub>Mit ❤️ von <a href="https://superk.ai">Mr.K Lab</a> · Nutzt <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
