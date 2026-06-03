# Project Workflow — Standard Rules

Regole standard da applicare a **qualsiasi progetto personale** gestito con Claude Code.
Coprono tre sistemi sempre da tenere sincronizzati: **Graphify**, **GitHub**, **Notion**.

Per le regole specifiche di un progetto, vedi il workflow dedicato in `Dev/NomeProgetto/PROJECT_WORKFLOW.md`.

---

## 1. Graphify — Knowledge Graph

### Quando inizializzare
- All'inizio di ogni nuovo progetto, esegui `/graphify` per costruire il grafo iniziale.
- Se `graphify-out/` non esiste, costruiscilo prima di rispondere a qualsiasi domanda sulla codebase.

### Quando aggiornare
- **Dopo ogni modifica al codice** che aggiunge/modifica/rimuove file sorgente: `graphify update .`
- Nessun costo API — è analisi AST statica.

### Come usarlo
- Per domande sulla codebase: `graphify query "<domanda>"` (non grep manuale)
- Per relazioni tra entità: `graphify path "<A>" "<B>"`
- Per concetti specifici: `graphify explain "<concetto>"`
- `GRAPH_REPORT.md` solo per architettura broad — altrimenti usa query/path/explain

---

## 2. GitHub — Versioning

### Quando creare la repo
- All'inizio di ogni nuovo progetto, verifica che esista una repo GitHub.
- Se non esiste: creala (privata di default) con `gh repo create`.

### Quando fare commit + push
- Dopo **ogni modifica significativa**: aggiunta feature, fix, refactor, aggiornamento config.
- Commit message: formato `<tipo>: <descrizione breve>` (feat / fix / refactor / chore / docs).
- Fare sempre push su `origin main` (o branch corrente).
- Non commitare: `.env`, credenziali, file generati (rispettare `.gitignore`).

---

## 3. Notion — Knowledge Base

### Struttura standard workspace

Ogni progetto ha una pagina root Notion con questa struttura fissa:

```
🏠 [Nome Progetto]                  ← root page: overview + stack + link sezioni
├── 🏗️ Architecture                 ← pagina: infra, stack, Docker, porte, DB, deploy
├── 📦 Modules                      ← pagina: elenco moduli con funzionalità, route, servizi
├── 🚀 Deploy Log                   ← DATABASE: storico deploy
├── 🗺️ Roadmap                      ← DATABASE: feature pianificate
├── 🛠️ Task Board                   ← DATABASE: task per Claude Code e sviluppo
├── 📋 Dev Notes & ADR              ← DATABASE: decisioni tecniche e note
└── 💰 Commerciale                  ← pagina: potenziale mercato e strategia
```

---

### Schemi database

#### 🚀 Deploy Log
| Campo | Tipo | Valori |
|---|---|---|
| Component | Title | nome modulo / feature / infra |
| Date | Date | data deploy |
| Version | Text | tag o hash commit (es. `v1.2.0` / `49488ad`) |
| Type | Select | `New Feature` / `Update` / `Fix` / `Migration` / `Infra` |
| Status | Select | `✅ Success` / `❌ Failed` / `🔄 In Progress` |
| Description | Text | cosa è stato deployato |
| Notes | Text | problemi riscontrati, rollback, ecc. |

#### 🗺️ Roadmap
| Campo | Tipo | Valori |
|---|---|---|
| Feature | Title | nome feature |
| Priority | Select | `🔴 Alta` / `🟡 Media` / `🟢 Bassa` |
| Effort | Select | `S` / `M` / `L` / `XL` |
| Status | Select | `Idea` / `Planned` / `In Progress` / `Done` / `Dropped` |
| Commercial | Checkbox | flag potenziale commerciale |
| Module | Text | modulo coinvolto |
| Notes | Text | contesto |

#### 🛠️ Task Board
| Campo | Tipo | Valori |
|---|---|---|
| Task | Title | descrizione breve |
| Status | Select | `Backlog` / `Ready for Claude` / `In Progress` / `Done` |
| Priority | Select | `🔴 Alta` / `🟡 Media` / `🟢 Bassa` |
| Assignee | Select | `Claude Code` / `Mattia` / `Both` |
| Context for Claude | Text | prompt/contesto completo da passare a Claude Code |
| Output expected | Text | risultato atteso (file, test, funzione, ecc.) |

