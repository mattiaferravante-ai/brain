# PVPL India — CDMS Project Notes
> Odoo Functional Consultant Reference | Avvale S.p.A. | Last updated: 2026-06-22
>
> **Fonti Q&A**: RFP Q&A AVVALE (`CDMS_India_Q&A-v2.xlsx`) + Q&A "Set 1" altro fornitore **KPMG** (`CONFIDENTIAL - ICT_INTERNATIONAL_PVPL_CDMS QA_2026_05_15_v1.xlsx`, domande 15-May, risposte PVPL 27-May-2026).

---

## 1. Contesto Progetto

| Campo | Valore |
|---|---|
| Cliente | Piaggio Vehicles Pvt. Ltd. (PVPL) — India |
| Acronimo soluzione | cDMS (customer Dealer Management System) |
| Piattaforma proposta | Odoo Enterprise |
| Hosting | TBD: Odoo.sh **o** Azure Piaggio (come Dealer Websites) — ancora aperto (Q01) |
| Perimetro | 2W (due ruote) + CV (commercial vehicles) |
| Business Lines | B2C dealer retail + B2B wholesale dealer↔PVPL + inter-dealer |
| Numero dealer | **~420** (CV ~295, 2W ~125) — fonte KPMG Q-04 |
| Layer integrazione | **SAP Integration Suite** (hub centrale) |
| ERP centrale | SAP S/4HANA (crediti, financial settlement, warranty SAP PWM **come TO-BE**) |
| Contabilità dealer | **Tally Prime** (versioni 6.0, 6.1, 7.0 + ERP 9) — via web services custom bridge |
| Onde di rilascio | Wave 1 (must-have go-live) + Wave 2 (enhancement / nice-to-have) |

### 1.1 Landscape Legacy AS-IS (da Q&A KPMG)

> Importante per scope migrazione e integrazioni. Il legacy non è un sistema unico ma un insieme di applicazioni eterogenee.

| Sistema legacy | Tecnologia | Dominio dati | Accesso dati |
|---|---|---|---|
| **CDMS legacy** | **SQL Server** | Master + transazionale (customer, dealer, vehicle, sales/purchase) | Nessun export format predefinito → serve cooperazione vendor attuale (KPMG Q-14) |
| **Oracle / D2K** | Oracle DB (programmi .net iniettati) | **Warranty CV, PDI, FSC**, dettagli EV | SQL query diretta possibile (minor tweaking lato Oracle); **nessuna API** su Oracle né su dblink server (KPMG Q-07, Q-13) |
| **Tally** | TallyPrime 6.0/6.1/7.0 + ERP 9 | Contabilità dealer (per istanza dealer) | Web services + "CDMS-Tally bridge" custom (auth + handshake) |
| **PLMS** | App mobile outsourced | Solo enquiry generation | Da rifare da zero nel nuovo scope (KPMG Q-18) |

**Flussi dati legacy rilevati (KPMG Q-07)**:
- `CDMS (SQL Server) → dblink (SQL Server) → Oracle` (insert via programma .net nel DB Oracle)
- Eccezione: accesso diretto a dettagli da Oracle DB via query Oracle
- EV: `Oracle → (.net program in SQL DB) → dblink → CDMS (SQL Server)`

> 🔴 **Impatto migrazione**: Warranty CV / PDI / FSC vivono su **Oracle/D2K**, non sul CDMS SQL Server. La pipeline di migrazione deve avere **due sorgenti distinte** (SQL Server + Oracle), entrambe senza API → estrazione via SQL diretta + dipendenza dal vendor legacy per il CDMS SQL Server.

---

## 2. Volumi e Sizing

### 2.1 Utenti

