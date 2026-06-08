# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/隐私-100%25本地-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/依赖-3个pip包-success" alt="Deps">
</p>

<p align="center">
  <b>实时语音转文字，开箱即用。</b><br>
  一个 Python 文件。零云端。全功能。
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <b>🇨🇳 中文</b> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## 为什么用 FunASR Live？

> 📖 查看 [ENHANCEMENTS_zh.md](ENHANCEMENTS_zh.md) 了解我们在原始 FunASR 基础上做了哪些增强。

市面上的实时转写工具分两类：

| | 云端 API | 桌面软件 | **FunASR Live** |
|---|---|---|---|
| 隐私 | ❌ 音频发送到服务器 | ✅ 本地 | ✅ **100% 本地，零网络** |
| 费用 | ❌ 按分钟计费 | 💰 一次性购买 | 🆓 **永久免费** |
| 延迟 | ⚠️ 1-3 秒 | ✅ 实时 | ✅ **SSE 推送，<100ms** |
| 语言 | ✅ 50+ | ⚠️ 有限 | ✅ **自动检测 20+ 语言** |
| 字幕导出 | ⚠️ 需要额外工具 | ⚠️ 格式锁定 | ✅ **一键 SRT** |
| 音频录制 | ❌ 不支持 | ✅ 通常支持 | ✅ **开关即录 WAV** |
| AI 总结 | ⚠️ API 额外收费 | ❌ 少见 | ✅ **内置（Ollama）** |
| 自定义 | ❌ 闭源 | ❌ 闭源 | ✅ **完整源码，20 套主题** |
| 部署 | N/A | 安装包 | 🚀 **一个 `.py` 文件** |

**最佳平衡点：** 云端 API 的专业级功能 + 本地软件的隐私性 + 一个可改造的 Python 文件。

---

## ✨ 功能一览

### 🎤 实时语音识别
说话 → 文字即时呈现。基于**阿里 SenseVoiceSmall** + VAD（语音活动检测）+ 标点恢复模型。自动检测语言或锁定至单一语言。

### ⚡ SSE 实时推送
不轮询、不刷新。通过 **Server-Sent Events** 将文本推送到浏览器，延迟低于 100ms。模型完成一帧处理，UI 即刻更新。

### 📥 SRT 字幕导出
一键（或按 `S` 键）下载标准 `.srt` 字幕文件，带时间戳。直接拖入 Premiere、DaVinci Resolve、Final Cut Pro 等剪辑软件。

### 🎙️ WAV 录音保存
打开录音开关 → 每一帧麦克风音频写入带时间戳的 `.wav` 文件，保存在桌面。关闭开关 → 自动修复文件头，即刻可用。无需后期处理。

