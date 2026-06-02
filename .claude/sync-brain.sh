#!/bin/bash
# Sync automatico del Brain su GitHub
# Chiamato dall'hook PostToolUse dopo ogni Write/Edit

BRAIN_DIR="$HOME/Brain"

cd "$BRAIN_DIR" || exit 0

# Nessuna modifica? Esci silenziosamente
if [ -z "$(git status --porcelain)" ]; then
  exit 0
fi

# Commit e push
git add -A
git commit -m "sync: $(date '+%Y-%m-%d %H:%M')" --quiet
git push origin main --quiet 2>&1

exit 0