| Metrica | Valore | Fonte |
|---|---|---|
| Concurrent users (prime time 11-12:30 / 15:30-17:30) | **3.500–4.000** | AVVALE Q02 |
| Concurrent users (normal time) | 2.000–2.500 | AVVALE Q02 |
| Incremento fine mese (ultimi 2 giorni) | +35–40% su entrambe le fasce | AVVALE Q02 |
| **Utenti nominali Dealer** (3S/2S/1S, tutti gli outlet, attivi+inattivi) | **~41.880** | KPMG Q-16 |
| **Utenti nominali PVPL** (2W + CV, attivi+inattivi) | **~834** | KPMG Q-16 |
| **Totale utenti nominali** | **~42.700** | KPMG Q-16 |

> ⚠️ **Sizing critico**: 4.000 concurrent users su Odoo.sh è un limite architetturale rilevante. Verificare il piano Odoo.sh Enterprise più alto disponibile e valutare se Azure Piaggio non sia obbligatorio per performance.
>
> 💡 **Licensing**: ~42.700 utenti nominali (vs 4.000 concurrent) impatta direttamente il modello di licenza Odoo Enterprise (named vs concurrent) — da chiarire con Odoo. PVPL non fornisce bifurcation per tipo utente sui concurrent (AVVALE Q02).

### 2.2 Database e Storico

| Metrica | Valore | Fonte |
|---|---|---|
| DB completo (2W + CV, 26-May-2026) | **3,5 TB** | AVVALE Q03 / Q31 |
| Stima DB da migrare (2W + CV) | **~2 TB** | AVVALE Q03 / Q31 |
| Storico | **8 anni** (da confermare con Legal — mantenimento completo per contenzioso) | AVVALE Q03 |

### 2.3 Transazioni giornaliere (media/giorno) — breakdown CV vs 2W (AVVALE Q04)

| Transazione | CV | 2W | Totale |
|---|---|---|---|
| Vehicle order | ~75 | *modulo non usato attualmente* | ~75 |
| Spare order | ~53 | ~33 | ~86 |
| Enquiry | ~524 | ~425 | ~949 |
| Vehicle sale invoice | ~284 | ~107 | ~391 |
| Job card | ~3.641 | ~2.568 | ~6.209 |
| Service invoice | ~2.518 | ~2.050 | ~4.568 |
| Counter sale invoice | ~176 | ~534 | ~710 |
| TICL / Dispatch POD | ~75 | ~41 | ~116 |
| Inter-dealer tx / mese | — | — | ~1.500 |

> ⚠️ **Nota 2W**: il modulo *vehicle order* per 2W **non è attualmente usato** (AVVALE Q04) → verificare in BBP se il TO-BE deve introdurlo o se l'ordine veicolo 2W resta fuori scope.

### 2.4 Volumi record per oggetto (migrazione) — KPMG Q-12

> Conteggio indicativo dei principali oggetti transazionali da migrare ("All business-relevant and operationally required data"). Numeri in notazione internazionale.

| Oggetto | Record (~) |
|---|---|
| Service invoice | **33.394.200** |
| Spare Billing | **18.628.596** |
| Spare Invoice | 5.479.488 |
| POD / TICL documents | 405.557 |
| Enquiry | 3.378.398 |
| Quotation | 3.289.881 |
| Vehicle Billing | 2.947.119 |
| Vehicle sales invoice | 2.751.798 |

> 🔴 **Driver di effort migrazione**: Service invoice (~33,4M) e Spare Billing (~18,6M) dominano il volume. Sono questi due oggetti a dimensionare la pipeline ETL e i tempi di mock migration, non gli ordini veicolo.

---

## 3. Mappa Requisiti per Area (Wave 1 must-have)

### Master Data & Entities
- Dealer / Sub-dealer / Broker / Outlet hierarchy (sub-dealer tipicamente sotto un solo dealer — rarissimi casi multi-dealer)
- Sales Territories, Business Units, Departments
- Vehicle & Spare Parts Catalog centralizzato
- Pricing & Discount Management (% o importo, per cliente o dealer)
- RTO Registration master data (compliance India)
- SLA & Customer Feedback master

