# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/licença-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/plataforma-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/privacidade-100%25local-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/dependências-3pacotespip-success" alt="Deps">
</p>

<p align="center">
  <b>Transcrição de voz em tempo real, pronta para usar.</b><br>
  Um único arquivo Python. Zero nuvem. Todas as funções incluídas.
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <a href="README_zh.md">🇨🇳 中文</a> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <a href="README_fr.md">🇫🇷 Français</a> · <a href="README_de.md">🇩🇪 Deutsch</a> · <b>🇧🇷 Português</b> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## Por que FunASR Live?

As ferramentas de transcrição em tempo real se dividem em duas categorias:

| | APIs na Nuvem | Apps Desktop | **FunASR Live** |
|---|---|---|---|
| Privacidade | ❌ Áudio enviado a servidores | ✅ Local | ✅ **100% local, sem rede** |
| Custo | ❌ Preço por minuto | 💰 Pagamento único | 🆓 **Grátis para sempre** |
| Latência | ⚠️ 1-3 segundos | ✅ Tempo real | ✅ **SSE push, <100ms** |
| Idiomas | ✅ 50+ | ⚠️ Limitado | ✅ **Detecção automática 20+ idiomas** |
| Exportar legendas | ⚠️ Ferramenta extra | ⚠️ Formato fixo | ✅ **SRT em um clique** |
| Gravação de áudio | ❌ Não | ✅ Sim | ✅ **Botão para salvar WAV** |
| Resumo IA | ⚠️ Custo extra de API | ❌ Raro | ✅ **Integrado (Ollama)** |
| Personalização | ❌ Código fechado | ❌ Código fechado | ✅ **Código completo, 20 temas** |
| Implantação | N/A | Instalador | 🚀 **Um único arquivo `.py`** |

**O equilíbrio perfeito:** funções profissionais de uma API na nuvem + privacidade de um app local + um arquivo Python modificável.

---

## ✨ Funcionalidades

### 🎤 Transcrição em tempo real
Fale → texto aparece instantaneamente. Baseado no **Alibaba SenseVoiceSmall** + VAD + modelo de pontuação. Detecção automática de idioma ou bloqueio em um só.

### ⚡ Push em tempo real SSE
Sem polling. Sem recarregamento. **Server-Sent Events** envia texto ao navegador com latência <100ms.

### 📥 Exportar legendas SRT
Um clique (ou tecla `S`) baixa um arquivo `.srt` padrão. Use diretamente no Premiere, DaVinci Resolve, etc.

### 🎙️ Gravação de áudio WAV
Ativar gravação → todo o áudio do microfone é salvo em `.wav` na área de trabalho. Desativar → cabeçalho reparado, arquivo pronto.

### 🧠 Resumo IA (Ollama)
Se o [Ollama](https://ollama.com) estiver rodando, a IA gera automaticamente:
- **Mapa mental** — árvore visual dos tópicos
- **Pontos-chave** — lista estruturada
- **Citações** — melhores frases textuais

### 🌍 Tradução em tempo real
Idioma A transcrito → traduzido instantaneamente para o idioma B. 20+ idiomas disponíveis.

### 🎨 20 temas
Não apenas modo escuro. **20 temas selecionados** — cyber green, neon night, midnight ink, minimal white, warm paper e mais.

---

## 🚀 Início rápido

```bash
pip install funasr deep-translator numpy
# Opcional: instalar Ollama para resumo IA
brew install ollama && ollama pull qwen2.5:14b
python3 funasr_live.py
open http://localhost:8765
```

A primeira execução baixa cerca de 400 MB de modelos ASR (em cache para usos seguintes).

---

## ⌨️ Atalhos

| Tecla | Ação |
|-------|------|
| `Space` | Pausar/Retomar |
| `S` | Baixar SRT |
| `R` | Ativar gravação |
| `1-4` | Trocar abas |

---

## 📡 API

| Endpoint | Descrição |
|----------|-----------|
| `/events` | Stream SSE (tempo real) |
| `/api` | Último resultado (polling) |
| `/config` | Configuração e estado |
| `/download/srt` | Baixar legendas SRT |
| `/toggle_pause` | Microfone ON/OFF |
| `/toggle_record` | Gravação ON/OFF |
| `/set_lang?mode=pt` | Bloquear idioma |
| `/set_translate?target=en` | Idioma alvo da tradução |

---

## 🔧 Configuração

Editar `CONFIG` no início de `funasr_live.py`:

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

| Cenário | Como ajuda |
|---------|-----------|
| Notas de reunião | Gravar + resumo IA + SRT |
| Criação de conteúdo | Ditar roteiros |
| Aprendizado de idiomas | Falar + tradução em tempo real |
| Acessibilidade | Legendas ao vivo para apresentações |
| Entrevistas | Gravar WAV + transcrição com timestamps |
| Legendagem de vídeo | Gerar SRT diretamente |
| Streaming ao vivo | Incorporar UI como sobreposição de legendas |

---

## 📦 Dependências

```text
funasr >= 1.3.0
deep-translator >= 1.11
numpy >= 1.24
```

Sem Node.js, Docker ou CUDA. Apenas Python + pip.

---

## 📄 Licença

MIT — uso livre, modificação e uso comercial permitidos.

---

<p align="center">
  <sub>Feito com ❤️ pelo <a href="https://superk.ai">Mr.K Lab</a> · Usa <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
