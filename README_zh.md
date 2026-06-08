# 🎙️ Kev.FunASR v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/license-MIT-green">
  <img src="https://img.shields.io/badge/平台-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey">
  <img src="https://img.shields.io/badge/引擎-SenseVoiceSmall-orange">
  <img src="https://img.shields.io/badge/隐私-100%25本地-blueviolet">
  <img src="https://img.shields.io/badge/依赖-3个pip包-success">
  <img src="https://img.shields.io/badge/体积-49KB-silver">
</p>

<p align="center">
  <b>FunASR 是阿里的引擎，Kev.FunASR 是把它变成产品的答案。</b><br>
  <sub>对比：<a href="#-kevfunasr-vs-原生-funasr">vs 原生 FunASR</a> · <a href="#-kevfunasr-vs-云端-api">vs 云端 API</a> · <a href="#-kevfunasr-vs-桌面应用">vs 桌面应用</a></sub>
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <b>🇨🇳 中文</b> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="Kev.FunASR — 极简白主题">
</p>

---

## ⚡ 一句话

> 原生 FunASR 是把枪，瞄准镜、弹匣、保险都得自己装。**Kev.FunASR** 是上膛的成品——拿起来就能用。

- **FunASR 给你：** 一个 Python 语音识别库
- **Kev.FunASR 给你：** 带 UI、带导出、带录音、带 AI 总结、带翻译的完整应用，一行命令启动

---

## 📊 Kev.FunASR vs 原生 FunASR

我们在原始引擎上加了什么：

| | 原生 FunASR | Kev.FunASR |
|------|------------|-----------|
| 启动方式 | 写 Python 脚本 + 配参数 | ✅ 一个命令：`python3 funasr_live.py` |
| 界面 | ❌ 只有命令行 | ✅ Web UI · 20 套主题 |
| 麦克风 | ❌ 自己搭 | ✅ 自动 ffmpeg 采集 · 蓝牙 HFP |
| 实时推送 | ❌ 自己写轮询 | ✅ SSE 推送 · &lt;100ms 延迟 |
| 字幕导出 | ❌ 没有 | ✅ 一键 SRT · 直接拖进剪辑软件 |
| 录音保存 | ❌ 没有 | ✅ 开关即录 · 自动修文件头 |
| AI 总结 | ❌ 单独搭 | ✅ 内置 Ollama · 思维导图+金句 |
| 实时翻译 | ❌ 单独搭 | ✅ Google 翻译 · 20+ 语言 |
| 语言检测 | 手动指定 | ✅ 自动检测 20+ · 8 种双语模式 |
| 标点恢复 | 另调模型 | ✅ 自动串联 |
| 静音过滤 | 另配参数 | ✅ 内置 VAD · 自动跳过 |
| 快捷键 | ❌ 无 | ✅ Space/S/R/1-4 |
| 文档 | 🇨🇳 仅中文 | ✅ 9 种语言 |

**一句话：原生 FunASR 是发动机，Kev.FunASR 是整车。**

---

## 📊 Kev.FunASR vs 云端 API

| | Google/Whisper API | Kev.FunASR |
|------|-----------------|-----------|
| 隐私 | ❌ 音频上传到云端 | ✅ 100% 本地 · 零网络 |
| 费用 | ❌ ~$0.006/分钟 · 重度使用~$200/月 | 🆓 永久免费 |
| 延迟 | ⚠️ 1-3 秒往返 | ✅ SSE 推送 &lt;100ms |
| 可定制 | ❌ 黑盒 | ✅ 完整源码 · 20 套主题 |
| 离线使用 | ❌ 不行 | ✅ 可以（关翻译） |

---

## 📊 Kev.FunASR vs 桌面应用

| | Otter/Buzz/MacWhisper | Kev.FunASR |
|------|----------------------|-----------|
| SRT 字幕 | ⚠️ 功能不一 | ✅ 一键标准格式 |
| WAV 录音 | ✅ 通常有 | ✅ 自动修文件头 |
| AI 总结 | ❌ 很少 · 付费墙 | ✅ 内置 · 任意 Ollama 模型 |
| 翻译 | ⚠️ 部分有 | ✅ 实时 · 20+ 语言 |
| 源码 | ❌ 闭源 | ✅ MIT · 随便改 |
| 主题 | 1-2 个 | ✅ 20 套精选主题 |
| 跨平台 | ⚠️ 系统绑定 | ✅ macOS / Linux / Windows |
| 价格 | 💰 $8-30/月或 $100+ 买断 | 🆓 完全免费 · 无需注册 |

---

## ✨ 功能

### 🎤 实时转写
对着麦克风说话，文字即时出现。基于阿里 SenseVoiceSmall + VAD 语音检测 + 标点恢复。自动识别语言或锁定单语。

