# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/プライバシー-100%25ローカル-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/依存-3つのpipパッケージ-success" alt="Deps">
</p>

<p align="center">
  <b>リアルタイム音声認識、すぐに使える。</b><br>
  たった1つのPythonファイル。クラウド不要。全機能搭載。
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <a href="README_zh.md">🇨🇳 中文</a> · <b>🇯🇵 日本語</b> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## FunASR Live を選ぶ理由

市場に出回るリアルタイム文字起こしツールは大きく2種類に分かれます：

| | クラウド API | デスクトップアプリ | **FunASR Live** |
|---|---|---|---|
| プライバシー | ❌ 音声がサーバーに送信 | ✅ ローカル | ✅ **100% ローカル、ネット不要** |
| コスト | ❌ 分単位の課金 | 💰 買い切り | 🆓 **永久無料** |
| 遅延 | ⚠️ 1〜3秒 | ✅ リアルタイム | ✅ **SSE プッシュ、100ms未満** |
| 言語 | ✅ 50+ | ⚠️ 限定的 | ✅ **20+言語自動検出** |
| 字幕出力 | ⚠️ 別ツール必要 | ⚠️ フォーマット固定 | ✅ **ワンクリック SRT** |
| 音声録音 | ❌ 非対応 | ✅ 対応 | ✅ **トグルでWAV保存** |
| AI要約 | ⚠️ API追加料金 | ❌ 稀 | ✅ **内蔵（Ollama）** |
| カスタマイズ | ❌ クローズド | ❌ クローズド | ✅ **完全ソース、20テーマ** |
| デプロイ | N/A | インストーラ | 🚀 **単一 `.py` ファイル** |

**ベストバランス：** クラウド API のプロ仕様機能 + ローカルアプリのプライバシー + 改造可能な Python ファイル。

---

## ✨ 機能

### 🎤 リアルタイム音声認識
話す → テキストが瞬時に表示。**Alibaba SenseVoiceSmall** + VAD（音声区間検出）+ 句読点復元モデル。言語を自動検出、または固定可能。

### ⚡ SSE リアルタイム配信
ポーリングなし、リロードなし。**Server-Sent Events** でテキストをブラウザにプッシュ、遅延100ms未満。

### 📥 SRT 字幕出力
ワンクリック（または `S` キー）で標準 `.srt` 字幕をダウンロード。Premiere、DaVinci Resolve などにそのまま取り込み可能。

### 🎙️ WAV 音声録音
録音トグルオン → 全マイク音声をデスクトップに `.wav` 保存。オフ → ヘッダー自動修正、即利用可能。

### 🧠 AI 要約（Ollama）
[Ollama](https://ollama.com) が動作中の場合、AI が自動生成：
- **マインドマップ** — 話題の可視化ツリー
- **重要ポイント** — 構造化された要点リスト
- **名言抜粋** — 最高の原文引用

### 🌍 リアルタイム翻訳
言語Aを認識 → 言語Bに即時翻訳。20+言語対応。Google翻訳ベース、ゼロ設定。

### 🎨 20種類のテーマ
ダークモードだけじゃない。**20種類の厳選テーマ** — サイバーグリーン、ネオンナイト、ミッドナイトインク、ミニマルホワイト、ウォームペーパーなど。

---

## 🚀 クイックスタート

```bash
pip install funasr deep-translator numpy
# オプション: AI要約用にOllamaをインストール
brew install ollama && ollama pull qwen2.5:14b
python3 funasr_live.py
open http://localhost:8765
```

初回実行時は約400MBのASRモデルをダウンロードします（次回以降はキャッシュ）。

---

## ⌨️ ショートカット

| キー | 機能 |
|------|------|
| `Space` | 認識の一時停止/再開 |
| `S` | SRT字幕ダウンロード |
| `R` | 録音ON/OFF |
| `1-4` | タブ切替 |

---

## 📡 API

| エンドポイント | 説明 |
|---------------|------|
| `/events` | SSEストリーム（リアルタイム配信） |
| `/api` | 最新結果（ポーリング用） |
| `/config` | 設定・状態 |
| `/download/srt` | SRT字幕ダウンロード |
| `/toggle_pause` | マイクON/OFF |
| `/toggle_record` | 録音ON/OFF |
| `/set_lang?mode=ja` | 言語ロック |
| `/set_translate?target=en` | 翻訳先設定 |

---

## 🔧 設定

`funasr_live.py` 上部の `CONFIG` を編集：

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

## 🎯 ユースケース

| シーン | 活用方法 |
|--------|---------|
| 会議メモ | 録音 + AI要約 + SRT出力 |
| コンテンツ制作 | 口述でスクリプト作成 |
| 語学学習 | 発話 + リアルタイム翻訳 |
| アクセシビリティ | プレゼン・通話の字幕 |
| インタビュー調査 | WAV録音 + タイムスタンプ付き文字起こし |
| 動画字幕 | SRTを直接生成 |
| ライブ配信 | UIを字幕オーバーレイとして埋め込み |

---

## 📦 依存関係

```text
funasr >= 1.3.0
deep-translator >= 1.11
numpy >= 1.24
```

Node.js、Docker、CUDA不要。Python + pipだけでOK。

---

## 📄 ライセンス

MIT — 自由に使用・改変・商用利用可能。

---

<p align="center">
  <sub>❤️ で <a href="https://superk.ai">Mr.K Lab</a> が制作 · <a href="https://github.com/modelscope/FunASR">FunASR</a> 採用</sub>
</p>
