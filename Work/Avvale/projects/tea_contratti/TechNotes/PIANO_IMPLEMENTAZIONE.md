# Anagrafica Prodotti CER — Piano di Implementazione (v6)

## 1. Contesto

TEA A&E è un'azienda di smaltimento rifiuti che opera come **rivenditore**: acquista
il servizio di trattamento dagli impianti e lo rivende ai clienti con un markup.

Due file Excel descrivono l'anagrafica e il prezziario:

1. `docs/TEA_AE_Anagrafica_Prodotti_CER_v02.xlsx` — Anagrafica ufficiale (struttura,
   codici CER, sotto-tipi, impianti, combinazioni)
2. `docs/OFFERTE RIFIUTI SPECIALI_WIP2025.xlsx` — Prezziario operativo 2025 (prezzi
   d'acquisto per impianto, markup +20% A&E, minimi di fatturazione)

### Identità modulo

| Proprietà | Valore |
|-----------|--------|
| Nome tecnico | `tea_quotations` |
| Versione Odoo | 19.0 Enterprise |
| Licenza | OEEL-1 |
| Dipendenze | `['account', 'crm', 'l10n_it_edi', 'product', 'sale_crm', 'sign', 'spreadsheet_dashboard', 'uom']` |
| Schema versione | `19.0.1.4.0` (OCA semver) |

L'obiettivo è implementare questa anagrafica nel modulo Odoo 19 `tea_quotations`,
integrando con i modelli standard (product, res.partner, supplierinfo), e fornire
un sistema completo di offerte/contratti (TMB, Discarica, Rifiuti Speciali) con
generazione PDF tramite template QWeb.

---

## 2. Analisi dati Excel

Il file contiene 6 fogli:

| Foglio | Contenuto | Righe dati |
|--------|-----------|------------|
| 0_Riepilogo | Struttura gerarchica e riepilogo | — |
| 2_CER Padri (115) | L1 — Codici CER a 6 cifre | 115 |
| 3_Prod Descrizione (130) | L2 — Prodotti = CER + sotto-tipo | 130 |
| 4_Varianti (131) | L3 — Prodotti con stato fisico | 131 |
| 5_Combinazioni Listino (263) | L4 — Righe listino fornitore | 268 |
| 6_Matrice HP×Destinatario | Vincoli HP accettati per impianto | 63 impianti |

### Gerarchia prodotti

```
L1  CER Padre (es. 020104) ─────────────── tea.cer.code
 └─ L2/L3  Prodotto (es. 020104RETIS2) ─── product.template (type=service)
     └─ L4  Listino fornitore ─────────────── product.supplierinfo (esteso)
              └─ Impianto ─────────────── res.partner (esteso)
```

> **Decisione chiave — NO VARIANTI**: ogni combinazione CER+sotto-tipo+stato fisico
> è un `product.template` a sé stante (type=service). **Non** si usano
> `product.attribute`, `product.attribute.value` né `product.product` varianti.
> Lo stato fisico è un campo Selection direttamente su `product.template`.

### Entità di supporto

- **Stati Fisici** (4): campo Selection su `product.template`:
  `S1 – Solido polverulento` · `S2 – Solido non polverulento` ·
  `S3 – Fangoso palabile` · `S4 – Liquido`
- **Operazioni R/D** (12): D1, D8, D13, D14, D15, R1, R3, R4, R5, R11, R12, R13
- **Codici HP** (11): HP2 Ossidante · HP3 Infiammabile · HP4 Irritante ·
  HP5 Nocivo · HP6 Tossico · HP7 Cancerogeno · HP8 Corrosivo · HP9 Infettivo ·
  HP10 Tossico per riprod. · HP13 Sensibilizzante · HP14 Ecotossico
- **Impianti/Destinatari** (63): ciascuno con indirizzo, flag "solo non pericolosi"
  e lista codici HP accettati

### Verifica di coerenza con normativa

I dati sono stati verificati rispetto alla normativa italiana/UE:

- I codici CER seguono il Catalogo Europeo dei Rifiuti (Decisione 2000/532/CE)
- I codici HP corrispondono all'Allegato III della Direttiva 2008/98/CE
- Le operazioni R/D corrispondono agli Allegati B e C del D.Lgs. 152/2006
- I CER pericolosi sono correttamente marcati con i relativi codici HP

### Analisi Prezziario 2025 (foglio "Prezziario 2025")

Il foglio "Prezziario 2025" contiene 180 righe con la struttura operativa dei prezzi.

**Colonne:**

| Colonna | Contenuto | Esempio |
|---------|-----------|---------|
| CER | Chiave concatenata CER+sotto-tipo+SF | `020104RETIS2`, `200307DITU2` |
| Descrizione | Descrizione rifiuto | "RETI ROTOBALLE E TNT" |
| Destino | Nome impianto destinatario | "S.A.BA.R. SPA - POLO TECNOLOGICO" |
| HP Pericolo | Codici HP (solo numeri, senza prefisso HP) | "4, 5, 14" |
| IMPIANTO (Kg) | Prezzo che l'impianto applica a TEA (€/kg) | 0.23 |
| A&E +20% | Prezzo che TEA applica al cliente (€/kg) | 0.276 |
| Min Fatt. Impianto | Fatturato minimo dall'impianto (€) | 150 |
| Min Fatt. A&E +20% | Fatturato minimo di TEA al cliente (€) | 180 |

**Osservazioni chiave:**

1. **Due livelli di prezzo**: prezzo d'acquisto (impianto) e prezzo di vendita
   (A&E +20%). Il markup standard è **+20%**, ma il foglio "€ Ricarico %"
   mostra che si usano anche 5%, 10%, 15%, 25%, 30%.

2. **Fatturato minimo**: sia lato impianto che lato A&E. Questo campo non esiste
   in `product.supplierinfo` standard → va aggiunto come estensione.

3. **Prezzi speciali**:
   - `gratis` → prezzo = 0 (es. filtri olio ECOBAS)
   - Prezzi negativi → **non ammessi** (bloccati da constraint `_check_no_negative_prices`)

4. **UdM**: i prezzi sono per **Kg**, non per tonnellata. L'UdM dei prodotti
   CER sarà kg.

5. **Nessuna colonna "Operazione"**: a differenza dell'anagrafica L4, il prezziario
   non esplicita l'operazione R/D per riga. L'operazione resta informativa/normativa
   sul prodotto, ma non è dimensione del prezzo.

6. **Chiavi CER / Internal Reference**: formato concatenato senza separatori
   e senza ".0" (es. `020104RETIS2`, `160214S2`). È il formato usato internamente
   dall'azienda e nel prezziario. L'anagrafica Excel usa underscore (`020104_RETI_S2.0`)
   ma lo script di import li rimuove per generare il `default_code` canonico.

---

## 3. Scelta architetturale

### Architettura "un prodotto per combinazione" (NO varianti)

Ogni combinazione CER + sotto-tipo + stato fisico è un **singolo `product.template`**
di tipo `service`. Non si utilizzano il sistema varianti di Odoo
(`product.attribute`, `product.attribute.value`, `product.product`).

**Motivazioni:**

1. **Semplicità**: ogni prodotto CER ha un solo `default_code` univoco, un solo
   record, un solo listino. Nessuna complessità legata alla gestione varianti.
2. **Prezziario diretto**: il listino `product.supplierinfo` si collega direttamente
   al `product.template` senza passare per `product.product`.
3. **Stato fisico come Selection**: il campo `physical_state` è una semplice
   Selection sul template, non un attributo prodotto. Più leggero e immediato.
4. **Nome = codice interno**: il campo `name` del prodotto coincide con il
   `default_code` (es. `020104RETIS2`). La descrizione testuale va nel campo
   `description`.

### Integrazione con modelli standard Odoo

| Concetto di dominio | Modello Odoo | Tipo |
|----------------------|-------------|------|
| Codice CER (L1) | `tea.cer.code` | **Custom** — tabella di riferimento normativo |
| Codice HP | `tea.hp.code` | **Custom** — nessun equivalente Odoo |
| Operazione R/D | `tea.waste.operation` | **Custom** — nessun equivalente Odoo |
| Stato Fisico (S1–S4) | Campo Selection su `product.template` | **Estensione** — campo `physical_state` |
| Prodotto CER (L2/L3) | `product.template` (type=service) | **Estensione** — campi CER aggiuntivi |
| Impianto/Destinatario | `res.partner` | **Estensione** — flag `is_waste_plant` |
| Listino fornitore (L4) | `product.supplierinfo` | **Estensione** — campi rifiuti |
| Markup rivendita | `res.company` | **Estensione** — `default_markup_pct` + firma offerte |
| Offerta/Contratto | `tea.offer` | **Custom** — modello autonomo con link CRM |
| Tipo offerta | `tea.offer.type` | **Custom** — configurazione con ref a report |
| Validità offerta | `tea.offer.validity` | **Custom** — tabella configurazione validità |
| Riga CER offerta | `tea.offer.line` | **Custom** — CER + impianto + prezzi |
| Servizio aggiuntivo | `tea.offer.line.service` | **Custom** — trasporto, analisi, noleggio... |
| Produttore Allegato 2 | `tea.contract.producer` | **Custom** — riga elenco produttori |
| Opportunità CRM | `crm.lead` | **Estensione** — smart button offerte |

### Vantaggi dell'integrazione

1. **Listino fornitori standard**: `product.supplierinfo` si integra con il ciclo di
   acquisto Odoo (ordini, fatture, report)
2. **Impianti come partner**: `res.partner` consente rubrica unificata, contatti,
   integrazione contabile e gestione documenti
3. **Riuso UX**: form prodotto, ricerca fornitori, e filtri standard funzionano
   out-of-the-box
4. **Campi prezzo nascosti**: `list_price` e `standard_price` sono nascosti solo
   per i prodotti gestiti da listino fornitore (`seller_ids` valorizzato)

### Dipendenze modulo

```python
'depends': ['account', 'crm', 'l10n_it_edi', 'product', 'sale_crm', 'sign', 'spreadsheet_dashboard', 'uom'],
```

`crm` porta transitivamente `mail`, `sales_team` e altri moduli necessari.
`product` include `product.supplierinfo`.
`sale_crm` è necessario per nascondere i bottoni standard "New Quotation", "Quotations"
e "Orders" dalla vista lead CRM (sostituiti dal flusso offerte `tea.offer`).
`sign` è richiesto per i gruppi `sign.group_sign_user` nei ruoli TEA.
`spreadsheet_dashboard` è richiesto per le restrizioni menù configurazione dashboard.
`l10n_it_edi` fornisce il campo `l10n_it_codice_fiscale` su `res.partner`, usato per
distinguere persona fisica/azienda nella stampa PDF (Egregio/Spett.).

### Note specifiche Odoo 19

- Constraint SQL con sintassi `models.Constraint("UNIQUE(col)", "msg")`
  (non `_sql_constraints`)
- Filtro prodotti: `filter[@name='goods']` non `consumable` nella search view
- `supplier_rank` richiede il modulo `account`
- `uom_po_id` non esiste in Odoo 19

---

## 4. Modelli — Dettaglio (7 custom + 4 estensioni)

### 4.1 Modelli CUSTOM (7 file)

#### 4.1.1 `tea.hp.code` → `models/tea_hp_code.py`

Codici di pericolo (Hazard Property). 11 record. Nessun equivalente in Odoo standard.

| Campo | Tipo | Note |
|-------|------|------|
| `code` | Char, required, unique | es. "HP2", "HP14" |
| `name` | Char, required | es. "Ossidante", "Ecotossico" |

- Constraint SQL: UNIQUE su `code`

#### 4.1.2 `tea.waste.operation` → `models/tea_waste_operation.py`

Operazioni di recupero (R) e smaltimento (D). 12 record. Nessun equivalente Odoo.

| Campo | Tipo | Note |
|-------|------|------|
| `code` | Char, required, unique | "R1", "D1", etc. |
| `name` | Char, required | Descrizione ufficiale |
| `operation_type` | Selection(recovery/disposal), required | Tipo operazione |

- Constraint SQL: UNIQUE su `code`

#### 4.1.3 `tea.cer.code` → `models/tea_cer_code.py`

Tabella di riferimento dei codici CER (L1). 115 record. Modello custom perché
i codici CER hanno campi regolamentari (is_hazardous, hp_code_ids) che non si
mappano su `product.category` o altri modelli standard.

| Campo | Tipo | Note |
|-------|------|------|
| `code` | Char, required, unique, size=6 | es. "020104" |
| `name` | Char, required | Descrizione ufficiale CER |
| `is_hazardous` | Boolean | Rifiuto pericoloso (codice con *) |
| `hp_code_ids` | Many2many → tea.hp.code, **computed** | Codici HP — calcolati da prodotti → listino fornitore |
| `product_tmpl_ids` | One2many → product.template | Prodotti collegati |
| `product_count` | Integer, computed | Conteggio prodotti |

- Constraint SQL: UNIQUE su `code`
- Metodo `action_view_products()`: apre i prodotti filtrati per CER, con contesto
  `default_cer_id` e `default_type: service`

#### 4.1.4 `tea.characterization.sheet` → `models/tea_characterization_sheet.py`

Anagrafica delle schede di caratterizzazione. 0 record all'inizio, popolata da script
Python. Nessun equivalente in Odoo standard.

| Campo | Tipo | Note |
|-------|------|------|
| `product_tmpl_id` | Many2one → product.template, required | Prodotto CER |
| `cer_id` | Many2one → tea.cer.code, related | Da `product_tmpl_id.cer_id`, stored, per ricerca |
| `plant_id` | Many2one → res.partner (is_waste_plant), required | Impianto destino |
| `client_type` | Char, optional | Tipologia cliente (campo descrittivo per ricerca) |
| `sheet_file` | Binary, required | Scheda PDF precompilata |
| `sheet_filename` | Char | Nome file |
| `active` | Boolean | Archiviabile |

**Vincolo unicità Python** (`_check_unique_product_plant_type`): constraint
`@api.constrains("product_tmpl_id", "plant_id", "client_type", "active")` che
impedisce schede attive duplicate per la stessa combinazione Prodotto / Destino /
Tipologia Cliente. La validazione tratta `NULL` e stringa vuota in `client_type`
come equivalenti (un constraint SQL `UNIQUE` tratterebbe i NULL come valori distinti,
permettendo duplicati). Il vincolo si applica solo ai record attivi (`active=True`):
archiviare una scheda consente di crearne una nuova con la stessa combinazione.

Display name: `"Prodotto — CER — Destino — Tipologia Cliente"`.

#### 4.1.5 `tea.offer` → `models/tea_offer.py`

Offerte/Contratti per TMB, Discarica e Rifiuti Speciali. Modello custom perché
le offerte hanno stati e transizioni proprie, distinte dalla pipeline CRM.

Inherits: `mail.thread`, `mail.activity.mixin`

| Campo | Tipo | Note |
|-------|------|------|
| `lead_id` | Many2one → crm.lead, **required** | Opportunità collegata — `ondelete="cascade"`, readonly in vista |
| `partner_id` | Many2one → res.partner, **related** | Cliente (azienda) — `related="lead_id.partner_id"`, store=True, readonly |
| `contact_id` | Many2one → res.partner, **related** | Contatto (persona) — `related="lead_id.tea_contact_id"`, store=True, readonly |
| `company_id` | Many2one → res.company | Azienda |
| `offer_type_id` | Many2one → tea.offer.type | Tipo (TMB/Discarica/RS) — readonly se la lead ha tipologia |
| `offer_type_code` | Char, related | Per visibilità condizionale nelle viste |
| `lead_offer_type_id` | Many2one, related | Tipo dalla lead, per readonly condizionale in vista |
| `name` | Char | Riferimento auto-generato (es. RS/2026/0001) |
| `rs_protocol` | Char | Protocollo offerte Rifiuti Speciali auto-generato: `O` + progressivo 4 cifre + `/` + anno corrente + `/` + iniziali referente commerciale (es. `O0010/2026/NM`) |
| `offer_date` | Date | Data offerta |
| `state` | Selection | **draft / approval / approved / sent / accepted / refused_client / refused_approver** |
| `sign_request_id` | Many2one → sign.request, readonly, copy=False | Richiesta firma digitale collegata |
| `approved_by_id` | Many2one → res.users | Utente approvatore |
| `approved_date` | Datetime | Data/ora approvazione |
| `sent_date` | Datetime | Data/ora invio al cliente |
| `refused_reason` | Text | Motivo rifiuto cliente (da Odoo Sign) |
| `approver_rejection_reason` | Text | Motivo rifiuto approvatore |
| `signed_pdf` | Binary, copy=False | PDF firmato a mano (alternativa a Odoo Sign) |
| `signed_pdf_filename` | Char, copy=False | Nome file PDF firmato |
| `custom_pdf` | Binary, copy=False | PDF offerta modificata manualmente (sovrascrive il PDF auto-generato) |
| `custom_pdf_filename` | Char, copy=False | Nome file offerta caricata manualmente |
| `has_custom_pdf` | Boolean, computed | True se `custom_pdf` è valorizzato |
| `notes` | Html | Note offerta (visibile nel report PDF) |
| `internal_notes` | Html | Note interne (NON renderate nei report PDF) |

#### Upload offerta manuale (`custom_pdf`)

Il campo `custom_pdf` consente al commerciale di caricare un PDF modificato manualmente
che sostituisce il PDF auto-generato dal report QWeb. Quando `has_custom_pdf = True`,
il bottone "Apri PDF" e il flusso di firma digitale utilizzano il PDF caricato anziché
quello generato. Utile per offerte con condizioni speciali non gestibili dal template.

#### State machine offerta (`tea.offer`)

```
draft ──→ approval ──→ approved ──→ sent ──→ accepted
            │              │          │
            │              │          └──→ refused_client (se il cliente rifiuta la firma)
            │              └──→ accepted (manuale con PDF firmato)
            └──→ refused_approver (se l'approvatore rifiuta)
```

Da qualsiasi stato, il bottone "Persa" (commerciale/admin) segna come persa l'offerta e la lead.
Il bottone "Ripristina" riporta in bozza.

| Stato | Descrizione | Regola |
|-------|-------------|--------|
| `draft` | Bozza, in fase di compilazione | Creazione automatica da lead |
| `approval` | In attesa di approvazione interna | `action_send()` porta l'offerta in approvazione |
| `approved` | Approvata dall'approvatore | `action_approve()` — non invia email, non avanza la lead |
| `sent` | Offerta inviata al cliente via firma digitale | `action_send_sign_request()` — commerciale/admin inviano la sign request, lead avanza a "Proposta inviata" |
| `accepted` | Offerta accettata dal cliente | **Automatico** via `sign.request._sign()` oppure **manuale** con `action_accept_manual()` (PDF firmato a mano) |
| `refused_client` | Offerta rifiutata dal cliente | **Automatico**: hook `sign.request._refuse()` |
| `refused_approver` | Offerta rifiutata internamente | `action_reject_approver()` da wizard approvatore |

> **Bottoni per stato e ruolo:**
> - **Bozza**: Commerciale/Admin editano + "Invia in approvazione"; Approvatore sola lettura
> - **In approvazione**: Tutti sola lettura; Approvatore/Admin: "Approva"/"Rifiuta"
> - **Approvata**: Tutti sola lettura; Commerciale/Admin: "Invia mail per firma digitale", "Accettata" (se PDF firmato caricato), "Riporta a Bozza", file picker per upload PDF
> - **Inviata**: Tutti sola lettura; Commerciale/Admin: "Accettata", "Riporta a Bozza"
> - **Accettata**: Tutti sola lettura
> - **Rifiutata approvatore**: Commerciale/Admin: "Riporta a Bozza"
> - **Persa** (lead archiviata): Ribbon rosso; Commerciale/Admin: "Ripristina"
> - "Persa" visibile da qualsiasi stato per Commerciale/Admin (apre wizard con motivo perdita)
> - "Apri PDF" sempre visibile per tutti i ruoli (genera il PDF con allegati concatenati e lo apre nel browser senza creare allegati nel chatter)
> - Il PDF firmato caricato manualmente viene allegato al messaggio chatter al momento dell'accettazione manuale

#### Pricing manuale RS su righe offerta

Per le offerte tipo **Rifiuti Speciali** sono stati aggiunti 3 campi editabili sia su
`tea.offer.line` (tab "Righe CER") sia su `tea.offer.line.service`
(tab "Servizi Generali"):

| Campo | Tipo | Logica |
|-------|------|--------|
| `cost` | Float | Costo base |
| `markup_20` | Float | Mark Up 20% |
| `sale_price` | Float | Vendita finale |

Regole onchange implementate su tutti e 3 i campi (in entrambi i modelli):

- Modifica `cost` → `markup_20 = cost * 0.2` e `sale_price = cost + markup_20`
- Modifica `markup_20` → `cost = markup_20 / 0.2` e `sale_price = cost + markup_20`
- Modifica `sale_price` → `cost = sale_price / 1.2` e `markup_20 = sale_price - cost`

In vista offerta:
- Tab **Righe CER**: i 3 campi sono inseriti subito dopo "Min. Fatt. A&E (€)"
- Tab **Servizi Generali**: i 3 campi sono inseriti subito dopo "Prezzo"

**Vincolo importi non negativi** su tutti i modelli con campi numerici editabili:
- `tea.offer.line` (`_check_no_negative_prices`): constraint
  `@api.constrains("price_unit_sale", "min_billing_sale", "markup_pct")` — impedisce valori negativi
  su prezzo di vendita (€/kg), minimo fatturabile A&E (€) e mark up (%).
- `tea.offer.line.service` (`_check_no_negative_prices`): constraint
  `@api.constrains("price", "sale_price", "markup_pct")` — impedisce valori negativi su costo
  del servizio, prezzo di vendita del servizio e mark up (%).
- `tea.offer` (`_check_disc_no_negative`): constraint
  `@api.constrains("disc_tons", "disc_tons_sludge", "disc_price_ton", "disc_price_ton_sludge", "disc_fidejussione")`
  — impedisce valori negativi su tonnellate, prezzi €/ton e fidejussione per offerte Discarica.
- `tea.offer` (`_check_tmb_no_negative`): constraint
  `@api.constrains("tmb_qty", "tmb_price", "tmb_transport_price", "tmb_omologa_price")`
  — impedisce valori negativi su quantità, prezzo trattamento, trasporto e analisi per offerte TMB.

#### 4.1.6 `tea.offer.type` → `models/tea_offer_type.py`

| Campo | Tipo | Note |
|-------|------|------|
| `name` | Char, translate | Nome tipo (es. "Offerta TMB") |
| `code` | Char, unique | Codice tecnico ("tmb", "discarica") |
| `sequence` | Integer | Ordinamento |
| `report_template_id` | Many2one → ir.actions.report | Template QWeb PDF |
| `active` | Boolean | Archiviabile |

Dati iniziali (noupdate): TMB (code=tmb, seq=10), Discarica (code=discarica, seq=20),
e Rifiuti Speciali (code=rifiuti_speciali, seq=30).

#### 4.1.7 `tea.contract.producer` → `models/tea_contract_producer.py`

| Campo | Tipo | Note |
|-------|------|------|
| `offer_id` | Many2one → tea.offer, cascade | Offerta collegata |
| `sequence` | Integer | Ordinamento |
| `partner_id` | Many2one → res.partner | Produttore — dominio in vista: solo indirizzi figlio del partner cliente (`parent_id = partner_id`, type delivery/invoice/other) |
| `cer_id` | Many2one → tea.cer.code | Codice CER |

Display name computato: `"NOME PARTNER - CER CODICE"`.

#### 4.1.8 `tea.offer.document` — Modello unificato documenti + schede

> **Nota:** Il modello `tea.lead.characterization` è stato eliminato e le sue funzionalità
> sono state assorbite da `tea.offer.document` tramite il campo `document_type`.

| Campo | Tipo | Note |
|-------|------|------|
| `lead_id` | Many2one → crm.lead, cascade | Lead collegata |
| `sequence` | Integer | Ordinamento |
| `document_type` | Selection (document/characterization), required | Tipo: Documento o Scheda di Caratterizzazione |
| `name` | Char, required | Nome documento |
| `document_file` | Binary | PDF documento |
| `document_filename` | Char | Nome file |
| `sheet_id` | Many2one → tea.characterization.sheet | Scheda anagrafica (solo per tipo characterization) |
| `cer_id` | Many2one, related, stored | CER (da sheet_id) |
| `plant_id` | Many2one, related, stored | Destino (da sheet_id) |
| `effective_file` | Binary, computed | File effettivo: per tipo "characterization" prende `sheet_id.sheet_file`, altrimenti `document_file` |
| `effective_filename` | Char, computed | Nome file effettivo (dalla stessa logica di `effective_file`) |
| `requires_signature` | Boolean | Richiede firma |
| `received` | Boolean | Documento ricevuto |
| `signed` | Boolean | Documento firmato |
| `is_complete` | Boolean, computed, stored | Completato |
| `to_send` | Boolean | Selezionato per invio email |

##### Invio email documenti

Il bottone "Invia Documenti Selezionati" sulla lead filtra i documenti con
`to_send=True AND received=False`, crea attachment temporanei e apre il
composer email con gli allegati precaricati.

### 4.2 Modelli ESTESI (5 file)

#### 4.2.1 `product.template` → `models/product_template.py`

Estensione di `product.template` con campi specifici CER. Ogni prodotto CER
(139 record = CER + sotto-tipo + stato fisico) è un singolo `product.template`
di tipo **service**.

| Campo aggiunto | Tipo | Note |
|----------------|------|------|
| `cer_id` | Many2one → tea.cer.code | Codice CER di appartenenza |
| `cer_subtype` | Char | Sotto-tipo, es. "RETI", "SERR" |
| `physical_state` | Selection | Stato fisico: S1, S2, S3 o S4 |
| `is_hazardous` | Boolean, related da cer_id | Per filtri/ricerche rapide |
| `hp_code_ids` | Many2many → tea.hp.code, **computed** | Codici HP — calcolati dal listino fornitore (`seller_ids.hp_code_id`) |
| `waste_operation_ids` | Many2many → tea.waste.operation, **computed** | Operazioni R/D — calcolate dal listino fornitore (`seller_ids.waste_operation_id`) |

Valori Selection per `physical_state`:

| Valore | Etichetta |
|--------|-----------|
| `S1` | S1 – Solido polverulento |
| `S2` | S2 – Solido non polverulento |
| `S3` | S3 – Fangoso palabile |
| `S4` | S4 – Liquido |

Constraint SQL: **UNIQUE su `default_code`** (`_default_code_unique`).

Campi standard riusati:
- `name` = codice interno (es. `020104RETIS2`) — **il nome è il riferimento interno**
- `default_code` = stesso valore di `name` (es. `020104RETIS2`)
- `description` = testo descrittivo del rifiuto (HTML)
- `type` = `service` (tutti i prodotti CER sono servizi)

Campi nascosti per prodotti gestiti da listino fornitore:
- `list_price`, `standard_price` — nascosti quando `seller_ids` è valorizzato
  (cioè il prodotto ha righe di listino fornitore `product.supplierinfo`).
  I prodotti CER con prezzo fisso (senza righe fornitore) li mantengono visibili.
- Tasse vendita/acquisto, categoria — nascosti quando `cer_id` è valorizzato
  oppure quando il contesto contiene `hide_prices: True`
  (propagato dalle action "Prodotti CER" e "Servizi" del menu Gestione Rifiuti)

Nota: i prodotti senza stato fisico (8 prodotti, es. CER 200307) hanno
`physical_state` vuoto.

#### 4.2.2 `res.partner` → `models/res_partner.py`

Estensione di `res.partner` per gli impianti di trattamento rifiuti.
63 impianti dall'Excel, ciascuno con flag `is_waste_plant = True`.

| Campo aggiunto | Tipo | Note |
|----------------|------|------|
| `is_waste_plant` | Boolean | Flag "Impianto di trattamento" |
| `tea_contract_address` | Char, computed | Indirizzo completo per contratti (auto da via/città/provincia) |
| `tea_contract_regimpr_loc` | Char | Registro imprese — sede |
| `tea_contract_regimpr_num` | Char | Registro imprese — numero |
| `tea_contract_legal_rep` | Char | Legale rappresentante |

Campi standard riusati:
- `name` = ragione sociale impianto
- `street` / `city` / campi indirizzo = indirizzo impianto (parsing dall'Excel)

Gli impianti sono importati come `is_company = True`.
Il flag `is_waste_plant` è visibile nella form partner accanto al tipo azienda.

I campi standard `vat` (P.IVA), `l10n_it_pec_email` (PEC), `l10n_it_codice_fiscale`
e `l10n_it_pa_index` (codice SDI) sono già coperti da Odoo standard / `l10n_it`.

#### 4.2.3 `product.supplierinfo` → `models/product_supplierinfo.py`

Estensione del listino fornitori standard per aggiungere operazione R/D,
codici HP e fatturato minimo. 268 record dal caricamento iniziale.

| Campo aggiunto | Tipo | Note |
|----------------|------|------|
| `waste_operation_id` | Many2one → tea.waste.operation | Operazione R/D |
| `hp_code_ids` | Many2many → tea.hp.code | Codici HP (multipli, solo per CER pericolosi) |
| `min_billing` | Float | Fatturato minimo impianto (€) |
| `min_billing_sale` | Float | Fatturato minimo vendita A&E (€) |
| `is_hazardous` | Boolean, related | Da `product_tmpl_id.is_hazardous`, per visibilità condizionale |

**Vincolo importi non negativi** (`_check_no_negative_prices`): constraint
`@api.constrains("price", "min_billing", "min_billing_sale")` che impedisce valori
negativi su prezzo di listino, minimo fatturabile impianto e minimo fatturabile vendita.

**Vincolo HP/pericolosità:** constraint Python che impedisce di assegnare codici HP
a un record il cui prodotto ha CER non pericoloso. Nella vista, il campo HP è nascosto
se il prodotto non è pericoloso.

**Vincolo unicità HP:** constraint Python che impedisce linee duplicate per lo stesso
fornitore e prodotto con esattamente lo stesso set di codici HP.

**Display name CER:** per i record con prodotto CER, il display name mostra
codice prodotto, codici HP e prezzo (es. `020104RETIS2 — HP: HP3, HP14 — 0.1200 €/kg`).

Campi standard riusati:
- `partner_id` = impianto di trattamento — domain `[('is_waste_plant', '=', True)]` a livello model
- `product_tmpl_id` = template prodotto CER — domain `[('cer_id', '!=', False)]` a livello model
- `price` = prezzo di acquisto (€/kg) — colonna "IMPIANTO (Kg)" del Prezziario
- `currency_id` = EUR
- `min_qty` = 0 (nessun minimo quantità, di default)

**Vincolo prodotto CER obbligatorio** (`_check_product_has_cer`): constraint
`@api.constrains("product_tmpl_id")` che impedisce di creare righe listino per
prodotti senza codice CER associato.

**Nota sui prezzi**: `price` è in €/kg (come da Prezziario). Valori speciali:
- 0.0 = gratuito o da definire
- Negativi = **bloccati** dal vincolo `_check_no_negative_prices`

**Nota sulla colonna "A&E +20%"**: il markup di rivendita (default 20%) è un parametro
di business salvato su `res.company` come `default_markup_pct`.
Verrà utilizzato in fase di offerta per calcolare il prezzo di vendita al cliente.
Ricarichi diversi (5%, 10%, 25%, 30%) potranno essere gestiti in futuro a livello
di singola offerta o per categoria di prodotto.

#### 4.2.4 `res.company` → `models/res_company.py`

Estensione di `res.company` per il parametro markup di rivendita.

| Campo aggiunto | Tipo | Note |
|----------------|------|------|
| `default_markup_pct` | Float | % markup standard per rivendita |

Questo valore verrà usato in fase di offerta per calcolare il prezzo di vendita
partendo dal prezzo d'acquisto dell'impianto.

---

### 4.3 `models/__init__.py`

Importa i 16 moduli (11 custom + 5 estensioni):

```python
from . import crm_lead
from . import product_supplierinfo
from . import product_template
from . import res_company
from . import res_partner
from . import tea_cer_code
from . import tea_contract_producer
from . import tea_hp_code
from . import tea_offer
from . import tea_offer_document
from . import tea_offer_line
from . import tea_offer_line_service
from . import tea_offer_type
from . import tea_offer_type_document
from . import tea_offer_validity
from . import tea_waste_operation
```

---

## 5. Caricamento dati iniziali

### Strategia: dati statici via XML + dati bulk via script Python

I **dati di riferimento statici** (pochi record, non cambiano) vengono caricati
come file XML nel modulo (`noupdate="1"`):

| # | File | Modello/Tipo | Records |
|---|------|-------------|---------|
| 1 | `data/tea_hp_code_data.xml` | tea.hp.code | 11 |
| 2 | `data/tea_waste_operation_data.xml` | tea.waste.operation | 12 |
| 3 | `data/approval_reminder_data.xml` | ir.cron + QWeb template | 1 cron + 1 template |

> **Nota**: non esiste `product_attribute_data.xml`. Lo stato fisico è un campo
> Selection su `product.template`, non un attributo prodotto.

I **dati bulk** (centinaia di record, provenienti dall'Excel) vengono caricati
tramite lo **script Python** `scripts/import_initial_data.py` via Odoo shell:

```bash
uv run python odoo-bin.py shell -c odoo.conf -d <db> --no-http --log-level=info \
  < addons/tea_quotations/scripts/import_initial_data.py
```

Lo script legge entrambi i file Excel e crea:

| Modello | Records | Fonte Excel |
|---------|---------|-------------|
| tea.cer.code | 115 | Anagrafica — foglio 2 |
| res.partner (impianti) | 63 | Anagrafica — foglio 6 + indirizzi da foglio 5 |
| product.template (type=service) | 139 | Anagrafica — fogli 3+4 (131 con SF + 8 senza) |
| product.supplierinfo | 268 | Anagrafica — foglio 5, prezzi da Prezziario 2025 |

### Formato riferimento interno

Il `default_code` e il `name` di ogni prodotto seguono il formato concatenato
senza separatori né `.0`:

- ✅ `020104RETIS2` (formato corretto)
- ❌ `020104_RETI_S2.0` (formato Excel, convertito dallo script)

La descrizione testuale del rifiuto va nel campo `description` (HTML).

### Parsing indirizzi impianti

Gli indirizzi dal foglio 5 (es. `VIA LEVATA, 64 - 42017 NOVELLARA (RE)`) vengono
parsati dallo script per estrarre i campi standard `res.partner`:

| Parte | Campo res.partner | Esempio |
|-------|-------------------|---------|
| Via e numero | `street` | "VIA LEVATA, 64" |
| CAP | `zip` | "42017" |
| Città | `city` | "NOVELLARA" |
| Provincia | `state_id` | RE (ricerca su res.country.state) |

### Merge prezzi dal Prezziario 2025

Lo script incrocia i dati dei due Excel:
- L'anagrafica fornisce la struttura (CER × sotto-tipo × SF × impianto × operazione)
- Il Prezziario 2025 fornisce i prezzi dove disponibili

Match basato su: chiave CER concatenata (colonna CER del prezziario) + nome impianto.
Dove il prezziario ha un prezzo, viene usato per `product.supplierinfo.price`.
Dove non c'è match, il prezzo resta 0 (da compilare manualmente).

I campi `min_billing` e `min_billing_sale` vengono popolati dalle colonne
"Min Fatt. Impianto" e "Min Fatt. A&E +20%" del Prezziario.

### Convenzioni XML ID (per dati statici)

- HP: `tea_hp_code_hp2`, `tea_hp_code_hp14`
- Operazioni: `tea_waste_operation_d1`, `tea_waste_operation_r13`

### Conteggi dati finali

| Entità | Modello | Count |
|--------|---------|-------|
| Codici CER | tea.cer.code | 115 |
| Codici HP | tea.hp.code | 11 |
| Operazioni R/D | tea.waste.operation | 12 |
| Impianti di trattamento | res.partner | 63 |
| Prodotti CER | product.template | 139 |
| Righe listino fornitore | product.supplierinfo | 268 |

---

## 6. Viste XML e Menu

### File di viste

| File | Contenuto |
|------|-----------|
| `views/tea_cer_code_views.xml` | List, Form, Search per codici CER + action |
| `views/product_template_views.xml` | Estensione form (gruppo CER a colonna singola verticale, UdM, prezzi nascosti via `seller_ids` o `context.hide_prices`), list (colonne CER condizionali via `context.hide_cer_columns`, prezzi nascosti), search (filtro CER). Action dedicate: Prodotti CER (`cer_id != False`) e Servizi (`cer_id = False, type = service`) |
| `views/product_supplierinfo_views.xml` | Estensione list/form + action rifiuti dedicata. Form: nascosto gruppo vendor e `min_qty`; `partner_id` spostato nel gruppo Pricelist (filtrato `is_waste_plant`); aggiunto `product_uom_id` readonly dopo prezzo; aggiunto campi rifiuti dopo discount. List: nascosto `product_id`, aggiunte colonne rifiuti |
| `views/res_partner_views.xml` | Estensione form con flag "Impianto di Trattamento" + tab dati contratto |
| `views/res_company_views.xml` | Estensione form con campo markup % e firma offerte |
| `views/tea_offer_views.xml` | Form (tab condizionali TMB/Discarica/RS), List, Search, Action |
| `views/crm_lead_views.xml` | Smart button "Offerte" su form crm.lead + stato offerta sempre visibile (form/kanban/lista) |
| `views/tea_configuration_views.xml` | List e Form CRUD per HP codes, Operazioni R/D, Tipologie Offerta e Validità Offerta |
| `views/tea_quotations_menus.xml` | Struttura menu completa (etichette italiane) |

### Struttura menu

```
Gestione Rifiuti (root menu)
├── Anagrafica CER                       [Commerciale, Admin]
│   ├── Codici CER                       → list/form tea.cer.code
│   ├── Prodotti CER                     → list/form product.template (cer_id != False)
│   ├── Servizi                          → list/form product.template (cer_id = False, type = service)
│   └── Schede di Caratterizzazione      → list/form tea.characterization.sheet
├── Offerte                              → list/form tea.offer
├── Listino Fornitori                    [Commerciale, Admin]
│   ├── Impianti di Trattamento          → list/form res.partner (is_waste_plant)
│   └── Listino Prezzi                   → list/form product.supplierinfo
└── Configurazione                       [Admin]
    ├── Tipologie Offerta                → list/form tea.offer.type
    ├── Codici HP                        → list/form tea.hp.code
    ├── Operazioni R/D                   → list/form tea.waste.operation
    └── Validità Offerta                 → list/form tea.offer.validity
```

  Note ruoli e visibilità:
  - Approvatore: vede solo il menu "Offerte" in Gestione Rifiuti.
  - Commerciale/Admin: vedono Anagrafica CER, Offerte e Listino Fornitori.
  - Solo Admin: vede il menu Configurazione (Tipologie, HP, Operazioni, Validità).
  - Smart button verso la lead CRM nella form offerta visibile solo a Commerciale/Admin.

  Note prezzi e contesto:
  - I campi prezzo (`list_price`, `standard_price`) sono nascosti solo per i prodotti
    con righe fornitore (`seller_ids` valorizzato). Tasse e categoria sono nascosti
    per tutti i CER (`cer_id`) o via contesto `hide_prices: True`.
  - Le colonne CER nella list view sono nascoste dal contesto `hide_cer_columns: True`
    (action Servizi).

### Etichette UI

Tutte le etichette utente sono in **italiano**:
- Menu: Gestione Rifiuti, Anagrafica CER, Prodotti CER, Listino Fornitori, etc.
- Campi: Codice CER, Sotto-tipo CER, Stato Fisico, Pericoloso, Codici HP,
  Operazione R/D, etc.
- Il codice (variabili, metodi) resta in **inglese** per convenzione OCA.

---

## 7. Sicurezza

### `security/ir.model.access.csv`

Solo i modelli custom necessitano di ACL esplicite (i modelli standard
`product.template`, `res.partner`, `product.supplierinfo`, `res.company`
hanno già le loro ACL):

| Modello | Gruppo | Read | Write | Create | Delete |
|---------|--------|------|-------|--------|--------|
| tea.hp.code | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.waste.operation | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.cer.code | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.offer | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.offer.type | base.group_user | ✓ | — | — | — |
| tea.offer.type | sales_team.group_sale_manager | ✓ | ✓ | ✓ | ✓ |
| tea.contract.producer | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.offer.line | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.offer.line.service | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.offer.approve.wizard | base.group_user | ✓ | ✓ | ✓ | ✓ |
| tea.offer.reject.wizard | base.group_user | ✓ | ✓ | ✓ | ✓ |
| crm.lead | tea_quotations.group_tea_approver | ✓ | — | — | — |

`tea.offer.type` è read-only per utenti base e full CRUD per Sales Manager.

Note sicurezza aggiuntive:
- `group_tea_approver` non implica `base.group_partner_manager`: sui contatti (`res.partner`) ha sola lettura.
- Root menu CRM e Dashboards sono esplicitamente limitati a Commerciale/Admin tramite override su `ir.ui.menu`.
- Le mass actions list-view ("Approva selezionate" / "Rifiuta selezionate") sono protette via controllo runtime in `ir.actions.server` (Approvatore/Admin only).

---

## 8. Test automatici

I test sono inclusi fin dalla prima implementazione.

### `tests/__init__.py` + `tests/test_*.py`

| File test | Cosa testa |
|-----------|------------|
| `tests/test_tea_hp_code.py` | Creazione, unicità codice |
| `tests/test_tea_waste_operation.py` | Creazione, unicità, tipo operazione |
| `tests/test_tea_cer_code.py` | Creazione, unicità, relazione HP, conteggio prodotti |
| `tests/test_product_template.py` | Campi CER su template, physical_state, UNIQUE default_code, onchange code |
| `tests/test_res_partner.py` | Campi impianto, flag is_waste_plant |
| `tests/test_product_supplierinfo.py` | Campi estesi: operation, min_billing, min_billing_sale |
| `tests/test_tea_offer.py` | Creazione offerte, transizioni stato, firma approvazione, onchange partner |
| `tests/test_tea_offer_line.py` | Righe CER, auto-fill prezzi, servizi annessi/standalone, cascata delete, onchange `cost`/`markup_20`/`sale_price` |
| `tests/test_tea_offer_line_service.py` | Servizi generali, compute `offer_id`, onchange `cost`/`markup_20`/`sale_price` |

---

## 9. Comandi di esecuzione

```bash
# Dal workspace root (odoo-venv-19e/)

# Installazione / aggiornamento modulo
uv run python odoo-bin.py -c odoo.conf -u tea_quotations -d tea_quotations_dev --stop-after-init

# Import dati iniziali da Excel
uv run python odoo-bin.py shell -c odoo.conf -d tea_quotations_dev --no-http --log-level=info \
  < addons/tea_quotations/scripts/import_initial_data.py

# Test automatici
uv run python odoo-bin.py -c odoo.conf -d tea_quotations_dev \
  --test-tags /tea_quotations --stop-after-init -u tea_quotations

# Lint e formattazione
uv run ruff check addons/tea_quotations && uv run ruff format addons/tea_quotations
```

---

## 10. Decisioni prese

| # | Decisione | Scelta |
|---|-----------|--------|
| 1 | Architettura prodotto | **NO varianti** — ogni CER+sotto-tipo+SF è un `product.template` (type=service) |
| 2 | Stato fisico | Campo Selection su `product.template`, non `product.attribute` |
| 3 | Nome prodotto | `name` = riferimento interno (es. `020104RETIS2`), descrizione in `description` |
| 4 | Formato default_code | Concatenato senza separatori: `020104RETIS2` (non `020104_RETI_S2.0`) |
| 5 | Unicità default_code | Constraint UNIQUE su `product_template.default_code` |
| 6 | Campi prezzo | `list_price` e `standard_price` nascosti solo quando `seller_ids` valorizzato (prodotti con listino fornitore); visibili per CER a prezzo fisso |
| 7 | Tipo prodotto | `service` (non consumabile) |
| 8 | Gruppi di sicurezza | `base.group_user` — nessun ruolo dedicato |
| 9 | Caricamento dati bulk | Script Python via `odoo shell` (non XML) |
| 10 | Dati statici (HP, operazioni) | XML con `noupdate="1"` |
| 11 | UdM prodotti | kg (come da Prezziario) |
| 12 | Markup vendita A&E | Parametro `default_markup_pct` su `res.company` |
| 13 | Fonte prezzi | Prezziario 2025 (180 righe con prezzi reali) |
| 14 | Fatturato minimo | Campi `min_billing` e `min_billing_sale` su `product.supplierinfo` |
| 15 | Impianti | Estensione `res.partner` con flag `is_waste_plant` |
| 16 | Listini | Standard Odoo `product.supplierinfo` esteso con campi rifiuti |
| 17 | Pricing manuale RS in offerta | Aggiunti `cost`, `markup_20`, `sale_price` su righe CER e servizi generali con onchange bidirezionali |
| 11 | Offerte come modello autonomo | `tea.offer` standalone con M2O a `crm.lead`, anziché ereditare crm.lead direttamente |
| 12 | TMB e Discarica flat | TMB/Discarica usano campi dedicati Char sul modello `tea.offer` (nessuna riga) |
| 13 | RS con righe strutturate | Rifiuti Speciali usa `tea.offer.line` (One2many CER) con `tea.offer.line.service` (servizi) |
| 14 | Produttore Allegato 2 | `tea.contract.producer` con M2O a `res.partner` e `tea.cer.code` (non campo testo libero) |
| 15 | Gruppo manager ACL | `sales_team.group_sale_manager` (non esiste `crm.group_crm_manager` in Odoo 19) |
| 16 | State machine separati | L'offerta (`tea.offer`) ha stati semplici: draft → sent → accepted / refused. La pipeline commerciale (New → Qualified → Proposition → On Hold → Won / Lost) è gestita tramite gli stage CRM standard (`crm.stage`) sulla lead |
| 17 | Firma approvazione | Widget `signature` su `res.company`, comune a tutte le offerte — apposta nel PDF prima dell'invio |
| 18 | Firma digitale cliente | Odoo Sign: PDF generato → sign.template → sign.request con email automatica al cliente |
| 19 | Accettazione offerta | **Solo via firma digitale**: hook `sign.request._sign()` auto-accept, nessun bottone manuale |
| 20 | Trasporto prezzi | Inserimento manuale nella riga; griglia tariffaria in fase successiva |
| 20 | Auto-fill prezzi RS | Onchange CER+Impianto → lookup `product.supplierinfo` con markup da `res.company` |
| 20b | Auto-fill descrizione CER | Onchange `supplierinfo_id` compila `description` con `cer_id.name` del prodotto (solo se vuoto, campo resta editabile) |
| 20c | Auto-fill prezzi servizi | Onchange `product_tmpl_id` su `tea.offer.line.service` compila `price` da `standard_price` e `sale_price` da `list_price` del prodotto. Il markup % si ricalcola automaticamente: `(sale_price / price - 1) × 100` |
| 21 | Referente commerciale | Campo `tea_commercial_ref_id` (Many2one → res.users) su `crm.lead` — default utente corrente, tracking. Rappresenta il referente commerciale della trattativa |
| 22 | Stato documentazione Speciali | 4 box radio con codifica colore (giallo=pending, verde=completato): Foto, Sopralluogo, Info Impianto, Info Cliente |
| 23 | Checklist documentale | Gestita tramite documenti (`tea.offer.document`) sulla lead, generati automaticamente dai template della tipologia. Ogni documento deve essere ricevuto (e firmato se richiesto) per poter avanzare al Won. Nessun campo booleano separato |
| 24 | Flag rinnovo | `tea_is_renewal` su `crm.lead` — distingue rinnovo da nuovo cliente per tutte le tipologie |
| 25 | Font report PDF | **Carlito** (Apache 2.0, metricamente compatibile con Calibri Light). @font-face URL-based in SCSS (pattern standard Odoo), wkhtmltopdf scarica i TTF via HTTP |
| 26 | Regole di stile PDF | Da `docs/Regole di stile.pdf`: Calibri Light 9-10pt, colore #595959, no grassetto, date estese senza zeri iniziali, provincia senza parentesi, minuscolo dopo "Oggetto:" |
| 25 | Fidejussione condizionale | Flag `tea_has_fidejussione` sulla lead, visibile solo per Discarica |
| 26 | Creazione offerte solo da lead | `lead_id` è required su `tea.offer`, creazione diretta disabilitata (form/list `create="0"`). Creazione automatica al passaggio a "Elaborazione proposta" |
| 27 | Schede di caratterizzazione | Anagrafica dedicata `tea.characterization.sheet` (chiave CER + Destino + Tipologia Cliente). Unificate in `tea.offer.document` con `document_type='characterization'` e link a `sheet_id`. Il modello `tea.lead.characterization` è stato eliminato |
| 28 | Protocollo offerte RS | Formato `O` + progressivo 4 cifre + `/` + anno corrente + `/` + iniziali referente commerciale (es. `O0010/2026/NM`) |
| 29 | Unicità schede di caratterizzazione | Constraint Python anziché SQL `UNIQUE`: tratta `NULL` e stringa vuota in `client_type` come equivalenti (SQL UNIQUE considera i NULL distinti, permettendo duplicati) e limita il vincolo ai soli record attivi |
| 30 | Blocco importi negativi | Constraint `@api.constrains` su `product.supplierinfo`, `tea.offer.line`, `tea.offer.line.service` e `tea.offer` (campi Discarica e TMB) per impedire valori negativi su tutti i campi float/monetary editabili |
| 31 | Separazione Cliente/Contatto | `partner_id` sulla lead = azienda (domain `is_company=True`), `tea_contact_id` = persona fisica (type=contact, figlio del partner). Nell'offerta entrambi sono campi `related` dalla lead, readonly |
| 32 | Saluto PDF Egregio/Spett. | Logica italiana sul `l10n_it_codice_fiscale` del partner: 16 caratteri alfanumerici → persona fisica → "Egregio"; altrimenti → azienda → "Spett." |
| 33 | Dipendenza l10n_it_edi | Necessaria per il campo `l10n_it_codice_fiscale` su `res.partner` |
| 34 | Domain produttori allegato 2 | `tea.contract.producer.partner_id` e `tmb_producer_id` filtrati per indirizzi figlio del cliente (type delivery/invoice/other) |
| 35 | Filtro date validità listino | Il domain di `supplierinfo_id` su `tea.offer.line` filtra per `date_start` ≤ `offer_date` e `date_end` ≥ `offer_date` (campi opzionali: se assenti, il listino è considerato sempre valido). Campo `offer_date` related dalla parent `tea.offer` |
| 36 | Upload offerta manuale | Campo `custom_pdf` su `tea.offer` consente di caricare un PDF modificato manualmente che sovrascrive il report QWeb auto-generato nel flusso "Apri PDF" e firma digitale |

---

## 11. Sistema Offerte / Contratti

### 11.1 Contesto

TEA A&E genera tre tipi di documenti PDF legati alle opportunità CRM:

1. **Offerta TMB** — Proposta economica per trattamento rifiuti presso impianto TMB.
   Documento breve con 3 tabelle e condizioni fisse di conferimento.
2. **Contratto Discarica** — Contratto formale in 18 articoli per conferimento rifiuti
   presso la discarica di Mariana Mantovana, con allegati.
3. **Offerta Rifiuti Speciali** — Offerta strutturata con righe CER (ciascuna con
   impianto destino e prezzi dal listino fornitore), servizi aggiuntivi per riga
   (trasporto, analisi, noleggio cassoni, big bags...) e servizi generali
   (trasporto cumulativo, extra-sosta...).

Precedentemente gestiti tramite stampa unione Word/Excel.

### 11.2 Architettura

| Concetto | Modello | Tipo |
|----------|---------|------|
| Offerta/Contratto | `tea.offer` | **Custom** — modello autonomo con link a CRM |
| Tipo offerta (TMB/Discarica/RS) | `tea.offer.type` | **Custom** — configurazione con ref a report |
| Riga CER offerta RS | `tea.offer.line` | **Custom** — listino fornitore + impianto + prezzi |
| Servizio aggiuntivo RS | `tea.offer.line.service` | **Custom** — trasporto, analisi, noleggio... |
| Produttore Allegato 2 | `tea.contract.producer` | **Custom** — riga elenco produttori |
| Opportunità CRM | `crm.lead` | **Estensione minima** — smart button offerte |

**Scelta architetturale**: `tea.offer` è un modello standalone (non eredita `crm.lead`) collegato tramite `lead_id` Many2one **required**. Le offerte non possono essere create manualmente: vengono generate automaticamente al passaggio a "Elaborazione proposta" o tramite il pulsante "Nuova Offerta" nella scheda dell'opportunità CRM. La creazione diretta dalla lista offerte è disabilitata (`create="0"`).

### 11.3 Modello `tea.offer` — `models/tea_offer.py`

Inherits: `mail.thread`, `mail.activity.mixin`

#### Campi comuni (tutti i tipi offerta)

| Campo | Tipo | Note |
|-------|------|------|
| `lead_id` | Many2one → crm.lead, **required** | Opportunità collegata — `ondelete="cascade"`, readonly in vista |
| `partner_id` | Many2one → res.partner, **related** | Cliente (azienda) — `related="lead_id.partner_id"`, store=True, readonly |
| `contact_id` | Many2one → res.partner, **related** | Contatto (persona) — `related="lead_id.tea_contact_id"`, store=True, readonly |
| `company_id` | Many2one → res.company | Azienda |
| `offer_type_id` | Many2one → tea.offer.type | Tipo (TMB/Discarica/RS) — readonly se la lead ha tipologia |
| `offer_type_code` | Char, related | Per visibilità condizionale nelle viste |
| `lead_offer_type_id` | Many2one, related | Tipo dalla lead, per readonly condizionale in vista |
| `name` | Char | Riferimento auto-generato (es. RS/2026/0001) |
| `rs_protocol` | Char | Protocollo offerte Rifiuti Speciali auto-generato: `O` + progressivo 4 cifre + `/` + anno corrente + `/` + iniziali referente commerciale (es. `O0010/2026/NM`) |
| `offer_date` | Date | Data offerta |
| `state` | Selection | **draft / approval / approved / sent / accepted / refused_client / refused_approver** |
| `sign_request_id` | Many2one → sign.request, readonly, copy=False | Richiesta firma digitale collegata |
| `approved_by_id` | Many2one → res.users | Utente approvatore |
| `approved_date` | Datetime | Data/ora approvazione |
| `sent_date` | Datetime | Data/ora invio al cliente |
| `refused_reason` | Text | Motivo rifiuto cliente (da Odoo Sign) |
| `approver_rejection_reason` | Text | Motivo rifiuto approvatore |
| `signed_pdf` | Binary, copy=False | PDF firmato a mano (alternativa a Odoo Sign) |
| `signed_pdf_filename` | Char, copy=False | Nome file PDF firmato |
| `custom_pdf` | Binary, copy=False | PDF offerta modificata manualmente (sovrascrive il PDF auto-generato) |
| `custom_pdf_filename` | Char, copy=False | Nome file offerta caricata manualmente |
| `has_custom_pdf` | Boolean, computed | True se `custom_pdf` è valorizzato |
| `notes` | Html | Note offerta (visibile nel report PDF) |
| `internal_notes` | Html | Note interne (NON renderate nei report PDF) |

#### Metodo `_get_cer_ids()` — codici CER generici dall'offerta

Restituisce i record `tea.cer.code` presenti nell'offerta, indipendentemente dalla tipologia:

| Tipologia | Fonte |
|-----------|-------|
| Rifiuti Speciali | `rs_line_ids.product_tmpl_id.cer_id` (dalle righe offerta) |
| Discarica | `disc_eer_ids \| disc_eer_sludge_ids` (CER non fanghi + fanghi) |
| TMB | `tmb_product_id.cer_id` (dal prodotto CER singolo) |

Se nessun CER è presente, restituisce un recordset vuoto di `tea.cer.code`.
Utilizzato da `crm.lead._compute_tea_offer_domains()` per aggregare i CER di tutte le offerte collegate.

#### State machine offerta (`tea.offer`)

```
draft ──→ approval ──→ approved ──→ sent ──→ accepted
            │              │          │
            │              │          └──→ refused_client (se il cliente rifiuta la firma)
            │              └──→ accepted (manuale con PDF firmato)
            └──→ refused_approver (se l'approvatore rifiuta)
```

| Stato | Descrizione | Regola |
|-------|-------------|--------|
| `draft` | Bozza, in fase di compilazione | Creazione automatica da lead |
| `approval` | In attesa di approvazione interna | `action_send()` porta l'offerta in approvazione |
| `approved` | Approvata dall'approvatore | `action_approve()` — non invia email, non avanza la lead |
| `sent` | Offerta inviata al cliente via firma digitale | `action_send_sign_request()` — commerciale/admin inviano la sign request |
| `accepted` | Offerta accettata dal cliente | **Automatico** via Sign hook oppure **manuale** con `action_accept_manual()` |
| `refused_client` | Offerta rifiutata dal cliente | **Automatico** tramite hook `sign.request._refuse()` |
| `refused_approver` | Offerta rifiutata internamente | `action_reject_approver()` da wizard approvatore |

> **Nota**: il flusso completo dei bottoni per stato e ruolo è documentato nella sezione 4.1.5.
> "Riporta a Bozza" è disponibile da `refused_approver`, `approved` e `sent`.

#### Pipeline CRM (crm.lead)

Gli stati del processo commerciale sono gestiti tramite gli **stage standard** del CRM di Odoo (`crm.stage`).
Il modulo crea automaticamente i seguenti stage via `data/crm_stage_data.xml`:

| Stage | Sequence | Note |
|-------|----------|------|
| Nuovo | 10 | Lead ricevuta, non ancora analizzata |
| Preso in carico | 15 | Lead assegnata, raccolta dati in corso |
| Elaborazione proposta | 20 | Dati raccolti, offerta in preparazione |
| Proposta inviata | 30 | Offerta inviata al cliente |
| Attesa documenti | 40 | Offerta accettata, in attesa documentazione |
| Offerta accettata | 50 | Contratto perfezionato (`is_won=True`) |

Lo stato "Lost" è gestito nativamente dal CRM di Odoo (pulsante "Persa" con motivo).
Il bottone "Won" standard è nascosto (la transizione a "won" avviene tramite gli stage "Offerta accettata").

##### Regole di transizione stage

Il metodo `_check_stage_transition()` valida le regole di business **prima** della scrittura
dello stage. Le azioni `action_send_sign_request` e `action_accept` su `tea.offer` avanzano automaticamente
lo stage della lead usando il contesto `tea_skip_stage_check=True` per bypassare la validazione.

```
                        ┌─────────────────────────────────────────┐
                        │   Flusso Pipeline CRM (crm.lead)        │
                        └─────────────────────────────────────────┘

  ┌──────────┐    ┌──────────────┐    ┌──────────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │  Nuovo   │───▶│ Preso in     │───▶│ Elaborazione         │───▶│ Proposta         │───▶│ Attesa           │───▶│ Offerta          │
  │  (10)    │    │ carico (15)  │    │ proposta (20)        │    │ inviata (30)     │    │ documenti (40)   │    │ accettata (50)   │
  └──────────┘    └──────────────┘    └──────────────────────┘    └──────────────────┘    └──────────────────┘    └──────────────────┘
       │                │                     │                         │ AUTOMATICO            │ AUTOMATICO
       │ Manuale        │ Manuale             │ Manuale                 │ da                    │ da action_accept
       │                │                     │                         │ action_send_sign_req  │ su tea.offer
       │ Condizione:    │                     │ Condizione:             │ su tea.offer          │
       │ Tipologia      │                     │ (Solo RS)               │                       │ Condizione:
       │ obbligatoria   │                     │ Documentazione          │ Condizione:           │ ≥1 offerta "accepted"
       │                │                     │ completata              │ ≥1 offerta "sent"    │
       │                │                     │ Azione auto:            │ o "accepted"          │
       │                │                     │ Crea tea.offer          │                       │
```

| # | Transizione | Tipo | Condizione | Tipologia | Dettaglio |
|---|-------------|------|------------|-----------|-----------|
| 1 | **Nuovo → qualsiasi** | Manuale | `tea_offer_type_id` impostata | Tutte | Non si può avanzare senza aver scelto la tipologia |
| 2 | **→ Elaborazione proposta (seq ≥ 20)** | Manuale | Stato documentazione completato | **Solo RS** | I 4 campi devono essere completati o "non necessario". Non si applica a TMB/Discarica |
| 3 | **→ Proposta inviata (seq = 30)** | **Automatico** | Offerta inviata per firma | Tutte | Impostato da `tea.offer.action_send_sign_request()`. Il passaggio manuale è **sempre bloccato**: richiede almeno un'offerta con stato `sent` o `accepted`. Il bottone "Avanza" è nascosto e il trascinamento kanban mostra un popup di errore |
| 4 | **→ Attesa documenti (seq = 40)** | **Automatico** | Offerta accettata | Tutte | Impostato da `tea.offer.action_accept()` o `action_accept_manual()`. Il passaggio manuale è **sempre bloccato**: richiede almeno un'offerta con stato `accepted`. Il bottone "Avanza" è nascosto e il trascinamento kanban mostra un popup di errore |
| 5 | **→ Offerta accettata (seq ≥ 50)** | Manuale | Documenti completi | Tutte | Bloccato se i documenti sulla lead non sono tutti completi (`tea_all_documents_complete == False`). I documenti vengono generati automaticamente dai template della tipologia al passaggio ad "Attesa documenti" |

##### Azioni automatiche

| Trigger | Azione su lead | Azione su offerta |
|---------|---------------|-------------------|
| Lead → **Elaborazione proposta** (manuale) | Crea `tea.offer` se non ne esistono | — |
| Offerta → **action_send** (da `tea.offer`) | Lead invariata | Stato → `approval` |
| Offerta → **action_approve** (da wizard) | Lead invariata | Stato → `approved` |
| Offerta → **action_send_sign_request** (da `tea.offer`) | Lead avanza a "Proposta inviata" | Stato → `sent` |
| Offerta → **action_accept** / **action_accept_manual** | Lead avanza a "Attesa documenti" | Stato → `accepted` |
| Offerta → **action_set_lost** (da wizard) | Lead segnata come persa | Sign request annullata |

> **Documenti cliente:** Quando il lead raggiunge lo stage "Attesa documenti", i documenti
> vengono generati automaticamente sulla lead dai template configurati nella tipologia offerta
> (`tea.offer.type.document`). Tutti i documenti devono essere completi (ricevuti e firmati
> se richiesto) prima di poter passare a "Offerta accettata".

> **Nota tecnica**: gli avanzamenti automatici usano `with_context(tea_skip_stage_check=True)`
> per bypassare la validazione `_check_stage_transition()` — la coerenza è garantita dall'azione
> dell'offerta stessa.

##### Elementi UI nascosti dalla vista lead

| Elemento | Origine | Motivo |
|----------|---------|--------|
| Bottone "Won" | `crm` base | La transizione a won avviene tramite lo stage "Offerta accettata" (is_won=True). Nascosto per tutti i tipi custom (`tea_is_custom_type`) |
| Bottone "Enrich" | `crm_iap_enrich` | Modulo disinstallato da Impostazioni → CRM → Lead Enrichment (non necessario per il flusso TEA) |
| Bottone "Avanza" | `tea_quotations` | Nascosto negli stadi "Elaborazione proposta", "Proposta inviata", "Attesa documenti" e "Offerta accettata" — visibile solo in "Nuovo" e "Preso in carico" |
| Bottone "New Quotation" | `sale_crm` | Sostituito dal flusso `tea.offer` |
| Smart button "Quotations" | `sale_crm` | Non pertinente |
| Smart button "Orders" | `sale_crm` | Non pertinente |
| Expected Revenue | `crm` base | Non utilizzato |
| Probability / AI scoring | `crm` base | Non utilizzato |

##### Flusso completo per tipologia

**Rifiuti Speciali:**
1. **Nuovo** → impostare Tipologia, Rinnovo sì/no _(manuale)_
2. **Preso in carico** → compilare tab "Gestione Rifiuti" (Foto, Sopralluogo, Info Impianto, Info Cliente) _(manuale)_
3. **Elaborazione proposta** → documentazione completata → offerta `tea.offer` creata auto → compilare righe CER, servizi, condizioni _(manuale)_
4. **Proposta inviata** → _(automatico: si attiva cliccando "Invia" nell'offerta)_
5. **Attesa documenti** → _(automatico: si attiva cliccando "Accettata" nell'offerta)_ → documenti generati sulla lead dai template della tipologia, da completare nel tab "Documenti Cliente"
6. **Offerta accettata** → tutti i documenti completi → contratto perfezionato _(manuale)_

**TMB:**
1. **Nuovo** → impostare Tipologia, Rinnovo sì/no _(manuale)_
2. **Preso in carico** → raccolta dati _(manuale)_
3. **Elaborazione proposta** → offerta `tea.offer` creata auto → compilare dati TMB _(manuale)_
4. **Proposta inviata** → _(automatico: "Invia" nell'offerta)_
5. **Attesa documenti** → _(automatico: "Accettata" nell'offerta)_ → documenti generati sulla lead dai template della tipologia, da completare nel tab "Documenti Cliente"
6. **Offerta accettata** → tutti i documenti completi → contratto perfezionato _(manuale)_

**Discarica:**
1. **Nuovo** → impostare Tipologia, Rinnovo sì/no, Fidejussione prevista sì/no _(manuale)_
2. **Preso in carico** → raccolta dati _(manuale)_
3. **Elaborazione proposta** → offerta `tea.offer` creata auto → compilare dati Discarica _(manuale)_
4. **Proposta inviata** → _(automatico: "Invia" nell'offerta)_
5. **Attesa documenti** → _(automatico: "Accettata" nell'offerta)_ → documenti generati sulla lead dai template della tipologia, da completare nel tab "Documenti Cliente"
6. **Offerta accettata** → tutti i documenti completi → contratto perfezionato _(manuale)_

#### Campi approvazione

| Campo | Tipo | Note |
|-------|------|------|
| `approved_by_id` | Many2one → res.users, readonly | Chi ha approvato l'invio |
| `approved_date` | Datetime, readonly | Quando è stata approvata |
| `sent_date` | Datetime, readonly | Data invio offerta (auto da action_approve) |
| `refused_reason` | Text, readonly, copy=False | Motivo rifiuto compilato dal cliente nel portale Sign — visibile nella vista solo in stato `refused_client` |
| `approver_rejection_reason` | Text, readonly, copy=False | Motivo rifiuto interno — visibile in stato `refused_approver` |
| `sign_request_id` | Many2one → sign.request, readonly, copy=False | Richiesta firma digitale collegata |

La firma digitale aziendale è configurata a livello aziendale (`res.company.tea_offer_signature`,
widget signature) e viene apposta automaticamente nel PDF dell'offerta prima dell'invio.

La transizione `draft → approval` richiede:
- Firma configurata in `res.company` (`tea_offer_signature` non vuoto)
- Email configurata sul partner destinatario
- L'utente che invia deve appartenere al ruolo commerciale o admin

La transizione `approval → sent` (bottone "Approva") richiede:
- Utente approvatore o admin
- Alla conferma, vengono compilati automaticamente `approved_by_id`, `approved_date` e `sent_date`

### 11.9 Integrazione Odoo Sign — Firma digitale via email

#### Flusso completo

Quando l'utente clicca **"Approva"** sull'offerta in stato `approval`:

1. **Genera PDF** — Render del report QWeb dell'offerta (TMB / Discarica / RS) con firma aziendale pre-apposta
2. **Crea `ir.attachment`** — Il PDF viene salvato come allegato Odoo
3. **Crea `sign.template`** — Usa `sign.template.create_sign_template_from_ir_attachment_data()` e imposta `active=True`
4. **Rileva posizioni firma** — `_sign_find_marker_positions()` scansiona il PDF con PyPDF2 `visitor_text` cercando testi marker nel PDF (es. "Letto confermato e sottoscritto", "Il Cliente", "PER ACCETTAZIONE")
5. **Crea `sign.item`** — Box firma posizionati dove rilevati nel PDF (tipo: `sign_item_type_signature`)
6. **Crea `sign.request`** — Con il partner dell'offerta come firmatario, viene inviata automaticamente via email
7. **Stato → `sent`** — L'offerta passa a "Inviata"

#### Rilevamento marker nel PDF (`_sign_find_marker_positions`)

Il motore PDF di wkhtmltopdf usa coordinate cumulative con una content matrix (`cm`) che scala e trasla
la text matrix (`tm`). La posizione reale si ottiene con la moltiplicazione `cm × tm`:

```python
actual_x = cm[0] * tm[4] + cm[2] * tm[5] + cm[4]
actual_y = cm[1] * tm[4] + cm[3] * tm[5] + cm[5]
```

Il testo viene normalizzato con `" ".join(text.split())` per gestire gli spazi variabili inseriti da wkhtmltopdf.

Configurazione marker per tipo offerta (`SIGN_MARKERS`):

| Tipo | Testo marker | dx | dy | Note |
|------|-------------|-----|-----|------|
| Discarica | "Letto confermato e sottoscritto" | -0.17 | 0.08 | Firma principale contratto |
| Discarica | "Firma per presa visione" | -0.17 | 0.03 | Firma Allegato 1 |
| TMB | "Il Cliente" | -0.07 | 0.03 | Firma singola |
| Rifiuti Speciali | "PER ACCETTAZIONE" | -0.07 | 0.03 | Firma singola |

Se nessun marker viene trovato, fallback all'ultima pagina in posizione fissa.

#### Auto-accettazione e auto-rifiuto (`sign.request` override)

Il modello `sign.request` è esteso da `models/sign_request.py` con due hook:

- **`_sign()`**: quando tutti i firmatari completano la firma, se il `reference_doc` è un `tea.offer` in stato `sent`,
  viene chiamato automaticamente `ref.action_accept()` → stato → `accepted` → lead avanza a "Attesa documenti".
- **`_refuse(refuser, refusal_reason)`**: quando un firmatario rifiuta la firma nel portale Sign, se il `reference_doc` è un `tea.offer` in stato `sent`,
  viene chiamato `ref.action_refuse_client(refusal_reason=refusal_reason)` → stato → `refused_client` con il motivo del rifiuto salvato in `refused_reason`.

#### Logging chatter su lead e offerta (`sign.request.item` + wizard)

Tutte le notifiche relative alla richiesta firma vengono loggate sia nel chatter di `tea.offer` che in quello di `crm.lead`:

- **`sign.request.item.send_signature_accesses()`** (override in `models/sign_request.py`): quando l'email di firma viene
  inviata al firmatario, il messaggio "The signature mail has been sent to: ..." viene postato anche nel chatter della lead collegata.
- **`sign.send.request._create_request_log_note()`** (override in `wizards/sign_send_request.py`): quando la sign request
  viene creata, il messaggio "A signature request has been linked to this document: ..." viene postato anche nel chatter della lead.
- **`_post_send_message_on_lead()`** (su `tea.offer`, chiamato dal wizard `create_request`): posta un messaggio dettagliato
  con il PDF allegato sia sul chatter dell'offerta che della lead ("Offerta X inviata per firma digitale a Partner").

#### Personalizzazione email (`data/sign_mail_template.xml`)

L'email di richiesta firma viene personalizzata tramite ereditarietà XPath del template `sign.sign_template_mail_request`:

1. **Rimossa intro** "X has requested your signature..." — per le offerte TEA (conditionale su `_is_tea`)
2. **Aggiunto testo post-firma**: *"Seguirà a questa offerta un'ulteriore email con gli allegati obbligatori da compilare separatamente."*
3. **Rimossa firma utente** (`user_signature`) — per le offerte TEA

Tutte le modifiche sono condizionali: si applicano solo quando la `sign.request` è collegata a un `tea.offer`, 
senza influenzare le altre sign request del sistema.

#### Nascosto "Request Signature" dal menu azioni (`static/src/js/sign_cog_menu.js`)

Override JavaScript del registro `cogMenu`: l'entry `sign-request-menu` viene nascosta quando 
il `resModel` è `tea.offer`, impedendo la creazione manuale di sign request dalla vista offerta.

#### Firma aziendale nei report PDF

La firma dell'azienda (`res.company.tea_offer_signature`) viene inclusa automaticamente
nei report QWeb di **TMB** e **Discarica** (il report Rifiuti Speciali la aveva già).
La firma è un'immagine `<img>` condizionale nella colonna "Per l'Azienda".

#### Vista offerta

- **Smart button "Firma"**: visibile quando `sign_request_id` è valorizzato, apre la form della `sign.request`
- **Bottone "Apri PDF"**: sempre visibile per tutti i ruoli — genera il PDF completo (con documenti allegati concatenati) e lo apre nel browser, senza creare allegati nel chatter
- **Bottoni workflow** (commerciale/admin):
  - "Invia in approvazione" (draft)
  - "Invia mail per firma digitale" (approved)
  - "Accettata" con PDF firmato (approved, se file caricato)
  - "Accettata" (sent, fallback)
  - "Riporta a Bozza" (refused_approver, approved, sent)
- **Bottoni workflow** (approvatore/admin): "Approva" / "Rifiuta" (approval)
- **"Persa"** (commerciale/admin): visibile in tutti gli stati — apre wizard con motivo perdita
- **"Ripristina"** (commerciale/admin): visibile quando lead è persa — riporta in bozza
- **Ribbon "Persa"**: visibile quando `lead_is_active = False`
- **Creazione/eliminazione disabilitate**: `create="0" delete="0"` su form e list

#### Sistema Documenti Cliente (Attesa documenti)

Quando il lead raggiunge lo stage "Attesa documenti" (impostato automaticamente da `action_accept`
sull'offerta), il sistema genera automaticamente i documenti sulla **lead** (`crm.lead`),
basandosi sui template configurati nella tipologia offerta.

##### Modello `tea.offer.type.document` — Template documenti

Configurato nella form della tipologia offerta (Configurazione → Tipologie Offerta).

| Campo | Tipo | Note |
|-------|------|------|
| `offer_type_id` | Many2one → tea.offer.type, cascade | Tipologia di appartenenza |
| `sequence` | Integer | Ordinamento |
| `name` | Char, required | Nome allegato (es. "Contratto", "Modulo Privacy") |
| `template_file` | Binary | Template PDF allegato |
| `template_filename` | Char | Nome file template |
| `requires_signature` | Boolean | Se il documento deve essere restituito firmato |

##### Modello `tea.offer.document` — Documento effettivo sulla lead

Generato automaticamente da `_generate_documents_from_type()` su `crm.lead` al passaggio ad "Attesa documenti".
L'operatore può aggiungere ulteriori documenti manualmente.

| Campo | Tipo | Note |
|-------|------|------|
| `lead_id` | Many2one → crm.lead, cascade | Lead collegata |
| `sequence` | Integer | Ordinamento |
| `name` | Char, required | Nome documento |
| `document_file` | Binary | Documento PDF da inviare |
| `document_filename` | Char | Nome file |
| `requires_signature` | Boolean | Richiede firma dal cliente |
| `received` | Boolean | Documento ricevuto dal cliente |
| `signed` | Boolean | Documento firmato ricevuto (visibile solo se `requires_signature`) |
| `received_file` | Binary | Documento restituito dal cliente |
| `received_filename` | Char | Nome file ricevuto |
| `is_complete` | Boolean, computed, stored | `True` se ricevuto (e firmato se richiesto) |

**Completamento:** `is_complete = received AND (signed IF requires_signature)`

##### Campi su `crm.lead`

| Campo | Tipo | Note |
|-------|------|------|
| `tea_document_ids` | One2many → tea.offer.document | Documenti generati/aggiunti |
| `tea_offer_ids` | One2many → tea.offer | Offerte collegate |
| `tea_offer_count` | Integer, computed | Conteggio per smart button |
| `tea_offer_type_id` | Many2one → tea.offer.type | Tipologia offerta — readonly dopo stage "Nuovo" |
| `tea_offer_type_code` | Char, related | Codice tipologia (da `tea_offer_type_id.code`) — per visibilità condizionale nelle viste |
| `tea_commercial_ref_id` | Many2one → res.users | Referente Commerciale — default utente corrente, tracking=True |
| `tea_offer_state` | Selection, computed | Stato sintetico offerta sulla lead: `no_offer`, `draft`, `approval`, `approved`, `sent`, `accepted`, `refused_client`, `refused_approver`, `lost` |
| `tea_offer_progress` | Integer, computed | Percentuale avanzamento offerta per progress bar (0..100), derivata da `tea_offer_state` |
| `tea_is_new_stage` | Boolean, computed | True se stage corrente = "Nuovo" (usato per readonly tipologia) |
| `tea_is_renewal` | Boolean | Flag rinnovo — distingue rinnovo da nuovo cliente (tutte le tipologie) |
| `tea_has_fidejussione` | Boolean | Fidejussione prevista — visibile solo per Discarica |
| `partner_id` | Many2one → res.partner (override) | Cliente (azienda) — domain `is_company=True`, string "Cliente" |
| `tea_contact_id` | Many2one → res.partner | Contatto (persona fisica) — domain `is_company=False, type=contact, parent_id=partner_id` |
| `tea_photo_status` | Selection | Foto: Non necessarie / Richieste / Ricevute (solo Rifiuti Speciali) |
| `tea_survey_status` | Selection | Sopralluogo: Non necessario / Pianificato / Eseguito (solo Rifiuti Speciali) |
| `tea_plant_info_status` | Selection | Info Impianto Destino: Non necessarie / Richieste / Ricevute (solo Rifiuti Speciali) |
| `tea_client_info_status` | Selection | Info Richieste a Cliente: Non necessarie / Richieste / Ricevute (solo Rifiuti Speciali) |
| `tea_all_documents_complete` | Boolean, computed, stored | True se tutti i documenti (incluse schede di caratterizzazione) sono completi |
| `tea_offer_plant_ids` | Many2many → res.partner, computed | Impianti destino presenti nelle righe offerta RS |
| `tea_offer_product_tmpl_ids` | Many2many → product.template, computed | Prodotti CER presenti nelle righe offerta RS |
| `tea_offer_cer_ids` | Many2many → tea.cer.code, computed | Codici CER aggregati da tutte le offerte collegate (via `tea.offer._get_cer_ids()`) — usato come domain per `sheet_id` nei documenti |

**Selection values:**

- `TRACKING_STATUS` (Foto, Info Impianto, Info Cliente): `not_needed` (Non necessarie) / `waiting` (Richieste) / `received` (Ricevute)
- `SURVEY_STATUS` (Sopralluogo): `not_needed` (Non necessario) / `planned` (Pianificato) / `done` (Eseguito)
- `OFFER_STATE_SELECTION` (stato offerta lead): `no_offer` (Nessuna offerta) / `draft` (Bozza) /
   `approval` (In approvazione) / `approved` (Approvata) / `sent` (Inviata) /
   `accepted` (Accettata) / `refused_client` (Rifiutata da cliente) /
   `refused_approver` (Rifiutata da approvatore) / `lost` (Persa)

**Mappatura avanzamento offerta (`OFFER_PROGRESS_BY_STATE`):**
- `no_offer`: 0
- `draft`: 20
- `approval`: 50
- `approved`: 70
- `sent`: 90
- `accepted`: 100
- `refused_client`: 20
- `refused_approver`: 20
- `lost`: 0

**Codifica colori nelle viste:**
- Giallo (`decoration-warning`): stati pendenti (`waiting`, `planned`)
- Verde (`decoration-success`): stati completati o non necessari (`received`, `done`, `not_needed`)

**Logica `write()` override:**
- Valida transizioni stage tramite `_check_stage_transition()`:
  - Blocca uscita da "Nuovo" senza tipologia impostata
  - Blocca passaggio a "Elaborazione proposta" o oltre se Sopralluogo/Foto/Info Impianto sono "In attesa"
  - Blocca passaggio a "Attesa documenti" o oltre senza almeno un'offerta con stato `accepted`
  - Blocca passaggio a "Offerta accettata" se i documenti non sono tutti completi
- Crea automaticamente `tea.offer` al passaggio a "Elaborazione proposta" se non esistono offerte
- Genera documenti cliente dai template della tipologia al passaggio ad "Attesa documenti" (`_generate_documents_from_type()`)

Azione `action_view_tea_offers()`: apre form (se 1 offerta) o lista (se multiple).
Passa `default_offer_type_id` dal tipo della lead nel contesto. Il contesto include `create: False`
per impedire la creazione manuale anche dalla lista delle offerte aperta dalla lead.


**Vista lead:** Expected Revenue, Probability e AI nascosti. Label `user_id` rinominato da
"Addetto vendite" a "Assegnatario" (xpath string override). Tab "Gestione Rifiuti" visibile
solo per tipo `rifiuti_speciali`, con 4 campi di stato documentazione (widget radio,
con decorazione colore giallo/verde). Tab "Documenti Cliente" visibile quando esistono documenti
(da stage "Attesa documenti" in poi), con alert di completamento e lista inline editabile.
In form e kanban lead è stata aggiunta una sezione "Avanzamento Offerta" con badge stato e
progress bar; in lista lead/opportunità è presente la colonna "Stato Offerta" con chip colorata.
La codifica colore della chip è allineata alla lista offerte: verde=`accepted`,
blu=`sent|approved`, giallo=`approval`, rosso=`refused_client|refused_approver|lost`.
Ordine campi nel gruppo opportunità: Tipologia → Referente Commerciale → Assegnatario →
Data chiusura → Priorità → Tag → Rinnovo → Fidejussione. Tipologia readonly fuori da stage "Nuovo".
Flag "Rinnovo" visibile per tutte le tipologie.
Flag "Fidejussione prevista" visibile solo per Discarica.

### 11.10 Cron: Reminder giornaliero offerte da approvare

Un cron job giornaliero (`ir.cron`) invia automaticamente una email di reminder a tutti gli utenti
con ruolo **Approvatore** (`group_tea_approver`), elencando le offerte in stato "In approvazione".

#### File coinvolti

| File | Contenuto |
|------|-----------|
| `data/approval_reminder_data.xml` | QWeb template email + record `ir.cron` |
| `models/tea_offer.py` | Metodo `_cron_send_approval_reminder()` |

#### Configurazione cron

| Proprietà | Valore |
|-----------|--------|
| Nome | TEA: Reminder offerte da approvare |
| Frequenza | Ogni giorno alle 08:00 UTC (10:00 CEST) |
| Attivo di default | **No** — da attivare manualmente in Impostazioni → Azioni pianificate |
| Modello | `tea.offer` |
| Metodo | `_cron_send_approval_reminder()` |

#### Email inviata

- **Oggetto**: "Offerte Ambiente e Ecologia da approvare su Odoo"
- **Destinatari**: tutti gli utenti attivi del gruppo `group_tea_approver` che hanno email configurata
- **Corpo**: saluto con nome di battesimo, tabella con Riferimento / Tipo Offerta / Cliente / Data Offerta,
  bottone "Approva offerte" che apre la pagina Offerte filtrata per "In approvazione", chiusura cortese
- **Mittente**: email dell'azienda (`res.company.partner_id.email_formatted`)

#### Casi limite gestiti

| Caso | Comportamento |
|------|---------------|
| Nessuna offerta in stato `approval` | Il cron termina senza inviare nulla |
| Gruppo `group_tea_approver` non esiste | Il cron termina senza errore |
| Nessun utente Approvatore | Il cron termina senza inviare nulla |
| Utente Approvatore senza email | Viene escluso dal filtro (non riceve la mail) |
| Utente Approvatore inattivo | Viene escluso dal filtro |
| Errore invio per singolo utente | Loggato come eccezione, gli altri utenti ricevono comunque la mail |

---

## 12. Riepilogo struttura file

```
tea_quotations/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── tea_hp_code.py                       # Custom — codici HP
│   ├── tea_waste_operation.py               # Custom — operazioni R/D
│   ├── tea_cer_code.py                      # Custom — codici CER
│   ├── tea_characterization_sheet.py        # Custom — anagrafica schede di caratterizzazione
│   ├── tea_offer.py                         # Custom — offerta/contratto (TMB + Discarica + RS)
│   ├── tea_offer_type.py                    # Custom — tipo offerta (TMB/Discarica/RS/Standard)
│   ├── tea_offer_type_document.py           # Custom — template documenti per tipologia
│   ├── tea_offer_document.py                # Custom — documento/scheda unificato sulla lead
│   ├── tea_offer_line.py                    # Custom — riga CER offerta RS
│   ├── tea_offer_line_service.py            # Custom — servizio aggiuntivo offerta RS
│   ├── tea_contract_producer.py             # Custom — produttore Allegato 2
│   ├── tea_offer_validity.py                # Custom — tabella validità offerta
│   ├── crm_lead.py                          # Estensione — smart button, documenti, validazioni stage
│   ├── sign_request.py                      # Estensione — auto-accept/refuse offerta + logging chatter lead
│   ├── product_template.py                  # Estensione — campi CER + physical_state
│   ├── product_supplierinfo.py              # Estensione — operazione, HP, minimi
│   ├── res_partner.py                       # Estensione — flag impianto + dati contratto
│   └── res_company.py                       # Estensione — markup % + firma offerte
├── wizards/
│   ├── __init__.py
│   ├── sign_send_request.py                 # Override sign.send.request per post-invio offerta
│   ├── tea_offer_approve_wizard.py          # Wizard approvazione (singola + massiva)
│   ├── tea_offer_approve_wizard_views.xml
│   ├── tea_offer_reject_wizard.py           # Wizard rifiuto approvatore
│   ├── tea_offer_reject_wizard_views.xml
│   ├── tea_offer_lost_wizard.py             # Wizard perdita offerta con motivo
│   ├── tea_offer_lost_wizard_views.xml
│   ├── tea_send_documents_wizard.py         # Wizard invio documenti selezionati via email
│   └── tea_send_documents_wizard_views.xml
├── scripts/
│   ├── import_initial_data.py               # Import dati da Excel (115+63+139+268)
│   ├── create_sample_data.py                # Dati demo per sviluppo
│   └── create_sample_offers.py              # Offerte demo per sviluppo
├── data/
│   ├── tea_hp_code_data.xml                 # 11 codici HP (noupdate=1)
│   ├── tea_waste_operation_data.xml         # 12 operazioni R/D (noupdate=1)
│   ├── crm_stage_data.xml                   # 6 stage CRM pipeline
│   ├── tea_offer_type_data.xml              # 4 tipi offerta + ir.sequence
│   ├── sign_mail_template.xml               # Override email firma digitale per tea.offer
│   └── approval_reminder_data.xml           # Cron + template email reminder approvazione
├── report/
│   ├── __init__.py
│   ├── tea_offer_reports.xml                # Report actions (TMB + Discarica + RS)
│   ├── report_tea_offer_tmb.xml             # QWeb template TMB
│   ├── report_tea_offer_discarica.xml       # QWeb template Discarica
│   └── report_tea_offer_rifiuti_speciali.xml # QWeb template Rifiuti Speciali
├── views/
│   ├── tea_cer_code_views.xml               # CER list/form/search + action
│   ├── tea_characterization_sheet_views.xml # Schede di caratterizzazione
│   ├── product_template_views.xml           # Inherited form/list/search
│   ├── product_supplierinfo_views.xml       # Inherited list/form + action
│   ├── res_partner_views.xml                # Inherited form (tab Impianto + referente)
│   ├── res_company_views.xml                # Inherited form (markup + firma)
│   ├── tea_offer_views.xml                  # Form (TMB/Discarica/RS), List, Search
│   ├── sign_send_request_views.xml          # Wizard firma semplificato per offerte TEA
│   ├── crm_lead_views.xml                   # Smart button, documenti, schede
│   ├── tea_configuration_views.xml          # HP, operazioni, tipologie offerta CRUD
│   └── tea_quotations_menus.xml             # Menu completi (italiano)
├── security/
│   ├── ir.model.access.csv                  # ACL per modelli custom
│   ├── tea_groups.xml                       # Ruoli TEA (Commerciale + Approvatore)
│   └── tea_menu_restrictions.xml            # Override menù + record rules Sign
├── i18n/
│   ├── it.po                                # Traduzioni italiane
│   └── tea_quotations.pot                   # Template traduzioni
├── tests/
│   ├── __init__.py
│   ├── test_tea_hp_code.py
│   ├── test_tea_waste_operation.py
│   ├── test_tea_cer_code.py
│   ├── test_tea_characterization_sheet.py
│   ├── test_product_template.py
│   ├── test_product_supplierinfo.py
│   ├── test_res_partner.py
│   ├── test_tea_offer.py                    # Offerte, stati, firma approvazione
│   ├── test_tea_offer_line.py               # Righe CER, auto-fill prezzi, servizi
│   ├── test_tea_offer_line_service.py
│   ├── test_tea_offer_document.py
│   ├── test_tea_contract_producer.py
│   ├── test_crm_lead.py
│   └── test_wizards.py
├── docs/
│   ├── PIANO_IMPLEMENTAZIONE.md
│   ├── rifiuti_speciali/                    # Template Word di riferimento per PDF RS
│   ├── TEA_AE_Anagrafica_Prodotti_CER_v02.xlsx
│   ├── OFFERTE RIFIUTI SPECIALI_WIP2025.xlsx
│   └── Stampa Unione/                      # Template Word TMB/Discarica
└── static/
    └── src/
        ├── js/
        │   └── sign_cog_menu.js             # Nasconde "Request Signature" dal cog menu
        ├── fonts/
        │   ├── Carlito-Regular.ttf          # Carlito Regular (Apache 2.0)
        │   ├── Carlito-Italic.ttf           # Carlito Italic
        │   ├── Carlito-Bold.ttf             # Carlito Bold
        │   └── Carlito-BoldItalic.ttf       # Carlito Bold Italic
        └── scss/
            └── report_fonts.scss            # @font-face URL-based per report PDF
```

---

> **Nota**: lo storico delle modifiche è disponibile nella history di Git (`git log --oneline`).
