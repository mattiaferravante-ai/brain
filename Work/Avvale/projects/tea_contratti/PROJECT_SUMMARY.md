# Project Summary — tea_contratti

**Cliente:** TEA Ambiente e Ecologia (TEA A&E)  
**Odoo:** 19.0 (Enterprise)  
**Tipo:** Nuova implementazione  
**Modulo custom:** `tea_quotations` — Schema versione `19.0.1.4.0`  
**Inizio:** marzo 2026 — **Stato:** UAT in fase di chiusura  
**Consulente:** [[PROFESSIONAL_PROFILE|Mattia Ferravante]]

Documento cumulativo aggiornato dopo ogni meeting e caricamento documenti.
Serve come base di input per l'Analisi Funzionale (`/functional-analysis`).

> Fonte primaria: `TechNotes/PIANO_IMPLEMENTAZIONE.md` — Piano implementazione completo v6.

---

## Stakeholders

| Nome | Ruolo | Azienda | Note |
|------|-------|---------|------|
| Michele Calvani | PM Avvale | Avvale S.p.A. | |
| Alessandro Caccialanza | Functional Lead Avvale | Avvale S.p.A. | |
| Mattia Ferravante | Consulente Avvale | Avvale S.p.A. | |
| Luisa Fiorini | Referente cliente | TEA Ambiente e Ecologia | |
| Andrea Bassoli | Responsabile Commerciale (Approvatore) | TEA Ambiente e Ecologia | Unico approvatore offerte |
| Noemi Menegazzo | Commerciale | TEA Ambiente e Ecologia | Key user principale |
| Claudia Grazioli | Backoffice (part-time) | TEA Ambiente e Ecologia | Accede post-accettazione per documentazione |

---

## Contesto di business

TEA A&E è un'azienda di **smaltimento rifiuti che opera come rivenditore**: acquista il servizio di trattamento dagli impianti e lo rivende ai clienti con un markup (default +20%).

Precedentemente la gestione offerte/contratti avveniva tramite **stampa unione Word/Excel** e file Excel di tracciamento. Il modulo `tea_quotations` digitalizza l'intero processo su Odoo 19 Enterprise.

**Volumi operativi:**
- ~400-500 offerte/anno per servizi standard (Rifiuti Speciali)
- ~100 contratti/anno per impianti (TMB e Discarica)
- ~500 clienti attivi (su 5000 anagrafiche totali nel VMS)
- 90% attività = richieste in entrata da clienti esistenti

**Confini del sistema:**
- Odoo gestisce il processo commerciale fino alla firma del contratto
- Post-accettazione: inserimento su VMS (gestionale interno) + coordinamento logistica esterna — fuori da Odoo
- Fatturazione: mensile a consuntivo su peso effettivo a destino — fuori da Odoo
- Nessuna integrazione con VMS nella prima fase

---

## Requisiti emersi

**Anagrafica e listino:**
- Anagrafica prodotti CER su 4 livelli (CER padre → Prodotto → Listino fornitore → Impianto)
- Chiave listino univoca: CER + stato fisico + impianto di destino
- Scadenza listini: annuale (31/12) o semestrale (30/06)
- HP (classificazioni pericolo): dato sulla riga listino, non sull'anagrafica prodotto
- Operazioni R/D: dato interno per backoffice, raramente stampato nell'offerta
- Univocità riga listino fornitore: Prodotto + Destino + elenco HP + Operazione
- HP e operazioni R/D sul prodotto CER: aggiornati automaticamente al censimento di un nuovo listino fornitore
- Listino Prezzi Cliente: no listini custom; funzionalità standard Odoo usate all'occorrenza nelle righe di contratto RS

**Offerte:**
- Tre tipi di documenti: **Offerta RS (Rifiuti Speciali)**, **Offerta TMB**, **Contratto Discarica**
- NO quotation standard Odoo → oggetto custom `tea.offer`
- Ricarico cliente: 15-20% su costo fornitore, modificabile manualmente
- Minimo fatturabile: campo libero, due tipologie (per rifiuto/formulario O cumulativo)
- Trasporto: riga separata (ragno = singola per CER, furgone = cumulativa)
- Possibilità firma manuale (PDF scaricabile + firma cartacea) oltre a firma digitale Odoo Sign
- Più versioni offerta sulla stessa lead

