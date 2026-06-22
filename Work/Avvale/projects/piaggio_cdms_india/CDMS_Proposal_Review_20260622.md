# CDMS India — Review Proposta Tecnica + Q&A v2
> Avvale S.p.A. | Mattia Ferravante | 2026-06-22
>
> **Fonti analizzate:**
> - `2026_PiaggioCSpA_RFP_CDMS-India_Quesiti-AVVALE_MM-RISPOSTE PIAGGIO-v2.xlsx` — risposte PVPL alle domande Avvale
> - `01 Avvale - Piaggio - CDMs - RFP - Technnical Proposal V1_WIP.docx` — bozza proposta tecnica

---

## 1. Nuove risposte PVPL (Q&A v2)

Riepilogo delle risposte ricevute che non erano presenti nel Q&A precedente.

| ID | Area | Risposta PVPL | Cosa cambia |
|---|---|---|---|
| Q07 | AI Fraud Detection | Nessun dataset storico di frodi disponibile | L'AI fraud detection può essere solo rule-based — nessun ML reale |
| Q08 | Predictive Maintenance | Low priority, perimetro troppo ampio | Rimandato a Wave 2 |
| Q20 | PDI transport damage | Nessun trigger automatico claim/notifica | Solo registrazione manuale del danno; trigger automatico è opzione Wave 2 |
| Q21 | Customer notifications | **Tutti e 3 i canali obbligatori**: SMS + email + mobile push | Multi-channel infrastruttura da dimensionare |
| Q24 | Job card → invoicing | Conferma dealer richiesta prima di fatturare i ricambi | Nessun auto-billing; step conferma obbligatorio nel workflow |
| Q25 | Service scheduling | Approccio proposto OK ma da confermare con team service | Non chiuso — serve sign-off stakeholder service PVPL |
| Q27 | Self-Service Portal | In scope Wave 1; UI standard Odoo + branding Piaggio; mobile-first; API real-time | Nessun custom frontend; integrazione backend obbligatoria |
| Q29 | Mobile app | Da valutare in una fase successiva | Ancora aperto — native e offline non definiti |
| Q30 | Telematics | Solo dati selettivi: health alerts, odometer, service triggers — nessuna integrazione real-time legacy | Feed limitato; no overhead real-time |
| Q33 | UX/UI | Standard product interface, customizzazione limitata a branding e journey | Nessun custom UI design; Odoo standard + brand Piaggio |
| Q36 | Training method | Train-the-Trainer per interni PVPL; ICT Team esterno per territorio | Modello diverso da quanto proposto — vedi discrepanze |
| Q38 | Training approach | Approccio a 2 fasi OK; ICT Team esterno può supportare | Conferma con variante ICT team al posto dei dealer champions |
| Q39 | Dealer Champions feasibility | **"Not feasible"** — suggerito ICT Team esterno | 🔴 Discrepanza critica — vedi sezione 2 |
| Q40 | Helpdesk post go-live | No, non gestito interamente da P&C | Helpdesk condiviso; modello da definire |
| Q41 | Training language | Inglese | Nessuna localizzazione richiesta in questa fase |
| Q42 | Training platform | Teams / SharePoint OK | Nessuna piattaforma dedicata |
| Q43 | User profiles per training | Da definire in fase successiva | Non stimabile ora |
| Q44 | Third-party training | "Question not clear" | Da riformulare con esempi concreti |
| Q45 | EV-related checks | "Question not clear" | Da riformulare con esempi concreti |

---

## 2. Discrepanze — Proposta Tecnica vs Dati PVPL

### 🔴 CRITICA — Sizing utenti: 3.200 dichiarati vs 42.700 confermati

**Cosa dice la proposta** (sezione Target Architecture / Indicative Sizing):
> "approximately 1,600 dealers and sub-dealers, with an average of two named users per dealer (in the order of 3,200 dealer-side users) in addition to PVPL internal users"

**Cosa dice PVPL** (KPMG Q-16):
- Utenti nominali dealer: **~41.880** (3S/2S/1S, tutti gli outlet, attivi+inattivi)
- Utenti nominali PVPL: **~834**
- **Totale nominale: ~42.700**
- Concurrent peak: 3.500–4.000

Il delta è **13 volte** in meno rispetto ai dati confermati. Anche ragionando solo sui concurrent (3.500–4.000), il numero di utenti nominali da licenziare è comunque ~42.700.

**Impatto concreto:**
- Il modello di licenza Odoo (named vs concurrent) non è ancora chiarito con Odoo — ma se è named, stiamo parlando di ~43.000 licenze, non 3.200
- Il sizing Azure (database connections, worker nodes, storage) è sottodimensionato se calcolato su 3.200 utenti
- PVPL ha questi numeri e li confronterà con quelli nella proposta — rischio di credibilità

