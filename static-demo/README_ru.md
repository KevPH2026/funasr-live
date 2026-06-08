# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/лицензия-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/платформа-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/конфиденциальность-100%25локально-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/зависимости-3pipпакета-success" alt="Deps">
</p>

<p align="center">
  <b>Распознавание речи в реальном времени, готово к работе.</b><br>
  Один файл Python. Ноль облака. Все функции включены.
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <a href="README_zh.md">🇨🇳 中文</a> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <b>🇷🇺 Русский</b>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## Почему FunASR Live?

Инструменты транскрибации в реальном времени делятся на две категории:

| | Облачные API | Десктопные приложения | **FunASR Live** |
|---|---|---|---|
| Конфиденциальность | ❌ Аудио отправляется на сервер | ✅ Локально | ✅ **100% локально, без сети** |
| Стоимость | ❌ Поминутная оплата | 💰 Единоразовая покупка | 🆓 **Бесплатно навсегда** |
| Задержка | ⚠️ 1-3 секунды | ✅ Реальное время | ✅ **SSE push, <100ms** |
| Языки | ✅ 50+ | ⚠️ Ограничено | ✅ **Автоопределение 20+ языков** |
| Экспорт субтитров | ⚠️ Нужен доп. инструмент | ⚠️ Фикс. формат | ✅ **SRT в один клик** |
| Запись аудио | ❌ Нет | ✅ Да | ✅ **Кнопка сохранения WAV** |
| ИИ-саммари | ⚠️ Доп. плата за API | ❌ Редко | ✅ **Встроено (Ollama)** |
| Настройка | ❌ Закрытый код | ❌ Закрытый код | ✅ **Полный код, 20 тем** |
| Развёртывание | N/A | Установщик | 🚀 **Один файл `.py`** |

**Идеальный баланс:** профессиональные функции облачного API + конфиденциальность локального приложения + модифицируемый файл Python.

---

## ✨ Возможности

### 🎤 Распознавание речи в реальном времени
Говорите → текст появляется мгновенно. На основе **Alibaba SenseVoiceSmall** + VAD + модель пунктуации. Автоопределение языка или фиксация одного.

### ⚡ SSE Push в реальном времени
Без опроса. Без перезагрузки. **Server-Sent Events** отправляют текст в браузер с задержкой <100ms.

### 📥 Экспорт субтитров SRT
Один клик (или клавиша `S`) скачивает стандартный файл `.srt`. Используйте напрямую в Premiere, DaVinci Resolve и др.

### 🎙️ Запись аудио WAV
Включить запись → весь аудиопоток с микрофона сохраняется в `.wav` на рабочем столе. Выключить → заголовок исправлен, файл готов.

### 🧠 ИИ-саммари (Ollama)
Если запущен [Ollama](https://ollama.com), ИИ автоматически генерирует:
- **Mindmap** — визуальное дерево тем
- **Ключевые моменты** — структурированный список
- **Цитаты** — лучшие дословные высказывания

### 🌍 Перевод в реальном времени
Язык А распознан → мгновенно переведён на язык Б. Доступно 20+ языков.

### 🎨 20 тем
Не только тёмный режим. **20 тщательно подобранных тем** — cyber green, neon night, midnight ink, minimal white, warm paper и другие.

---

## 🚀 Быстрый старт

```bash
pip install funasr deep-translator numpy
# Опционально: установить Ollama для ИИ-саммари
brew install ollama && ollama pull qwen2.5:14b
python3 funasr_live.py
open http://localhost:8765
```

При первом запуске скачивается около 400 МБ моделей ASR (кэшируются).

---

## ⌨️ Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| `Space` | Пауза/Продолжить |
| `S` | Скачать SRT |
| `R` | Вкл/выкл запись |
| `1-4` | Переключение вкладок |

---

## 📡 API

| Endpoint | Описание |
|----------|----------|
| `/events` | SSE-поток (реальное время) |
| `/api` | Последний результат (опрос) |
| `/config` | Конфигурация и состояние |
| `/download/srt` | Скачать субтитры SRT |
| `/toggle_pause` | Микрофон вкл/выкл |
| `/toggle_record` | Запись вкл/выкл |
| `/set_lang?mode=ru` | Зафиксировать язык |
| `/set_translate?target=en` | Язык перевода |

---

## 🔧 Конфигурация

Отредактируйте `CONFIG` в начале `funasr_live.py`:

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

## 🎯 Сценарии использования

| Сценарий | Применение |
|----------|-----------|
| Заметки совещаний | Запись + ИИ-саммари + SRT |
| Создание контента | Диктовка сценариев |
| Изучение языков | Речь + перевод в реальном времени |
| Доступность | Живые субтитры для презентаций |
| Интервью | Запись WAV + транскрибация с метками времени |
| Субтитры для видео | Генерация SRT напрямую |
| Стриминг | Встроить UI как оверлей субтитров |

---

## 📦 Зависимости

```text
funasr >= 1.3.0
deep-translator >= 1.11
numpy >= 1.24
```

Без Node.js, Docker или CUDA. Только Python + pip.

---

## 📄 Лицензия

MIT — свободное использование, модификация и коммерческое применение.

---

<p align="center">
  <sub>Сделано с ❤️ <a href="https://superk.ai">Mr.K Lab</a> · На базе <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
