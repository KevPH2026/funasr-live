#!/bin/bash
# FunASR Live — real-time ASR with 7 features, 20 themes
pip install -q funasr deep-translator numpy 2>/dev/null
python3 funasr_live.py
