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
- Per documenti di progetto: salvare sempre in `Work/Clients/NomeProgetto/`
- Per template: usare quelli in `Work/Templates/` come base

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

---

## Workflow per contesto

| Contesto | Regole operative |
|----------|-----------------|
| Progetti Odoo / Avvale | `Work/WORK_WORKFLOW.md` |
| Progetti personali (mini PC) | `Personal/Dev/PROJECT_WORKFLOW.md` |

---

## Struttura Brain

```
Brain/
├── Work/           → Progetti Odoo, clienti, deliverable, template
├── Finance/        → Portafoglio, FIRE, budget
├── Learning/       → Note tecniche, libri, corsi
└── Personal/       → Viaggi, obiettivi, journaling, dev personale
```