### Pre-Sales & Sales
- Lead → Quotation → Order → Invoice (B2C + B2B)
- Monthly Order Plan (MOP) con rilascio ordini al ricevimento pagamento dealer
- Sales Employee management (DSE, DSM)
- Wholesale + Inter-dealer (ordini, stock, approvazioni)
- SRN (Stock Receipt Note)
- Subsidy EV (nazionale e statale)
- EV-related checks (da dettagliare — Q45 aperta)
- RTO registration

### Service
- Job Card digitale end-to-end (apertura → chiusura → fattura)
- PDI (Pre-Delivery Inspection) con checklist obbligatoria
- Free Service Coupon (FSC) con validità giorni/km
- SQI (Service Quality Index) audit module
- Field Service Management (recall, campagne tecniche)
- Appointment scheduling (proposta automatica, conferma advisor)
- Goodwill claim generation & settlement
- Superbike workflow separato

### After-Sales & Warranty
- **AS-IS**: Warranty **CV** gestita su **Oracle / D2K** legacy (insieme a PDI e FSC CV) — sorgente per migrazione (KPMG Q-07, Q-13)
- **TO-BE**: Warranty eligibility su **SAP PWM (S/4HANA)** — roll-out della soluzione PWM esistente anche in India (Q10)
- Multi-tier warranty categorization
- Approval workflow (livelli da definire in BBP — Q11)
- Automated settlement → SAP ERP
- Dealer Claims Portal digitale

### Spare Parts
- Tipologie ordine: VOR (Vehicle Off Road), SOR (Standard Order Replenishment), counter sale
- SOR: ripetizione automatica per i 2 mesi successivi del trimestre (attualmente solo 2W → da estendere a CV)
- VOR/warranty claim orders: **priorità più alta** sull'allocazione inventario
- TAT discrepancy claims: **90 giorni**
- Foto obbligatorie per damaged parts claims
- E-Catalogue (KeyTech): **da dismettere in 2-3 anni** → nessuna integrazione pianificata, futura integrazione con nuova piattaforma

### Transporter & Logistica
- Tracking VIN-level (non solo shipment/batch)
- POD upload da **trasportatori** (non da PVPL)
- Percorsi: PVPL→Dealer, Dealer→SubDealer, Dealer↔Dealer, Dealer→Customer
- PDI transport damage → notifica manuale (nessun trigger automatico per ora)

### Financial & Compliance
- GST compliance (India): HSN codes, tax dependencies
- Tally bridge: dealer genera invoice in CDMS → sync a Tally via web service custom
- Credit management: check automatico su SAP ERP al momento ordine; **sincronizzazione periodica** (non real-time — Q22)
- Multi-currency (India regulations)
- Statutory reports obbligatori (da mappare in BBP)
- **Financial Year change** (KPMG Q-26): reset della serie di numerazione per ogni FY, a livello **outlet**
  - Schema numerazione: `[prefisso doc][YY anno solare][NN outlet][NNNNNNN seriale]` — es. `DI25000000006` (DI = ICE Dealer vehicle Invoice), `DIEV25000000006` (DIEV = EV Dealer vehicle Invoice)
  - Anno solare + seriale si resettano dopo **consenso del dealer ad Aprile**; fino ad allora il dealer può ancora registrare nel FY precedente con data 31-March
  - Report obbligatori a fine anno (livello dealer-outlet): stock veicoli/spare, **Annual Day book**, GST, taxation, ecc.

### Integrations
- **SAP Integration Suite** come middleware hub
- SAP ERP: real-time su credit check, periodico su balance
- SAP PWM: warranty eligibility
- Tally Prime (tutte le versioni): web service custom
- Telematics: dati selettivi (vehicle health alerts, odometer, service triggers)
- E-Catalogue: TBD (fase successiva)
- KeyTech: nessuna integrazione

