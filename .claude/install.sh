#!/bin/bash
# install.sh — Installa il Brain e i comandi Claude Code su una nuova macchina
# Uso: bash ~/Brain/.claude/install.sh
# Prerequisiti: git, Claude Code CLI installato

set -e

BRAIN_DIR="$HOME/Brain"
CLAUDE_DIR="$HOME/.claude"
COMMANDS_DIR="$CLAUDE_DIR/commands"
SETTINGS="$CLAUDE_DIR/settings.json"

echo "=== Brain Install ==="
echo ""

# 1. Clone Brain se non esiste
if [ ! -d "$BRAIN_DIR" ]; then
  echo "► Clono il Brain da GitHub..."
  git clone https://github.com/mattiferra/brain.git "$BRAIN_DIR"
else
  echo "✓ Brain già presente in $BRAIN_DIR"
  echo "► Pull ultime modifiche..."
  cd "$BRAIN_DIR" && git pull origin main --quiet
fi

# 2. Crea ~/.claude/commands/ se non esiste
mkdir -p "$COMMANDS_DIR"

# 3. Copia i comandi Brain in ~/.claude/commands/
echo "► Installo comandi Claude Code..."
cp "$BRAIN_DIR/.claude/commands/uploadbrain.md" "$COMMANDS_DIR/uploadbrain.md"
cp "$BRAIN_DIR/.claude/commands/pullbrain.md"   "$COMMANDS_DIR/pullbrain.md"
echo "  ✓ /uploadbrain"
echo "  ✓ /pullbrain"

# 4. Rendi eseguibile lo script di sync
chmod +x "$BRAIN_DIR/.claude/sync-brain.sh"

# 5. Aggiungi hook PostToolUse a ~/.claude/settings.json (se non già presente)
if [ ! -f "$SETTINGS" ]; then
  echo "► Creo settings.json..."
  cat > "$SETTINGS" << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/Brain/.claude/sync-brain.sh"
          }
        ]
      }
    ]
  }
}
EOF
elif ! grep -q "sync-brain" "$SETTINGS"; then
  echo "► ATTENZIONE: aggiungi manualmente l'hook sync-brain a $SETTINGS"
  echo "  Vedi Brain/.claude/hook-snippet.json per il frammento da aggiungere"
fi

echo ""
echo "=== Setup completato ==="
echo ""
echo "Comandi disponibili in Claude Code:"
echo "  /uploadbrain  — collega il Brain a un progetto (o pull se già presente)"
echo "  /pullbrain    — pull delle ultime modifiche del Brain"
echo ""
echo "Sync automatico: ogni Write/Edit triggera sync-brain.sh → git commit + push"
