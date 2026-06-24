# Skills Index — Documentazione completa

Documentazione dettagliata delle skill Claude disponibili nel Brain.
File di riferimento per `/minute`, `/functional-analysis`, `/uat-testbook`, ecc.

> **Per Claude:** leggi la sezione specifica solo quando stai per eseguire quella skill. Non caricare tutto all'inizio della sessione.

---

## Avvale Brand Identity (`avvale-brand`)

**PREREQUISITO** per tutti i documenti che rappresentano Avvale o un cliente Avvale: `.docx`, `.xlsx`, `.pptx`, `.pdf`, immagine, CV, report, one-pager, presentazione.

**Trigger:** "applica il brand", "metti il logo Avvale", "usa i nostri colori", "rendilo brandizzato", "crea una presentazione Avvale" — oppure implicito prima di `functional-analysis` o `uat-testbook`.

**Pipeline obbligatoria:**
1. Carica `avvale-brand` → leggi `tokens.json` + `references/<formato>_brand.md`
2. Esegui la skill di produzione applicando i token
3. A fine lavoro: verifica contro `references/qa_checklist.md`

**Skill file:** `Work/Skills/avvale-brand/avvale-brand/SKILL.md`

---

## Analisi Funzionale (`functional-analysis`)

**Trigger:** AF, analisi funzionale, gap analysis, AS-IS/TO-BE, specifiche funzionali, documento di analisi per un modulo Odoo.

**Input principale:** `PROJECT_SUMMARY.md` del progetto — non usare il piano tecnico come fonte primaria.

**Output:** file `.docx` salvato in `Work/Clients/NomeProgetto/AF/` (o `Work/Avvale/projects/NomeProgetto/AF/` per progetti Avvale)

**Prerequisito:** caricare `avvale-brand` prima.

**Skill file:** `Work/Skills/functional-analysis/SKILL.md`

---

## UAT Test Book (`uat-testbook`)

**Trigger:** UAT, test book, casi di test, piano di test, test acceptance, testing Odoo.

**Output:** file `.xlsx` con fogli Summary + Test book Funzionale + Test book Tecnico + Data validation. Salvato in `Work/Clients/NomeProgetto/UAT/`.

**Prerequisito:** caricare `avvale-brand` prima.

**Skill file:** `Work/Skills/uat-testbook/SKILL.md`

---

## Meeting Minutes (`minute`)

**Trigger:** verbale, minute, meeting notes, trascrizione riunione, recap meeting, note di riunione.

**Output:** file `.md` in `Work/<progetto>/MeetingNotes/YYYY-MM-DD_meeting.md` + aggiornamento `PROJECT_SUMMARY.md` + aggiornamento README progetto + aggiornamento `STATO_PROGETTI.md`.

**Skill file:** `Work/Skills/minute.md`

---

## Manuale Utente (`user-manual`)

**Trigger:** manuale utente, guida operativa, guida end-user, documentazione utente, guida key user. Anche: "scrivi il manuale per", "prepara la guida utente di", "crea la documentazione utente per".

**Output:** file `.docx` salvato in `Work/Clients/NomeProgetto/` o sottocartella dedicata.

**Skill file:** `Work/Skills/user-manual/SKILL.md`

---

## AF Sync (`af-sync`)

**Trigger:** "rileggere l'AF", "aggiornare il summary dall'AF", "sincronizzare l'AF", "ho modificato l'AF".

**Output:** `PROJECT_SUMMARY.md` aggiornato + report delle modifiche.

**Skill file:** `Work/Skills/af-sync/SKILL.md`

---

## Odoo Permission Builder (`odoo-permission-builder`)

**Trigger:** record rules, ir.rule, access rights, restrizioni su modelli Odoo, permessi utente.

**Output:** XML pronto per modulo custom.

---

## Pipeline meeting → AF

Flusso standard per arrivare all'Analisi Funzionale:

```
/minute (ogni riunione)
  → accumula in PROJECT_SUMMARY.md
  → /functional-analysis (quando pronto)
  → modifica AF in Word
  → /af-sync (per riallineare PROJECT_SUMMARY.md)
  → torna a /functional-analysis se serve nuova versione
```
