# Project Summary — piaggio_cdms_india

**Cliente:** Piaggio Vehicles Pvt. Ltd. (PVPL) — India  
**Odoo:** Enterprise (versione TBD)  
**Tipo:** Nuova implementazione — cDMS (Customer Dealer Management System)  
**Inizio:** Da definire (gara in corso) — **Durata stimata:** Da definire (Wave 1 + Wave 2)  
**Progetto correlato (stesso cliente):** [[piaggio_dealer_website/PROJECT_SUMMARY|Piaggio Dealer Website]]  
**Consulente:** [[PROFESSIONAL_PROFILE|Mattia Ferravante]]

Documento cumulativo aggiornato automaticamente dopo ogni meeting.
Serve come base di input per l'Analisi Funzionale (`/functional-analysis`).

> Aggiornato dalla skill `/minute` ad ogni verbale. Per correzioni: chiedi a Claude o edita direttamente in Obsidian.

---

## Stakeholders

| Nome | Ruolo | Azienda | Note |
|------|-------|---------|------|
| Mattia Ferravante | Functional Consultant | Avvale S.p.A. | Referente analisi funzionale |
| Da definire | PM | Avvale S.p.A. | |
| Da definire | Referente progetto | Piaggio Vehicles Pvt. Ltd. (PVPL) | |

---

## Requisiti emersi

- Gestione rete dealer 2W (~125) e CV (~295) con ~420 dealer totali in India
- ~42.700 utenti nominali (dealer + PVPL); picco concurrent 3.500–4.000
- Job card digitale end-to-end con PDI obbligatoria, FSC, SQI audit
- Flusso vendite B2C retail + B2B wholesale + inter-dealer (~1.500 tx/mese)
- Compliance GST India (CGST/SGST/IGST/UTGST), e-invoice IRN, e-way bill
- Tally integration: sync invoice da CDMS a Tally Prime (versioni 6.x, 7.0, ERP 9) via web service custom
- Credit management con sync periodica SAP ERP (non real-time)
- Warranty eligibility check real-time su SAP PWM (S/4HANA)
- Migration storico 8 anni (~2 TB da 3 sorgenti: SQL Server, Oracle/D2K, Tally)
- App mobile: spare parts + service + self-service portal cliente — con offline support
- Financial Year change con numerazione per outlet (schema DI/DIEV + YY + outlet + seriale)

---

## Processi da coprire

### AS-IS

- Gestione lead/enquiry su PLMS (app mobile outsourced, solo 2W)
- Warranty CV su Oracle/D2K; PDI e FSC CV su Oracle/D2K
- Contabilità dealer su Tally Prime (multi-versione, per dealer)
- Credit check dealer su SAP ERP
- Job card e service su CDMS legacy (SQL Server)
- Inter-dealer transactions (~1.500/mese) su CDMS legacy

### TO-BE

- **Pre-Sales & CRM**: Lead → Opportunity → Quotation su Odoo CRM
- **Sales B2C**: Quotation → Order → Invoice con VIN assignment, subsidy EV, RTO registration
- **Sales B2B/Wholesale**: Monthly Order Plan (MOP), SRN, inter-dealer con approval workflow
- **Service/Job Card**: apertura → lavorazione multi-technician → PDI → FSC check → chiusura → service invoice
- **Warranty**: eligibility check su SAP PWM, multi-tier claim, approval workflow, settlement SAP
- **Spare Parts**: VOR (urgenti), SOR (trimestrale auto-repeat), counter sale, discrepancy claims (TAT 90gg)
- **Transporter**: tracking VIN-level, POD upload da portale transporter
- **Finance**: GST India, e-invoice, Tally bridge, credit management con SAP
- **Reporting**: dashboard PVPL per area, dashboard dealer, statutory reports India
- **Mobile**: app spare, app service (offline), self-service portal cliente
- **Data Migration**: ETL multi-sorgente (SQL Server + Oracle/D2K + Tally), mock migration, storico read-only

---

## Decisioni chiave

