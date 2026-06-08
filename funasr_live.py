#!/usr/bin/env python3
"""FunASR Live v2.0 — Real-time ASR with SSE push, SRT export, WAV recording, shortcuts

Usage: python3 funasr_live.py
Then open http://localhost:8765
"""
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import json, time, threading, wave, subprocess, sys, re, collections, io, struct
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from deep_translator import GoogleTranslator

# ============================================================
# Configuration
# ============================================================
CONFIG = {
    "port": 8765,
    "chunk_seconds": 1.5,
    "sample_rate": 16000,
    "rms_threshold": 0.003,
    "bt_hfp_helper": True,
    "translate_enabled": True,
    "translate_target": "en",
}

# ============================================================
# Load ASR models
# ============================================================
print("Loading models...")
from funasr import AutoModel
import numpy as np

if CONFIG["bt_hfp_helper"]:
    print("Activating BT mic (HFP mode)...")
    try:
        p = subprocess.Popen(
            ["osascript", "-e", 'tell app "QuickTime Player" to activate',
             "-e", 'tell app "QuickTime Player" to new audio recording'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.wait(timeout=3)
        time.sleep(0.5)
    except (subprocess.TimeoutExpired, Exception):
        p.kill(); p.wait()
        print("(QuickTime helper skipped — no Bluetooth mic needed)")

asr_model = AutoModel(
    model="iic/SenseVoiceSmall", disable_update=True, device="mps",
    vad_model="fsmn-vad", vad_kwargs={"max_single_segment_time": 60000}
)
print("ASR model loaded.")

punc_model = AutoModel(
    model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
    disable_update=True, device="mps"
)
print("Punctuation model loaded.")

# ============================================================
# Language config
# ============================================================
LANG_MAP = {
    "zh": "中文", "en": "English", "ja": "日本語", "ko": "한국어",
    "yue": "粵語", "fr": "Français", "de": "Deutsch", "es": "Español",
    "ru": "Русский", "th": "ไทย", "vi": "Tiếng Việt",
    "it": "Italiano", "pt": "Português", "id": "Bahasa Indonesia",
    "ar": "العربية", "tr": "Türkçe", "hi": "हिन्दी",
    "nl": "Nederlands", "ms": "Bahasa Melayu", "tl": "Tagalog",
    "sv": "Svenska", "pl": "Polski", "uk": "Українська",
}

LANG_MODES = {
    "auto":      {"label": "🌐 自动检测", "allowed": None},
    "zh":        {"label": "🇨🇳 仅中文", "allowed": {"zh"}},
    "en":        {"label": "🇺🇸 English only", "allowed": {"en"}},
    "ja":        {"label": "🇯🇵 日本語のみ", "allowed": {"ja"}},
    "ko":        {"label": "🇰🇷 한국어만", "allowed": {"ko"}},
    "yue":       {"label": "🇭🇰 僅粵語", "allowed": {"yue"}},
    "fr":        {"label": "🇫🇷 Français seul", "allowed": {"fr"}},
    "de":        {"label": "🇩🇪 Nur Deutsch", "allowed": {"de"}},
    "es":        {"label": "🇪🇸 Solo Español", "allowed": {"es"}},
    "ru":        {"label": "🇷🇺 Только русский", "allowed": {"ru"}},
    "th":        {"label": "🇹🇭 ภาษาไทยเท่านั้น", "allowed": {"th"}},
    "vi":        {"label": "🇻🇳 Chỉ tiếng Việt", "allowed": {"vi"}},
    "it":        {"label": "🇮🇹 Solo Italiano", "allowed": {"it"}},
    "pt":        {"label": "🇧🇷 Só Português", "allowed": {"pt"}},
    "id":        {"label": "🇮🇩 Bahasa saja", "allowed": {"id"}},
    "ar":        {"label": "🇸🇦 العربية فقط", "allowed": {"ar"}},
    "tr":        {"label": "🇹🇷 Sadece Türkçe", "allowed": {"tr"}},
    "hi":        {"label": "🇮🇳 केवल हिन्दी", "allowed": {"hi"}},
    "nl":        {"label": "🇳🇱 Alleen Nederlands", "allowed": {"nl"}},
    "ms":        {"label": "🇲🇾 Bahasa sahaja", "allowed": {"ms"}},
    "zh+en":     {"label": "🇨🇳🇺🇸 中英双语", "allowed": {"zh", "en"}},
    "zh+ja":     {"label": "🇨🇳🇯🇵 中日双语", "allowed": {"zh", "ja"}},
    "zh+ko":     {"label": "🇨🇳🇰🇷 中韩双语", "allowed": {"zh", "ko"}},
    "zh+fr":     {"label": "🇨🇳🇫🇷 中法双语", "allowed": {"zh", "fr"}},
    "zh+de":     {"label": "🇨🇳🇩🇪 中德双语", "allowed": {"zh", "de"}},
    "zh+es":     {"label": "🇨🇳🇪🇸 中西双语", "allowed": {"zh", "es"}},
    "en+ja":     {"label": "🇺🇸🇯🇵 EN+JP", "allowed": {"en", "ja"}},
    "en+ko":     {"label": "🇺🇸🇰🇷 EN+KR", "allowed": {"en", "ko"}},
}

# ============================================================
# Theme config (20 themes)
# ============================================================
STYLES = {
    "dark-tech": {"name":"🌑 暗黑科技","css":"--bg:#0d1117;--bg2:#161b22;--border:#30363d;--text:#c9d1d9;--title:#fff;--accent:#58a6ff;--accent2:#f0883e;--tag-bg:#21262d;--panel-bg:#161b22;--item-bg:#0d1117;--dim:#484f58;--font:sans-serif;--sub-size:48px;--trans-size:24px;--radius:6px;--shadow:none;--glow:none"},
    "neon-night": {"name":"💜 霓虹之夜","css":"--bg:#0a0a0f;--bg2:#120f1a;--border:#2a1f4e;--text:#d4c5f0;--title:#fff;--accent:#c084fc;--accent2:#34d399;--tag-bg:#1a1240;--panel-bg:#0f0b1a;--item-bg:#120f1a;--dim:#6b5c8a;--font:sans-serif;--sub-size:48px;--trans-size:24px;--radius:10px;--shadow:0_0_30px_rgba(192,132,252,0.15);--glow:0_0_20px_rgba(192,132,252,0.4)"},
    "cyber-green": {"name":"🟢 赛博终端","css":"--bg:#000;--bg2:#0a0a0a;--border:#0f3a0f;--text:#00ff41;--title:#00ff41;--accent:#00ff41;--accent2:#00cc33;--tag-bg:#0a1a0a;--panel-bg:#050505;--item-bg:#0a0a0a;--dim:#0a5a0a;--font:'Courier New',monospace;--sub-size:42px;--trans-size:20px;--radius:0px;--shadow:0_0_15px_rgba(0,255,65,0.2);--glow:0_0_10px_rgba(0,255,65,0.5)"},
    "midnight-ink": {"name":"🌌 午夜墨蓝","css":"--bg:#0b0e1a;--bg2:#13172b;--border:#1e2548;--text:#a8b5e0;--title:#e8edff;--accent:#6c8cff;--accent2:#ff8fa3;--tag-bg:#161d3a;--panel-bg:#0f1324;--item-bg:#0b0e1a;--dim:#4a5580;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:8px;--shadow:none;--glow:0_0_15px_rgba(108,140,255,0.2)"},
    "crimson-red": {"name":"❤️ 赤红暗影","css":"--bg:#0d0707;--bg2:#1a0f0f;--border:#3d1515;--text:#e0c0c0;--title:#fff;--accent:#ff4444;--accent2:#ff8c42;--tag-bg:#250d0d;--panel-bg:#120808;--item-bg:#0d0707;--dim:#6e3a3a;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:6px;--shadow:0_0_20px_rgba(255,68,68,0.12);--glow:0_0_8px_rgba(255,68,68,0.3)"},
    "ocean-blue": {"name":"🌊 深海之蓝","css":"--bg:#061524;--bg2:#0b1f35;--border:#1a3a5c;--text:#90c8e8;--title:#dcf0ff;--accent:#38bdf8;--accent2:#f59e0b;--tag-bg:#102a45;--panel-bg:#081a2e;--item-bg:#061524;--dim:#3a5e7e;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:10px;--shadow:none;--glow:0_0_12px_rgba(56,189,248,0.25)"},
    "forest-deep": {"name":"🌲 暗夜森林","css":"--bg:#0a1610;--bg2:#0f1f17;--border:#1a3a26;--text:#98c9a8;--title:#d4f0dc;--accent:#22c55e;--accent2:#e0a82e;--tag-bg:#162d1e;--panel-bg:#0c1a13;--item-bg:#0a1610;--dim:#3e6a4e;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:8px;--shadow:0_0_15px_rgba(34,197,94,0.1);--glow:none"},
    "minimal-light": {"name":"☀️ 极简白","css":"--bg:#fafafa;--bg2:#fff;--border:#e5e5e5;--text:#333;--title:#111;--accent:#2563eb;--accent2:#ea580c;--tag-bg:#f0f0f0;--panel-bg:#fff;--item-bg:#f9fafb;--dim:#9ca3af;--font:sans-serif;--sub-size:52px;--trans-size:22px;--radius:10px;--shadow:0_1px_3px_rgba(0,0,0,0.08);--glow:none"},
    "nature-calm": {"name":"🌿 自然静谧","css":"--bg:#f0f7f4;--bg2:#fff;--border:#c5ddd0;--text:#2d4a3e;--title:#1a3328;--accent:#059669;--accent2:#d97706;--tag-bg:#dceee4;--panel-bg:#f8fbf9;--item-bg:#f0f7f4;--dim:#87a898;--font:sans-serif;--sub-size:50px;--trans-size:22px;--radius:8px;--shadow:0_2px_12px_rgba(26,51,40,0.08);--glow:none"},
    "warm-paper": {"name":"📜 暖纸书香","css":"--bg:#f5f0e8;--bg2:#faf6ef;--border:#d4c5a9;--text:#5c4b2e;--title:#2c1810;--accent:#8b5e3c;--accent2:#c1440e;--tag-bg:#ebe3d5;--panel-bg:#faf6ef;--item-bg:#f5f0e8;--dim:#b8a88a;--font:'Georgia','Songti SC',serif;--sub-size:50px;--trans-size:22px;--radius:3px;--shadow:0_2px_8px_rgba(92,75,46,0.1);--glow:none"},
    "mint-fresh": {"name":"🍃 薄荷清新","css":"--bg:#f2faf6;--bg2:#fff;--border:#c8e6d4;--text:#2d5a3a;--title:#153a20;--accent:#10b981;--accent2:#f59e0b;--tag-bg:#ddf4e8;--panel-bg:#fafdfb;--item-bg:#f2faf6;--dim:#7db890;--font:sans-serif;--sub-size:50px;--trans-size:22px;--radius:12px;--shadow:0_2px_10px_rgba(16,185,129,0.08);--glow:none"},
    "lavender-dream": {"name":"🌸 薰衣草梦","css":"--bg:#f5f2fa;--bg2:#fff;--border:#d8cee8;--text:#4a3a5e;--title:#291e3a;--accent:#8b5cf6;--accent2:#ec4899;--tag-bg:#ede4f4;--panel-bg:#faf8fc;--item-bg:#f5f2fa;--dim:#9a8ab8;--font:sans-serif;--sub-size:50px;--trans-size:22px;--radius:14px;--shadow:0_2px_12px_rgba(139,92,246,0.08);--glow:none"},
    "rose-blush": {"name":"🌹 玫瑰晨露","css":"--bg:#fdf2f4;--bg2:#fff;--border:#f0c6cc;--text:#5e2d3a;--title:#3a1520;--accent:#e11d48;--accent2:#6366f1;--tag-bg:#fce4e8;--panel-bg:#fffafa;--item-bg:#fdf2f4;--dim:#c88a96;--font:sans-serif;--sub-size:50px;--trans-size:22px;--radius:12px;--shadow:0_2px_10px_rgba(225,29,72,0.06);--glow:none"},
    "arctic-frost": {"name":"❄️ 极地冰霜","css":"--bg:#f0f4f8;--bg2:#fff;--border:#d0dde8;--text:#2e3d5a;--title:#15203a;--accent:#3b82f6;--accent2:#14b8a6;--tag-bg:#e0eaf4;--panel-bg:#f8fafc;--item-bg:#f0f4f8;--dim:#8a9ab8;--font:sans-serif;--sub-size:50px;--trans-size:22px;--radius:10px;--shadow:0_2px_10px_rgba(59,130,246,0.06);--glow:none"},
    "sunset-orange": {"name":"🌅 日落橙光","css":"--bg:#1a0f08;--bg2:#241610;--border:#4a2a18;--text:#e8c8a8;--title:#ffe0c0;--accent:#f97316;--accent2:#facc15;--tag-bg:#301e12;--panel-bg:#1f120a;--item-bg:#1a0f08;--dim:#8a5a3a;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:10px;--shadow:0_0_20px_rgba(249,115,22,0.15);--glow:none"},
    "amber-glow": {"name":"🕯️ 琥珀暖光","css":"--bg:#1a1408;--bg2:#241e10;--border:#4a3a18;--text:#e8d8a8;--title:#ffe8c0;--accent:#eab308;--accent2:#f97316;--tag-bg:#302a12;--panel-bg:#1f180a;--item-bg:#1a1408;--dim:#8a7a3a;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:10px;--shadow:0_0_20px_rgba(234,179,8,0.12);--glow:0_0_8px_rgba(234,179,8,0.2)"},
    "aurora-teal": {"name":"🌌 极光青","css":"--bg:#081416;--bg2:#0e1f23;--border:#1a3840;--text:#98d8e0;--title:#c8f8ff;--accent:#06b6d4;--accent2:#a78bfa;--tag-bg:#122830;--panel-bg:#0a181b;--item-bg:#081416;--dim:#3e6e78;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:12px;--shadow:0_0_20px_rgba(6,182,212,0.12);--glow:none"},
    "coffee-roast": {"name":"☕ 咖啡烘焙","css":"--bg:#1c1410;--bg2:#261c16;--border:#4a3224;--text:#d4b8a0;--title:#f0d8c0;--accent:#c87848;--accent2:#f0a868;--tag-bg:#302218;--panel-bg:#201814;--item-bg:#1c1410;--dim:#7a5a3e;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:6px;--shadow:none;--glow:none"},
    "steel-slate": {"name":"🔩 工业灰","css":"--bg:#18191b;--bg2:#212226;--border:#35373d;--text:#b0b3b8;--title:#e4e5e7;--accent:#6366f1;--accent2:#ef4444;--tag-bg:#26272c;--panel-bg:#1c1d20;--item-bg:#18191b;--dim:#5c5f66;--font:sans-serif;--sub-size:46px;--trans-size:22px;--radius:4px;--shadow:none;--glow:none"},
    "solar-flare": {"name":"⭐ 日冕耀斑","css":"--bg:#0f0a02;--bg2:#1a1206;--border:#4a3010;--text:#f0e0b0;--title:#ffe8a0;--accent:#f59e0b;--accent2:#ef4444;--tag-bg:#302010;--panel-bg:#140e04;--item-bg:#0f0a02;--dim:#8a6a20;--font:sans-serif;--sub-size:48px;--trans-size:22px;--radius:10px;--shadow:0_0_25px_rgba(245,158,11,0.2);--glow:0_0_10px_rgba(245,158,11,0.35)"},
}

# ============================================================
# State
# ============================================================
latest = {"text": "", "time": 0, "rms": 0, "lang": "", "translated": "", "mode": "auto"}
latest_summary = {"key": "", "core_points": [], "key_quotes": [], "mindmap": None, "time": 0}
lang_mode = "auto"
translate_target = CONFIG["translate_target"]
translate_enabled = CONFIG["translate_enabled"]
translate_queue = collections.deque(maxlen=20)
lock = threading.Lock()
sum_lock = threading.Lock()

# v2.0 new state
history_segments = []  # [{time, text, lang, translated}, ...] for SRT
recording_enabled = False
recording_file = None    # WAV file handle
recording_path = ""
recording_bytes = 0
paused = False           # mic capture paused
sse_condition = threading.Condition()
sse_latest = {"seq": 0, "data": None}  # pushed to SSE clients

# ============================================================
# Ollama detection
# ============================================================
HAS_OLLAMA = False
OLLAMA_MODEL = None
try:
    r = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
    if r.returncode == 0:
        models = r.stdout
        for preferred in ["qwen2.5:7b", "qwen2.5:14b", "deepseek-r1:7b"]:
            if preferred in models:
                OLLAMA_MODEL = preferred; break
        if not OLLAMA_MODEL:
            for line in models.split("\n"):
                if line and not line.startswith("NAME"):
                    OLLAMA_MODEL = line.split()[0]; break
        if OLLAMA_MODEL:
            HAS_OLLAMA = True
            print(f"Ollama detected: {OLLAMA_MODEL} → AI summarization ENABLED")
except:
    pass
if not HAS_OLLAMA:
    print("Ollama not found → AI summarization DISABLED (core ASR works standalone)")

# ============================================================
# Core functions
# ============================================================
def parse_sv(raw):
    tags = re.findall(r'<\|([^|]*)\|>', raw)
    clean = re.sub(r'<\|[^|]*\|>', '', raw).strip()
    return clean, tags[0] if tags else ""

def add_punc(text):
    if not text or len(text) < 2: return text
    try:
        r = punc_model.generate(input=text)
        if r and isinstance(r, list) and r[0]: return r[0].get("text", text)
    except: pass
    return text

def fmt_srt_time(t):
    """Format seconds as SRT timestamp: HH:MM:SS,mmm"""
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def generate_srt(segments):
    """Generate SRT subtitle content from segments"""
    if not segments: return ""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = fmt_srt_time(seg.get("start", seg["time"] - 1.5))
        end = fmt_srt_time(seg.get("end", seg["time"] + 0.5))
        text = seg["text"]
        if seg.get("translated"):
            text = f"{text}\\n{seg['translated']}"
        lines.append(f"{i}")
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
    # Replace literal \n in SRT with actual newlines
    return "\n".join(lines).replace("\\n", "\n")

def start_recording():
    global recording_file, recording_path, recording_bytes
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    recording_path = os.path.expanduser(f"~/Desktop/FunASR_Recording_{timestamp}.wav")
    recording_file = open(recording_path, "wb")
    # Write placeholder WAV header (will be fixed on close)
    recording_file.write(b"\x00" * 44)
    recording_bytes = 0
    print(f"🎙️  Recording started → {recording_path}", flush=True)

def stop_recording():
    global recording_file, recording_path, recording_bytes
    if recording_file:
        # Fix WAV header
        data_size = recording_bytes
        recording_file.seek(0)
        sample_rate = CONFIG["sample_rate"]
        num_channels = 1
        bits_per_sample = 16
        byte_rate = sample_rate * num_channels * bits_per_sample // 8
        block_align = num_channels * bits_per_sample // 8
        
        header = struct.pack('<4sI4s4sIHHIIHH4sI',
            b'RIFF', 36 + data_size,
            b'WAVE',
            b'fmt ', 16, 1, num_channels, sample_rate,
            byte_rate, block_align, bits_per_sample,
            b'data', data_size)
        recording_file.seek(0)
        recording_file.write(header)
        recording_file.close()
        size_mb = data_size / (1024 * 1024)
        print(f"💾 Recording saved: {recording_path} ({size_mb:.1f} MB)", flush=True)
        recording_file = None
        recording_path = ""

def append_wav_frames(frames_bytes):
    global recording_file, recording_bytes
    if recording_file:
        recording_file.write(frames_bytes)
        recording_bytes += len(frames_bytes)

def sse_broadcast(data):
    """Notify all SSE long-poll clients"""
    with sse_condition:
        sse_latest["seq"] += 1
        sse_latest["data"] = json.dumps(data, ensure_ascii=False)
        sse_condition.notify_all()

# ============================================================
# AI Summarization (optional, Ollama)
# ============================================================
def summarize(buffer_text):
    if not HAS_OLLAMA or len(buffer_text) < 50: return None
    prompt = f"""你是一个会议纪要助手。请从以下语音转录内容中提取关键信息，严格按照指定的JSON格式输出，不要添加任何解释、前言或后缀。

输出格式（必须完全遵守）：
{{"key":"一句话主题概括","core_points":[{{"title":"观点1"}},{{"title":"观点2"}}],"key_quotes":["原文金句1","原文金句2"],"mindmap":{{"name":"主题","children":[{{"name":"分支1","children":[{{"name":"要点"}}]}}]}}}}

转录内容：{buffer_text}

只输出JSON："""
    try:
        import urllib.request
        payload = json.dumps({"model": OLLAMA_MODEL, "prompt": prompt, "stream": False})
        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=payload.encode(),
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=60)
        raw = json.loads(resp.read()).get("response", "")
        m = re.search(r'\{[\s\S]*\}', raw)
        if not m: return None
        d = json.loads(m.group(0))
        if "key" not in d:
            for k in d:
                if isinstance(d[k], dict):
                    inner = d[k]
                    if "key" in inner: d = inner
                    else: d = {"key": k, **inner}
                    break
        return d
    except Exception as e:
        print(f"Summarize error: {e}", file=sys.stderr)
    return None

# ============================================================
# Translation
# ============================================================
TRANS_LANG_MAP = {
    "zh": "zh-CN", "ja": "ja", "ko": "ko", "en": "en",
    "fr": "fr", "de": "de", "es": "es",
    "ru": "ru", "th": "th", "vi": "vi",
    "it": "it", "pt": "pt", "id": "id",
    "ar": "ar", "tr": "tr", "hi": "hi",
    "nl": "nl", "ms": "ms", "sv": "sv",
    "pl": "pl", "uk": "uk", "tl": "tl",
}
def translate_text(text, target="en"):
    if not text or len(text.strip()) < 2: return ""
    tc = TRANS_LANG_MAP.get(target, target)
    try:
        return GoogleTranslator(source='auto', target=tc).translate(text)
    except Exception as e:
        print(f"Translate error: {e}", file=sys.stderr)
        return ""

def translate_worker():
    global latest, translate_target, translate_enabled, translate_queue
    while True:
        time.sleep(0.3)
        if not translate_enabled or not translate_queue: continue
        try:
            text = translate_queue.popleft()
            result = translate_text(text, translate_target)
            if result:
                with lock:
                    if latest["text"] == text:
                        latest["translated"] = result
        except: pass

def summary_worker(buffer_queue):
    global latest_summary
    seen_texts = set()
    while True:
        time.sleep(15)
        with lock: segments = list(buffer_queue)
        if not segments: continue
        texts = []
        for s in segments:
            t = s.strip()
            if t and t not in seen_texts and len(t) > 3:
                texts.append(t); seen_texts.add(t)
            if len(seen_texts) > 200: seen_texts = set(list(seen_texts)[-100:])
        if not texts: continue
        combined = "。".join(texts[-15:])
        if len(combined) < 40: continue
        result = summarize(combined)
        if result:
            with sum_lock:
                latest_summary = {
                    "key": result.get("key", ""),
                    "core_points": result.get("core_points", []),
                    "key_quotes": result.get("key_quotes", []),
                    "mindmap": result.get("mindmap"),
                    "time": time.time()
                }
            print(f"Summary: {result.get('key', '')[:60]}", flush=True)

# ============================================================
# Audio capture + ASR loop
# ============================================================
buffer_queue = collections.deque(maxlen=300)

def mic_loop():
    global latest, lang_mode, buffer_queue, history_segments, paused
    seq = 0
    while True:
        if paused:
            time.sleep(0.5)
            # Still update RMS to show silence
            with lock:
                latest["rms"] = 0
            sse_broadcast(dict(latest))
            continue
        
        seq += 1
        tmp = f"/tmp/funasr_{seq}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
            "-f", "avfoundation", "-i", ":0",
            "-t", str(CONFIG["chunk_seconds"]),
            "-ar", str(CONFIG["sample_rate"]), "-ac", "1",
            "-sample_fmt", "s16", tmp], capture_output=True, timeout=8)
        if not os.path.exists(tmp) or os.path.getsize(tmp) < 500:
            time.sleep(0.2); continue
        
        if recording_enabled:
            with open(tmp, 'rb') as f:
                raw_audio = f.read()
            append_wav_frames(raw_audio)
        
        with wave.open(tmp, 'rb') as wf:
            frames = wf.readframes(wf.getnframes())
            data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768
            rms = float(np.sqrt(np.mean(data ** 2)))
        
        if rms < CONFIG["rms_threshold"]:
            os.remove(tmp); time.sleep(0.2); continue
        
        try:
            mode = lang_mode
            asr_lang = "auto" if mode == "auto" or "+" in mode else mode
            result = asr_model.generate(input=tmp, language=asr_lang, use_itn=True)
            raw_text = ""
            for item in result:
                if isinstance(item, dict): raw_text = item.get("text", "")
                elif isinstance(item, list) and item:
                    x = item[0]; raw_text = x if isinstance(x, str) else x.get("text", "")
        except:
            os.remove(tmp); continue
        
        text, lang_code = parse_sv(raw_text) if raw_text else ("", "")
        
        # Bilingual mode re-check
        if "+" in mode and lang_code:
            modes = LANG_MODES.get(mode)
            if modes and modes["allowed"] and lang_code not in modes["allowed"]:
                primary = mode.split("+")[0]
                try:
                    result2 = asr_model.generate(input=tmp, language=primary, use_itn=True)
                    raw2 = ""
                    for item in result2:
                        if isinstance(item, dict): raw2 = item.get("text", "")
                        elif isinstance(item, list) and item:
                            x2 = item[0]; raw2 = x2 if isinstance(x2, str) else x2.get("text", "")
                    if raw2:
                        text2, lc2 = parse_sv(raw2)
                        if text2 and text2 != text: text, lang_code = text2, primary
                except: pass
        
        lang = LANG_MAP.get(lang_code, lang_code)
        if text: text = add_punc(text)
        os.remove(tmp)
        
        if text:
            now = time.time()
            seg = {"time": now, "text": text, "lang": lang, "translated": "",
                   "start": now - CONFIG["chunk_seconds"] - 0.5,
                   "end": now + 0.5}
            with lock:
                latest = {"text": text, "time": now, "rms": rms,
                          "lang": lang, "translated": "", "mode": lang_mode,
                          "paused": paused, "recording": recording_enabled}
                buffer_queue.append(text)
                history_segments.append(seg)
                if len(history_segments) > 1000:
                    history_segments = history_segments[-500:]
                if translate_enabled: translate_queue.append(text)
            
            tag = f"[{lang}]" if lang else ""
            print(f"> {tag} {text}  (RMS:{rms:.4f})", flush=True)
            
            # SSE push
            sse_broadcast(dict(latest))

