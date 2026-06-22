Esegui il setup o l'aggiornamento del Brain nel progetto corrente.

Prima controlla se il symlink `Brain` esiste già:

```bash
ls -la Brain 2>/dev/null
```

---

## Caso A — Brain già presente (aggiornamento)

Se il symlink esiste, esegui il pull e avvisa l'utente di cosa è cambiato:

```bash
cd ~/Brain && git pull origin main
```

- Se il pull porta modifiche: mostra la lista dei file aggiornati e di' esattamente cosa è cambiato (es. "aggiornati 3 file: Work/PROFESSIONAL_PROFILE.md, Personal/Goals/2026.md, ...")
- Se è già aggiornato: di' "Brain già aggiornato, nessuna modifica."

Poi esegui la sezione **Sync Skills** qui sotto.

---

## Caso B — Prima installazione

Se il symlink non esiste, esegui questi step:

### Step 1 — Symlink
```bash
ln -sf ~/Brain ./Brain
```

### Step 2 — .gitignore
```bash
grep -qxF 'Brain' .gitignore 2>/dev/null || echo 'Brain' >> .gitignore
```

### Step 3 — CLAUDE.md del progetto

Aggiungi questa sezione al `CLAUDE.md` del progetto (crealo se non esiste):

```
## Brain — Memoria personale

Il Brain di Mattia è disponibile nella cartella `Brain/`.
Leggi `Brain/CLAUDE.md` per le istruzioni operative.
Leggi `Brain/Personal/PERSONAL_PROFILE.md` per il profilo personale.
Leggi `Brain/Work/PROFESSIONAL_PROFILE.md` per il profilo professionale.
```

### Step 4 — Sync Skills (vedi sezione sotto)

### Step 5 — Conferma
```bash
ls Brain/
```

Avvisa: "Brain installato. Symlink creato, .gitignore aggiornato, istruzioni aggiunte al CLAUDE.md, skill sincronizzate."

---

## Sync Skills (eseguito sempre — Caso A e Caso B)

Sincronizza automaticamente le skill e i comandi dal Brain a Claude Code.

### 1. Skill con cartella (`Brain/Work/Skills/<name>/SKILL.md`)

Per ogni cartella in `Brain/Work/Skills/` che contiene `SKILL.md`, copia o aggiorna in `~/.claude/skills/<name>/`:

```bash
for dir in Brain/Work/Skills/*/; do
  name=$(basename "$dir")
  if [ -f "${dir}SKILL.md" ]; then
    cp -r "$dir" ~/.claude/skills/"$name"
    echo "Skill aggiornata: $name"
  fi
done
```

### 2. Skill file singolo (`Brain/Work/Skills/<name>.md`)

Per ogni file `.md` singolo (non cartella) in `Brain/Work/Skills/`, crea `~/.claude/skills/<name>/SKILL.md`:

```bash
for f in Brain/Work/Skills/*.md; do
  [ -f "$f" ] || continue
  name=$(basename "$f" .md)
  mkdir -p ~/.claude/skills/"$name"
  cp "$f" ~/.claude/skills/"$name"/SKILL.md
  echo "Skill aggiornata: $name"
done
```

### 3. Commands (`Brain/.claude/commands/<name>.md`)

Copia tutti i comandi del Brain in `~/.claude/commands/`:

```bash
cp Brain/.claude/commands/*.md ~/.claude/commands/
echo "Comandi aggiornati."
```

### 4. Riepilogo finale

Mostra le skill e i comandi installati:

```bash
echo "=== Skills ===" && ls ~/.claude/skills/
echo "=== Commands ===" && ls ~/.claude/commands/
```
