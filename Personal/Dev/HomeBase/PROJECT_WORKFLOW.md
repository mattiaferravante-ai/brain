# Project Workflow — HomeBase

> Regole standard: [[../PROJECT_WORKFLOW]]
> Overview progetto: [[../HomeBase]]

---

## Runtime e avvio

| | |
|--|--|
| Container | `homebase` (docker compose) |
| Avvio | `cd /home/mattia/homelab/appSolo && docker compose up -d` |
| Hot reload | Sì — uvicorn rileva modifiche in `./app/` automaticamente (~2s) |
| Logs | `docker logs -f homebase` |
| Rebuild | Solo se cambia `requirements.txt` o `Dockerfile`: `./deploy.sh --build` |

**Regola:** dopo ogni modifica a `./app/`, l'app si riavvia da sola. Nessun restart manuale necessario, salvo errori nei log.

Volumi montati:
- `./app/` → `/app/app` (codice, hot reload)
- `~/homebase-data/` → `/app/data` (dati SQLite persistenti)

---

## DB e migrazioni

### Struttura
- SQLite per-utente in `/app/data/homebase_*.db`
- Pattern: `homebase_*.db` (es. `homebase_mattia.db`, `homebase_Paolo.db`)
- **Ignorare** `homebase.db` — è il template vuoto

### Regola fondamentale
SQLAlchemy crea automaticamente **nuove tabelle** al riavvio, ma **non aggiunge colonne** a tabelle esistenti.  
Ogni volta che si aggiunge una colonna in `models.py`, eseguire subito la migration su **tutti** i DB utente prima di fare commit.

### Migration — nuova colonna

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

### Migration — nuova tabella (se non auto-creata)

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

### Verifica post-migration

```bash
touch /home/mattia/homelab/appSolo/app/routes/finance.py   # forza hot-reload
docker logs homebase 2>&1 | tail -5                         # nessun OperationalError atteso
```

---

## Ordine operazioni (nuova feature)

1. Scrivi / modifica il codice
2. Se modificato `models.py`: **migration DB** su tutti `homebase_*.db` (pattern sopra)
3. `graphify update .`
4. `git add <files> && git commit -m "feat: ..." && git push`
5. Verifica hot-reload nei log (`docker logs -f homebase`, attendi ~2s)
6. Aggiorna Notion: Modules, Deploy Log, Architecture (se cambia stack), Commerciale (se potenziale)

---

## Quirks e gotchas

- SQLAlchemy non fa ALTER TABLE automatico → migration manuale obbligatoria per nuove colonne
- I DB sono **per-utente** — migrarli tutti con `glob.glob('homebase_*.db')`, non solo uno
- Hot reload attivo: nessun rebuild necessario per modifiche a `./app/`
- Rebuild obbligatorio solo per `requirements.txt` o `Dockerfile`
- Il volume `~/homebase-data/` è persistente tra deploy — i dati non vanno persi con `docker compose down`
