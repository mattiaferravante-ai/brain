# PVPL India CDMS — Proposta Moduli Odoo per Area
> Odoo Functional Consultant Reference | Avvale S.p.A. | Last updated: 2026-06-22
>
> **Legenda effort**: A = Config only | B = Minor custom | C = Major custom | D = Custom dev | E = Integration (third-party)
>
> **Legenda copertura**: ✅ Nativo | 🟡 Parziale | 🔴 Gap / Mancante
>
> **Aggiornamento 2026-06-22**: integrate risposte Q&A "Set 1" altro fornitore (KPMG, risposte PVPL 27-May-2026) — landscape legacy Oracle/D2K, volumi migrazione, sizing utenti/dealer, app PLMS, FY change.

### Sizing di riferimento (Q&A)

| Metrica | Valore | Fonte |
|---|---|---|
| Utenti nominali totali | **~42.700** (Dealer ~41.880 + PVPL ~834) | KPMG Q-16 |
| Concurrent users (peak) | 3.500–4.000 | AVVALE Q02 |
| Dealer | **~420** (CV ~295, 2W ~125) | KPMG Q-04 |
| DB totale / da migrare | 3,5 TB / ~2 TB | AVVALE Q03 |
| Oggetti dominanti migrazione | Service invoice ~33,4M, Spare Billing ~18,6M | KPMG Q-12 |

> ⚠️ **Licensing**: il delta named (~42.700) vs concurrent (~4.000) è il principale driver di costo licenze Odoo Enterprise — da chiarire con Odoo.

---

## Indice

