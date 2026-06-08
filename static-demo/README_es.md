# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/privacidad-100%25local-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/dependencias-3paquetespip-success" alt="Deps">
</p>

<p align="center">
  <b>Transcripción de voz en tiempo real, lista para usar.</b><br>
  Un solo archivo Python. Cero nube. Todas las funciones incluidas.
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <a href="README_zh.md">🇨🇳 中文</a> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <b>🇪🇸 Español</b> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## ¿Por qué FunASR Live?

Las herramientas de transcripción en tiempo real se dividen en dos categorías:

| | API en la Nube | Apps de Escritorio | **FunASR Live** |
|---|---|---|---|
| Privacidad | ❌ Audio enviado a servidores | ✅ Local | ✅ **100% local, sin red** |
| Costo | ❌ Precio por minuto | 💰 Pago único | 🆓 **Gratis para siempre** |
| Latencia | ⚠️ 1-3 segundos | ✅ Tiempo real | ✅ **SSE push, <100ms** |
| Idiomas | ✅ 50+ | ⚠️ Limitado | ✅ **Detección automática 20+ idiomas** |
| Exportar subtítulos | ⚠️ Herramienta extra | ⚠️ Formato fijo | ✅ **SRT en un clic** |
| Grabación de audio | ❌ No | ✅ Sí | ✅ **Toggle para guardar WAV** |
| Resumen IA | ⚠️ Costo extra de API | ❌ Raro | ✅ **Integrado (Ollama)** |
| Personalización | ❌ Código cerrado | ❌ Código cerrado | ✅ **Código completo, 20 temas** |
| Despliegue | N/A | Instalador | 🚀 **Un solo archivo `.py`** |

**El equilibrio perfecto:** funciones profesionales de una API en la nube + privacidad de una app local + un archivo Python modificable.

---

## ✨ Funciones

### 🎤 Transcripción en tiempo real
Habla → texto al instante. Basado en **Alibaba SenseVoiceSmall** + VAD + modelo de puntuación. Detección automática de idioma o bloqueo a uno.

### ⚡ Push en tiempo real SSE
Sin polling. Sin recargas. **Server-Sent Events** envía el texto al navegador con <100ms de latencia.

### 📥 Exportar subtítulos SRT
Un clic (o tecla `S`) descarga un archivo `.srt` estándar. Úsalo directamente en Premiere, DaVinci Resolve, etc.

### 🎙️ Grabación de audio WAV
Activar grabación → todo el audio del micrófono se guarda en `.wav` en el escritorio. Desactivar → cabecera reparada, archivo listo.

### 🧠 Resumen IA (Ollama)
Si [Ollama](https://ollama.com) está en ejecución, la IA genera automáticamente:
- **Mapa mental** — árbol visual de temas
- **Puntos clave** — lista estructurada
- **Citas destacadas** — mejores frases textuales

### 🌍 Traducción en tiempo real
Idioma A transcrito → traducido instantáneamente al idioma B. 20+ idiomas disponibles.

### 🎨 20 temas
No solo modo oscuro. **20 temas curados** — cyber green, neon night, midnight ink, minimal white, warm paper, y más.

---

## 🚀 Inicio rápido

```bash
pip install funasr deep-translator numpy
# Opcional: instalar Ollama para resumen IA
brew install ollama && ollama pull qwen2.5:14b
python3 funasr_live.py
open http://localhost:8765
```

La primera ejecución descarga ~400MB de modelos ASR (en caché para siguientes usos).

---

## ⌨️ Atajos

| Tecla | Acción |
|-------|--------|
| `Space` | Pausar/Reanudar |
| `S` | Descargar SRT |
| `R` | Activar grabación |
| `1-4` | Cambiar pestañas |

---

## 📡 API

| Endpoint | Descripción |
|----------|-------------|
| `/events` | Stream SSE (tiempo real) |
| `/api` | Último resultado (polling) |
| `/config` | Configuración y estado |
| `/download/srt` | Descargar subtítulos SRT |
| `/toggle_pause` | Micrófono ON/OFF |
| `/toggle_record` | Grabación ON/OFF |
| `/set_lang?mode=es` | Bloquear idioma |
| `/set_translate?target=en` | Idioma de traducción |

---

## 🔧 Configuración

Editar `CONFIG` al inicio de `funasr_live.py`:

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

## 🎯 Casos de uso

| Escenario | Cómo ayuda |
|-----------|-----------|
| Notas de reunión | Grabar + resumen IA + SRT |
| Creación de contenido | Dictar guiones |
| Aprendizaje de idiomas | Hablar + traducción en tiempo real |
| Accesibilidad | Subtítulos en vivo para presentaciones |
| Entrevistas | Grabar WAV + transcripción con marcas de tiempo |
| Subtitulado de video | Generar SRT directamente |
| Streaming en vivo | Incrustar UI como superposición de subtítulos |

---

## 📦 Dependencias

```text
funasr >= 1.3.0
deep-translator >= 1.11
numpy >= 1.24
```

Sin Node.js, Docker ni CUDA. Solo Python + pip.

---

## 📄 Licencia

MIT — uso libre, modificación y uso comercial permitidos.

---

<p align="center">
  <sub>Hecho con ❤️ por <a href="https://superk.ai">Mr.K Lab</a> · Usa <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