### Mobile & Applications
- **App attuale = PLMS** (solo enquiry generation, outsourced a vendor) → da **rifare da zero** se non nativa nel prodotto (KPMG Q-18). Logica business leggermente diversa CV vs 2W.
- Spare parts mobile app (dealer, ASC, distributors, PGO) con sync stock SAP
- Service mobile app (job card, service history, appointments) — con supporto **offline**
- E-commerce portal (no creazione ordini da esterno, ordini da BM/CDMS)
- Telematics mobile app (customer, dealer, PVPL)
- Self-Service Portal cliente (appointment, service status, warranty, accessori) — Wave 1

### Change Management & Training
- Train-the-Trainer per utenti interni PVPL
- ~10 Dealer Champions (Area Manager) per supporto territoriale
- Adoption Enablement Toolkit per dealer 1° e 2° livello (self-sustained)
- Helpdesk dedicato post go-live
- Lingua materiali: da confermare (Q41 aperta)
- Piattaforma training: proposta fornitore (Teams/SharePoint o equivalente)

---

## 4. Integrazioni — Mappa Ownership Dati (da finalizzare in BBP)

| Dominio | System of Record (TO-BE) | Sorgente legacy (AS-IS / migrazione) | Note |
|---|---|---|---|
| Credito dealer | SAP ERP | SAP ERP | Sync periodica verso CDMS |
| Warranty eligibility | SAP PWM (S/4) | **Oracle/D2K** (warranty CV) | TO-BE: real-time check da CDMS; AS-IS CV su Oracle → migrazione via SQL diretto |
| PDI / FSC (CV) | CDMS (Odoo) | **Oracle/D2K** | Migrazione via SQL diretto da Oracle (KPMG Q-13) |
| Contabilità dealer | Tally Prime | Tally Prime | CDMS → Tally (bridge custom) |
| Anagrafica veicoli / parti | CDMS (Odoo) | CDMS legacy (SQL Server) | Feed da SAP catalogo |
| Ordini / enquiry / invoice dealer | CDMS (Odoo) | CDMS legacy (SQL Server) | → SAP per financial; estrazione legacy senza export format → dipende dal vendor (KPMG Q-14) |
| Dettagli EV | CDMS (Odoo) | **Oracle/D2K** → SQL DB → CDMS | Flusso EV passa da Oracle (KPMG Q-07) |
| Telematics | Piattaforma telematics | — | Feed selettivo a CDMS |
| E-Catalogue (futura) | Nuova piattaforma (post KeyTech) | — | TBD |

> ⚠️ **Q28 ancora aperta**: ownership per customer, product, orders non ancora definita formalmente. Da chiudere **prima** del BBP.

---

## 5. PUNTI CRITICI — Coesistenza Vecchio/Nuovo Sistema (Dealer Rollout Scaglionato)

Questo è il rischio operativo principale della fase di go-live. Quando alcuni dealer sono già su Odoo/nuovo CDMS e altri sono ancora sul legacy, si creano le seguenti frizioni:

### 5.1 Inter-Dealer Transactions (~1.500/mese)
**Problema**: una transazione inter-dealer coinvolge due dealer. Se uno è sul nuovo sistema e l'altro sul vecchio, la transazione non può essere gestita end-to-end su nessuno dei due.

**Opzioni**:
1. **Escludere le inter-dealer transaction tra dealer "misti"** durante la coesistenza (operativamente difficile — richiede coordinamento)
2. **Gestire via PVPL come intermediario**: PVPL riceve richiesta dal dealer new-system, la inserisce manualmente nel legacy per conto del dealer old-system
3. **Double-entry**: il dealer su Odoo registra l'uscita; l'operatore PVPL registra manualmente l'entrata nel vecchio sistema del dealer ricevente
4. **API bridge temporanea**: esporre endpoint legacy per accettare notifiche di transazioni inter-dealer — tecnicalmente costoso

> 🔴 **Raccomandazione**: definire una **policy chiara in BBP** su chi può fare inter-dealer durante rollout scaglionato. Considerare che i dealer con più volume (da cui si parte) tendono a fare più inter-dealer tra loro → coordinare i cluster di go-live geograficamente.

