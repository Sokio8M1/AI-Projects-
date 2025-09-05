#!/bin/bash
# Auto-activate venv and run assistant.py (Linux/macOS)

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

python3 assistant.py
