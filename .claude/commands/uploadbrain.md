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

Fermati qui, non eseguire il Caso B.

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

### Step 4 — Conferma
```bash
ls Brain/
```

Avvisa: "Brain installato. Symlink creato, .gitignore aggiornato, istruzioni aggiunte al CLAUDE.md."
