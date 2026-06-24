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

### Avvale Brand Identity (PREREQUISITO per tutti i documenti)
**Trigger:** ogni volta che stai per generare un documento, file o materiale visivo che rappresenta Avvale o un cliente Avvale — incluso qualsiasi `.docx`, `.xlsx`, `.pptx`, `.pdf`, immagine, CV, report, one-pager, presentazione. Trigger anche con: "applica il brand", "metti il logo Avvale", "usa i nostri colori", "rendilo brandizzato", "crea una presentazione Avvale".  
**Skill da usare:** `avvale-brand`  
**Come usarla:** caricare PRIMA di qualunque skill di produzione. Non genera il deliverable — fornisce design tokens (colori, font Archivo, path logo/asset) e linee guida da passare alla skill di produzione successiva.  
**Pipeline obbligatoria:**
1. Carica `avvale-brand` → leggi `tokens.json` + `references/<formato>_brand.md`
2. Poi esegui la skill di produzione (es. `functional-analysis`, `uat-testbook`, ecc.) applicando i token
3. A fine lavoro: verifica contro `references/qa_checklist.md`

> **Nota:** questa skill è prerequisito implicito di `functional-analysis` e `uat-testbook` — caricala sempre prima di queste due.

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

### Manuale Utente
**Trigger:** ogni volta che si parla di manuale utente, guida operativa, guida end-user, documentazione utente, guida key user, o qualsiasi documento che spiega come usare Odoo a un utente finale. Triggera anche per: "scrivi il manuale per", "prepara la guida utente di", "crea la documentazione utente per", "manuale operativo per".  
**Skill da usare:** `user-manual`  
**Output:** file `.docx` salvato in `Work/Clients/NomeProgetto/` o sottocartella dedicata

### AF Sync (rilettura AF modificata)
**Trigger:** ogni volta che si parla di "rileggere l'AF", "aggiornare il summary dall'AF", "sincronizzare l'AF", "ho modificato l'AF".  
**Skill da usare:** `af-sync`  
**Output:** `PROJECT_SUMMARY.md` aggiornato + report delle modifiche

### Pipeline Meeting → AF
Il flusso standard per arrivare all'Analisi Funzionale è:
1. `/minute` dopo ogni riunione → accumula dati in `PROJECT_SUMMARY.md`
2. Correzioni puntuali: chiedi a Claude oppure edita direttamente in Obsidian
3. `/functional-analysis` quando pronto → legge `PROJECT_SUMMARY.md` come input primario
4. Modifica AF in Word → `/af-sync [progetto]` per riallineare `PROJECT_SUMMARY.md` → torna al punto 3

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
| `/af-sync [progetto]` | Brain | Rilegge l'AF .docx modificata e sincronizza PROJECT_SUMMARY.md |
| `/user-manual` | Brain | Genera Manuale Utente .docx per un modulo Odoo |

---

## Struttura Brain

```
Brain/
├── Work/           → Progetti Odoo, clienti, deliverable, template
├── Finance/        → Portafoglio, FIRE, budget
├── Learning/       → Note tecniche, libri, corsi
└── Personal/       → Viaggi, obiettivi, journaling, dev personale
```
