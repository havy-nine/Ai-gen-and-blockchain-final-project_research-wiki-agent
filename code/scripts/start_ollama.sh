#!/usr/bin/env bash
set -euo pipefail
export LD_LIBRARY_PATH="$HOME/.local/lib/ollama:${LD_LIBRARY_PATH:-}"
export OLLAMA_MODELS="$HOME/.ollama/models"
export OLLAMA_HOST="127.0.0.1:11434"
exec "$HOME/.local/bin/ollama" serve