**Azione richiesta:** allineare i numeri nella proposta con i dati PVPL. Se si vuole ragionare su concurrent (per pricing/sizing infrastrutturale), dichiararlo esplicitamente, citare il dato PVPL (3.500–4.000 concurrent, 42.700 nominali) e spiegare perché il dimensionamento tecnico si basa sui concurrent.

---

### 🔴 CRITICA — Dealer Champions: modello di adozione rifiutato da PVPL

**Cosa dice la proposta** (Phase 2 – ADOPTION):
L'intera architettura di adozione territoriale si basa su:
- 10 Hub Dealer Champions (virtual classroom, fase CORE)
- 100 Local Dealer Champions (Adoption Enablement Toolkit, fase ADOPTION)
- 1.500 Retail Dealers in self-adoption guidata dai champions

La proposta descrive i Dealer Champions come "active contributors throughout the lifecycle of the CORE phase" e come il motore dell'adozione a cascata sul territorio.

**Cosa dice PVPL (Q39):**
> "Not feasible. The idea could be to train the ICT Team composed by external people to perform this activity"

PVPL ha rifiutato il modello. Le ragioni implicite dalla risposta e dal contesto:
- Alto turnover di personale nei dealer
- I dealer non hanno disponibilità/incentivo a supportare altri dealer
- PVPL preferisce un ICT Team esterno dedicato e formato da Avvale

**Impatto concreto:**
- La Phase 2 / ADOPTION della proposta è da riscrivere nella sua logica di propagazione
- Il ruolo dei 10 Hub Champions nella Virtual Classroom (CORE phase) sembra ancora accettabile, ma non possono essere il meccanismo di adozione scalabile
- Va ridisegnato chi forma, supporta e abilita i dealer di secondo livello

**Azione richiesta:** riscrivere la sezione ADOPTION sostituendo il ruolo dei Dealer Champions territoriali con un modello basato su ICT Team esterno formato da Avvale. Mantenere i 10 Hub Champions solo come early adopters di validazione nel CORE, non come vettori di adozione.

---

### 🟠 IMPORTANTE — Hosting: decisione presa unilateralmente

**Cosa dice la proposta** (sezione Target Architecture):
Ha già commesso la scelta di **Azure / AKS** con architettura completa: AKS, PostgreSQL managed su Azure, Front Door + WAF, ExpressRoute/VPN verso MPLS Piaggio, 4 ambienti, CI/CD pipeline. L'intera sezione è scritta come se la decisione fosse presa.

**Cosa dice il Q&A (Q01):**
> "2 options to be evaluated: Odoo.sh, Piaggio's infra on Azure (like Dealer Websites)"

Q01 è ancora formalmente aperta. PVPL non ha ancora scelto.

**Rischi:**
1. Se PVPL sceglie Odoo.sh, tutta la sezione architetturale va riscritta
2. PVPL potrebbe percepire la scelta come imposta senza consultazione
3. La proposta non dichiara esplicitamente che si tratta di un'assunzione — sembra una decisione

**Azione richiesta:** una di due strade:
- Allinearsi con PVPL sulla scelta Azure **prima della consegna** e inserire una nota che la scelta è stata concordata
- Oppure riformulare la sezione architetturale come "Architettura proposta basata su Azure (opzione raccomandata)" con un paragrafo comparativo vs Odoo.sh che motivi la raccomandazione, lasciando la decisione finale a PVPL

---

### 🟠 IMPORTANTE — Mobile/offline: escluso dalla proposta ma richiesto dall'RFP

**Cosa dice la proposta** (sezione Exclusions):
> "Native mobile application development for iOS or Android is excluded from the proposed scope"
> "Offline capabilities, advanced synchronization logic, mobile-first capabilities... excluded from the baseline scope"

**Cosa richiedono RFP e Q&A:**
- Spare parts mobile app (req. 11.x) — dealer, ASC, distributors, PGO
- Service mobile app con **supporto offline** (req. 11.x)
- Self-Service Portal cliente (Q27 — confermato in scope Wave 1)
- PLMS da rifare da zero (KPMG Q-18)
- Q29 ancora aperto ("da valutare in fase successiva")

**Il problema:**
Le exclusions contraddicono requisiti espliciti dell'RFP. Se PVPL legge le Exclusions confrontandole con i requisiti, emergerà un gap evidente. In negoziazione questo diventa uno scope dispute su chi paga lo sviluppo mobile.

**Azione richiesta:** chiarire in proposta la posizione sul mobile con una di queste opzioni:
- Definire un work package separato "Mobile Development" con effort e costi stimati (raccomandato)
- Oppure dichiarare esplicitamente che il mobile è "fuori dal perimetro Avvale / gestito da terzi designati da PVPL", allineandosi con PVPL su chi lo sviluppa
- Non si può escluderlo silenziosamente senza una posizione esplicita

---

### 🟡 MINORE — Oracle/D2K descritto come "in dismissione"