# ============================================================
# Web UI HTML
# ============================================================
style_opts = "\n".join(
    f'<option value="{k}"{" selected" if k=="dark-tech" else ""}>{v["name"]}</option>'
    for k, v in STYLES.items()
)
themes_json = json.dumps({k: v["css"] for k, v in STYLES.items()}, ensure_ascii=False)
show_summary = "true" if HAS_OLLAMA else "false"

summary_tab_html = ""
summary_tab_js = ""
if HAS_OLLAMA:
    summary_tab_html = """
<button class="tab-btn" onclick="switchTab('mindmap')" id="tab-mindmap">🧠 脑图</button>
<button class="tab-btn" onclick="switchTab('points')" id="tab-points">💡 观点</button>
<button class="tab-btn" onclick="switchTab('quotes')" id="tab-quotes">✨ 金句</button>"""
    summary_tab_js = """
let lastSumTime=0,currentTab='mindmap';
window.switchTab=function(t){currentTab=t;
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  if(document.getElementById('tab-'+t))document.getElementById('tab-'+t).classList.add('active');
  document.getElementById('tab-mindmap').style.display=t==='mindmap'?'block':'none';
  document.getElementById('tab-points').style.display=t==='points'?'block':'none';
  document.getElementById('tab-quotes').style.display=t==='quotes'?'block':'none';};
function renderMindmap(node,depth){if(!node)return'';
  let h='<div class="node '+(depth===0?'root':depth===1?'branch':'leaf')+'">';
  if(depth>0)h+='<span class="connector">'+('│  '.repeat(depth-1))+'├─ </span>';
  h+=node.name||node.title||'';h+='</div>';
  if(node.children)for(let c of node.children)h+=renderMindmap(c,depth+1);return h;}
function renderSummary(d){if(!d||!d.time||d.time===lastSumTime)return;lastSumTime=d.time;
  const e='<div class="empty-state"><span class="empty-icon">📝</span><p>持续说话中，AI 会自动整理...</p></div>';
  if(d.key){
    document.getElementById('tab-mindmap').innerHTML=d.mindmap?
      '<div class="section-label">'+d.key+'</div><div class="mindmap-tree">'+renderMindmap(d.mindmap,0)+'</div>':e;
    let p='';if(d.core_points&&d.core_points.length){p='<ul class="points-list">';
      for(let i=0;i<d.core_points.length;i++)p+='<li><span class="point-num">'+(i+1)+'</span><span class="point-title">'+d.core_points[i].title+'</span></li>';p+='</ul>';}
    document.getElementById('tab-points').innerHTML=p||e;
    let q='';if(d.key_quotes&&d.key_quotes.length){q='<ul class="quotes-list">';
      for(let qt of d.key_quotes)q+='<li>'+qt+'</li>';q+='</ul>';}
    document.getElementById('tab-quotes').innerHTML=q||e;
  }else{[...document.querySelectorAll('#tab-mindmap,#tab-points,#tab-quotes')].forEach(b=>b.innerHTML=e);}}
setInterval(async()=>{try{const r=await fetch('/summary');renderSummary(await r.json())}catch(e){}},3000);
"""