### 5.2 Inventario e Stock a Livello VIN
**Problema**: il tracking è richiesto a **livello VIN**. Un veicolo che parte da un dealer Odoo e arriva a un dealer legacy (o viceversa) crea un gap di tracciabilità — il VIN viene "perso" al confine dei sistemi.

**Punti da presidiare**:
- Chi è responsabile di inserire il VIN nel sistema ricevente al momento del trasferimento?
- Come si gestisce il caso in cui il transporter carica il POD sul nuovo sistema ma il dealer destinatario è sul legacy?
- Riconciliazione inventario VIN al momento del cutover del secondo dealer

> 🔴 **Azione richiesta**: definire un **VIN transfer protocol** per transizioni cross-system. Probabilmente serve un registro PVPL-side che tiene lo stato di ogni VIN indipendentemente dal sistema del dealer.

### 5.3 Credit Management (SAP → CDMS sync)
**Problema**: SAP è source of truth per il credito dealer. Il nuovo CDMS legge il credito da SAP (sync periodica). Il vecchio CDMS probabilmente ha la sua logica di credit check.

- Se un dealer ha ordini su entrambi i sistemi (es. durante migrazione parziale), il credito potrebbe essere consumato doppione o non aggiornato correttamente
- La sync periodica (non real-time) amplifica il rischio durante la coesistenza

> 🟡 **Azione richiesta**: verificare se SAP mantiene un saldo credito unico per dealer indipendentemente dal sistema che lo consuma. Definire la frequenza di sync (giornaliera? oraria?) e bloccare l'ordine se sync non è avvenuta entro X ore.

### 5.4 Warranty Claims (SAP PWM)
**Problema**: Warranty eligibility è su SAP PWM. Durante la coesistenza, entrambi i sistemi fanno call a SAP PWM per validare la warranty.

- Rischio di doppia apertura claim sullo stesso VIN/intervento
- Necessità di un **claim ID univoco a livello SAP** che blocchi duplicati indipendentemente dal sistema di origine

> 🟡 **Azione richiesta**: confermare con team SAP che il claim ID in PWM è generato centralmente e che il sistema blocca duplicati per VIN + tipo intervento + data.

### 5.5 Tally Integration (Contabilità Dealer)
**Problema**: ogni dealer ha la sua istanza Tally. Il bridge CDMS→Tally genera i record contabili. Durante la coesistenza:

- I dealer sul **vecchio CDMS** continuano a generare i loro record Tally dal vecchio sistema
- I dealer sul **nuovo Odoo CDMS** useranno il nuovo bridge
- Nessun problema in sé **se il bridge è dealer-specifico** (che normalmente è)
- Rischio se ci sono dealer che hanno transazioni su entrambi i sistemi nella stessa giornata (es. migrazione a metà giornata)

> 🟡 **Azione richiesta**: definire la **cutover window** a livello dealer come inizio giornata contabile (no mid-day cutover). Garantire che l'ultimo voucher del vecchio sistema e il primo del nuovo usino numerazioni Tally non sovrapposte.

### 5.6 SOR Orders (Ripetizione Trimestrale)
**Problema**: gli ordini SOR si ripetono automaticamente per i 2 mesi successivi del trimestre. Se un dealer fa il go-live a metà trimestre, ha ordini SOR già generati nel vecchio sistema.

- Rischio di duplicazione (vecchio sistema genera automaticamente il mese 2, nuovo sistema pure)
- Necessità di "chiudere" il ciclo SOR nel vecchio sistema prima del go-live del dealer

> 🟡 **Azione richiesta**: includere nella **go-live checklist per-dealer** la verifica e chiusura di tutti i SOR attivi nel vecchio sistema.

### 5.7 Reporting e KPI Consolidati
**Problema**: durante la coesistenza, i KPI di PVPL (retail, stock, job card, service invoice) provengono da due sistemi diversi. I report consolidati sono impossibili se non si costruisce un layer di aggregazione.

