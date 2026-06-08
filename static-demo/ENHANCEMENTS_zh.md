# 🚀 我们在 FunASR 基础上做了哪些增强

> FunASR 是阿里开源的语音识别引擎。我们把它从"命令行工具"变成了"产品级应用"。

---

## 📊 对比：原始 FunASR vs FunASR Live v2.0

| 能力 | 原始 FunASR | FunASR Live v2.0 |
|------|------------|-----------------|
| **启动方式** | Python 脚本 + 命令行参数 | 一个文件，`python3 funasr_live.py` 即跑 |
| **用户界面** | ❌ 无 | ✅ 完整 Web UI，20 套主题 |
| **麦克风采集** | ❌ 需自己写 | ✅ 自动 ffmpeg 采集，蓝牙 HFP 支持 |
| **实时推送** | ❌ 需轮询 | ✅ SSE Server-Sent Events，<100ms 延迟 |
| **SRT 字幕导出** | ❌ 无 | ✅ 一键下载标准 SRT，直接进剪辑软件 |
| **WAV 录音** | ❌ 无 | ✅ 开关即录，桌面保存，自动修文件头 |
| **AI 总结** | ❌ 无 | ✅ Ollama 集成，思维导图+要点+金句 |
| **实时翻译** | ❌ 无 | ✅ Google Translate，20+ 目标语言 |
| **语言支持** | 中文为主 | ✅ 20+ 语言自动检测 + 8 种双语模式 |
| **标点恢复** | 需单独调用 | ✅ 自动串联 punc_ct-transformer |
| **VAD 语音检测** | 需单独配置 | ✅ 内置 fsmn-vad，自动静音跳过 |
| **快捷键** | ❌ 无 | ✅ Space/S/R/1-4，全局快捷键 |
| **多语言文档** | 中文 | ✅ README 9 语言版本 |

---

## 🏗️ 架构增强

```
原始 FunASR:              我们做的：
                          ┌─────────────────────────────────┐
  音频文件                  │  🎤 麦克风 (ffmpeg 实时采集)      │
     │                     │     ↓                            │
     ▼                     │  🔇 VAD 静音过滤                   │
  SenseVoiceSmall          │     ↓                            │
     │                     │  🧠 SenseVoiceSmall (ASR)        │
     ▼                     │     ↓                            │
  文本输出                  │  📝 punc_ct-transformer (标点)    │
                           │     ↓                            │
                           │  🌍 Google Translate (实时翻译)    │
                           │     ↓                            │
                           │  🤖 Ollama (AI 总结)              │
                           │     ↓                            │
                           │  ⚡ SSE → 浏览器实时推送           │
                           │     ↓                            │
                           │  ┌──────────┬──────────┬───────┐ │
                           │  │ 📥 SRT   │ 🎙️ WAV  │ 🎨 UI │ │
                           │  │ 导出字幕  │ 录音保存  │ 20主题│ │
                           │  └──────────┴──────────┴───────┘ │
                           └─────────────────────────────────┘
```

---

## 🔧 技术栈

```yaml
ASR 引擎:   FunASR + SenseVoiceSmall
VAD 检测:   fsmn-vad (语音活动检测)
标点恢复:   punc_ct-transformer (中英文标点)
翻译引擎:   deep-translator (Google Translate)
AI 总结:    Ollama (支持任意模型)
音频采集:   ffmpeg (macOS/Linux/Windows)
前端界面:   原生 HTML/CSS/JS (零框架依赖)
实时通信:   SSE (Server-Sent Events)
主题系统:   20 套 CSS 变量主题
```

**核心设计原则：零额外依赖。** 除了 FunASR 本身需要的 pip 包，不引入任何新依赖。SSE 用 Python 标准库 `http.server` 实现，不需要 WebSocket 库。

---

## 📦 单文件哲学

整个应用是一个 **49KB 的 Python 文件**，包含：

```
funasr_live.py
├── CONFIG          (配置字典)
├── 模型加载         (ASR + VAD + 标点)
├── HTTP Server     (路由、SSE、文件下载)
├── 麦克风采集       (ffmpeg subprocess)
├── ASR 处理循环     (实时识别 + 翻译 + 总结)
├── WAV 录音         (PCM 追加 + 文件头修复)
├── SRT 生成         (时间戳计算 + 格式化)
├── HTML 模板        (完整 UI + CSS 变量 + JS)
└── 20 套主题        (CSS 变量)
```

不需要 `npm install`、`docker-compose`、数据库、Redis、Nginx。就是 Python + 浏览器。

---

## 🎯 解决的问题

| 痛点 | 我们的方案 |
|------|-----------|
| **FunASR 只有命令行** | Web UI，鼠标操作，手机也能用 |
| **结果只能看不能导出** | SRT 字幕 + WAV 录音，一键下载 |
| **没有实时反馈** | SSE 推送，边说边看 |
| **没有翻译** | 20+ 语言实时翻译，开会/学语言直接用 |
| **没有 AI 能力** | Ollama 集成，自动生成会议纪要 |
| **界面丑** | 20 套精心设计的主题 |
| **部署麻烦** | 一个文件，pip install 三行搞定 |
| **文档只有中文** | README 9 语言，全球开发者都能看懂 |

---

## 🚦 开发迭代

```
v1.0 基础版
  ├── SenseVoiceSmall ASR 引擎
  ├── 基础 Web UI (轮询模式)
  ├── 3 套主题
  └── 中英日韩识别

v2.0 (2026-06-08 发布)
  ├── ⚡ SSE 实时推送 (替换 300ms 轮询)
  ├── 📥 SRT 字幕一键导出
  ├── 🎙️ WAV 录音开关保存
  ├── ⌨️ 全局快捷键 (Space/S/R/1-4)
  ├── 🎨 20 套主题 (赛博/霓虹/墨蓝/极简/暖纸...)
  ├── 🌍 20+ 语言单语识别
  ├── 🔀 8 种双语模式 (中英/中日/中韩/中法/中德/中西/英日/英韩)
  ├── 🌐 20+ 翻译目标语言 (分组: 常用/欧洲/亚洲)
  ├── 🧠 Ollama AI 智能总结 (思维导图 + 关键要点 + 金句摘录)
  ├── 🔧 macOS 蓝牙 HFP 麦克风支持 (QuickTime 助手)
  └── 📖 9 语言 README 文档 (中/英/日/韩/法/德/西/葡/俄)
```

---

## ⚡ 性能指标

| 指标 | 数值 |
|------|------|
| 识别延迟 | <100ms (SSE 推送) |
| 内存占用 | ~1.5GB (模型加载后) |
| 模型大小 | ~400MB (首次下载，后续缓存) |
| 启动时间 | 5-8s (模型加载) |
| 代码体积 | 49KB (单文件) |

---

## 📄 许可证

本项目基于 FunASR (MIT License) 构建，同样采用 MIT 开源。

上游项目：https://github.com/modelscope/FunASR

---

<p align="center">
  <sub>由 <a href="https://superk.ai">Mr.K Lab</a> 构建 · FunASR Live v2.0 · 2026 年 6 月</sub>
</p>