**Pipeline e flusso:**
- Flusso approvazione: commerciale crea → Andrea (backoffice) assegna protocollo → Andrea firma → invio cliente
- Pipeline CRM customizzata con 6 stage e blocchi di transizione
- Stato intermedio "Attesa documenti" (On Hold) post-accettazione per backoffice
- Notifiche email per Claudia (contratto firmato) e Andrea (offerte da approvare)
- Su ogni Opportunità: **Referente Commerciale** (fisso, non cambia mai) distinto da **Assegnatario** (cambia per fase del processo)
- Creazione manuale di un'Opportunità possibile senza passare da una Lead

**Clienti:**
- Ogni cliente può avere più unità produttive → offerta separata per ogni sede
- Migrazione: solo ~500 clienti attivi (non tutte le 5000 anagrafiche VMS); unità produttive create all'occorrenza o import separato
- Sede legale ≠ sede di ritiro (fondamentale per trasporto e documenti)
- Segmentazione clienti tramite tag nativi Odoo (es. azienda agricola, officina, edilizia, ente pubblico) — no custom fields
- Dati fatturazione elettronica (SDI/PEC) completati al momento della firma tramite modulo allegato — non bloccanti per la generazione dell'offerta
- Campi minimi per creazione cliente: ragione sociale, sede legale, indirizzo, P.IVA, PEC, referente commerciale (nome, email, telefono)

**Documenti:**
- Schede di caratterizzazione: chiave univocità = Tipologia Cliente + Prodotto CER + Destino + elenco HP + Operazione → su modello dedicato per ricerca agevole
- Allegati standard (privacy, condizioni generali): template email offerta
- Cron giornaliero reminder offerte in approvazione; supporto approvazione massiva contratti in coda giornaliera
- PDF con font Carlito (compatibile Calibri Light); label UI in italiano
- Contratto e allegati inviati in due email separate: (1) contratto con richiesta firma digitale, (2) allegati inviati manualmente dopo conferma firma
- Tabella allegati in Opportunità: per ogni allegato → flag "deve tornare firmato dal cliente" + flag "è stato ricevuto firmato" + link Google Drive
- Per stampa cliente: nascosti sotto-dettagli interni (stato fisico es. RETI/S1, operazione R/D, HP pericolo) — mantenuti nel sistema per backoffice ai fini inserimento VMS
- Flag "Contiene dati Sensibili" su riga CER nell'offerta
- Fornitore (testo libero) su righe servizi aggiuntivi (non un M2O a res.partner)

---

## Processi da coprire

### Pipeline commerciale (CRM)

| Stage | Seq | Condizioni per avanzare |
|-------|-----|------------------------|
| Nuovo | 10 | — (impostare tipologia obbligatoria) |
| Preso in carico | 15 | — |
| Elaborazione proposta | 20 | Solo RS: 4 campi documentazione completati. Crea `tea.offer` automaticamente |
| Proposta inviata | 30 | **Automatico** da `action_send_sign_request()` su offerta |
| Attesa documenti | 40 | **Automatico** da `action_accept()` su offerta. Genera documenti cliente |
| Offerta accettata | 50 | Tutti i documenti completi |

### Flusso offerta (state machine `tea.offer`)

```
draft → approval → approved → sent → accepted
          │              │       │
          └→ refused_approver    └→ refused_client
```

### Tipi offerta

| Tipo | Struttura | Note |
|------|-----------|------|
| TMB | Campi flat + prodotto CER singolo | Documento breve, 3 tabelle |
| Discarica | Campi flat + produttori (Allegato 2) | Contratto 18 articoli |
| Rifiuti Speciali | Righe CER (`tea.offer.line`) + servizi | Auto-fill prezzi da listino |

---

## Decisioni chiave

- `2026-03` — NO varianti Odoo: ogni CER+sotto-tipo+stato fisico è un `product.template` (type=service) separato
- `2026-03` — Stato fisico come campo Selection su `product.template`, non `product.attribute`
- `2026-03` — `tea.offer` è modello standalone (non eredita `crm.lead`), collegato via `lead_id` M2O required
- `2026-03` — Creazione offerta solo da lead (disabilitata creazione diretta)
- `2026-03` — Firma digitale tramite Odoo Sign; accettazione automatica via hook `sign.request._sign()`
- `2026-03` — Font PDF: Carlito (Apache 2.0, metricamente compatibile con Calibri Light)
- `2026-03` — Saluto PDF Egregio/Spett. basato su `l10n_it_codice_fiscale` (16 char = persona fisica)
- `2026-03` — Unicità schede di caratterizzazione via constraint Python (non SQL UNIQUE, perché NULL trattati diversamente)
- `2026-03` — Protocollo RS: `O` + progressivo 4 cifre + `/` + anno + `/` + iniziali referente commerciale
- `2026-03` — Documenti cliente generati automaticamente dai template tipologia al passaggio ad "Attesa documenti"
- `2026-03` — `sales_team.group_sale_manager` per ACL (non `crm.group_crm_manager`, non esiste in Odoo 19)
- `2026-03` — Dipendenza `l10n_it_edi` obbligatoria per campo `l10n_it_codice_fiscale` su `res.partner`