**Opzioni**:
1. **Report separati** per periodo di coesistenza (accettabile se breve)
2. **ETL verso data warehouse neutro** (SAP Analytics o equivalente) che aggrega da entrambi i sistemi — raccomandato se la coesistenza dura > 3 mesi
3. **Replica periodica legacy → Odoo** in sola lettura per report (tecnicamente pesante)

> 🟡 **Azione richiesta**: stimare la durata della coesistenza. Se > 90 giorni, pianificare un layer di aggregazione dati.

### 5.8 Migrazione Dati Dealer-by-Dealer
**Problema**: ~2 TB da migrare su 3,5 TB totali (8 anni). Una migrazione completa prima del go-live è impraticabile se il rollout è scaglionato.

**Approccio consigliato**:
- Migrazione **master data** (veicoli, parti, dealer, utenti) in modo centralizzato prima del Wave 1
- Migrazione **dati transazionali** dealer-by-dealer al momento del singolo go-live
- Storico pre-migrazione: accessibile in **modalità read-only** dal nuovo sistema (archivio) — come indicato da PVPL (Q03)
- **Mock migration** obbligatoria per ogni cluster prima del go-live reale (req. 14.08)

**Sorgenti dati eterogenee (KPMG Q-07/Q-13/Q-14)** — la pipeline deve gestire:
1. **CDMS legacy (SQL Server)**: master + transazionale principale. **Nessun export format predefinito** → serve cooperazione del vendor legacy attuale sia per estrarre sia per "match" durante la migrazione.
2. **Oracle / D2K**: warranty CV, PDI, FSC, dettagli EV. Estraibili via **SQL diretto** (minor tweaking lato Oracle), nessuna API.
3. **Tally** (per dealer): contabilità — versioni multiple.

**Volumi guida (KPMG Q-12)**: Service invoice ~33,4M e Spare Billing ~18,6M sono i due oggetti dominanti → dimensionano effort e finestra di migrazione.

> 🔴 **Rischio alto**: 3,5 TB con cleansing e standardizzazione richiedono un team dedicato. Non sottostimare la qualità attuale dei dati — PVPL ha dati su Tally ERP 9 (vecchissimo), CDMS SQL Server custom e Oracle/D2K. Ogni dealer potrebbe avere anomalie specifiche.
> 🔴 **Dipendenza vendor legacy**: senza export format predefiniti, l'estrazione dal CDMS SQL Server è subordinata alla collaborazione del vendor attuale → rischio contrattuale/tempistico da presidiare prima del go-live.

### 5.9 Approvazioni e Workflow Cross-System
**Problema**: alcuni workflow (inter-dealer approval, claim approval) richiedono l'approvazione di ruoli PVPL che lavorano su Odoo anche quando il dealer è sul legacy.

- PVPL key user su Odoo non vede le richieste del dealer legacy
- Serve un meccanismo (email/notifica manuale o API bridge) per portare le richieste di approvazione nel nuovo sistema

> 🟡 **Azione richiesta**: mappare tutti i workflow di approvazione che coinvolgono PVPL e verificare quale sistema li origina. Durante la coesistenza, queste approvazioni dovranno probabilmente restare sul vecchio sistema fino al cutover del dealer.

---

## 6. Q&A — Risposte Chiave Ricevute

