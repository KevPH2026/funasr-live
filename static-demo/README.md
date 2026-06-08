# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/privacy-100%25%20local-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/dependencies-3%20pip%20packages-success" alt="Deps">
</p>

<p align="center">
  <b>Real-time speech-to-text that just works.</b><br>
  One Python file. Zero cloud. All features included.
</p>

<p align="center">
  <b>🇺🇸 English</b> · <a href="README_zh.md">🇨🇳 中文</a> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## Why FunASR Live?

> 📖 See [ENHANCEMENTS.md](ENHANCEMENTS.md) for what we built on top of the original FunASR.

Most real-time transcription tools fall into two camps:

| | Cloud APIs | Desktop Apps | **FunASR Live** |
|---|---|---|---|
| Privacy | ❌ Audio sent to servers | ✅ Local | ✅ **100% local, zero network** |
| Cost | ❌ Per-minute pricing | 💰 One-time purchase | 🆓 **Free, forever** |
| Latency | ⚠️ 1-3 seconds | ✅ Real-time | ✅ **SSE push, sub-100ms** |
| Languages | ✅ 50+ | ⚠️ Limited | ✅ **Auto-detect 20+ languages** |
| Subtitle Export | ⚠️ Extra tool needed | ⚠️ Format lock-in | ✅ **SRT one-click** |
| Audio Recording | ❌ No | ✅ Often | ✅ **Toggle-to-save WAV** |
| AI Summarization | ⚠️ API extra cost | ❌ Rare | ✅ **Built-in (Ollama)** |
| Customization | ❌ Closed source | ❌ Closed | ✅ **Full source, 20 themes** |
| Deployment | N/A | Installer | 🚀 **Single `.py` file** |

**The sweet spot:** Professional-grade features of a cloud API, with the privacy of a local app, in a single hackable Python file.

---

## ✨ What It Does

### 🎤 Real-time Transcription
Speak — see text appear instantly. Powered by **Alibaba SenseVoiceSmall** with VAD (voice activity detection) and a punctuation restoration model. Auto-detects language or locks to one.

### ⚡ SSE Live Push
No polling. No refresh. Text streams to the browser via **Server-Sent Events** with sub-100ms latency. The UI updates the moment the model finishes a chunk.

### 📥 SRT Subtitle Export
One click (or press `S`) downloads a standard `.srt` file with timestamps. Drop it directly into Premiere, DaVinci Resolve, or any video editor.

### 🎙️ WAV Audio Recording
Toggle recording on — every mic chunk gets written to a timestamped `.wav` file on your desktop. Toggle off — header gets fixed, file is ready. No post-processing needed.

### 🧠 AI Summarization *(Ollama)*
If you have [Ollama](https://ollama.com) running, the AI auto-generates:
- **Mindmap** — visual tree of topics discussed
- **Key Points** — structured bullet list of arguments
- **Golden Quotes** — best verbatim lines

Works with any Ollama model (qwen2.5, llama3, deepseek, etc.)

### 🌍 Real-time Translation
Speech transcribed in language A → instant translation to language B. 7 target languages. Zero-config Google Translate integration (can be disabled for full offline mode).

### 🎨 20 Color Themes
Not just dark mode. **20 curated themes** — cyber green, neon night, midnight ink, minimal white, warm paper, forest deep, sunset orange, arctic frost, and more. Each one changes fonts, spacing, glow effects, and color palette.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install funasr deep-translator numpy

# 2. (Optional) Install Ollama for AI summarization
brew install ollama && ollama pull qwen2.5:14b

# 3. Run — that's it
python3 funasr_live.py

# 4. Open browser
open http://localhost:8765
```

First run downloads ~400MB of ASR models (cached for subsequent runs).

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Pause / Resume transcription |
| `S` | Download SRT subtitles |
| `R` | Toggle WAV recording |
| `1` | Switch to History tab |
| `2` | Switch to Mindmap tab |
| `3` | Switch to Key Points tab |
| `4` | Switch to Quotes tab |

---

## 📡 API Reference

All endpoints are GET-only for simplicity. Use as a backend for your own apps.

| Endpoint | Returns | Description |
|----------|---------|-------------|
| `/events` | SSE stream | Real-time transcription push |
| `/api` | JSON | Latest result (polling fallback) |
| `/config` | JSON | Current settings and status |
| `/download/srt` | `.srt` file | Export subtitles |
| `/summary` | JSON | Latest AI summary |
| `/toggle_pause` | JSON | Toggle mic on/off |
| `/toggle_record` | JSON | Toggle WAV saving |
| `/set_lang?mode=zh` | JSON | Set language lock |
| `/set_translate?target=en` | JSON | Set translation target |

---

## 🏗️ Architecture

```
┌──────────┐    ffmpeg     ┌──────────────┐    SSE    ┌───────────┐
│  Mic 🎤  │ ────────────→ │ SenseVoice   │ ────────→ │  Browser  │
│  (local) │   1.5s chunk  │ Small + VAD  │  <100ms   │  :8765    │
└──────────┘               └──────┬───────┘           └───────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              ┌──────────┐ ┌───────────┐ ┌───────────┐
              │ Punc      │ │ Google    │ │ Ollama    │
              │ Model     │ │ Translate │ │ Summarize │
              │ (zh/en)   │ │ (7 langs) │ │ (mindmap) │
              └──────────┘ └───────────┘ └───────────┘
                    │             │             │
                    ▼             ▼             ▼
              ┌──────────────────────────────────────┐
              │  History → SRT export                │
              │  PCM chunks → WAV recording          │
              │  All local, no cloud dependency      │
              └──────────────────────────────────────┘
```

---

## 🔧 Configuration

Edit the top of `funasr_live.py`:

```python
CONFIG = {
    "port": 8765,                # Web UI port
    "chunk_seconds": 1.5,        # Audio chunk size (lower = less latency)
    "sample_rate": 16000,        # 16kHz mono
    "rms_threshold": 0.003,      # Silence detection threshold
    "bt_hfp_helper": True,       # macOS: auto-open QuickTime for BT HFP mode
    "translate_enabled": True,   # Enable Google Translate
    "translate_target": "en",    # Default target language
}
```

---

## 🎯 Use Cases

| Scenario | How FunASR Live Helps |
|----------|----------------------|
| **Meeting notes** | Record + get AI summary + export SRT for minutes |
| **Content creation** | Dictate scripts, get instant text output |
| **Language learning** | Speak + see translation in real-time |
| **Accessibility** | Live captions for presentations or calls |
| **Research interviews** | Record WAV + get timestamped transcript |
| **Video subtitling** | Generate SRT directly, no manual timing |
| **Live streaming** | Embed the UI as a caption overlay |
| **Privacy-first setups** | Medical, legal, or confidential scenarios where cloud APIs aren't allowed |

---

## 📦 Dependencies

```text
funasr >= 1.3.0          # Alibaba SenseVoiceSmall ASR engine
deep-translator >= 1.11  # Google Translate (optional)
numpy >= 1.24             # Audio buffer math
```

That's it. No Node.js, no Docker, no CUDA toolkit. Just Python + pip.

---

## 🤝 Contributing

Found a bug? Want a new theme? PRs welcome.

```bash
git clone https://github.com/KevPH2026/funasr-live.git
cd funasr-live
python3 funasr_live.py
```

---

## 📄 License

MIT — do whatever you want. Build products on it, fork it, sell it.

---

<p align="center">
  <sub>Made with ❤️ by <a href="https://superk.ai">Mr.K Lab</a> · Powered by <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