---

## Punti aperti

- [ ] ~~Numero di protocollo: generazione automatica da Odoo o manuale da VMS?~~ → Risolto: protocollo RS auto-generato (`O` + progressivo + `/` + anno + `/` + iniziali referente) → [[2026-03-16_incontro-analisi-1]]
- [ ] Filtri ricerca lead per zona/provincia (non standard Odoo) → [[2026-03-23_incontro-analisi-3]]
- ~~Automazione contratti complessi Discarica (17-20 pp): approccio con stampa unione → confermato nell'AF Rev. 02.0~~ → Risolto

---

## Note tecniche / vincoli

### Identità modulo

| Proprietà | Valore |
|-----------|--------|
| Nome tecnico | `tea_quotations` |
| Versione Odoo | 19.0 Enterprise |
| Dipendenze | `account, crm, l10n_it_edi, product, sale_crm, sign, spreadsheet_dashboard, uom` |
| Schema versione | `19.0.1.4.0` (OCA semver) |

### Dati caricati (import iniziale da Excel)

| Entità | Modello | Record |
|--------|---------|--------|
| Codici CER | tea.cer.code | 115 |
| Codici HP | tea.hp.code | 11 |
| Operazioni R/D | tea.waste.operation | 12 |
| Impianti di trattamento | res.partner | 63 |
| Prodotti CER | product.template | 139 |
| Righe listino fornitore | product.supplierinfo | 268 |

### Modelli custom (7)

`tea.hp.code`, `tea.waste.operation`, `tea.cer.code`, `tea.characterization.sheet`, `tea.offer`, `tea.offer.type`, `tea.contract.producer`, `tea.offer.document`, `tea.offer.line`, `tea.offer.line.service`, `tea.offer.validity`

### Estensioni modelli standard (5)

`product.template` (campi CER + physical_state), `res.partner` (flag `is_waste_plant`), `product.supplierinfo` (operazione R/D + HP + minimi), `res.company` (markup % + firma offerte), `crm.lead` (smart button + pipeline + documenti)

### Note specifiche Odoo 19

- Constraint SQL con `models.Constraint("UNIQUE(col)", "msg")` (non `_sql_constraints`)
- Filtro prodotti: `filter[@name='goods']` (non `consumable`) nella search view
- `supplier_rank` richiede modulo `account`
- `uom_po_id` non esiste in Odoo 19

### Ambienti

- Produzione: Odoo.sh (URL da definire)
- Staging: Odoo.sh (URL da definire)

---

## Documenti Knowledge Base

- `AF/TEA_AE_CRM_Contratti_AF_00.1.docx` — Analisi Funzionale bozza 00.1 — basata su meeting notes analisi
- `TEA - A&E - Gestione preventivi ed ordini di vendita CRM Odoo - Analisi Funzionale - Rev. 02.0.docx` — AF Rev. 02.0 (20/05/2026) — aggiornamenti a valle di sviluppo e sessioni di preview (attualmente in Downloads)
- `TechNotes/PIANO_IMPLEMENTAZIONE.md` — Piano implementazione completo v6 (architettura, modelli, viste, sicurezza, test)
- `MeetingNotes/2026-03-16_incontro-analisi-1.md` — AS-IS processo offerte, requisiti CRM, flusso approvazione
- `MeetingNotes/2026-03-19_incontro-analisi-2.md` — Utenti, migrazione clienti, listino prezzi, logica trasporto
- `MeetingNotes/2026-03-23_incontro-analisi-3.md` — Decisione architettura contratti, pipeline CRM, struttura prodotti/HP

---

*Ultimo aggiornamento: 2026-06-04 — sincronizzato da AF Rev. 02.0 (20/05/2026)*
