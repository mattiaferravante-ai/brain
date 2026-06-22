# piaggio_cdms_india

Nuova implementazione Odoo Enterprise per Piaggio Vehicles Pvt. Ltd. (PVPL) India — Customer Dealer Management System (cDMS) per la rete dealer 2W (due ruote) e CV (commercial vehicles). Progetto attualmente **in fase di gara** (bid), non ancora confermato.

## Stack

- **Odoo:** Enterprise (versione da definire — probabile 17 o 18)
- **Moduli nativi (~30–35):** CRM, Sales, Purchase, Stock, MRP Repair, Account, l10n_in, l10n_in_edi, l10n_in_edi_ewaybill, Helpdesk, HR, Calendar, Appointment, Portal, Website, Survey, eLearning, SMS, Mass Mailing, Spreadsheet Dashboard
- **Custom modules (~8–12):** Job Card/Service, Warranty Claim, SQI Audit, Monthly Order Plan, PDI, FSC, RTO Registration, VIN Transfer Protocol, ir.sequence per outlet/FY
- **Integrazioni esterne (5):** SAP ERP (S/4HANA), SAP PWM (warranty), Tally Prime (multi-versione: 6.x, 7.0, ERP 9), Telematics, Firebase (push notifications)
- **Middleware:** SAP Integration Suite (hub centrale)
- **Hosting:** TBD — Odoo.sh o Azure Piaggio (Q01 aperta)

## Timeline

- **Inizio:** Da definire (gara in corso)
- **Durata stimata:** Da definire (Wave 1 + Wave 2)
- **Stato:** `#bid`

## Contatti

| Ruolo | Nome |
|-------|------|
| PM Avvale | Da definire |
| Referente cliente | Da definire |
| Functional Consultant | Mattia Ferravante |

## Ambienti

| Ambiente | URL |
|----------|-----|
| Produzione | Da definire |
| Staging | Da definire |
| Dev | Da definire |

## Sizing chiave

| Metrica | Valore |
|---------|--------|
| Utenti nominali | ~42.700 (dealer ~41.880 + PVPL ~834) |
| Concurrent users (peak) | 3.500–4.000 |
| Dealer | ~420 (CV ~295, 2W ~125) |
| DB da migrare | ~2 TB su 3,5 TB totali |
| Storico | 8 anni |
| Job card/giorno | ~6.209 |

## Scadenze

<!-- - `YYYY-MM-DD` — descrizione scadenza -->
<!-- - Risposta Q&A aperte critiche (Q01, Q11, Q28, Q32) prima della presentazione -->

## Punti aperti critici (gara)

- `Q01` — Hosting: Odoo.sh vs Azure Piaggio — blocca architettura
- `Q11` — Warranty approval levels — blocca workflow warranty
- `Q28` — System of Record ownership (customer, product, orders) — blocca BBP
- `Q32` — SLA infrastruttura — blocca HA/DR design
- `Q45` — EV checks — blocca design modulo vendite EV

## Sottocartelle

- `AF/` — Analisi Funzionali
- `UAT/` — Test Book e risultati
- `MeetingNotes/` — Verbali meeting
- `TechNotes/` — Note tecniche, workaround, configurazioni
- `PROJECT_SUMMARY.md` — Riepilogo cumulativo requisiti e decisioni
- `CDMS_Odoo_Module_Proposal.md` — Proposta moduli Odoo per area con gap analysis
- `CDMS_Piaggio_Project_Notes.md` — Note di progetto, volumi, punti critici, Q&A

## Tag

`#avvale` `#odoo` `#work` `#bid` `#india` `#pvpl`
