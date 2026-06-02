# Skill: minute

Genera il verbale strutturato di una riunione a partire da una trascrizione grezza.

## Trigger

Ogni volta che si parla di: verbale, meeting notes, minute di riunione, trascrizione riunione, recap meeting, note meeting.

## Parametri

- **progetto:** percorso relativo dentro `Work/` (es. `Avvale/projects/ClienteRossi`)
- **trascrizione:** testo incollato direttamente o path a file `.txt`
- **data:** data della riunione (default: oggi)
- **tipo:** `interno` | `cliente` (default: `cliente`) — influenza il tono del verbale

## Comportamento

### Step 1 — Analisi trascrizione

Dalla trascrizione estrai:

| Campo | Istruzioni |
|-------|-----------|
| **Data** | Cerca date esplicite, altrimenti usa il parametro data |
| **Partecipanti** | Nomi citati, ruoli se disponibili |
| **Argomenti trattati** | Lista dei topic principali discussi |
| **Decisioni prese** | Solo decisioni formali/concordate, non opinioni |
| **Action items** | Chi fa cosa entro quando — se la deadline non è esplicita, lascia TBD |
| **Punti aperti / blocchi** | Questioni irrisolte o bloccanti emersi |
| **Prossimo meeting** | Se citato |

### Step 2 — Genera il verbale

Salva in `Work/<progetto>/MeetingNotes/YYYY-MM-DD_meeting.md` con questa struttura:

```markdown
# Meeting — <data>

**Progetto:** <nome progetto>  
**Tipo:** interno | cliente  
**Partecipanti:** <lista>  

---

## Argomenti trattati

- ...

## Decisioni prese

- ...

## Action items

| # | Azione | Owner | Deadline | Stato |
|---|--------|-------|----------|-------|
| 1 | ...    | ...   | ...      | Open  |

## Punti aperti

- ...

## Prossimo meeting

<data e obiettivo, oppure "Da definire">
```

### Step 3 — Aggiorna PROJECT_SUMMARY.md

Apri `Work/<progetto>/PROJECT_SUMMARY.md`. Se non esiste, crealo dal template in `Work/Templates/PROJECT_SUMMARY_template.md`.

Per ogni sezione, **aggiungi in append** le nuove informazioni emerse dal meeting corrente — non sovrascrivere mai le righe esistenti:

| Sezione PROJECT_SUMMARY | Cosa aggiungere da questo meeting |
|------------------------|----------------------------------|
| `## Requisiti emersi` | Nuovi requisiti o vincoli espressi |
| `## Decisioni chiave` | Decisioni formali prese, con data e link `[[YYYY-MM-DD_meeting]]` |
| `## Processi da coprire` | Processi AS-IS o TO-BE menzionati |
| `## Punti aperti` | Nuovi blocchi o issue aperti; chiudi con `~~testo~~` quelli risolti |
| `## Stakeholders` | Nuovi partecipanti con nome, ruolo, azienda |

Regole append:
- Ogni riga nuova termina con `→ [[YYYY-MM-DD_meeting]]` come riferimento alla fonte
- Non duplicare righe già presenti
- Se un punto aperto viene risolto in questo meeting, barralocol con `~~testo~~` e aggiungi `✓ risolto [[YYYY-MM-DD_meeting]]`

### Step 4 — Aggiorna il README del progetto

Apri `Work/<progetto>/README.md` e aggiorna (o crea) la sezione `## Ultimo meeting`:

```markdown
## Ultimo meeting

**Data:** YYYY-MM-DD  
**Decisioni chiave:** <sintesi 1-2 righe>  
**Action items aperti:** N  
→ [[YYYY-MM-DD_meeting]]
```

Se la sezione esiste già, sostituiscila con i nuovi dati.

### Step 5 — Output a schermo

Mostra all'utente:
1. Il verbale completo generato
2. La lista action items in formato checklist
3. Riepilogo di cosa è stato aggiunto al PROJECT_SUMMARY (quante righe per sezione)
4. Conferma del README aggiornato

## Note

- Non inventare decisioni o owner non presenti nella trascrizione — se un'informazione è ambigua, segnalala con `[?]`
- Se la trascrizione è in inglese, genera il verbale in italiano salvo richiesta esplicita
- Il file `.md` del verbale deve essere wikilinked dal README con `[[YYYY-MM-DD_meeting]]`
- Se `MeetingNotes/` non esiste nella cartella progetto, creala prima di salvare