### ⚡ SSE 实时推送（v2.0）
不轮询、不刷新。文字通过 Server-Sent Events 直接推送到浏览器，延迟不到 100ms。

### 📥 一键 SRT 字幕
按 `S` → `.srt` 文件下载到桌面。带时间戳，直接拖进 Premiere、DaVinci Resolve、Final Cut、剪映。

### 🎙️ WAV 录音
开关一按 → 所有音频保存为 `.wav` 到桌面。停止时自动修复文件头，不需要后处理。

### 🧠 AI 智能总结（Ollama）
装了 [Ollama](https://ollama.com) 就自动生成：思维导图、关键要点、金句摘录。支持任意模型。

### 🌍 实时翻译
说中文看英文，说英文看日文。Google 翻译引擎，20+ 目标语言。关了就是纯离线。

### 🎨 20 套主题

不仅是深色模式。**20 套精心设计的主题** — 每一套都改变了字体、间距、光影和配色。

<p align="center">
  <img src="themes/theme-switcher.gif" width="640" alt="主题切换 + 功能演示">
</p>

<p align="center">
  <img src="themes/demo-main.png" width="280" alt="实时转写 + 翻译">
  <img src="themes/demo-history.png" width="280" alt="历史记录带时间戳">
  <img src="themes/demo-mindmap.png" width="280" alt="AI 思维导图">
  <img src="themes/demo-quotes.png" width="280" alt="AI 金句摘录">
</p>

> 转写 → 历史 → AI 总结 → 导出 SRT。一个流程，全部搞定。

---

## 🚀 快速开始

```bash
pip install funasr deep-translator numpy
brew install ollama && ollama pull qwen2.5:14b  # 可选
python3 funasr_live.py
open http://localhost:8765
```

首次运行下载约 400MB 模型（后续缓存）。

---

## ⌨️ 快捷键

| 键 | 功能 |
|-----|------|
| `Space` | 暂停 / 继续 |
| `S` | 下载 SRT 字幕 |
| `R` | 开关录音 |
| `1-4` | 切换页：历史 / 思维导图 / 要点 / 金句 |

---

## 📡 API 接口

全部 GET，可直接当后端用：

| 接口 | 返回 |
|------|------|
| `/events` | SSE 实时流 |
| `/api` | JSON（轮询备选） |
| `/config` | 当前状态 |
| `/download/srt` | `.srt` 文件 |
| `/summary` | AI 总结 JSON |
| `/toggle_pause` | 切换麦克风 |
| `/toggle_record` | 切换录音 |
| `/set_lang?mode=zh` | 锁定语言 |
| `/set_translate?target=en` | 设置翻译 |

---

## 🏗️ 架构

```
麦克风 🎤 ──ffmpeg──→ SenseVoiceSmall + VAD ──SSE──→ 浏览器 :8765
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
          标点模型          Google翻译      Ollama AI
          (自动)           (实时)          (思维导图)
              │               │               │
              ▼               ▼               ▼
        ┌─────────────────────────────────────────┐
        │  历史记录 → SRT 字幕导出                 │
        │  PCM 音频 → WAV 录音保存                 │
        │  全本地 · 零云端                         │
        └─────────────────────────────────────────┘
```

---

## 📦 依赖

```text
funasr  deep-translator  numpy
```

不需要 Node.js、Docker、CUDA。用 Python 就够了。

---

## 🎯 适用场景

| 你是... | 你会喜欢... |
|---------|------------|
| 内容创作者 | 口播 → 文字 + SRT 一条龙 |
| 开会的人 | 录音 + AI 总结 = 会议纪要搞定 |
| 学语言的人 | 说话 → 实时翻译反馈 |
| 做研究的 | WAV 录音 + 时间戳文本 |
| 开发者 | SSE API → 自己搭 UI |
| 注重隐私 | 医疗 / 法务 / 机密场合 |

---

## 📄 许可证

MIT — fork 随便改，商业化随便卖。

---

<p align="center">
  <img src="https://img.shields.io/badge/by-@KevPH2026-555?style=flat&logo=github"><br>
  <a href="https://github.com/KevPH2026/kev-funasr"><img src="https://img.shields.io/badge/🐙_GitHub-kev--funasr-181717?logo=github"></a>
  <a href="https://superk.ai"><img src="https://img.shields.io/badge/🌐_官网-superk.ai-blue"></a>
  <a href="https://x.com/skyerK12"><img src="https://img.shields.io/badge/𝕏-@skyerK12-black?logo=x"></a><br>
  <sub>Made with ❤️ by <a href="https://superk.ai">Mr.K Lab</a> · Powered by <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
