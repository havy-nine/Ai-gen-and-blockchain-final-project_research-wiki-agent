#!/bin/sh
set -eu
VAULT="/home/cheon/Documents/workspace/ai_blockchain/0608_ob"
HOME_NOTE="$VAULT/Home.md"
if [ ! -d "$VAULT/.obsidian" ]; then
  echo "Vault not found: $VAULT"
  echo "Run: python demo/build_obsidian_vault.py --wiki-dir output/wiki_cvpr2026_random10 --vault-dir 0608_ob --min-source-files 10"
  exit 1
fi
if [ ! -f "$HOME_NOTE" ]; then
  echo "Home note not found: $HOME_NOTE"
  exit 1
fi
echo "Opening 0608_ob Obsidian vault: $VAULT"
echo "Expected Home note: $HOME_NOTE"
URI=$(python - <<'PYURI'
from pathlib import Path
from urllib.parse import quote
home_note = Path('/home/cheon/Documents/workspace/ai_blockchain/0608_ob/Home.md')
print('obsidian://open?path=' + quote(str(home_note), safe=''))
PYURI
)
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URI" >/dev/null 2>&1 && exit 0
fi
if [ -x "$HOME/.local/bin/obsidian" ]; then
  "$HOME/.local/bin/obsidian" "$HOME_NOTE" >/dev/null 2>&1 && exit 0
fi
if command -v obsidian >/dev/null 2>&1; then
  obsidian "$HOME_NOTE" >/dev/null 2>&1 && exit 0
fi
echo "Obsidian app not found. Open this folder manually with Open folder as vault:"
echo "$VAULT"