#### 📋 Dev Notes & ADR
| Campo | Tipo | Valori |
|---|---|---|
| Title | Title | titolo decisione/nota |
| Type | Select | `ADR` / `Note` / `Bug` / `Decision` |
| Date | Date | data |
| Content | Text | contenuto esteso |

---

### Quando aggiornare ogni pagina

| Evento | Pagine da aggiornare |
|---|---|
| Nuova feature / modulo aggiunto | **Modules** (aggiungi/aggiorna sezione), **Deploy Log** (nuova riga) |
| Feature aggiornata o modificata | **Modules** (aggiorna sezione), **Deploy Log** (nuova riga) |
| Deploy eseguito (qualsiasi tipo) | **Deploy Log** (nuova riga obbligatoria) |
| Cambia stack / infrastruttura / DB | **Architecture** |
| Cambia stack anche nella root | **🏠 Root** (tabella Stack) |
| Decisione tecnica importante | **Dev Notes & ADR** (nuova riga) |
| Feature con potenziale commerciale | **Commerciale** (aggiorna tabella moduli) |
| Nuova feature pianificata | **Roadmap** (nuova riga) |
| Task assegnato a Claude Code | **Task Board** (nuova riga con Context for Claude) |

---

### Come compilare il Deploy Log

```
Component  → nome del modulo o area (es. "Finance", "Meals & Pantry", "Infra")
Date       → data odierna
Version    → hash commit git (git rev-parse --short HEAD)
Type       → New Feature / Update / Fix / Migration / Infra
Status     → ✅ Success (o 🔄 In Progress se non ancora verificato)
Description → cosa è cambiato in 1-2 righe
Notes      → eventuali problemi, migration eseguite, warning
```

---

### Formato sezione Modules

```markdown
## [Emoji] [Nome Modulo]

[Descrizione breve in una riga]

**Funzionalità:**
- punto 1
- punto 2

**Route:** `GET/POST /api/...`

**Servizi:** `nome_servizio.py` (descrizione)
```

---

## 4. Ordine operazioni standard (nuova feature)

1. Scrivi / modifica il codice
2. `graphify update .` — aggiorna knowledge graph
3. `git add <files> && git commit -m "feat: ..." && git push` — versioning
4. Riavvia / verifica l'app (segui il workflow specifico del progetto)
5. Aggiorna **Notion**: Modules, Deploy Log, Architecture (se cambia stack), Commerciale (se potenziale)

---

## 5. Come creare un workflow specifico per progetto

Crea `Dev/NomeProgetto/PROJECT_WORKFLOW.md` con le seguenti sezioni. Includi solo quelle rilevanti al progetto.

### Sezioni da documentare

**Runtime e avvio**
- Come si avvia l'app (comando, script, Docker, process manager)
- Come si riavvia dopo una modifica al codice
- Hot reload disponibile? Quando serve rebuild/restart manuale?

**Database e migrazioni**
- Quale DB? (SQLite, Postgres, MongoDB, ecc.)
- ORM e strategia di migrazione (Alembic, script manuale, auto-create)
- Pattern obbligatorio quando si modifica lo schema (ALTER TABLE, rollback, verifica)
- Eventuali istanze multiple dello stesso DB (es. DB per-utente)

**Comandi frequenti**
- Build, test, linting, deploy — i comandi esatti del progetto

**Quirks e gotchas**
- Comportamenti non ovvi da ricordare
- Pattern obbligatori che non emergono leggendo il codice
- Errori comuni e come evitarli

**Ordine operazioni (nuova feature)**
- Versione estesa dell'ordine standard, con i passi aggiuntivi specifici del progetto

### Template base

```markdown
# Project Workflow — [NomeProgetto]

> Regole standard: [[../PROJECT_WORKFLOW]]
> Overview progetto: [[../NomeProgetto]]

---

## Runtime e avvio

## DB e migrazioni

## Comandi frequenti

## Quirks e gotchas

## Ordine operazioni (nuova feature)
```

---

## Note operative

- Usare sempre i tool MCP Notion (`notion-update-page`, `notion-fetch`, `notion-search`) per aggiornare le pagine.
- Per il Deploy Log usare `notion-create-pages` sul database corretto (recuperare l'ID con `notion-search`).
- Il commit hash si ottiene con `git rev-parse --short HEAD`.
- Non aspettare che l'utente chieda di aggiornare Notion o GitHub — farlo automaticamente dopo ogni modifica.
