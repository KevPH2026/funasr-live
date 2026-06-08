# 🎙️ FunASR Live v2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/licence-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/plateforme-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey" alt="Platform">
  <img src="https://img.shields.io/badge/ASR-SenseVoiceSmall-orange?logo=alibabacloud" alt="ASR Engine">
  <img src="https://img.shields.io/badge/confidentialité-100%25local-blueviolet?logo=lock" alt="Privacy">
  <img src="https://img.shields.io/badge/dépendances-3paquetspip-success" alt="Deps">
</p>

<p align="center">
  <b>Transcription vocale en temps réel, prête à l'emploi.</b><br>
  Un seul fichier Python. Zéro cloud. Toutes les fonctionnalités incluses.
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> · <a href="README_zh.md">🇨🇳 中文</a> · <a href="README_ja.md">🇯🇵 日本語</a> · <a href="README_ko.md">🇰🇷 한국어</a> · <a href="README_es.md">🇪🇸 Español</a> · <b>🇫🇷 Français</b> · <a href="README_de.md">🇩🇪 Deutsch</a> · <a href="README_pt.md">🇧🇷 Português</a> · <a href="README_ru.md">🇷🇺 Русский</a>
</p>

<p align="center">
  <img src="screenshot.png" width="720" alt="FunASR Live UI — dark tech theme">
</p>

---

## Pourquoi FunASR Live ?

Les outils de transcription en temps réel se divisent en deux catégories :

| | API Cloud | Apps Bureau | **FunASR Live** |
|---|---|---|---|
| Confidentialité | ❌ Audio envoyé aux serveurs | ✅ Local | ✅ **100% local, sans réseau** |
| Coût | ❌ Tarification à la minute | 💰 Achat unique | 🆓 **Gratuit à vie** |
| Latence | ⚠️ 1-3 secondes | ✅ Temps réel | ✅ **SSE push, <100ms** |
| Langues | ✅ 50+ | ⚠️ Limité | ✅ **Détection auto 20+ langues** |
| Export sous-titres | ⚠️ Outil supplémentaire | ⚠️ Format verrouillé | ✅ **SRT en un clic** |
| Enregistrement audio | ❌ Non | ✅ Oui | ✅ **Bouton pour sauver en WAV** |
| Résumé IA | ⚠️ Coût API supplémentaire | ❌ Rare | ✅ **Intégré (Ollama)** |
| Personnalisation | ❌ Code fermé | ❌ Code fermé | ✅ **Code complet, 20 thèmes** |
| Déploiement | N/A | Installateur | 🚀 **Un seul fichier `.py`** |

**L'équilibre parfait :** fonctionnalités pro d'une API cloud + confidentialité d'une app locale + un fichier Python modifiable.

---

## ✨ Fonctionnalités

### 🎤 Transcription en temps réel
Parlez → le texte apparaît instantanément. Basé sur **Alibaba SenseVoiceSmall** + VAD + modèle de ponctuation. Détection automatique de la langue ou verrouillage sur une seule.

### ⚡ Push temps réel SSE
Pas de polling. Pas de rechargement. **Server-Sent Events** envoie le texte au navigateur avec une latence <100ms.

### 📥 Export de sous-titres SRT
Un clic (ou touche `S`) télécharge un fichier `.srt` standard. Utilisable directement dans Premiere, DaVinci Resolve, etc.

### 🎙️ Enregistrement audio WAV
Activer l'enregistrement → tout l'audio du micro est sauvegardé en `.wav` sur le bureau. Désactiver → en-tête réparé, fichier prêt.

### 🧠 Résumé IA (Ollama)
Si [Ollama](https://ollama.com) est lancé, l'IA génère automatiquement :
- **Carte mentale** — arbre visuel des sujets
- **Points clés** — liste structurée
- **Citations** — meilleures phrases textuelles

### 🌍 Traduction en temps réel
Langue A transcrite → traduite instantanément en langue B. 20+ langues disponibles.

### 🎨 20 thèmes
Pas seulement le mode sombre. **20 thèmes soignés** — cyber green, neon night, midnight ink, minimal white, warm paper, et plus.

---

## 🚀 Démarrage rapide

```bash
pip install funasr deep-translator numpy
# Optionnel : installer Ollama pour le résumé IA
brew install ollama && ollama pull qwen2.5:14b
python3 funasr_live.py
open http://localhost:8765
```

Première exécution : téléchargement d'environ 400 Mo de modèles ASR (mis en cache).

---

## ⌨️ Raccourcis

| Touche | Action |
|--------|--------|
| `Space` | Pause/Reprendre |
| `S` | Télécharger SRT |
| `R` | Activer l'enregistrement |
| `1-4` | Changer d'onglet |

---

## 📡 API

| Endpoint | Description |
|----------|-------------|
| `/events` | Flux SSE (temps réel) |
| `/api` | Dernier résultat (polling) |
| `/config` | Configuration et état |
| `/download/srt` | Télécharger les sous-titres SRT |
| `/toggle_pause` | Micro ON/OFF |
| `/toggle_record` | Enregistrement ON/OFF |
| `/set_lang?mode=fr` | Verrouiller la langue |
| `/set_translate?target=en` | Langue cible de traduction |

---

## 🔧 Configuration

Modifier `CONFIG` en haut de `funasr_live.py` :

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

## 🎯 Cas d'usage

| Scénario | Utilisation |
|----------|------------|
| Notes de réunion | Enregistrer + résumé IA + SRT |
| Création de contenu | Dicter des scripts |
| Apprentissage des langues | Parler + traduction en temps réel |
| Accessibilité | Sous-titres en direct pour présentations |
| Entretiens | Enregistrer WAV + transcription horodatée |
| Sous-titrage vidéo | Générer SRT directement |
| Streaming live | Intégrer l'UI comme superposition de sous-titres |

---

## 📦 Dépendances

```text
funasr >= 1.3.0
deep-translator >= 1.11
numpy >= 1.24
```

Pas de Node.js, Docker ni CUDA. Juste Python + pip.

---

## 📄 Licence

MIT — utilisation, modification et usage commercial libres.

---

<p align="center">
  <sub>Fait avec ❤️ par <a href="https://superk.ai">Mr.K Lab</a> · Utilise <a href="https://github.com/modelscope/FunASR">FunASR</a></sub>
</p>