1. [Piattaforma & Infrastruttura](#1-piattaforma--infrastruttura)
2. [Master Data & Entities](#2-master-data--entities)
3. [Pre-Sales & CRM](#3-pre-sales--crm)
4. [Sales — B2C Retail Dealer](#4-sales--b2c-retail-dealer)
5. [Sales — B2B Wholesale & Inter-Dealer](#5-sales--b2b-wholesale--inter-dealer)
6. [Service & Job Card](#6-service--job-card)
7. [After-Sales & Warranty](#7-after-sales--warranty)
8. [Spare Parts](#8-spare-parts)
9. [Transporter & Logistica Veicoli](#9-transporter--logistica-veicoli)
10. [Financial & Compliance (India GST + Tally)](#10-financial--compliance-india-gst--tally)
11. [Credit Management](#11-credit-management)
12. [Mobile Applications](#12-mobile-applications)
13. [Customer Self-Service Portal](#13-customer-self-service-portal)
14. [Reporting & Analytics](#14-reporting--analytics)
15. [Integrations (SAP + Tally + Telematics)](#15-integrations-sap--tally--telematics)
16. [Data Migration](#16-data-migration)
17. [Change Management & Training](#17-change-management--training)
18. [Riepilogo Effort Complessivo](#18-riepilogo-effort-complessivo)

---

## 1. Piattaforma & Infrastruttura

### Moduli Odoo attivati di base
| Modulo | Scopo |
|---|---|
| `base` | Core framework, utenti, gruppi, lingua |
| `base_setup` | Configurazione iniziale multi-company |
| `mail` | Chatter, notifiche, email engine |
| `web` | Frontend framework |
| `auth_totp` | MFA (Time-based OTP) |
| `iap` | In-App Purchase per servizi cloud |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| MFA obbligatorio per tutti i dealer | ✅ Nativo (`auth_totp`) | A | Policy enforcement a livello gruppi |
| Multi-language UI + dati (COA, spare parts) | ✅ Nativo | A | Attivare lingue; traduzione dati via `ir.translation` |
| RBAC multi-role (dealer, sub-dealer, PVPL, transporter, ASC, PGO) | 🟡 Parziale | B | Nativo come framework; user role matrix PVPL da progettare e configurare — complessità elevata |
| Multi-company (2W + CV come Business Unit separate) | ✅ Nativo | B | Setup multi-company o BU via analytic; da valutare se separazione contabile richiede multi-company reale |
| Remote access HTTPS | ✅ Nativo (Odoo.sh) | A | DNS + SSL su Odoo.sh |
| Hosting: Odoo.sh vs Azure | 🟡 Da decidere | — | 4.000 concurrent users → verificare piano Odoo.sh Enterprise; Azure Piaggio potrebbe essere obbligatorio |
| High Availability / DR | 🟡 Parziale | B–E | Odoo.sh gestisce HA; su Azure richiede architettura dedicata |
| SLA uptime | 🔴 Da definire | — | Non ancora specificato da PVPL (Q32 aperta) |

---

## 2. Master Data & Entities

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `contacts` (res.partner) | Anagrafica dealer, sub-dealer, cliente, fornitore, transporter |
| `product` | Veicoli, spare parts, servizi come prodotti Odoo |
| `stock` | Serial number / lot tracking per VIN e spare parts |
| `uom` | Unità di misura |
| `hr` | Sales employee (DSE, DSM) come HR employees |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Dealer / Sub-dealer / Broker / Outlet hierarchy | 🟡 Parziale | B | `res.partner` con `parent_id`; aggiungere campi custom (tipo dealer, livello, territorio, SQI level) |
| Sales Territory management | 🔴 Gap | C | `crm.team` parzialmente; serve modello custom per territory → dealer assignment con override geografico |
| Business Unit (2W / CV) | 🟡 Parziale | B | Tag o `res.partner.category`; meglio come campo `business_line` selection su dealer + prodotti |
| VIN come Serial Number su prodotto | ✅ Nativo (`stock.lot`) | A | Attivare tracking seriale; un VIN = un serial number |
| Spare parts multi-attribute (codice, categoria, compatibilità veicolo) | 🟡 Parziale | B | `product.template` + `product.attribute`; campo custom per compatibilità modello veicolo |
| Pricing & Discount multi-livello (%, amount, per dealer/cliente) | 🟡 Parziale | B | `product.pricelist` + `discount` su sale.order.line; pricelist per dealer tier |
| RTO Registration master data | 🔴 Gap | C | Modello custom `pvpl.rto.registration` con VIN, customer, RTO office, date |
| Dealer level (post-SQI audit) | 🔴 Gap | B | Campo custom su `res.partner` con history; campo readonly da aggiornare da audit |
| FSC (Free Service Coupon) master | 🔴 Gap | C | Modello custom: validità giorni + km, tipo veicolo, tipo servizio — collegato a job card |
| T1/T2/FRT Fault Codes | 🔴 Gap | B | Tabella master custom per codici difetto/riparazione; usata in job card e warranty |
| PDI checklist master | 🔴 Gap | C | Template checklist dinamico per modello veicolo; compilazione obbligatoria pre-delivery |
| AMC (Additional Maintenance Contract) | 🔴 Gap | C | Contratto servizio custom con scadenze, km, servizi inclusi — collegato a customer + VIN |
| Business Goals / Target per dealer | 🔴 Gap | B | Modello `pvpl.dealer.target` con periodo, BU, KPI, valore target vs actual |

---

## 3. Pre-Sales & CRM

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `crm` | Lead, Opportunity, Pipeline |
| `sale_crm` | Bridge CRM → Sales Order |
| `utm` | Tracking sorgenti lead (digitale) |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Lead capture + Enquiry management | ✅ Nativo (`crm.lead`) | A | Configurare stage pipeline per BU; tag per 2W/CV |
| Quotation generation da opportunity | ✅ Nativo | A | `sale.order` da `crm.lead` |
| Follow-up automatico post-quotation | 🟡 Parziale | B | `crm` activity scheduling; aggiungere automation rule per scadenza follow-up |
| Test drive / Demo management | 🔴 Gap | B | Activity type custom + campo su `crm.lead`; calendario slot |
| DSE / DSM tracking su lead e opportunity | 🟡 Parziale | B | `crm.team` + salesperson; aggiungere DSM come livello gerarchico |
| Customer analytics / conversion rate report | 🟡 Parziale | B | `crm` report nativo; custom per KPI PVPL specifici (enquiry → retail rate) |
| Digital lead da sito web / e-commerce | ✅ Nativo (`website_crm`) | A | Form contatto sito → lead CRM automatico |

---

## 4. Sales — B2C Retail Dealer

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `sale_management` | Sales order, conferma, flusso standard |
| `sale_stock` | Collegamento ordine → stock |
| `account` | Fatturazione cliente |
| `l10n_in` | Localizzazione India (GST, HSN, e-invoice) |
| `l10n_in_edi` | E-invoicing India (GST IRN) |
| `stock` | Delivery order, VIN assignment |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Quotation → Order → Invoice (veicolo) con VIN assignment | ✅ Nativo | B | Configurare flusso; aggiungere VIN (serial) selection obbligatoria su order line |
| Subsidy EV nazionale e statale | 🔴 Gap | C | Modello `pvpl.ev.subsidy` con stato (approvato/pending), importo, tipo; integrazione con invoice come riga negativa o nota credito |
| EV-related checks su order (Q45 aperta) | 🔴 Gap | C | Popup/wizard custom con checklist EV obbligatoria prima della conferma ordine; da dettagliare con PVPL |
| RTO Registration workflow | 🔴 Gap | C | Stato custom post-delivery: `pvpl.rto.registration` collegato a sale.order + VIN; alert scadenza |
| Delivery Certificate generazione | 🔴 Gap | B | Report PDF custom da `stock.picking` con firma cliente |
| Payment receipt management | 🟡 Parziale | B | `account.payment` nativo; aggiungere gestione anticipo + progressivo pagamenti dealer |
| Discount su veicolo (% o importo, per cliente o dealer) | ✅ Nativo | A | `sale.order.line` discount + pricelist |
| Dealer receipt immediato al dispatch | 🔴 Gap | B | Trigger su `stock.picking` validato → generazione automatica receipt document |
| Sales Employee (DSE, DSM) su ordine | 🟡 Parziale | B | `salesperson` su `sale.order`; aggiungere DSM come manager field + commissione tracking |
| Happy calling post-vendita automatico | 🔴 Gap | B | Automation rule: X giorni post-delivery → activity su CRM per chiamata follow-up |
| Customer notification (SMS + email + push) | 🟡 Parziale | C | `sms` + `mail` nativi; push notification richiede integrazione app mobile (Firebase o equivalente) |
| Report retail/enquiry/stock per giorno/mese/anno | 🟡 Parziale | B | Report nativo estendibile; custom per formato PVPL e drill-down per territorio/BU |

---

## 5. Sales — B2B Wholesale & Inter-Dealer

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `purchase` | Purchase order PVPL → dealer (wholesale) |
| `sale_management` | Sale order dealer ↔ dealer |
| `stock_inter_warehouse` | Trasferimento tra location |
| `stock` | Inventory update real-time |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Monthly Order Plan (MOP) con rilascio ordini su payment received | 🔴 Gap | C | Modello `pvpl.monthly.order.plan` con finestra di ordinazione, allocazione quota dealer, stato rilascio; trigger su conferma payment |
| Wholesale dispatch PVPL → Dealer | 🟡 Parziale | B | `sale.order` + `stock.picking`; aggiungere gestione lotto di spedizione e multi-VIN |
| SRN (Stock Receipt Note) | 🔴 Gap | B | Document custom post-ricezione stock; collegato a `stock.picking` + firma dealer |
| Inter-dealer transfer (stock + ordine) | 🟡 Parziale | C | Trasferimento interno Odoo OK; inter-dealer tra company diverse richiede SO→PO automatico con approval PVPL |
| Approval workflow inter-dealer | 🔴 Gap | C | Modello approvazione multi-livello custom (dealer richiedente → PVPL area manager → PVPL HQ); approvazione per tipo e soglia |
| Inventory update automatico post-ricezione | ✅ Nativo | A | `stock.picking` validate → inventory aggiornato |
| Stock visibility autorizzata per ruolo (ordini, stock, retail) | 🟡 Parziale | B | Record rules su `stock.quant` e `sale.order` per dealer; PVPL vede tutto |
| B2B report (retail, enquiry, stock) per territorio | 🟡 Parziale | B | Custom dashboard per PVPL area manager con aggregazione per territorio/BU |

---

## 6. Service & Job Card

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `helpdesk` | Base ticket / job card (alternativa: `mrp_repair`) |
| `mrp_repair` | Repair order — più vicino al job card DMS |
| `project` | Task scheduling, workload |
| `hr` | Technician management |
| `stock` | Consumo spare parts da job card |
| `account` | Service invoice da job card |
| `calendar` | Appointment / service scheduling |

> **Nota architetturale**: `mrp_repair` è il modulo Odoo più vicino al job card automotive ma manca di molti elementi PVPL. Valutare se estendere `mrp_repair` (C) o costruire un modulo job card custom dedicato (D). La seconda opzione è più pulita per questo livello di complessità.

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Job Card digitale end-to-end (apertura → lavorazione → chiusura → fattura) | 🟡 Parziale (`mrp_repair`) | C | Estendere con: stato workflow custom, multi-technician, ore lavoro, FSC check, VIN lookup |
| PDI obbligatorio pre-delivery (checklist per modello) | 🔴 Gap | C | Wizard PDI su `stock.picking` di delivery; template checklist da modello veicolo; blocco delivery se PDI incompleta |
| PDI Complaint & Defect management | 🔴 Gap | B | Modello `pvpl.pdi.defect` con codice difetto, gravità, azione correttiva; collegato a PDI |
| Service appointment scheduling (slot automatico + advisor) | 🟡 Parziale (`calendar`) | C | Slot disponibilità per stall/tecnico; booking online da self-service portal; reminder SMS/email |
| Multi-technician su job card + ore lavoro | 🔴 Gap | C | `mrp.workcenter` adattato; timesheet tecnico per job card; FRT (Flat Rate Time) per tipo riparazione |
| FSC (Free Service Coupon) check su job card | 🔴 Gap | C | Lookup FSC per VIN + km attuali + data; applicazione automatica sconto/esenzione su service invoice |
| SQI (Service Quality Index) Audit module | 🔴 Gap | D | Modulo custom completo: checklist audit per dealer, scoring, storico livelli, alert |
| Goodwill claim workflow | 🔴 Gap | C | Estensione claim: approvazione PVPL per rimborsi fuori warranty; importo e motivazione |
| Technical Campaign / Recall execution tracking | 🔴 Gap | C | Modello `pvpl.campaign` con VIN affected list, stato esecuzione per dealer, deadline, comunicazione dealer |
| Recall compliance (regulatory) | 🔴 Gap | C | Collegamento campaign a RTO/authority notification; report stato per autorità |
| Superbike workflow separato | 🔴 Gap | B | Tipo job card = "superbike" con checklist e approvazioni diverse; filtri e viste dedicate |
| Popup/checks workflow per dealer e PVPL | 🔴 Gap | B | Automation rules + wizard custom su step critici del job card (conferma diagnosi, approvazione cliente, spare request) |
| Service invoice con auto-generazione da job card | 🟡 Parziale | B | `mrp_repair` genera invoice; aggiungere logica multi-tipo (customer copy, dealer accounting, warranty portion) |
| Happy calling post-service automatico | 🔴 Gap | B | Automation rule: X giorni post-chiusura job card → activity follow-up |
| CSI (Customer Satisfaction Index) tracking | 🔴 Gap | C | Survey post-service (SMS/email) → risposta → score su `res.partner` + dashboard |
| Predictive maintenance (Wave 2) | 🔴 Gap | D–E | Richiede feed telematics (odometer, alert) → regole predittive o ML; da pianificare in Wave 2 |
| AI sentiment analysis (Wave 2) | 🔴 Gap | D–E | NLP su customer feedback; Wave 2, dipende da dataset |

---

## 7. After-Sales & Warranty

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `helpdesk` | Warranty ticket base |
| `account` | Settlement finanziario |
| `mrp_repair` | Repair order collegato |

> **AS-IS vs TO-BE (KPMG Q-07/Q-13)**: la warranty **CV** legacy risiede su **Oracle / D2K** (insieme a PDI e FSC CV), accessibile solo via SQL diretto (no API). Il TO-BE è il roll-out di **SAP PWM (S/4HANA)** anche in India (Q10). Implica: (a) integrazione runtime CDMS↔SAP PWM, (b) **migrazione one-off** dei dati warranty/PDI/FSC CV da Oracle verso Odoo (storico) e/o SAP PWM.

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Warranty eligibility check (→ SAP PWM) | 🔴 Gap | E | API call a SAP PWM per VIN + tipo intervento + data; risposta eligible/not eligible in tempo reale; blocco claim se not eligible |
| Migrazione storico warranty CV / PDI / FSC da **Oracle/D2K** | 🔴 Gap | D | Estrazione SQL diretta da Oracle (no API); mapping verso modelli Odoo / archivio read-only; coordinamento eventuale con vendor Oracle |
| Multi-tier warranty categorization (standard, extended, goodwill, recall) | 🔴 Gap | C | Campo `warranty_type` su claim; workflow e approval diversi per tipo |
| Claim creation + submission da dealer | 🔴 Gap | C | Portale dealer per inserimento claim: VIN, sintomo, fault code, foto, ricambi usati |
| Multi-level claim approval (Dealer → Regional → PVPL HQ) | 🔴 Gap | C | Approval matrix custom su `pvpl.warranty.claim`; notifiche email per ogni step |
| Claim tracking real-time (dealer dashboard) | 🔴 Gap | B | Vista kanban/list filtrata per dealer con stato claim e importo |
| Automated settlement → SAP ERP | 🔴 Gap | E | Claim approvato → payload a SAP via SAP Integration Suite per credit note/pagamento dealer |
| Fraud detection / anomaly (Wave 2) | 🔴 Gap | D | Dataset fraud non disponibile (Q07); approccio rule-based come fallback Wave 1 (soglie KPI) |
| Spare parts priority su warranty/recall orders | 🔴 Gap | B | Campo `priority` su `stock.picking` e `purchase.order`; route dedicata per VOR warranty |

---

## 8. Spare Parts

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `purchase` | Ordini acquisto spare (VOR, SOR, counter) |
| `stock` | Gestione magazzino dealer, movimenti, resi |
| `inventory` | Inventario fisico periodico |
| `sale` | Counter sale spare parts a cliente |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| VOR Order (Vehicle Off Road, urgente) | 🟡 Parziale | C | `purchase.order` con tipo VOR + flag priorità alta; blocco operativo su veicolo linkato; alert PVPL |
| SOR Order (standard replenishment trimestrale) | 🟡 Parziale | C | `purchase.order` ricorrente; custom: auto-repeat mesi 2 e 3 del trimestre + email automatica a dealer + sommario ordini; estendere a CV (oggi solo 2W) |
| Counter Sale da magazzino dealer | ✅ Nativo (`point_of_sale` o `sale`) | B | POS o SO semplificato; aggiungere lookup catalogo parti per modello veicolo |
| Spares receipt con discrepancy claim | 🔴 Gap | C | Wizard ricezione: confronto quantità attesa vs ricevuta; auto-generazione discrepancy claim; TAT 90 giorni tracked |
| Foto obbligatoria su damaged claim | 🔴 Gap | B | Campo `image_ids` mandatory su `pvpl.spare.claim` con validazione salvataggio |
| Return Dealer → PVPL (con approvazione) | 🟡 Parziale | C | `stock.return.picking` + approvazione PVPL; motivi rientro codificati; nota credito automatica |
| Return Customer → Dealer | ✅ Nativo | B | `stock.return.picking` da delivery; collegamento a job card o counter sale |
| Dealer warehouse management (min/max stock) | 🟡 Parziale | B | `stock.warehouse.orderpoint` (reorder rules); aggiungere min/max definiti da PVPL per codice parte |
| E-Catalogue integration (futura, post-KeyTech) | 🔴 Gap | E | Placeholder in Wave 2; nessuna integrazione con KeyTech nell'immediato (Q06 confermata) |
| Spare parts mobile app con offline support | 🔴 Gap | D–E | Non coperto da Odoo standard; richiede sviluppo app dedicata o progressive web app |

---

## 9. Transporter & Logistica Veicoli

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `stock` | Picking, transfer, delivery |
| `fleet` | (Parziale) Veicoli in transito |
| `mail` | Notifiche transporter |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Transporter master data (dati anagrafici, tipologia, percorsi) | 🟡 Parziale | B | `res.partner` con tag Transporter; aggiungere campi custom (percorsi autorizzati, tipo mezzo) |
| Shipment con lista VIN assegnati | 🟡 Parziale | C | `stock.picking` con serial numbers; custom per raggruppamento VIN per spedizione + documento manifesto |
| POD upload da transporter (portale) | 🔴 Gap | C | Portale Odoo custom per transporter: login → accesso spedizioni assegnate → upload PDF/foto POD |
| VIN-level tracking durante trasporto | 🟡 Parziale | B | Serial number tracking nativo; aggiungere stati custom (in transit, delivered, damaged) per VIN |
| Transport damage reporting durante PDI | 🔴 Gap | B | Campo danno su PDI form; collegamento a spedizione/transporter; notifica manuale (no auto-claim per ora) |
| Percorsi: PVPL→Dealer, Dealer→SubDealer, Dealer↔Dealer, Dealer→Customer | 🟡 Parziale | C | Multi-route via `stock.route`; location hierarchy dealer/sub-dealer; inter-company per dealer diversi |
| TICL / Dispatch POD report | 🔴 Gap | B | Report PDF custom da picking con TICL number, VIN list, transporter, firma |

---

## 10. Financial & Compliance (India GST + Tally)

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `account` | Core contabilità |
| `l10n_in` | GST India (CGST, SGST, IGST, UTGST) |
| `l10n_in_edi` | E-invoicing IRN (GSTIN → IRP) |
| `l10n_in_edi_ewaybill` | E-way bill (trasporto merci India) |
| `account_accountant` | Reconciliation, journal avanzati |
| `account_tax_python` | Tax con formula Python (per tax dependencies complesse) |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| GST multi-tipo (CGST/SGST/IGST/UTGST) su tutti i flussi | ✅ Nativo (`l10n_in`) | A | Configurare tax group per tipo transazione (veicolo, spare, service) |
| HSN code su prodotti | ✅ Nativo | A | Campo HSN su `product.template` (già in `l10n_in`) |
| Tax Dependencies (GST cascata, esclusioni) | 🟡 Parziale | C | `account_tax_python` per formule; complessità alta su tax dependencies PVPL-specific |
| E-invoicing IRN (GSTIN obbligatorio) | ✅ Nativo (`l10n_in_edi`) | B | Configurare per ogni dealer company; test con sandbox GST portal |
| E-way bill su spedizioni veicoli | ✅ Nativo (`l10n_in_edi_ewaybill`) | B | Attivare e configurare soglie |
| Statutory reports obbligatori India | 🟡 Parziale | C | GSTR-1, GSTR-3B nativi; altri report statutory da identificare in BBP e sviluppare |
| Tally integration (bridge custom) | 🔴 Gap | D–E | Invoice Odoo → web service Tally; autenticazione + handshake per versioni 6.x, 7.0, ERP 9; gestione errori e retry; voucher mapping (vendita, acquisto, pagamento) |
| Tally: categorizzazione transazioni in Tally post-sync | 🔴 Gap | D | Logica mapping account Odoo → ledger Tally; da validare dealer per dealer (ogni dealer ha COA Tally propria) |
| Multi-currency | ✅ Nativo | A | Attivare; rate da ECB o fonte India RBI |
| Financial data security (DPDPA India) | 🟡 Parziale | B | Odoo data access controls + audit log; verificare compliance DPDPA 2023 |
| Historical tax restoration (storico modifiche aliquote) | 🟡 Parziale | B | Tax `lock_date` + `price_include` history; custom report storico aliquote per periodo |
| **Financial Year change** + numerazione per outlet (KPMG Q-26) | 🟡 Parziale | C | `ir.sequence` nativo non basta: serve sequenza custom con schema `[prefisso][YY][outlet][seriale]` (es. `DI25000000006`, `DIEV25...`), reset annuale **a livello outlet** post-consenso dealer ad Aprile, con finestra di registrazione nel FY precedente (data 31-March). Prefissi distinti ICE/EV e per tipo documento. |
| Report obbligatori year-end (Annual Day book, stock, GST, taxation per outlet) | 🟡 Parziale | C | GSTR nativi; Annual Day book e report stock/taxation per dealer-outlet da sviluppare |

---

## 11. Credit Management

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `account_credit_control` | Credit limit base |
| `sale_management` | Blocco ordine su credito |
| `account` | Saldo partite aperte |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Credit limit check automatico su ordine | 🟡 Parziale | C | `account_credit_control` base; custom per: soglia da SAP (non da Odoo), sync periodica, blocco hard su SO confirmation |
| Sync periodica saldo credito da SAP ERP | 🔴 Gap | E | Job schedulato (cron Odoo) → API SAP → update `res.partner.credit_limit` + `balance`; gestione errori |
| Blocco ordine se credito insufficiente | 🟡 Parziale | B | Override `_action_confirm` su `sale.order`; messaggio errore con saldo attuale |
| Approvazione eccezione credito (manager PVPL) | 🔴 Gap | C | Workflow approvazione su SO bloccato: notifica area manager PVPL → sblocco manuale con nota |
| Real-time credit visibility per dealer | 🟡 Parziale | B | Dashboard dealer: saldo disponibile, ordini pending, scaduto; dati da ultima sync SAP |
| Overdue payment workflow + blocco | 🔴 Gap | B | Regola: fatture scadute > X giorni → blocco automatico nuovi ordini + notifica email dealer + PVPL |

---

## 12. Mobile Applications

> **Nota**: Odoo ha app mobile nativa (Odoo Mobile) ma non copre i casi d'uso automotive specifici PVPL. Richiede sviluppo app dedicata o estensione PWA.
>
> **App attuale = PLMS (KPMG Q-18)**: copre **solo enquiry generation** ed è outsourced a vendor → **nessun riuso**, va rifatta da zero insieme alle app spare/service. Business logic **diversa tra CV e 2W** → prevedere parametrizzazione per business line. Customer self-service app (booking, service status, history, warranty, accessori stock) è in scope.

### Gap Analysis & Custom

| Applicazione | Copertura Odoo | Effort | Stack consigliato |
|---|---|---|---|
| Spare Parts mobile (dealer, ASC, PGO) — stock lookup, ordini, sync SAP | 🔴 Gap | D | Progressive Web App (PWA) su Odoo + API JSON-RPC; offline via service worker |
| Service mobile (job card, appointment, service history) | 🔴 Gap | D | PWA o app nativa (React Native / Flutter) con Odoo backend |
| **Offline support** per aree con connettività limitata | 🔴 Gap | D | Service worker + local storage → sync quando online; complessità alta, testare con dealer rurali |
| Telematics mobile app (customer, dealer, PVPL) | 🔴 Gap | D–E | App che consuma API telematics + dati CDMS; fuori dal core Odoo |
| PVPL team access su spare/service app per territorio | 🔴 Gap | C | Role-based view nell'app: PVPL vede tutti i dealer del territorio |
| Push notifications (Firebase) | 🔴 Gap | C | Integrazione Odoo → Firebase Cloud Messaging per notifiche app mobile |

---

## 13. Customer Self-Service Portal

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `portal` | Framework portale customer Odoo |
| `website` | CMS e UI base |
| `appointment` | Prenotazione appuntamenti online |
| `survey` | CSI feedback post-service |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Service appointment booking online | 🟡 Parziale (`appointment`) | B | Configurare slot per dealer; aggiungere selezione veicolo (VIN) e tipo servizio |
| Service status tracking real-time | 🔴 Gap | C | Vista portale che espone stato job card (ricevuto → in lavorazione → pronto → consegnato); aggiornamento real-time via WebSocket o polling |
| Service history per cliente / VIN | 🟡 Parziale | B | Vista portale su `mrp.repair` filtrata per customer + VIN |
| Warranty claim status tracking | 🔴 Gap | B | Vista portale su `pvpl.warranty.claim` con stato e importo |
| Accessori / spare parts stock info | 🔴 Gap | B | Vista catalogo filtrata per modello veicolo + disponibilità magazzino dealer |
| Mobile-first UI (branding Piaggio) | 🟡 Parziale | C | Odoo website responsive; customizzazione CSS/theme per brand Piaggio; usability review obbligatoria |
| Multi-channel: SMS + email + push | 🟡 Parziale | C | SMS (`sms`), email (`mail`) nativi; push notification richiede integrazione Firebase |

---

## 14. Reporting & Analytics

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `report` | PDF report engine (QWeb) |
| `spreadsheet_dashboard` | Dashboard Odoo Spreadsheet |
| `web_studio` | (opzionale) Custom view/report no-code |
| `bi_view_editor` | Custom BI views |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Report operativi standard (retail, enquiry, stock, job card) per giorno/mese/anno/territorio | 🟡 Parziale | C | Modelli nativi estendibili; custom per KPI PVPL, filtri territorio, BU, dealer, comparativo periodo |
| Statutory reports India (GSTR, etc.) | 🟡 Parziale | C | GSTR-1 e GSTR-3B nativi; altri da sviluppare in BBP |
| Dashboard PVPL (KPI consolidati per area manager) | 🔴 Gap | C | Odoo Spreadsheet o custom dashboard con aggregazione multi-dealer per territorio |
| Dealer dashboard (stock, credito, claim status) | 🔴 Gap | B | Vista filtrata per dealer; dati da sync SAP + Odoo |
| Report SQI audit per dealer nel tempo | 🔴 Gap | B | Vista storico `pvpl.sqi.audit` con trend |
| Reporting in periodo coesistenza (legacy + Odoo) | 🔴 Gap | C–E | Layer ETL verso data warehouse neutro (SAP Analytics o equivalente) se coesistenza > 90 giorni |
| Advanced BI / Analytics (Wave 2) | 🔴 Gap | E | Integrazione con SAP Analytics Cloud o Power BI tramite Odoo Data Export API |

---

## 15. Integrations (SAP + Tally + Telematics)

> **Hub**: SAP Integration Suite gestisce tutti i flussi. Odoo espone API REST (JSON-RPC + OpenAPI). SAP Integration Suite mappa e orchestra.

### Gap Analysis & Custom

| Integrazione | Direzione | Effort | Dati / Trigger |
|---|---|---|---|
| **SAP ERP → Odoo**: credit limit dealer | SAP → Odoo | E + B | Sync periodica (cron); `res.partner` credit fields aggiornati |
| **Odoo → SAP ERP**: financial settlement warranty | Odoo → SAP | E + C | Claim approvato → credit note / pagamento dealer in SAP |
| **Odoo → SAP ERP**: ordini wholesale | Odoo → SAP | E + B | Sale order confermato → ordine SAP per financial |
| **SAP PWM → Odoo**: warranty eligibility | Odoo → SAP PWM (sync) | E + C | API check per VIN + intervento; risposta real-time integrata nel claim form |
| **Tally ← Odoo**: invoice sync (tutti i dealer) | Odoo → Tally | D + E | Invoice validata → web service Tally; gestione multi-versione (ERP 9, 6.x, 7.0) |
| **Telematics → Odoo**: dati selettivi | Telematics → Odoo | E + B | Odometer, health alerts, service triggers → `pvpl.vehicle.telematic` model; update VIN record |
| **E-Catalogue → Odoo** (Wave 2) | Esterno → Odoo | E | Post-KeyTech dismissal; da pianificare in Wave 2 |
| **SAP Integration Suite**: middleware hub | Bidirezionale | E | Tutti i flussi passano per CPI; Odoo è spoke; standard REST/JSON |
| **Firebase**: push notifications mobile | Odoo → Firebase | C | Evento Odoo (job card pronto, appuntamento reminder) → Firebase → app |

---

## 16. Data Migration

### Sorgenti legacy (KPMG Q-07/Q-13/Q-14)

| Sorgente | Tecnologia | Dati | Estrazione |
|---|---|---|---|
| CDMS legacy | **SQL Server** | Master + transazionale principale | **Nessun export format predefinito** → cooperazione vendor attuale obbligatoria |
| Oracle / D2K | Oracle DB (.net injected) | Warranty CV, PDI, FSC, dettagli EV | SQL diretto (minor tweaking), **no API** |
| Tally | TallyPrime 6.x/7.0 + ERP 9 | Contabilità dealer | Web services / bridge (per dealer) |

### Volumi record per oggetto (KPMG Q-12)

| Oggetto | Record (~) | | Oggetto | Record (~) |
|---|---|---|---|---|
| Service invoice | **33.394.200** | | Quotation | 3.289.881 |
| Spare Billing | **18.628.596** | | Vehicle Billing | 2.947.119 |
| Spare Invoice | 5.479.488 | | Vehicle sales invoice | 2.751.798 |
| Enquiry | 3.378.398 | | POD / TICL | 405.557 |

> Service invoice (~33,4M) e Spare Billing (~18,6M) dominano l'effort ETL.

### Tool e approccio Odoo

| Strumento | Uso |
|---|---|
| Odoo Import (CSV/XLS) | Master data semplici (partner, product, pricelist) |
| Odoo ORM / `base_import` | Import batch via script Python |
| Custom ETL scripts (Python + `xmlrpc`) | Transazionali complessi (job card, ordini, fatture storiche) |
| Connettori sorgente: `pyodbc`/`SQLAlchemy` (SQL Server) + `cx_Oracle`/`oracledb` (Oracle) | Estrazione diretta da legacy multi-DB |
| Staging database Odoo | Ambiente dedicato per mock migration e validazione |

### Gap Analysis & Custom

| Requirement | Copertura | Effort | Note |
|---|---|---|---|
| ETL multi-sorgente: CDMS SQL Server + Oracle/D2K + Tally ERP 9 | 🔴 Gap | D | Nessun connettore nativo; script Python custom per estrazione + mapping + caricamento Odoo; **3 sorgenti distinte** |
| Estrazione CDMS legacy senza export format (dipendenza vendor) | 🔴 Gap | D | Nessun export predefinito → ingaggio vendor attuale per estrazione e matching dati (KPMG Q-14); rischio contrattuale/tempistico |
| Data cleansing & standardization | 🔴 Gap | D | Pipeline cleansing con regole PVPL (deduplica anagrafica, normalizzazione VIN, codici GST) |
| 8 anni storico transazionale (~2 TB da migrare su 3,5 TB totali) | 🔴 Gap | D | Migrazione per batch dealer; storico pre-8 anni in archivio read-only |
| Mock migration (almeno 2 run per dealer) | 🔴 Gap | D | Ambiente staging Odoo dedicato; script ripetibili; UAT di validazione dati |
| Storico read-only post-cutover | 🔴 Gap | C | Viste Odoo in sola lettura su tabelle archivio; o accesso al vecchio sistema in readonly per X mesi |
| Parallel run / cutover per-dealer | 🔴 Gap | C | Procedura standard: freeze transazioni legacy → migration run finale → go-live → validazione → retire |
| Riconciliazione dati post-migrazione | 🔴 Gap | C | Script di reconcile: count record, hash check su dati critici (VIN, invoice amount totals) |

---

## 17. Change Management & Training

### Moduli Odoo
| Modulo | Scopo |
|---|---|
| `survey` | Evaluation criteria / feedback form |
| `elearning` | (opzionale) Training material hosting |
| `portal` | Accesso dealer ai materiali |

### Gap Analysis & Custom

| Requisito | Copertura | Effort | Note |
|---|---|---|---|
| Training Needs Analysis | 🔴 Gap | B | Deliverable Avvale; survey + interviste KU PVPL |
| Training material (slide, esercizi, video) | 🔴 Gap | C | Produzione contenuti per profilo utente (dealer owner, service advisor, DSE, parts manager, PVPL) |
| Virtual classroom (PVPL HQ + Dealer Champions) | 🔴 Gap | B | Teams / Zoom + Odoo demo environment |
| Adoption Enablement Toolkit (auto-formazione dealer) | 🔴 Gap | C | Video guide, quick reference card, FAQ per ogni modulo; distribuiti via SharePoint o portale |
| Helpdesk post go-live | 🔴 Gap | C | Odoo `helpdesk` configurato per ticketing; SLA risposta per livello dealer; FAQ self-service |
| Feedback / evaluation post-training | 🟡 Parziale (`survey`) | A | Survey Odoo nativa |
| Train-the-Trainer per utenti interni | 🔴 Gap | B | Sessioni dedicate su PVPL KU che poi formano dealer champion |

---

## 18. Riepilogo Effort Complessivo

### Volume custom per tipo

| Tipo | Sigla | Stima moduli/feature |
|---|---|---|
| Configuration only | A | ~15 |
| Minor customization | B | ~35 |
| Major customization | C | ~40 |
| Custom development | D | ~20 |
| Integration (third-party) | E | ~12 |

### Aree ad alto rischio implementativo

| Area | Rischio | Motivazione |
|---|---|---|
| Tally Bridge | 🔴 Alto | Multi-versione Tally, logica custom bridge, COA diversa per dealer |
| Job Card / Service | 🔴 Alto | Nessun modulo Odoo aderente al 100%; rischio scope creep |
| Warranty (SAP PWM) | 🔴 Alto | Dipendenza su SAP PWM non ancora definita in dettaglio (Q10, Q11) |
| Credit sync SAP | 🟡 Medio | Logica sync + blocco ordine; rischio dati stale in coesistenza |
| Mobile + Offline | 🟡 Medio | Fuori dal core Odoo; effort alto, testing su connettività India |
| Data Migration 3,5 TB | 🔴 Alto | Qualità dati legacy sconosciuta; **3 sorgenti** (SQL Server, Oracle/D2K, Tally multi-versione); 8 anni storico; volumi dominanti Service invoice ~33,4M + Spare Billing ~18,6M |
| Dipendenza vendor legacy | 🔴 Alto | CDMS SQL Server senza export format → estrazione subordinata a cooperazione vendor attuale (KPMG Q-14) |
| FY change / numerazione per outlet | 🟡 Medio | Sequenze custom con reset annuale per outlet, prefissi ICE/EV, finestra cross-FY (KPMG Q-26) |
| Licensing utenti | 🟡 Medio | ~42.700 nominali vs ~4.000 concurrent → modello licenza da definire con Odoo |
| Rollout scaglionato coesistenza | 🔴 Alto | 9 punti critici identificati — vedi `CDMS_Piaggio_Project_Notes.md` §5 |
| SQI Audit module | 🟡 Medio | Custom dev completo; logica scoring da definire con PVPL |
| VIN tracking cross-system | 🟡 Medio | Protocol da progettare; rischio gap durante coesistenza |

### Moduli Odoo Enterprise — Lista Completa Raccomandata

```
# Core
base, base_setup, mail, web, auth_totp

# CRM & Sales
crm, sale_crm, sale_management, sale_stock, utm, website_crm

# Finance & India
account, account_accountant, account_credit_control, account_tax_python
l10n_in, l10n_in_edi, l10n_in_edi_ewaybill

# Inventory & Manufacturing
stock, mrp_repair, purchase, inventory

# HR & Scheduling
hr, calendar, appointment

# Service
helpdesk, survey

# Portal & Website
portal, website, elearning

# Reporting
report, spreadsheet_dashboard

# SMS & Communication
sms, mass_mailing

# (Opzionale)
web_studio, bi_view_editor
```

> **Totale stimato moduli nativi attivati**: ~30–35
> **Custom modules da sviluppare**: stimare 8–12 moduli custom Odoo
> **Integrazioni esterne**: 5 (SAP ERP, SAP PWM, Tally, Telematics, Firebase)
