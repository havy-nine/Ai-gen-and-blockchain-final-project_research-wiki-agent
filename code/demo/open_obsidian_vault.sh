#!/bin/sh
set -eu
VAULT="/home/cheon/Documents/workspace/ai_blockchain/obsidian_workspace/obsidian_vault"
if [ ! -d "$VAULT/.obsidian" ]; then
  echo "Vault not found: $VAULT"
  echo "Run: python demo/build_obsidian_vault.py"
  exit 1
fi
URI=$(python - <<'PYURI'
from pathlib import Path
from urllib.parse import quote
vault = Path('/home/cheon/Documents/workspace/ai_blockchain/obsidian_workspace/obsidian_vault')
print('obsidian://open?path=' + quote(str(vault), safe=''))
PYURI
)
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URI" >/dev/null 2>&1 && exit 0
fi
if [ -x "$HOME/.local/bin/obsidian" ]; then
  "$HOME/.local/bin/obsidian" "$VAULT" >/dev/null 2>&1 && exit 0
fi
if command -v obsidian >/dev/null 2>&1; then
  obsidian "$VAULT" >/dev/null 2>&1 && exit 0
fi
echo "Obsidian app not found. Open this folder manually:"
echo "$VAULT"