**Cosa dice la proposta** (Integration layer):
> "The legacy Oracle/D2K system is in dismission and is retained only for residual analytics and settlement feeds during transition"

**Realtà dai Q&A** (KPMG Q-07, Q-13):
Oracle/D2K è la sorgente attiva di:
- Warranty CV (non ancora su SAP PWM — il roll-out PWM India è il TO-BE)
- PDI e FSC per CV
- Dettagli EV (flusso Oracle → .net → SQL DB → CDMS)

Non è "in dismissione" nel senso che non viene usato. È attivo, ha flussi complessi (.net/dblink), non ha API, ed è una delle sorgenti primarie della migrazione. La dismissione è l'obiettivo finale del progetto, non il punto di partenza.

**Azione richiesta:** correggere la descrizione. Oracle/D2K va descritto come "sistema legacy attivo, sorgente primaria per migrazione di dati Warranty/PDI/FSC CV, in fase di dismissione progressiva nell'ambito del progetto".

---

### 🟡 MINORE — E-catalogue: integrazione citata vs no-integrazione PVPL

**Cosa dice la proposta** (Spare Parts):
> "The e-catalogue requirement is treated as an external integration capability... the CDMS will integrate with the relevant catalogue components according to the target architecture"

**Cosa dice PVPL (Q06):**
> "KeyTech will be dismissed in 2-3 years. For this reason initial willing is no integration between new CDMS and KeyTech, instead for the future we will integrate it with the new platform."

La proposta accenna a un'integrazione e-catalogue che PVPL ha già escluso per il periodo del progetto.

**Azione richiesta:** allineare il testo. Nessuna integrazione con KeyTech nel perimetro del progetto. L'integrazione futura è con la nuova piattaforma (successore di KeyTech), ed è out of scope attuale.

---

### 🟡 MINORE — Assumptions/Exclusions Training e Change Management vuote

**Cosa dice la proposta:**
Le sezioni Assumptions ed Exclusions di Training e Change Management contengono placeholder non compilati:
> "Assuzione 1", "Assunzione 2 etc", "Esclusione 1", "Esclusione 2 etc"

**Azione richiesta:** compilare usando le risposte Q36-Q43 come base. In particolare:
- Assumption: materiali in inglese (Q41); piattaforma Teams/SharePoint (Q42); ICT Team esterno come vettore territoriale (Q39); helpdesk condiviso (Q40)
- Exclusion: localizzazione materiali in lingue locali; sviluppo piattaforma training dedicata; gestione autonoma helpdesk post go-live

---

## 3. Domande da re-inviare a PVPL

Queste domande hanno ricevuto una risposta "Question not clear" e vanno riformulate.

### Q44 — Training per attori terzi (trasportatori, ecc.)
**Domanda originale:** troppo generica sul perimetro di training per soggetti non-PVPL/non-dealer.

**Riformulare come:**
> I trasportatori devono caricare il POD direttamente nel sistema (risposta Q19). Per garantire l'operatività, prevedete che Avvale fornisca materiale di training dedicato per i trasportatori (es. guida all'uso del portale POD)? Oppure il training dei trasportatori è responsabilità di PVPL/operativo team?

### Q45 — EV-related checks (req. 4.18)
**Domanda originale:** troppo tecnica e astratta per PVPL.

**Riformulare come:**
> Il requisito 4.18 cita "EV-related checks (Partially available)". Potete fornire 2-3 esempi concreti di questi check? Ad esempio: verifica che il veicolo sia nella lista approvata FAME/EMPS per il sussidio? Verifica Aadhaar del cliente? Verifica certificazione dealer per vendita EV? Senza esempi concreti non possiamo valutare se serve configurazione o sviluppo custom.

---

## 4. Priorità azioni prima della consegna

| Priorità | Azione | Responsabile |
|---|---|---|
| 🔴 1 | Allineare sizing utenti nella proposta (3.200 → 42.700 o spiegare la logica concurrent) | Chi scrive la proposta |
| 🔴 2 | Riscrivere Phase 2 ADOPTION senza Dealer Champions territoriali | Chi scrive la proposta |
| 🟠 3 | Chiarire con PVPL la scelta hosting (Azure vs Odoo.sh) o riformulare come raccomandazione | Mattia + PM |
| 🟠 4 | Definire posizione su mobile/offline (work package separato o esclusione dichiarata) | Chi scrive la proposta |
| 🟡 5 | Correggere descrizione Oracle/D2K (non "in dismissione" — sorgente migrazione attiva) | Chi scrive la proposta |
| 🟡 6 | Allineare testo e-catalogue con risposta Q06 (no integrazione KeyTech) | Chi scrive la proposta |
| 🟡 7 | Compilare Assumptions/Exclusions di Training e Change Management | Chi scrive la proposta |
| 🟡 8 | Re-inviare Q44 e Q45 riformulate a PVPL | Mattia |

---

*Documento creato: 2026-06-22*
