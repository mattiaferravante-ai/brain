# 🏠 HomeBase

**Tipo:** App personale self-hosted — obiettivo a lungo termine: prodotto vendibile
**Repo:** github.com/mattiferra/homebase
**Notion:** pagina principale con Architecture, Modules, Roadmap, Task Board, Deploy Log, Dev Notes & ADR, Commerciale
**Tag:** #homebase #dev #personal #python #fastapi

---

## Infrastruttura

| Componente | Dettaglio |
|------------|-----------|
| Machine | HP EliteDesk 800 G5 Mini |
| OS | Ubuntu Server 24.04 LTS |
| Runtime | Docker (single container) + Portainer (porta 9000) |
| Database | SQLite 3 — `~/homebase-data/homebase.db` |
| Dev access | VS Code Remote SSH |
| Deploy | `./deploy.sh` → build → stop old → run new |

## Stack applicativo

| Layer | Tech |
|-------|------|
| Backend | Python 3.12, FastAPI 0.111, SQLAlchemy 2.0 |
| AI / LLM | Claude Sonnet via Anthropic SDK |
| Scheduler | APScheduler (notifiche Telegram) |
| Market data | yfinance, feedparser, pdfplumber |
| Frontend | Vanilla JS + Chart.js (SPA single-file) |
| AI Dev Skill | Graphify (knowledge graph dalla codebase) |

---

## Moduli

| Modulo | Descrizione | Potenziale commerciale |
|--------|-------------|----------------------|
| 💰 Finance | Transazioni, budget, categorie, import estratto conto Allianz, report AI mensile, portfolio ETF/azioni con P&L live | 🟢 Alto |
| 📈 Markets Monitor | Prezzi live, Fear & Greed Index, calendario macro, news RSS, report AI | 🟢 Alto |
| 🧠 Graphify | Knowledge graph della codebase via AST statica, query semantiche per Claude Code | 🟢 Alto |
| 🍽️ Meals & Pantry | Piano pasti settimanale AI, dispensa con sezioni, alert scorte basse | 🟡 Medio |
| 🛒 Grocery | Liste spesa multi-lista, suggerimenti da storico, move-to-pantry | 🟡 Medio |
| 📦 Product Catalog | Catalogo prodotti con storico prezzi, auto-link a grocery/pantry | 🟡 Medio |
| ✅ Habits | Abitudini con streak giornaliero | 🟡 Medio |
| 🎯 Quests & XP | Gamification: quest generate da Claude, sistema XP e livelli | 🟡 Medio |
| 💪 Exercise Programs | Programmi allenamento con generazione AI basata su attrezzatura disponibile | 🟡 Medio |
| 🏋️ Equipment | Gestione attrezzatura fitness — input per generazione programmi | 🟡 Medio |
| 📊 Body Metrics | Tracciamento peso, body fat, massa muscolare con grafici | 🟠 Basso-Medio |
| 🏠 Casa Smart | Controllo locale robot Xiaomi, condizionatori, feeder Giacomino (Tuya), LG ThinQ in sviluppo | 🟡 Medio |
| 🧠 Brain | File manager per note Obsidian esposte via API — tree view, viewer MD, editor inline | — |
| 👤 Profile | Dati anagrafici, goal (bulk/cut/maintain), XP/livello | — |
| ⚙️ Settings | Token Telegram Bot, preferenze notifiche | — |
| 🤖 Scheduler | Notifiche Telegram mattino/sera, penalità XP automatiche, level-up alert | — |

---

## Strategia commerciale

**Obiettivo:** costruire un prodotto modulare e solido che possa diventare:
- SaaS multi-tenant (subscription mensile)
- Moduli licenziabili standalone (es. Graphify, Markets Monitor)
- Servizio gestito per utenti non tecnici

**ICP principale:** professionista 25–40 anni, tech-savvy, gestisce da solo finanze/fitness/alimentazione.

**Differenziante chiave:** integrazione tra moduli (es. pasto → lista spesa → dispensa → budget → report AI).

**Prima di multi-tenant:** risolvere autenticazione (oggi single-user, nessun login).

---

## Note tecniche

- Migrazioni gestite con ALTER TABLE idempotenti in `app/database.py` — no Alembic
- Volume `~/homebase-data` persiste SQLite tra deploy
- Cache-busting automatico CSS/JS tramite build timestamp
- Il modulo Brain monta `~/Brain` come volume Docker (`~/Brain:/app/brain-data`)

---

**Vedi anche:** [[2026|Obiettivi 2026]] | [[HomeBase/PROJECT_WORKFLOW|Workflow HomeBase]]