- `2026-06-22` — Piattaforma: Odoo Enterprise (confermata come proposta Avvale)
- `2026-06-22` — Integration hub: SAP Integration Suite confermato come middleware
- `2026-06-22` — Tally: bridge custom da replicare/migliorare (versioni multiple)
- `2026-06-22` — Mobile PLMS: da rifare da zero, nessun riuso (KPMG Q-18)
- `2026-06-22` — E-Catalogue KeyTech: fuori scope, dismissione in 2-3 anni, no integrazione (Q06)
- `2026-06-22` — VIN tracking: a livello VIN singolo (non batch/shipment)
- `2026-06-22` — Credit sync SAP: periodica (non real-time), frequenza da definire (Q22)
- `2026-06-22` — Customer notifications: **tutti e 3 i canali** (SMS + email + mobile push) obbligatori (Q21)
- `2026-06-22` — Job card invoicing: conferma dealer obbligatoria prima di fatturare ricambi (Q24)
- `2026-06-22` — PDI transport damage: nessun trigger automatico claim — manuale (Q20)
- `2026-06-22` — AI fraud detection warranty: solo rule-based (nessun dataset storico disponibile, Q07)
- `2026-06-22` — Predictive maintenance: Wave 2, low priority (Q08)
- `2026-06-22` — Training language: inglese (Q41); piattaforma: Teams/SharePoint (Q42)
- `2026-06-22` — Dealer Champions per adozione territoriale: **non fattibile** — sostituire con ICT Team esterno (Q39)
- `2026-06-22` — Self-Service Portal cliente: **in scope Wave 1**, UI standard Odoo + branding Piaggio (Q27)
- `2026-06-22` — Telematics: solo dati selettivi (health alerts, odometer, service triggers) — no real-time (Q30)
- `2026-06-22` — UX/UI: standard product interface con customizzazione limitata a branding e journey (Q33)

---

## Punti aperti

- [ ] Q01 — Hosting: Odoo.sh vs Azure Piaggio → blocca architettura; proposta tecnica ha già scelto Azure (**discrepanza**)
- [ ] Q11 — Warranty approval levels (quanti livelli, ruoli) → blocca design workflow warranty
- [ ] Q25 — Service scheduling: da confermare con team service PVPL
- [ ] Q28 — System of Record ownership (customer, product, orders) → blocca BBP e integrations
- [ ] Q29 — Mobile native/offline → da valutare in fase successiva (escluso dalla proposta ma richiesto da RFP — **discrepanza**)
- [ ] Q32 — SLA infrastruttura uptime → blocca design HA/DR
- [ ] Q34/Q35 — Numero PO/KU/EU per change management → blocca piano training
- [ ] Q44 — Training third-party actors: riformulare la domanda con esempi (PVPL non ha capito)
- [ ] Q45 — EV-related checks: riformulare la domanda con esempi concreti (PVPL non ha capito)
- [ ] Chiarire con Odoo modello licenza: named (~42.700) vs concurrent (~4.000)
- [ ] Allineare sizing proposta tecnica (3.200 utenti dichiarati) con dati PVPL (42.700 nominali) — **discrepanza critica**
- [ ] Riscrivere Phase 2 ADOPTION per sostituire Dealer Champions con ICT Team esterno (Q39)
- [ ] Definire policy rollout dealer (cluster geografici, sequenza)
- [ ] Progettare VIN transfer protocol per coesistenza cross-system
- [ ] Ingaggiare vendor legacy per estrazione CDMS SQL Server (no export format — KPMG Q-14)
- [ ] Confermare unicità claim ID in SAP PWM per bloccare duplicati cross-system
- [ ] Compilare assumption/exclusion Training e Change Management nella proposta (oggi vuote)

---

## Note tecniche / vincoli

- **Legacy multi-sorgente**: CDMS SQL Server (nessun export format → dipendenza vendor), Oracle/D2K (SQL diretto, no API), Tally multi-versione
- **Volume migrazione dominante**: Service invoice ~33,4M + Spare Billing ~18,6M → dimensionano pipeline ETL
- **Aree alto rischio**: Tally Bridge, Job Card/Service (no modulo Odoo aderente al 100%), Warranty (SAP PWM non ancora definito), Data Migration 3,5 TB, dipendenza vendor legacy
- **FY change (Q-26)**: sequenza custom `ir.sequence` per outlet, schema DI/DIEV+YY+outlet+seriale, reset Aprile post-consenso dealer, finestra cross-FY (registrazione entro 31-March)
- **Job Card**: valutare se estendere `mrp_repair` (effort C) o sviluppare modulo custom dedicato (effort D)
- **Coesistenza**: 9 punti critici identificati — vedere [[CDMS_Piaggio_Project_Notes]] §5
- **Hosting**: 4.000 concurrent users su Odoo.sh è al limite architetturale → valutare Azure

---

*Ultimo aggiornamento: 2026-06-22 — aggiunto v2 Q&A PVPL + analisi proposta tecnica WIP*