### 🧠 AI 智能总结（Ollama）
如果本地运行了 [Ollama](https://ollama.com)，AI 会自动生成：
- **思维导图** — 讨论主题的可视化树状结构
- **关键要点** — 结构化要点列表
- **金句摘录** — 最佳原话摘录

支持任何 Ollama 模型（qwen2.5、llama3、deepseek 等）

### 🌍 实时翻译
语言 A 识别 → 即时翻译为语言 B。20+ 目标语言可选。基于 Google 翻译，零配置（可关闭以完全离线运行）。

### 🎨 20 套主题
不只是暗色模式。**20 套精心设计的主题** — 赛博终端、霓虹之夜、午夜墨蓝、极简白、暖纸、森林深处、夕阳橙、极地冰霜等。每套主题改变字体、间距、发光效果和配色。

---

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install funasr deep-translator numpy

# 2.（可选）安装 Ollama 启用 AI 总结
brew install ollama && ollama pull qwen2.5:14b

# 3. 运行
python3 funasr_live.py

# 4. 打开浏览器
open http://localhost:8765
```

首次运行会下载约 400MB 的 ASR 模型（后续运行使用缓存）。

---

## ⌨️ 快捷键

| 按键 | 功能 |
|------|------|
| `空格` | 暂停/恢复识别 |
| `S` | 下载 SRT 字幕 |
| `R` | 开关录音 |
| `1` | 切换到历史 Tab |
| `2` | 切换到思维导图 Tab |
| `3` | 切换到关键要点 Tab |
| `4` | 切换到金句 Tab |

---

## 📡 API 接口

所有接口均为 GET，简单直接。可作为自己应用的后端使用。

| 接口 | 返回 | 说明 |
|------|------|------|
| `/events` | SSE 流 | 实时转写推送 |
| `/api` | JSON | 最新结果（轮询兜底） |
| `/config` | JSON | 当前配置和状态 |
| `/download/srt` | `.srt` 文件 | 导出字幕 |
| `/summary` | JSON | 最新 AI 总结 |
| `/toggle_pause` | JSON | 开关麦克风 |
| `/toggle_record` | JSON | 开关录音 |
| `/set_lang?mode=zh` | JSON | 设置语言锁定 |
| `/set_translate?target=en` | JSON | 设置翻译目标 |

---

## 🏗️ 架构

```
┌──────────┐    ffmpeg     ┌──────────────┐    SSE     ┌───────────┐
│  麦克风🎤 │ ────────────→ │ SenseVoice   │ ─────────→ │  浏览器   │
│  (本地)  │   1.5秒片段   │ Small + VAD  │  <100ms   │  :8765    │
└──────────┘               └──────┬───────┘           └───────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
              ┌──────────┐ ┌───────────┐ ┌───────────┐
              │ 标点模型  │ │ Google    │ │ Ollama    │
              │ (中/英)  │ │ Translate │ │ 总结      │
              └──────────┘ │ (20+语言) │ │ (思维导图) │
                           └───────────┘ └───────────┘
                    │             │             │
                    ▼             ▼             ▼
              ┌──────────────────────────────────────┐
              │  历史记录 → SRT 导出                 │
              │  PCM 片段 → WAV 录音                 │
              │  全部本地，无需云端                  │
              └──────────────────────────────────────┘
```

---

## 🔧 配置

编辑 `funasr_live.py` 顶部的 `CONFIG` 字典：

```python
CONFIG = {
    "port": 8765,                # Web UI 端口
    "chunk_seconds": 1.5,        # 音频片段时长（越小延迟越低）
    "sample_rate": 16000,        # 16kHz 单声道
    "rms_threshold": 0.003,      # 静音检测阈值
    "bt_hfp_helper": True,       # macOS：自动打开 QuickTime 启用蓝牙 HFP 模式
    "translate_enabled": True,   # 启用 Google 翻译
    "translate_target": "en",    # 默认目标语言
}
```

---

## 🎯 使用场景

| 场景 | FunASR Live 如何帮助 |
|------|---------------------|
| **会议记录** | 录音 + AI 总结 + 导出 SRT 作为会议纪要 |
| **内容创作** | 口述脚本，即时获取文字稿 |
| **语言学习** | 说话 + 实时查看翻译 |
| **无障碍** | 演示或通话的实时字幕 |
| **研究访谈** | 录制 WAV + 获取带时间戳的文字记录 |
| **视频字幕** | 直接生成 SRT，无需手动打点 |
| **直播** | 嵌入 UI 作为字幕叠加层 |
| **隐私场景** | 医疗、法律等不允许使用云端 API 的场景 |

---

## 📦 依赖

```text
funasr >= 1.3.0          # 阿里 SenseVoiceSmall ASR 引擎
deep-translator >= 1.11  # Google 翻译（可选）
numpy >= 1.24             # 音频缓冲处理
```

就这些。不需要 Node.js、Docker、CUDA toolkit。Python + pip 搞定。

---

## 🤝 参与贡献

发现 Bug？想要新主题？欢迎 PR。

```bash
git clone https://github.com/KevPH2026/funasr-live.git
cd funasr-live
python3 funasr_live.py
```

---

## 📄 许可证

MIT — 随便用。基于它做产品、fork 它、卖它，都行。

---

<p align="center">
  <sub>用 ❤️ 打造 by <a href="https://superk.ai">Mr.K Lab</a> · 基于 <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
