# 🧠 Brain — Second Brain di Mattia Ferravante

Questo è il tuo sistema di knowledge management personale, ottimizzato per VSCode + Obsidian.

## Setup — Prima installazione

Dopo aver clonato la repo in `~/Brain`:

```bash
# 1. Rendi eseguibile ed esegui lo script di installazione
chmod +x ~/Brain/install.sh && ~/Brain/install.sh
```

Lo script fa tutto: copia i comandi Claude globali e verifica i prerequisiti.

**Oppure manualmente:**

```bash
# Copia i comandi Claude globali (disponibili in tutti i progetti)
mkdir -p ~/.claude/commands
cp ~/Brain/.claude/commands/pullbrain.md ~/.claude/commands/
cp ~/Brain/.claude/commands/uploadbrain.md ~/.claude/commands/
```

I comandi rimanenti (`/minute`, `/new-project`, `/generate-cv`, ecc.) sono già attivi quando Claude Code è aperto nella cartella `~/Brain`.

Per usare il Brain in un altro progetto, aprilo con Claude Code ed esegui `/uploadbrain`.

---

## Struttura

```
Brain/
├── Work/               → Progetti Odoo, clienti, deliverable
│   ├── Avvale/         → Progetti Avvale (projects/ + archive/)
│   ├── Clients/        → Una cartella per cliente esterno
│   ├── Templates/      → Template riutilizzabili (AF, UAT, meeting notes)
│   ├── Skills/         → Skill Claude per produzione deliverable
│   ├── CV/             → CV aggiornati (IT + EN)
│   └── PROFESSIONAL_PROFILE.md → Profilo professionale completo
│
└── Learning/           → Studio e crescita professionale
    ├── Odoo/           → Gotchas, breaking changes, pattern custom — la fonte unica
    ├── Tech/           → Python, SQL, Docker, ERP patterns
    ├── Books/          → Note da libri tecnici
    └── Courses/        → Note da corsi e certificazioni Odoo
```

## Convenzioni

- File in formato Markdown `.md`
- Naming: `YYYY-MM-DD_titolo.md` per note datate
- Naming: `NomeCliente_NomeProgetto_TipoDoc.md` per deliverable
- Tag Obsidian: `#odoo`, `#fire`, `#client`, `#learning`, `#todo`

## Workflow per contesto

| Contesto | File di riferimento |
|----------|---------------------|
| Progetti Odoo / Avvale | `Work/WORK_WORKFLOW.md` |

## AI Context

Questo Brain è usato come contesto per Claude (Cowork mode).
I due workflow sopra si applicano in base al contesto del progetto — **non sono intercambiabili**.

**Profilo:** [[PROFESSIONAL_PROFILE]]