| ID | Area | Risposta PVPL | Impatto |
|---|---|---|---|
| Q01 | Hosting | Odoo.sh **o** Azure Piaggio | Decisione architetturale da chiudere subito — impatta sizing e costi |
| Q02 | Volumi | 3.500–4.000 concurrent peak | Sizing critico per Odoo.sh |
| Q03 | Migration | 3,5 TB DB, 8 anni storico, cleansing obbligatorio | Effort elevato, team dedicato |
| Q05 | Tally | TallyPrime 6.x, 7.0 + ERP 9, via web service custom | Bridge già esistente — da replicare/migliorare |
| Q06 | KeyTech | Dismissione in 2-3 anni, no integrazione nel progetto | Semplificazione scope |
| Q09 | Inter-dealer | ~1.500/mese, approvazioni richieste | Workflow complesso, critico in coesistenza |
| Q10 | Warranty | SAP PWM (S/4) sarà la soluzione per India | Integrazione SAP obbligatoria per warranty |
| Q12 | Spare VOR | Priority alta per warranty/recall orders | Logica di prioritizzazione da implementare |
| Q13 | SOR | Ripetizione automatica 2 mesi/trimestre, da estendere a CV | Automazione + rischio duplicazione in cutover |
| Q14 | Spare TAT | 90 giorni per discrepancy claims | SLA da configurare |
| Q15 | Foto damaged | **Obbligatorie** | Campo mandatory nel form |
| Q17 | Sub-dealer | Tipicamente 1 dealer → many sub-dealer | Hierarchy semplice in Odoo |
| Q18 | VIN tracking | **A livello VIN** (non batch) | Tracking granulare obbligatorio |
| Q19 | POD | Upload da **trasportatori** | Accesso portale/app per transporters |
| Q22 | Credit | Sync **periodica** (non real-time) da SAP | Frequenza sync da definire |
| Q26 | E-commerce | Ordini **solo da BM/CDMS**, no da piattaforma esterna | Semplificazione scope integrazione |

### 6.1 Q&A altro fornitore (KPMG — Set 1, risposte PVPL 27-May-2026)

| ID | Area | Risposta PVPL | Impatto |
|---|---|---|---|
| Q-04 | Tally / Dealer | TallyPrime 7.0/6.1/6.0 + ERP 9; **dealer: CV ~295, 2W ~125 (~420 tot)**; no API, web services + bridge custom | Sizing dealer noto; conferma multi-versione Tally |
| Q-07 | Warranty CV / Oracle | Warranty CV su **Oracle/D2K**; flussi via dblink + programmi .net; **no API** su Oracle/dblink | Sorgente migrazione separata; estrazione solo SQL diretto |
| Q-12 | Migration volumes | Record per oggetto (Service invoice ~33,4M, Spare Billing ~18,6M, ecc.) | Dimensiona pipeline ETL e mock migration |
| Q-13 | Oracle data | Warranty CV/PDI/FSC su Oracle, accessibili via SQL (minor tweaking) | PDI/FSC CV migrano da Oracle, non da CDMS |
| Q-14 | Legacy export | **Nessun export format predefinito** sul CDMS legacy → serve vendor attuale | Dipendenza vendor + rischio tempistico migrazione |
| Q-16 | Users | Dealer ~41.880, PVPL ~834 (~42.700 nominali) | Impatto licensing Odoo (named vs concurrent) |
| Q-18 | Mobile | App attuale **PLMS** (solo enquiry, outsourced) → da rifare da zero; logica CV≠2W | Effort mobile pieno, no riuso PLMS |
| Q-26 | FY change | Reset serie numerazione per FY a livello outlet; schema `DI/DIEV+YY+outlet+seriale`; reset post-consenso dealer ad Aprile | Requisito custom ir.sequence per outlet/anno |

---

## 7. Q&A — Risposte Ancora Mancanti / Aperte Critiche

| ID | Area | Perché è critica |
|---|---|---|
| Q01 | Hosting | Blocca architettura e contratto infrastruttura |
| Q11 | Warranty approval levels | Blocca design workflow warranty |
| Q28 | System of Record ownership | Blocca design integrations e BBP |
| Q32 | SLA infrastruttura | Blocca architettura HA/DR |
| Q34/Q35 | Change Management — PO/KU/EU numbers | Blocca piano training |
| Q38–Q44 | Training strategy | Aperte — da sollecitare prima di finalizzare offerta |
| Q45 | EV checks | Blocca design modulo vendite EV |

---

## 8. Decisioni Architetturali da Chiudere in BBP

