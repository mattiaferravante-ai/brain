Archivia un progetto spostandolo da `Work/Avvale/projects/` a `Work/Avvale/archive/`.

## Argomenti

1. **nome-progetto** — nome della cartella del progetto (es. `piaggio_cdms_india`)
2. **motivo** *(opzionale)* — breve descrizione del motivo (es. "gara persa", "progetto cancellato dal cliente")

Esempi:
- `/archive-project piaggio_cdms_india`
- `/archive-project piaggio_cdms_india "gara persa"`

## Comportamento

### Step 1 — Verifica e intake

1. Verificare che `Work/Avvale/projects/<nome>/` esista
2. Leggere il README del progetto per identificare cliente e stato corrente
3. Se il motivo non è fornito, chiedere:
   - Motivo archivizione: `gara persa` / `progetto cancellato` / `concluso` / `altro`
   - Data archivizione (default: oggi)

### Step 2 — Aggiorna README del progetto

Nel README del progetto (`Work/Avvale/projects/<nome>/README.md`):

- Sostituire il tag di stato con `#archived` (o `#closed` se concluso con successo)
- Aggiungere in cima al file, dopo il titolo, la sezione:

```markdown
> **Archiviato il:** YYYY-MM-DD
> **Motivo:** [motivo]
```

- Aggiornare la sezione `## Timeline` con:
  ```
  - **Stato:** `#archived`  (o `#closed`)
  - **Archiviato il:** YYYY-MM-DD
  - **Motivo:** [motivo]
  ```

### Step 3 — Sposta la cartella con git mv

```bash
git mv Work/Avvale/projects/<nome> Work/Avvale/archive/<nome>
```

Preserva la history git del progetto.

### Step 4 — Aggiorna gli indici

**`Work/Avvale/projects/README.md`:**
- Rimuovere il progetto dalla tabella "Progetti attivi" o "Gare in corso"

**`Work/Avvale/archive/README.md`:**
- Aggiungere il progetto nella tabella "Progetti archiviati":

| Progetto | Cliente | Stato | Motivo | Archiviato |
|----------|---------|-------|--------|------------|
| [[nome]] | [cliente] | `#archived` | [motivo] | YYYY-MM-DD |

### Step 5 — Commit

```bash
git add -A
git commit -m "brain: archive project <nome> — [motivo]"
```

### Step 6 — Conferma

Mostrare riepilogo:
- Progetto spostato da → a
- Stato aggiornato
- Motivo e data archivizione
