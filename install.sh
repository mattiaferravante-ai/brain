#!/bin/bash
# Brain — script di installazione
# Eseguire dopo aver clonato la repo in ~/Brain

set -e

BRAIN_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"

echo "==> Brain setup da: $BRAIN_DIR"

# Verifica che la repo sia in ~/Brain
if [ "$BRAIN_DIR" != "$HOME/Brain" ]; then
  echo "ATTENZIONE: la repo non è in ~/Brain (trovata in $BRAIN_DIR)."
  echo "Alcuni comandi Claude potrebbero non funzionare correttamente."
  echo ""
fi

# Verifica Claude Code installato
if ! command -v claude &> /dev/null; then
  echo "ERRORE: Claude Code non trovato."
  echo "Installalo da: https://claude.ai/code"
  exit 1
fi

# Copia comandi globali Claude
echo "==> Copio comandi Claude globali in $CLAUDE_COMMANDS_DIR..."
mkdir -p "$CLAUDE_COMMANDS_DIR"
cp "$BRAIN_DIR/.claude/commands/pullbrain.md" "$CLAUDE_COMMANDS_DIR/"
cp "$BRAIN_DIR/.claude/commands/uploadbrain.md" "$CLAUDE_COMMANDS_DIR/"
echo "    /pullbrain e /uploadbrain disponibili globalmente."

echo ""
echo "Setup completato."
echo ""
echo "Comandi disponibili ovunque:   /pullbrain  /uploadbrain"
echo "Comandi disponibili in ~/Brain: /minute  /new-project  /generate-cv"
echo ""
echo "Per usare il Brain in un altro progetto, aprilo con Claude Code ed esegui /uploadbrain"