mode_pill = "ct-punc" if not HAS_OLLAMA else "ct-punc + AI"
ollama_badge = "" if not HAS_OLLAMA else f'<span class="badge badge-on">AI {OLLAMA_MODEL}</span>'

HTML = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kev.FunASR Live · by @KevPH2026</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{font-size:16px}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);height:100vh;
  display:flex;transition:background 0.4s,color 0.4s;overflow:hidden}}

.sidebar{{width:270px;min-width:270px;background:var(--panel-bg);
  border-right:1px solid var(--border);display:flex;flex-direction:column;
  padding:0;overflow-y:auto;z-index:10}}
.sidebar-header{{padding:20px 20px 16px;border-bottom:1px solid var(--border)}}
.sidebar-header h1{{font-size:18px;color:var(--title);font-weight:700;margin-bottom:4px}}
.sidebar-header .ver{{font-size:11px;color:var(--dim)}}
.sidebar-section{{padding:14px 20px;border-bottom:1px solid var(--border)}}
.sidebar-section:last-child{{border-bottom:none}}
.section-title{{font-size:10px;color:var(--dim);text-transform:uppercase;
  letter-spacing:1.5px;margin-bottom:10px;font-weight:600}}

.status-row{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.rec-dot{{width:10px;height:10px;border-radius:50%;background:#22c55e;
  box-shadow:0 0 8px rgba(34,197,94,0.5);transition:all 0.3s}}
.rec-dot.paused{{background:#f59e0b;box-shadow:0 0 8px rgba(245,158,11,0.5);animation:none}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.5}}}}
.status-text{{font-size:14px;color:var(--title);font-weight:600;flex:1}}
.status-sub{{font-size:11px;color:var(--dim);margin-top:2px}}

.meter-row{{display:flex;align-items:center;gap:8px;margin-top:4px}}
.meter-label{{font-size:11px;color:var(--dim);min-width:28px}}
.meter-bar{{flex:1;height:3px;background:var(--tag-bg);border-radius:2px;overflow:hidden}}
.meter-fill{{height:100%;background:var(--accent2);border-radius:2px;transition:width 0.15s}}
.meter-val{{font-size:11px;color:var(--text);min-width:40px;text-align:right;font-family:monospace}}

.ctrl-select{{width:100%;padding:7px 10px;border:1px solid var(--border);
  border-radius:var(--radius);background:var(--bg2);color:var(--text);
  font-size:13px;cursor:pointer;outline:none;margin-bottom:6px}}
.ctrl-select:focus{{border-color:var(--accent)}}
.ctrl-select:last-child{{margin-bottom:0}}

/* Toggle button */
.toggle-btn{{width:100%;padding:8px 12px;border:1px solid var(--border);
  border-radius:var(--radius);background:var(--bg2);color:var(--text);
  font-size:13px;cursor:pointer;outline:none;text-align:left;
  transition:all 0.2s;display:flex;align-items:center;gap:8px}}
.toggle-btn:hover{{border-color:var(--accent)}}
.toggle-btn.active{{border-color:#22c55e;background:rgba(34,197,94,0.08);color:#22c55e}}
.toggle-btn .tog-dot{{width:8px;height:8px;border-radius:50%;background:var(--dim);
  transition:all 0.2s}}
.toggle-btn.active .tog-dot{{background:#22c55e;box-shadow:0 0 6px rgba(34,197,94,0.5)}}

/* Action button */
.action-btn{{width:100%;padding:8px 12px;border:1px solid var(--border);
  border-radius:var(--radius);background:var(--bg2);color:var(--accent);
  font-size:13px;cursor:pointer;outline:none;text-align:center;
  transition:all 0.2s;margin-top:6px}}
.action-btn:hover{{border-color:var(--accent);background:rgba(88,166,255,0.06)}}
.action-btn:active{{transform:scale(0.97)}}
.action-btn .kbd{{float:right;background:var(--tag-bg);color:var(--dim);
  padding:1px 6px;border-radius:3px;font-size:10px;font-family:monospace}}

.badge{{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;
  font-weight:600;margin-top:6px}}
.badge-on{{background:rgba(34,197,94,0.15);color:#22c55e}}
.badge-off{{background:var(--tag-bg);color:var(--dim)}}
.badge-rec{{background:rgba(239,68,68,0.15);color:#ef4444;animation:pulse 1.5s infinite}}

.sidebar-footer{{margin-top:auto;padding:14px 20px;border-top:1px solid var(--border);
  font-size:10px;color:var(--dim);text-align:center}}

.main{{flex:1;display:flex;flex-direction:column;min-width:0;position:relative}}

/* Keyboard hint overlay */
.kbd-hint{{position:fixed;bottom:20px;right:20px;background:var(--tag-bg);
  color:var(--dim);font-size:11px;padding:6px 12px;border-radius:var(--radius);
  font-family:monospace;pointer-events:none;opacity:0.6;z-index:100}}

.subtitle-zone{{flex:1;display:flex;align-items:center;justify-content:center;
  padding:60px 60px 20px;flex-direction:column}}
.subtitle{{font-size:var(--sub-size);font-weight:700;color:var(--title);text-align:center;
  max-width:900px;line-height:1.3;text-shadow:var(--glow)}}
.subtitle .text{{animation:fadeIn 0.35s ease-out;display:block}}
.subtitle .trans{{font-size:var(--trans-size);color:var(--accent2);
  margin-top:8px;font-weight:400;animation:fadeIn 0.4s ease-out;
  opacity:0.85;font-style:italic;display:block}}
.subtitle .lang-tag{{display:inline-block;background:var(--tag-bg);color:var(--accent);
  font-size:12px;padding:2px 8px;border-radius:var(--radius);margin-bottom:10px;
  font-weight:400}}

/* Pause overlay */
.pause-overlay{{display:none;position:absolute;top:0;left:0;right:0;bottom:0;
  background:rgba(0,0,0,0.3);justify-content:center;align-items:center;z-index:5}}
.pause-overlay.show{{display:flex}}
.pause-badge{{font-size:24px;color:#f59e0b;font-weight:700;
  background:var(--panel-bg);padding:12px 32px;border-radius:var(--radius);
  border:2px solid #f59e0b}}

.tab-panel{{border-top:1px solid var(--border);background:var(--panel-bg);
  max-height:42vh;display:flex;flex-direction:column}}
.tab-bar{{display:flex;gap:2px;padding:8px 20px 0;border-bottom:1px solid var(--border);
  overflow-x:auto;align-items:center}}
.tab-bar-spacer{{flex:1}}
.tab-btn{{padding:8px 16px;border:none;border-bottom:2px solid transparent;
  background:none;color:var(--dim);font-size:13px;cursor:pointer;
  white-space:nowrap;transition:all 0.2s}}
.tab-btn:hover{{color:var(--text)}}
.tab-btn.active{{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}}
.dl-btn{{padding:6px 12px;border:1px solid var(--border);
  border-radius:var(--radius);background:var(--bg2);color:var(--accent2);
  font-size:12px;cursor:pointer;white-space:nowrap;margin-bottom:4px;
  transition:all 0.2s;text-decoration:none;display:inline-block}}
.dl-btn:hover{{border-color:var(--accent2);background:rgba(240,136,62,0.06)}}
.tab-content{{flex:1;overflow-y:auto;padding:16px 20px}}

.history-item{{padding:3px 0;color:var(--text);border-bottom:1px solid var(--border);
  display:flex;gap:10px}}
.history-item .h-time{{color:var(--dim);min-width:70px;flex-shrink:0}}
.history-item .h-lang{{color:var(--accent);min-width:36px;flex-shrink:0;font-size:10px}}
.history-item .h-text{{flex:1;word-break:break-all}}

.points-list{{list-style:none}}
.points-list li{{padding:10px 14px;margin:4px 0;background:var(--item-bg);
  border-radius:var(--radius);border-left:3px solid var(--accent);
  display:flex;align-items:baseline;gap:12px}}
.point-num{{color:var(--accent);font-size:13px;font-weight:700;min-width:18px}}
.point-title{{font-size:14px;color:var(--title);font-weight:500;line-height:1.5}}

.quotes-list{{list-style:none}}
.quotes-list li{{padding:12px 16px;margin:6px 0;background:var(--item-bg);
  border-radius:var(--radius);border-left:3px solid var(--accent2);
  font-size:14px;line-height:1.7;color:var(--text);font-style:italic}}

.mindmap-tree{{font-size:13px;line-height:1.9;padding:8px 0}}
.mindmap-tree .node{{padding:3px 0}}
.mindmap-tree .root{{font-size:16px;font-weight:700;color:var(--accent);padding:6px 0}}
.mindmap-tree .branch{{margin-left:24px;color:var(--text);font-weight:500}}
.mindmap-tree .leaf{{margin-left:48px;color:var(--dim);font-size:12px}}
.mindmap-tree .connector{{color:var(--border)}}
.section-label{{font-size:11px;color:var(--dim);text-transform:uppercase;
  letter-spacing:1px;margin-bottom:8px;font-weight:600}}
.empty-state{{text-align:center;padding:40px 20px;color:var(--dim)}}
.empty-icon{{font-size:32px;display:block;margin-bottom:10px}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}

/* Toast notification */
.toast{{position:fixed;top:20px;left:50%;transform:translateX(-50%);
  background:var(--accent);color:#fff;padding:10px 24px;border-radius:8px;
  font-size:13px;font-weight:600;z-index:200;animation:fadeIn 0.3s ease-out,toastOut 0.3s 2s ease-out forwards;
  pointer-events:none}}
@keyframes toastOut{{to{{opacity:0;transform:translateX(-50%) translateY(-10px)}}}}

::-webkit-scrollbar{{width:4px}}
::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}
</style></head><body>

<!-- Sidebar -->
<aside class="sidebar">
  <div class="sidebar-header">
    <h1>🎙️ Kev.FunASR</h1>
    <div class="ver">by <a href="https://github.com/KevPH2026" target="_blank" style="color:var(--accent2);text-decoration:none">@KevPH2026</a> · <a href="https://superk.ai" target="_blank" style="color:var(--accent2);text-decoration:none">Mr.K Lab</a></div>
  </div>

  <div class="sidebar-section">
    <div class="section-title">状态</div>
    <div class="status-row">
      <div class="rec-dot" id="recDot"></div>
      <span class="status-text" id="statusText">Listening</span>
    </div>
    <div class="status-sub" id="modePill">{mode_pill}</div>
    {ollama_badge}
    <span class="badge badge-rec" id="recBadge" style="display:none">🔴 REC</span>
    <div class="meter-row">
      <span class="meter-label">Level</span>
      <div class="meter-bar"><div class="meter-fill" id="meterBar" style="width:0%"></div></div>
      <span class="meter-val" id="meterVal">--</span>
    </div>
  </div>

  <div class="sidebar-section">
    <div class="section-title">外观</div>
    <select class="ctrl-select" id="stylesel" onchange="setStyle(this.value)">
      {style_opts}
    </select>
  </div>

  <div class="sidebar-section">
    <div class="section-title">语言</div>
    <select class="ctrl-select" id="langsel" onchange="setLang(this.value)">
      <option value="auto">🌐 自动检测</option>
      <optgroup label="单语言">
        <option value="zh">🇨🇳 仅中文</option>
        <option value="en">🇺🇸 English only</option>
        <option value="ja">🇯🇵 日本語のみ</option>
        <option value="ko">🇰🇷 한국어만</option>
        <option value="yue">🇭🇰 僅粵語</option>
        <option value="fr">🇫🇷 Français seul</option>
        <option value="de">🇩🇪 Nur Deutsch</option>
        <option value="es">🇪🇸 Solo Español</option>
        <option value="ru">🇷🇺 Только русский</option>
        <option value="th">🇹🇭 ภาษาไทยเท่านั้น</option>
        <option value="vi">🇻🇳 Chỉ tiếng Việt</option>
        <option value="it">🇮🇹 Solo Italiano</option>
        <option value="pt">🇧🇷 Só Português</option>
        <option value="id">🇮🇩 Bahasa saja</option>
        <option value="ar">🇸🇦 العربية فقط</option>
        <option value="tr">🇹🇷 Sadece Türkçe</option>
        <option value="hi">🇮🇳 केवल हिन्दी</option>
        <option value="nl">🇳🇱 Alleen Nederlands</option>
        <option value="ms">🇲🇾 Bahasa sahaja</option>
      </optgroup>
      <optgroup label="双语模式">
        <option value="zh+en">🇨🇳🇺🇸 中英双语</option>
        <option value="zh+ja">🇨🇳🇯🇵 中日双语</option>
        <option value="zh+ko">🇨🇳🇰🇷 中韩双语</option>
        <option value="zh+fr">🇨🇳🇫🇷 中法双语</option>
        <option value="zh+de">🇨🇳🇩🇪 中德双语</option>
        <option value="zh+es">🇨🇳🇪🇸 中西双语</option>
        <option value="en+ja">🇺🇸🇯🇵 EN+JP</option>
        <option value="en+ko">🇺🇸🇰🇷 EN+KR</option>
      </optgroup>
    </select>
  </div>

  <div class="sidebar-section">
    <div class="section-title">翻译</div>
    <select class="ctrl-select" id="transSel" onchange="setTransTarget(this.value)">
      <optgroup label="常用">
        <option value="en">🌐 → English</option>
        <option value="zh">🇨🇳 → 中文</option>
        <option value="ja">🇯🇵 → 日本語</option>
        <option value="ko">🇰🇷 → 한국어</option>
      </optgroup>
      <optgroup label="欧洲">
        <option value="fr">🇫🇷 → Français</option>
        <option value="de">🇩🇪 → Deutsch</option>
        <option value="es">🇪🇸 → Español</option>
        <option value="it">🇮🇹 → Italiano</option>
        <option value="pt">🇧🇷 → Português</option>
        <option value="nl">🇳🇱 → Nederlands</option>
        <option value="sv">🇸🇪 → Svenska</option>
        <option value="pl">🇵🇱 → Polski</option>
        <option value="uk">🇺🇦 → Українська</option>
      </optgroup>
      <optgroup label="亚洲">
        <option value="th">🇹🇭 → ไทย</option>
        <option value="vi">🇻🇳 → Tiếng Việt</option>
        <option value="id">🇮🇩 → Bahasa</option>
        <option value="ms">🇲🇾 → Melayu</option>
        <option value="tl">🇵🇭 → Tagalog</option>
        <option value="hi">🇮🇳 → हिन्दी</option>
        <option value="tr">🇹🇷 → Türkçe</option>
        <option value="ar">🇸🇦 → العربية</option>
      </optgroup>
      <option value="off" style="color:#ef4444">⏸️ 关闭翻译</option>
    </select>
  </div>

  <div class="sidebar-section">
    <div class="section-title">控制</div>
    <button class="toggle-btn" id="pauseBtn" onclick="togglePause()">
      <span class="tog-dot"></span> ⏯️ 暂停识别 <span class="kbd" style="float:right">Space</span>
    </button>
    <button class="toggle-btn" id="recBtn" onclick="toggleRecording()">
      <span class="tog-dot"></span> 🎙️ 录音保存 <span class="kbd" style="float:right">R</span>
    </button>
  </div>

  <div class="sidebar-section">
    <button class="action-btn" onclick="downloadSRT()">
      📥 导出 SRT 字幕 <span class="kbd">S</span>
    </button>
  </div>

  <div class="sidebar-footer">
    <div style="margin-bottom:4px;font-weight:600">🎙️ Kev.FunASR</div>
    by <a href="https://github.com/KevPH2026" target="_blank" style="color:var(--accent2);text-decoration:none">@KevPH2026</a>
    · <a href="https://superk.ai" target="_blank" style="color:var(--accent2);text-decoration:none">Mr.K Lab</a><br>
    <a href="https://github.com/KevPH2026/kev-funasr" target="_blank" style="color:var(--muted);text-decoration:none;font-size:11px">🐙 GitHub</a>
    &nbsp;·&nbsp; <a href="https://x.com/skyerK12" target="_blank" style="color:var(--muted);text-decoration:none;font-size:11px">𝕏 @skyerK12</a><br>
    <span style="font-size:10px;color:var(--muted)">Powered by FunASR · SenseVoiceSmall</span>
  </div>
</aside>

<!-- Main -->
<main class="main">
  <div class="pause-overlay" id="pauseOverlay">
    <div class="pause-badge">⏸️ PAUSED</div>
  </div>

  <div class="subtitle-zone">
    <div class="subtitle" id="sub">
      <span class="text"></span>
      <span class="trans" id="transText"></span>
    </div>
  </div>

  <div class="tab-panel">
    <div class="tab-bar">
      <button class="tab-btn active" onclick="switchMainTab('history')" id="mtab-history">📜 历史</button>
      {summary_tab_html}
      <span class="tab-bar-spacer"></span>
      <a class="dl-btn" href="/download/srt" download="funasr_subtitles.srt" id="srtLink">📥 SRT ↓</a>
    </div>
    <div class="tab-content" id="tab-history"></div>
    <div class="tab-content" id="tab-mindmap" style="display:none"></div>
    <div class="tab-content" id="tab-points" style="display:none"></div>
    <div class="tab-content" id="tab-quotes" style="display:none"></div>
  </div>
</main>

<div class="kbd-hint">Space:暂停 · S:导出SRT · R:录音 · 切换Tab:1-4</div>

<script>
const THEMES={themes_json};
const SHOW_SUMMARY={show_summary};
function applyTheme(k){{const css=THEMES[k]||THEMES['dark-tech'];
  document.documentElement.style.cssText=css;localStorage.setItem('funasr-style',k);}}
function setStyle(v){{applyTheme(v)}}
(function(){{const s=localStorage.getItem('funasr-style')||'dark-tech';applyTheme(s);
  document.getElementById('stylesel').value=s;}})();

const sub=document.getElementById('sub'),meterBar=document.getElementById('meterBar'),
  meterVal=document.getElementById('meterVal'),recDot=document.getElementById('recDot'),
  transText=document.getElementById('transText'),statusText=document.getElementById('statusText'),
  pauseBtn=document.getElementById('pauseBtn'),recBtn=document.getElementById('recBtn'),
  pauseOverlay=document.getElementById('pauseOverlay'),recBadge=document.getElementById('recBadge');

let lastTime=0,mainTab='history',isPaused=false,isRecording=false;

function toast(msg){{const t=document.createElement('div');t.className='toast';t.textContent=msg;
  document.body.appendChild(t);setTimeout(()=>t.remove(),2500);}}

window.switchMainTab=function(t){{mainTab=t;
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('mtab-'+t).classList.add('active');
  document.getElementById('tab-history').style.display=t==='history'?'block':'none';
  if(SHOW_SUMMARY){{
    document.getElementById('tab-mindmap').style.display=t==='mindmap'?'block':'none';
    document.getElementById('tab-points').style.display=t==='points'?'block':'none';
    document.getElementById('tab-quotes').style.display=t==='quotes'?'block':'none';
  }}}}

async function setLang(v){{await fetch('/set_lang?mode='+encodeURIComponent(v))}}

async function setTransTarget(v){{
  if(v==='off')await fetch('/set_translate?enabled=0');
  else await fetch('/set_translate?target='+encodeURIComponent(v)+'&enabled=1');
  localStorage.setItem('funasr-trans',v);
  if(v==='off')transText.textContent='';
}}

async function togglePause(){{
  const r=await fetch('/toggle_pause');const d=await r.json();
  isPaused=d.paused;
  pauseBtn.classList.toggle('active',isPaused);
  if(isPaused){{
    statusText.textContent='Paused';recDot.classList.add('paused');
    pauseOverlay.classList.add('show');
    toast('⏸️ 已暂停');
  }}else{{
    statusText.textContent='Listening';recDot.classList.remove('paused');
    pauseOverlay.classList.remove('show');
    toast('▶️ 继续识别');
  }}
}}

async function toggleRecording(){{
  const r=await fetch('/toggle_record');const d=await r.json();
  isRecording=d.recording;
  recBtn.classList.toggle('active',isRecording);
  recBadge.style.display=isRecording?'inline-block':'none';
  if(isRecording)toast('🔴 录音已开始 → 桌面');
  else toast('💾 录音已保存 → 桌面');
}}

function downloadSRT(){{
  const a=document.createElement('a');
  a.href='/download/srt';a.download='funasr_subtitles.srt';
  document.body.appendChild(a);a.click();document.body.removeChild(a);
  toast('📥 SRT 已下载');
}}

// SSE real-time push (replaces polling)
(function(){{
  const evt=new EventSource('/events');
  evt.onmessage=function(e){{
    try{{
      const d=JSON.parse(e.data);
      const rms=d.rms!==undefined?Number(d.rms):0;
      meterVal.textContent=rms.toFixed(4);
      meterBar.style.width=Math.min(100,rms*2000)+'%';
      
      // Update pause/rec state
      if(d.paused!==undefined && d.paused!==isPaused){{
        isPaused=d.paused;
        pauseBtn.classList.toggle('active',isPaused);
        if(isPaused){{statusText.textContent='Paused';recDot.classList.add('paused');
          pauseOverlay.classList.add('show');}}
        else{{statusText.textContent='Listening';recDot.classList.remove('paused');
          pauseOverlay.classList.remove('show');}}
      }}
      if(d.recording!==undefined && d.recording!==isRecording){{
        isRecording=d.recording;
        recBtn.classList.toggle('active',isRecording);
        recBadge.style.display=isRecording?'inline-block':'none';
      }}
      
      if(isPaused){{
        recDot.style.background='#f59e0b';
      }}else{{
        recDot.style.background=rms>0.003?'#22c55e':'#f85149';
        recDot.style.boxShadow=rms>0.003?'0 0 8px rgba(34,197,94,0.5)':'0 0 8px rgba(248,81,73,0.3)';
      }}
      
      if(d.mode)document.getElementById('langsel').value=d.mode;
      
      if(d.text&&d.time!==lastTime){{
        lastTime=d.time;let h='';
        if(d.lang)h+='<span class="lang-tag">'+d.lang+'</span>';
        h+='<span class="text">'+d.text+'</span>';sub.innerHTML=h;
        if(d.translated)transText.textContent=d.translated;
        const div=document.createElement('div');div.className='history-item';
        div.innerHTML='<span class="h-time">'+new Date(d.time*1000).toLocaleTimeString()+'</span>'
          +'<span class="h-lang">'+(d.lang||'')+'</span>'
          +'<span class="h-text">'+d.text+'</span>';
        const hist=document.getElementById('tab-history');
        hist.prepend(div);
        while(hist.children.length>100)hist.removeChild(hist.lastChild);
      }}
    }}catch(e){{}}
  }};
  evt.onerror=function(){{console.log('SSE reconnect...');}};
}})();

// Keyboard shortcuts
document.addEventListener('keydown',function(e){{
  if(e.target.tagName==='SELECT'||e.target.tagName==='INPUT')return;
  switch(e.key.toLowerCase()){{
    case ' ': e.preventDefault(); togglePause(); break;
    case 's': if(!e.ctrlKey&&!e.metaKey){{e.preventDefault();downloadSRT();}}break;
    case 'r': e.preventDefault(); toggleRecording(); break;
    case '1': switchMainTab('history'); break;
    case '2': if(SHOW_SUMMARY)switchTab('mindmap'); break;
    case '3': if(SHOW_SUMMARY)switchTab('points'); break;
    case '4': if(SHOW_SUMMARY)switchTab('quotes'); break;
  }}
}});

(function(){{const t=localStorage.getItem('funasr-trans')||'en';
  document.getElementById('transSel').value=t;}})();

{summary_tab_js}
</script>
</body></html>"""

# ============================================================
# HTTP Server
# ============================================================
import socketserver
socketserver.TCPServer.allow_reuse_address = True

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global lang_mode
        parsed = urlparse(self.path)
        path, qs = parsed.path, parse_qs(parsed.query)
        
        # Language mode
        if path == "/set_lang":
            mode = qs.get("mode", ["auto"])[0]
            if mode in LANG_MODES: lang_mode = mode
            self._json({"ok": True, "mode": lang_mode}); return
        
        # Translation settings
        if path == "/set_translate":
            global translate_target, translate_enabled
            t = qs.get("target", [None])[0]
            if t: translate_target = t
            e = qs.get("enabled", [None])[0]
            if e is not None: translate_enabled = e.lower() in ("1","true","yes")
            self._json({"ok": True, "target": translate_target, "enabled": translate_enabled}); return
        
        # Toggle pause
        if path == "/toggle_pause":
            global paused
            paused = not paused
            self._json({"ok": True, "paused": paused}); return
        
        # Toggle recording
        if path == "/toggle_record":
            global recording_enabled, recording_file
            recording_enabled = not recording_enabled
            if recording_enabled:
                start_recording()
            else:
                stop_recording()
            self._json({"ok": True, "recording": recording_enabled}); return
        
        # Config
        if path == "/config":
            self._json({
                "has_ollama": HAS_OLLAMA,
                "ollama_model": OLLAMA_MODEL,
                "lang_mode": lang_mode,
                "translate_enabled": translate_enabled,
                "translate_target": translate_target,
                "paused": paused,
                "recording": recording_enabled,
                "version": "2.0.0"
            }); return
        
        # Summary
        if path == "/summary":
            with sum_lock: d = dict(latest_summary)
            self._json(d); return
        
        # API (polling fallback)
        if path == "/api":
            self._json(latest); return
        
        # SSE events (real-time push)
        if path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            last_seq = sse_latest["seq"]
            while True:
                with sse_condition:
                    sse_condition.wait(timeout=15)
                    if sse_latest["seq"] > last_seq:
                        last_seq = sse_latest["seq"]
                        data = sse_latest["data"]
                    else:
                        data = None
                if data:
                    try:
                        self.wfile.write(f"data: {data}\n\n".encode())
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        break
                else:
                    # Keepalive comment
                    try:
                        self.wfile.write(b": keepalive\n\n")
                        self.wfile.flush()
                    except:
                        break
            return
        
        # SRT download
        if path == "/download/srt":
            with lock:
                segs = list(history_segments)
            srt = generate_srt(segs)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain;charset=utf-8")
            self.send_header("Content-Disposition", "attachment; filename=funasr_subtitles.srt")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(srt.encode("utf-8"))
            return
        
        # Default: serve HTML
        self.send_response(200)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Type", "text/html;charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode())
    
    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json;charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        with lock:
            d = dict(data) if isinstance(data, dict) else data
        self.wfile.write(json.dumps(d, ensure_ascii=False).encode())
    
    def log_message(self, *a): pass

# ============================================================
# Start
# ============================================================
threading.Thread(target=mic_loop, daemon=True).start()
threading.Thread(target=translate_worker, daemon=True).start()
if HAS_OLLAMA:
    threading.Thread(target=summary_worker, args=(buffer_queue,), daemon=True).start()

features = "SSE Push + ASR + Punc + 20 Themes + Translate + SRT Export + WAV Record"
if HAS_OLLAMA:
    features += f" + AI Summarize ({OLLAMA_MODEL})"

print()
print(f"✅ FunASR Live v2.0 — http://localhost:{CONFIG['port']}")
print(f"   {features}")
print(f"   快捷键: Space=暂停  S=导出SRT  R=录音  1-4=切换Tab")
print()
HTTPServer(("0.0.0.0", CONFIG["port"]), Handler).serve_forever()
