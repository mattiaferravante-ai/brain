# CLAUDE.md — Brain di Mattia Ferravante

Questo file viene letto automaticamente da Claude ad ogni sessione.
Contiene le regole operative per lavorare correttamente in questo Brain.

---

## Chi è l'utente

Mattia Ferravante — Odoo Functional & ERP Consultant @ Avvale S.p.A.
Vedi `Work/PROFESSIONAL_PROFILE.md` per il profilo completo.

---

## Regole generali

- Risposte in italiano salvo diversa indicazione
- Stile: diretto, tecnico, senza fluff
- Per progetti Avvale: salvare sempre in `Work/Avvale/projects/NomeProgetto/`
- Per altri clienti/progetti: salvare in `Work/Clients/NomeProgetto/`
- Per template: usare quelli in `Work/Templates/` come base

## Manutenzione struttura Brain (OBBLIGATORIO)

Ad ogni modifica strutturale del Brain (nuovo file, nuova cartella, rimozione, rinomino) devi:

1. **Aggiornare il README.md della cartella** interessata con il nuovo file/cartella
2. **Aggiornare `README.md` radice** se cambia la struttura di primo livello
3. **Aggiornare i tag** del file nuovo per coerenza con la cartella (`#personal`, `#work`, ecc.)
4. **Aggiornare i wikilink Obsidian** (`[[NomeFile]]`) in tutti i file che referenziano la struttura modificata
5. **Non lasciare mai file orfani** — ogni file deve comparire in almeno un README o indice

Questo vale anche per file generati (CV, AF, UAT) — aggiungerli sempre all'indice della cartella.

---

## Skill obbligatorie per contesto Work

### Analisi Funzionale
**Trigger:** ogni volta che si parla di AF, analisi funzionale, gap analysis, AS-IS/TO-BE, specifiche funzionali, documento di analisi per un modulo Odoo.  
**Skill da usare:** `functional-analysis`  
**Output:** file `.docx` salvato in `Work/Clients/NomeProgetto/AF/`

### UAT Test Book
**Trigger:** ogni volta che si parla di UAT, test book, casi di test, piano di test, test acceptance, testing Odoo.  
**Skill da usare:** `uat-testbook`  
**Output:** file `.xlsx` salvato in `Work/Clients/NomeProgetto/UAT/`

### Odoo Permission Builder
**Trigger:** ogni volta che si parla di record rules, ir.rule, access rights, restrizioni su modelli Odoo, permessi utente.  
**Skill da usare:** `odoo-permission-builder`  
**Output:** XML pronto per modulo custom

### Meeting Minutes
**Trigger:** ogni volta che si parla di verbale, minute, meeting notes, trascrizione riunione, recap meeting, note di riunione.  
**Skill da usare:** `minute`  
**Output:** file `.md` in `Work/<progetto>/MeetingNotes/` + aggiornamento `PROJECT_SUMMARY.md` + aggiornamento README progetto

### Pipeline Meeting → AF
Il flusso standard per arrivare all'Analisi Funzionale è:
1. `/minute` dopo ogni riunione → accumula dati in `PROJECT_SUMMARY.md`
2. Correzioni puntuali: chiedi a Claude oppure edita direttamente in Obsidian
3. `/functional-analysis` quando pronto → legge `PROJECT_SUMMARY.md` come input primario

---

## Workflow per contesto

| Contesto | Regole operative |
|----------|-----------------|
| Progetti Odoo / Avvale | `Work/WORK_WORKFLOW.md` |
| Progetti personali (mini PC) | `Personal/Dev/PROJECT_WORKFLOW.md` |

---

## Comandi disponibili

| Comando | Dove | Funzione |
|---------|------|----------|
| `/generate-cv` | Brain o qualsiasi progetto con Brain | Genera CV da PROFESSIONAL_PROFILE |
| `/uploadbrain` | Qualsiasi progetto | Aggiunge symlink Brain, .gitignore, CLAUDE.md e attiva sync |
| `/new-project` | Brain | Crea struttura cartelle per un nuovo progetto in Work/ |
| `/minute` | Brain | Genera verbale + action items da trascrizione riunione |

---

## Struttura Brain

```
Brain/
├── Work/           → Progetti Odoo, clienti, deliverable, template
├── Finance/        → Portafoglio, FIRE, budget
├── Learning/       → Note tecniche, libri, corsi
└── Personal/       → Viaggi, obiettivi, journaling, dev personale
```