1. **Hosting**: Odoo.sh vs Azure Piaggio — impatta SLA, costi, governance
2. **Integration hub**: SAP Integration Suite confermato — definire API standards (REST/JSON)
3. **System of Record per dominio** (Q28): customer, product, order, warranty
4. **Frequenza sync crediti SAP→CDMS**: oraria? giornaliera?
5. **Dealer rollout order**: definire cluster geografici per minimizzare inter-dealer coesistenza
6. **Cutover strategy per-dealer**: data, orario, checklist standard
7. **Reporting in coesistenza**: layer aggregazione o report separati
8. **VIN transfer protocol** cross-system durante rollout scaglionato
9. **Tally cutover**: allineamento con chiusura giornata contabile
10. **Strategia estrazione legacy multi-sorgente**: SQL Server (via vendor) + Oracle/D2K (SQL diretto) + Tally — definire connettori e responsabilità
11. **Modello di licenza Odoo**: named (~42.700) vs concurrent (~4.000) — impatto costi rilevante
12. **Sequence management per FY/outlet** (FY change Q-26): design ir.sequence custom con prefissi DI/DIEV e reset annuale post-consenso dealer

---

## 9. Note Odoo Implementation

| Area | Odoo Support | Note tecniche |
|---|---|---|
| Multi-language | Nativo | Anche su dati (COA, spare parts) via traduzione |
| RBAC multi-role | Nativo | User role matrix da definire con Piaggio prima della config |
| MFA | Nativo | Policy sicurezza Piaggio su tutta la popolazione dealer |
| GST India | Nativo (l10n_in) | HSN codes, tax dependencies, e-invoice |
| Credit management | Parzialmente nativo | Custom per sync SAP e blocchi automatici |
| Tally bridge | Custom development | Replica/migliora bridge esistente — versioni multiple Tally |
| VIN-level tracking | Custom | Odoo tracking è a livello lot/serial — configurabile ma richiede test su volumi |
| SOR auto-repeat | Custom | Logica trimestrale + email automatica → scheduled action |
| SQI Audit module | Custom development | Non nativo |
| Inter-dealer approval matrix | Custom | Workflow approval Odoo adattabile ma richiede design |
| Warranty → SAP PWM | Integration (E) | API call a SAP PWM per eligibility check |
| Telematics feed | Integration (E) | Dati selettivi: odometer, health alerts, service triggers |

---

## 10. To-Do / Prossimi Passi Avvale

- [ ] Sollecitare risposta su Q11, Q28, Q32, Q34/Q35 prima della presentazione BBP
- [ ] Definire la **policy di rollout dealer** (cluster geografici, sequenza, criterio) con PVPL
- [ ] Progettare **VIN transfer protocol** per fase di coesistenza
- [ ] Definire **frequenza sync SAP credito** e meccanismo di hard-block su ordine
- [ ] Valutare capacity Odoo.sh per 4.000 concurrent users — eventuale proposta Azure
- [ ] Pianificare **mock migration** per almeno 2 dealer pilota prima del go-live Wave 1
- [ ] Costruire **dealer go-live checklist standard** con voce esplicita su SOR attivi e inter-dealer pending
- [ ] Chiarire warranty claim ID univocità su SAP PWM per bloccare duplicati cross-system
- [ ] Progettare **pipeline migrazione multi-sorgente** (CDMS SQL Server + Oracle/D2K + Tally); ingaggiare il vendor legacy per estrazione CDMS (no export format)
- [ ] Stimare effort migrazione sui volumi dominanti: Service invoice ~33,4M, Spare Billing ~18,6M (KPMG Q-12)
- [ ] Chiarire con Odoo il **modello di licenza** per ~42.700 utenti nominali
- [ ] Disegnare **ir.sequence per outlet/FY** con prefissi DI/DIEV e logica reset Aprile (KPMG Q-26)
- [ ] Confermare in BBP se introdurre il **vehicle order 2W** (oggi modulo non usato)
- [ ] Mappare migrazione **warranty CV / PDI / FSC da Oracle** verso modelli Odoo + SAP PWM (TO-BE)
