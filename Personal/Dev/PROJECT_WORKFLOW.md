# Project Workflow — Standard Rules

Regole globali da applicare a **qualsiasi progetto** gestito con Claude Code.
Coprono tre sistemi sempre da tenere sincronizzati: **Graphify**, **GitHub**, **Notion**.

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

Ogni volta che viene deployata una modifica (anche piccola), crea una nuova riga nel database Deploy Log con:

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

### Aggiornamento pagina Modules

Ogni sezione nella pagina Modules segue questo formato standard:

```markdown
## [Emoji] [Nome Modulo]

[Descrizione breve in una riga]

**Funzionalità:**
- punto 1
- punto 2
...

**Route:** `GET/POST /api/...`

**Servizi:** `nome_servizio.py` (descrizione)
```

---


## 4. Database Migration (homebase / appSolo)

### Regola fondamentale

SQLAlchemy crea automaticamente **nuove tabelle** al riavvio, ma **non aggiunge colonne** a tabelle già esistenti.

**Ogni volta che si aggiunge una colonna a un modello esistente in `models.py`**, eseguire subito la migration su tutti i DB utente prima di fare commit.

### DB utente

I DB sono per-utente in `/app/data/`:
- Pattern: `homebase_*.db` (es. `homebase_mattia.db`, `homebase_Paolo.db`, `homebase_Simone.db`)
- **Non** `homebase.db` (template vuoto — ignorarlo)

### Comando migration — nuova colonna

```bash
docker exec homebase python3 -c "
import sqlite3, glob
dbs = glob.glob('/app/data/homebase_*.db')
for path in dbs:
    try:
        conn = sqlite3.connect(path)
        cols = [r[1] for r in conn.execute('PRAGMA table_info(NOME_TABELLA)')]
        if 'NOME_COLONNA' not in cols:
            conn.execute('ALTER TABLE NOME_TABELLA ADD COLUMN NOME_COLONNA TIPO DEFAULT VALORE')
            conn.commit()
            print(f'migrated: {path}')
        else:
            print(f'already ok: {path}')
        conn.close()
    except Exception as e:
        print(f'ERROR {path}: {e}')
"
```

### Comando migration — nuova tabella (se non auto-creata)

```bash
docker exec homebase python3 -c "
import sqlite3, glob
dbs = glob.glob('/app/data/homebase_*.db')
for path in dbs:
    conn = sqlite3.connect(path)
    tables = [r[0] for r in conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")]
    if 'NOME_TABELLA' not in tables:
        conn.execute('CREATE TABLE NOME_TABELLA (id INTEGER PRIMARY KEY AUTOINCREMENT, ...)')
        conn.commit()
        print(f'created: {path}')
    conn.close()
"
```

### Dopo la migration — forzare hot-reload

```bash
touch /home/mattia/homelab/appSolo/app/routes/finance.py
docker logs homebase 2>&1 | tail -5   # verifica: nessun OperationalError
```

### Ordine operazioni quando si tocca models.py

1. Aggiungi colonna/tabella in `models.py`
2. Aggiorna Pydantic models e route
3. **Migration su tutti i DB** (pattern sopra)
4. Hot-reload + verifica log
5. Poi commit + push

---
## Ordine operazioni standard (nuova feature)

1. Scrivi / modifica il codice
2. Se modificato `models.py`: **esegui migration DB** (vedi sezione 4)
3. `graphify update .` — aggiorna knowledge graph
3. `git add <files> && git commit -m "feat: ..." && git push` — versioning
4. Riavvia l'app se necessario
5. Aggiorna **Notion**:
   - Modules (sezione del modulo coinvolto)
   - Deploy Log (nuova riga)
   - Architecture (solo se cambiano stack/infra/DB)
   - Commerciale (solo se feature ha potenziale)

---

## Note operative

- Usare sempre i tool MCP Notion (`notion-update-page`, `notion-fetch`, `notion-search`) per aggiornare le pagine — mai descrivere solo cosa fare.
- Per il Deploy Log usare `notion-create-pages` sul database corretto (recuperare l'ID con `notion-search`).
- Il commit hash si ottiene con `git rev-parse --short HEAD`.
- Non aspettare che l'utente chieda di aggiornare Notion o GitHub — farlo automaticamente dopo ogni modifica.
