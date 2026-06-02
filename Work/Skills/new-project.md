# Skill: new-project

Crea la struttura cartelle per un nuovo progetto all'interno del Brain (Work).

## Trigger

Ogni volta che si vuole creare un nuovo progetto, una nuova sezione, un nuovo cliente, un nuovo engagement Avvale.

## Parametri

- **area:** percorso relativo dentro `Work/` dove creare il progetto (es. `Avvale/projects`, `Clients`)
- **nome:** nome del progetto/cliente (es. `AziendaXYZ`, `MigrazioneCRM`)
- **tipo:** `full` (default) | `minimal`

## Comportamento

### Step 0 — Onboarding (OBBLIGATORIO per tipo `full`)

Prima di creare qualsiasi file, poni queste domande all'utente in un unico messaggio strutturato. Non procedere finché non hai le risposte.

```
Perfetto, creo il progetto <nome>. Prima dimmi:

1. **Cliente** — ragione sociale o nome breve dell'azienda cliente
2. **Tipo progetto** — nuova implementazione / migrazione / personalizzazione / supporto continuativo
3. **Versione Odoo** — es. 16, 17, 18 (Community o Enterprise?)
4. **Moduli coinvolti** — es. Contabilità, Magazzino, Acquisti, CRM, Produzione...
5. **Data inizio** — anche approssimativa (es. "giugno 2026")
6. **Durata stimata** — es. 3 mesi, 6 mesi, ongoing
7. **PM Avvale** — nome del Project Manager interno
8. **Referente cliente** — nome e ruolo del referente lato cliente
9. **Ambienti** — URL prod / staging / dev (anche "da definire")
10. **Note aggiuntive** — vincoli, dipendenze, contesto utile (opzionale)
```

Accetta risposte parziali: se l'utente non sa qualcosa, usa `Da definire` come placeholder.

### Step 1 — Crea struttura

Costruisci il percorso `Work/<area>/<nome>/` e crea le sottocartelle:
- **full:** `AF/`, `UAT/`, `MeetingNotes/`, `TechNotes/`
- **minimal:** solo `README.md`, nessuna sottocartella

### Step 2 — Crea README.md pre-compilato

Usa le risposte dell'onboarding per riempire il README (nessun placeholder vuoto):

```markdown
# <NomeProgetto>

<descrizione sintetica: tipo progetto + cliente + obiettivo principale>

## Stack

- **Odoo:** <versione> (<Community|Enterprise>)
- **Moduli:** <lista moduli>

## Timeline

- **Inizio:** <data inizio>
- **Durata stimata:** <durata>
- **Stato:** `#active`

## Contatti

| Ruolo | Nome |
|-------|------|
| PM Avvale | <PM> |
| Referente cliente | <referente> |

## Ambienti

| Ambiente | URL |
|----------|-----|
| Produzione | <url o "Da definire"> |
| Staging | <url o "Da definire"> |
| Dev | <url o "Da definire"> |

## Sottocartelle

- `AF/` — Analisi Funzionali
- `UAT/` — Test Book e risultati
- `MeetingNotes/` — Verbali meeting
- `TechNotes/` — Note tecniche, workaround, configurazioni
- `PROJECT_SUMMARY.md` — Riepilogo cumulativo: requisiti, decisioni, processi, stakeholders

## Setup Brain

Dopo aver clonato la repo, attiva il Brain con Claude Code:

```
/uploadbrain
```

Crea il symlink `Brain/`, aggiorna `.gitignore` e carica le istruzioni operative.
Richiede che `~/Brain` esista in locale (clonato da GitHub).

## Tag

`#avvale` `#odoo` `#work` `#active`
```

### Step 3 — Crea PROJECT_SUMMARY.md pre-compilato

Copia il template da `Work/Templates/PROJECT_SUMMARY_template.md` e pre-compila:
- Intestazione con nome progetto, cliente, versione Odoo
- Sezione **Stakeholders** con PM e referente cliente già inseriti
- Tutto il resto vuoto, pronto per essere riempito dai `/minute`

### Step 4 — Aggiorna README padre e indici

- Aggiorna `Work/<area>/README.md` aggiungendo il progetto nella sezione Progetti
- Aggiorna `Work/README.md` solo se è una nuova area di primo livello

### Step 5 — Conferma

Mostra il tree della struttura creata e un riepilogo delle info inserite.

## Template README progetto (minimal)

```markdown
# <NomeProgetto>

<!-- descrizione breve -->

## Tag

`#work` `#odoo`
```

## Note

- Usa sempre nomi in CamelCase o kebab-case per le cartelle (es. `AziendaXYZ`, `migrazione-crm`)
- Dopo la creazione, mostra il tree della struttura creata
- Ricorda di fare commit con messaggio: `brain: add project <nome>`
