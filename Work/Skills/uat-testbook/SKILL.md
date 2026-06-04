---
name: uat-testbook
description: >
  Genera file Excel di UAT Test Book per progetti Odoo Enterprise, seguendo
  il formato standard Avvale con fogli Summary, Test book - Funzionale,
  Test book - Tecnico e Data validation. Usa SEMPRE questa skill quando
  l'utente chiede di creare, generare, aggiornare o compilare un test book,
  un UAT plan, un piano di test, casi di test UAT, o qualsiasi documento
  Excel per la fase di User Acceptance Testing su Odoo. Triggera anche per:
  "prepara i test UAT per", "crea il test book del modulo X", "aggiungi
  test case per", "genera l'Excel UAT per", "aggiorna il test book".
  Output: file .xlsx con due Test book separati (Funzionale per il cliente,
  Tecnico per QA interno), Summary automatico e dropdown preconfigurati.
---

# UAT Test Book Generator — Avvale Standard

## Scopo

Produrre file Excel UAT Test Book conformi allo standard Avvale con **due
Test book separati**:

- **Test book - Funzionale** → consegnato al cliente, contiene test che
  riproducono i **processi end-to-end** descritti nell'Analisi Funzionale,
  con righe di **intro processo** in linguaggio non tecnico prima dei test
  di ogni area. Pensato per essere eseguito in workshop con il cliente.
- **Test book - Tecnico** → uso interno QA Avvale, contiene controlli
  granulari su vincoli, validazioni, ACL/permessi, cron, import, edge case
  e tutto ciò che il cliente non deve vedere ma che noi dobbiamo testare
  prima della consegna.

Entrambi i fogli condividono lo stesso Summary con totali per foglio,
per stato e per area.

---

## Filosofia: Funzionale vs Tecnico

| Aspetto              | Test book - Funzionale                                  | Test book - Tecnico                                   |
|----------------------|---------------------------------------------------------|-------------------------------------------------------|
| **Pubblico**         | Cliente (key user, sponsor, business owner)             | QA Avvale, consultant interno                         |
| **Quando si esegue** | Workshop UAT con cliente                                | Pre-UAT, internal dry-run                             |
| **Cosa testa**       | Processi end-to-end, decisioni di business, output cliente-visibili | Vincoli DB, ACL, formule, cron, import, edge case |
| **Wording**          | Non tecnico, orientato all'attività di business         | Tecnico, riferimenti a campi/modelli/log              |
| **Intro per area**   | Sì, paragrafo descrittivo del processo                  | No, solo header colonne                               |
| **Esempio**          | "Crea Lead → qualifica in Opportunità → genera Offerta → invia a firma" | "Verifica che `state` sia `draft` alla creazione" |

**Regola di classificazione** — durante l'intake, per ogni test case decidere
l'audience con questo criterio:

- **F (Funzionale)** se il test riproduce un'azione che il cliente farà
  realmente in produzione, ha output visibile e fa parte di un processo
  documentato nell'AF.
- **T (Tecnico)** se il test verifica un vincolo, una regola di sicurezza,
  un comportamento di sistema (cron, sequence, log) o un edge case che il
  cliente non eseguirebbe spontaneamente.

In dubbio → **T**. È meglio avere il foglio Funzionale snello che gonfiarlo
con dettagli che frustrano il cliente in workshop.

---

## Struttura file — 4 fogli obbligatori

### Foglio 1: Summary

Sezione **Totali generali** (somma dei due Test book):

- Contatore totale test case
- Contatori per stato: `to be tested | passed | to be retested | failed | blocked | post-poned`

Sezione **Per foglio**:

| Foglio                  | Test Case | Passed | Failed |
|-------------------------|-----------|--------|--------|
| Test book - Funzionale  | =COUNTA   | =COUNTIFS | =COUNTIFS |
| Test book - Tecnico     | =COUNTA   | =COUNTIFS | =COUNTIFS |

Sezione **Per area** (separata per foglio): colonne `Area | Test Case | Passed | Result %`

Tutto alimentato tramite formule **COUNTIF / COUNTIFS / COUNTA** — mai
hardcoded.

### Foglio 2: Test book - Funzionale

Struttura colonne identica al foglio Tecnico (vedi sotto), ma con
**righe intro processo** prima dei test di ogni area.

**Riga intro processo**:

- Cella A merged su A:K, altezza ~80 pt
- Sfondo `#FFF2CC` (giallo chiaro), font Arial 11 bold italic, colore `#1F4E79`
- Testo: `"Area {N} - {Nome Area}\n\n{descrizione processo non tecnica, 3-5 frasi}"`
- La descrizione spiega in linguaggio business cosa il cliente vedrà nei
  test successivi: chi fa cosa, perché, quale risultato osservare.

**Importante per le formule Summary**: la riga intro ha colonne C, D, H
vuote, quindi `COUNTA('Test book - Funzionale'!D2:D500)` conta solo i
test reali (no falsi positivi).

### Foglio 3: Test book - Tecnico

Stesso layout colonne, **senza** righe intro. Solo header + righe test.

### Colonne fisse (entrambi i Test book)

| Colonna | Nome                   | Tipo     | Note                                              |
|---------|------------------------|----------|---------------------------------------------------|
| A       | ID                     | Numero   | ID area (intero, **non** progressivo per test case) |
| B       | Area                   | Testo    | Nome area funzionale                              |
| C       | Step ID                | Numero   | Progressivo **per area**                          |
| D       | Title                  | Testo    | Titolo sintetico del test case                    |
| E       | Pre-requisite          | Testo    | Condizioni necessarie prima del test              |
| F       | Test Step description  | Testo    | Cosa fa il tester step-by-step                    |
| G       | Expected result        | Testo    | Risultato atteso da Odoo                          |
| H       | Test Result            | Dropdown | Valori da Data validation: esito test             |
| I       | Test Date              | Testo    | Data esecuzione (es. "January 8th")               |
| J       | Tester                 | Testo    | Chi ha eseguito il test                           |
| K       | Notes                  | Testo    | Note libere, bug, osservazioni                    |

### Foglio 4: Data validation

Contiene le liste valori per i dropdown del foglio Test book:

| Riferimento     | Lista                | Valori                                                              |
|-----------------|----------------------|---------------------------------------------------------------------|
| Test Result     | Test book col H      | `to be tested, passed, to be retested, failed, blocked, post-poned` |
| Issue status    | riferimento          | `opened, in progress, resolved, to be tested, closed`               |
| Issue priority  | riferimento          | `P1 - Critical, P2 - High, P3 - Medium, P4 - Low`                   |

---

## ID e Step ID — logica di numerazione

- **ID** = identificatore dell'**Area funzionale** (intero, stesso per tutti
  i test case della stessa area). Il numero di area è **condiviso** fra i
  due fogli: se "CRM Lead-to-Opportunity" è Area 1 nel foglio Funzionale,
  i suoi test Tecnici hanno ID=1 nel foglio Tecnico.
- **Step ID** = progressivo all'interno dell'area, **indipendente per
  foglio**. Funzionale e Tecnico hanno ciascuno la propria sequenza
  partendo da 1.

Esempio:

```
# Test book - Funzionale
ID  Area                    Step ID  Title
1   CRM Lead-to-Opportunity 1        Crea Lead da modulo web
1   CRM Lead-to-Opportunity 2        Qualifica Lead in Opportunità
2   Offerta                 1        Genera Offerta da Opportunità

# Test book - Tecnico
ID  Area                    Step ID  Title
1   CRM Lead-to-Opportunity 1        Vincolo email obbligatoria su lead
1   CRM Lead-to-Opportunity 2        ACL Sales/User non vede team altri
2   Offerta                 1        Sequence auto-genera numero progressivo
```

---

## Aree funzionali standard

Le aree riflettono i **processi di business**, non i moduli Odoo tecnici.
Adattare al perimetro indicato nel prompt.

| ID | Area (processo)                            | Moduli Odoo coinvolti              |
|----|--------------------------------------------|------------------------------------|
| 1  | Login & Navigation                         | Base, Web                          |
| 2  | Anagrafiche (Master data)                  | Contacts, Product, Pricelist       |
| 3  | CRM — Lead-to-Opportunity                  | CRM                                |
| 4  | Offerta / Quotation                        | Sales, modulo custom               |
| 5  | Contratto & Firma digitale                 | Sign, modulo custom contratti      |
| 6  | Order-to-Cash (vendita, consegna, incasso) | Sales, Stock, Account              |
| 7  | Procure-to-Pay (acquisto, ricezione, pagamento) | Purchase, Stock, Account      |
| 8  | Magazzino & Logistica                      | Stock, Inventory                   |
| 9  | Contabilità & Reporting                    | Account, Analytic                  |
| 10 | Permessi e sicurezza                       | Res.Users, Groups, ir.rule         |

Se il perimetro include integrazioni (SAP, Tagetik, FINA HR, EDI/SDI),
aggiungere aree dedicate con ID progressivi.

Per dettagli sui test case standard per ciascuna area → vedere
`references/test-case-library.md`.

---

## Formattazione Excel

### Colori Avvale

| Uso                            | Hex                                         |
|--------------------------------|---------------------------------------------|
| Header colonne                 | `#1F4E79` (blu scuro) con testo bianco bold |
| Righe alternate                | `#D9E2F3` / bianco                          |
| Header Summary sezione         | `#2E75B6` con testo bianco                  |
| Intro processo (foglio Funz.)  | `#FFF2CC` (giallo chiaro), testo `#1F4E79`  |
| Bordi                          | `#CCCCCC` stile thin                        |

### Larghezze colonne (approssimative)

| Col | Larghezza |
|-----|-----------|
| A (ID)                    | 6  |
| B (Area)                  | 22 |
| C (Step ID)               | 10 |
| D (Title)                 | 32 |
| E (Pre-requisite)         | 35 |
| F (Test Step description) | 50 |
| G (Expected result)       | 50 |
| H (Test Result)           | 16 |
| I (Test Date)             | 14 |
| J (Tester)                | 18 |
| K (Notes)                 | 30 |

### Altre impostazioni
- Font: **Arial 10pt** per dati, **Arial 11pt bold** per header
- Testo a capo (`wrap_text=True`) su colonne E, F, G, K
- Riga header bloccata (`freeze_panes = 'A2'`) su entrambi i Test book
- `row_height` righe dati: **45 pt**
- `row_height` righe intro processo (solo Funzionale): **80 pt**
- Dropdown su colonna H via `openpyxl.worksheet.datavalidation.DataValidation`
  applicato a entrambi i fogli Test book

### Dropdown Test Result (colonna H, entrambi i fogli)

```python
from openpyxl.worksheet.datavalidation import DataValidation

for ws in (ws_funzionale, ws_tecnico):
    dv = DataValidation(
        type="list",
        formula1='"to be tested,passed,to be retested,failed,blocked,post-poned"',
        allow_blank=True,
        showDropDown=False
    )
    dv.sqref = "H2:H500"
    ws.add_data_validation(dv)
```

### Intro processo (solo foglio Funzionale)

```python
# Inserire prima dei test di ciascuna area
from openpyxl.styles import Font, PatternFill, Alignment

intro_text = f"Area {area_id} - {area_name}\n\n{process_description}"
ws_funzionale.cell(row=row_idx, column=1, value=intro_text)
ws_funzionale.merge_cells(start_row=row_idx, start_column=1, end_row=row_idx, end_column=11)
cell = ws_funzionale.cell(row=row_idx, column=1)
cell.font = Font(name="Arial", size=11, bold=True, italic=True, color="1F4E79")
cell.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
ws_funzionale.row_dimensions[row_idx].height = 80
```

---

## Summary — formule

```python
# === TOTALI GENERALI (somma fogli) ===
ws_summary['B2'] = "=COUNTA('Test book - Funzionale'!D2:D500)+COUNTA('Test book - Tecnico'!D2:D500)"

# Contatori per stato
for row, status in enumerate(["to be tested", "passed", "to be retested",
                              "failed", "blocked", "post-poned"], start=4):
    ws_summary[f'B{row}'] = (
        f"=COUNTIF('Test book - Funzionale'!H2:H500,\"{status}\")"
        f"+COUNTIF('Test book - Tecnico'!H2:H500,\"{status}\")"
    )

# === PER FOGLIO ===
ws_summary['B12'] = "=COUNTA('Test book - Funzionale'!D2:D500)"
ws_summary['C12'] = "=COUNTIF('Test book - Funzionale'!H2:H500,\"passed\")"
ws_summary['D12'] = "=COUNTIF('Test book - Funzionale'!H2:H500,\"failed\")"

ws_summary['B13'] = "=COUNTA('Test book - Tecnico'!D2:D500)"
ws_summary['C13'] = "=COUNTIF('Test book - Tecnico'!H2:H500,\"passed\")"
ws_summary['D13'] = "=COUNTIF('Test book - Tecnico'!H2:H500,\"failed\")"

# === PER AREA (esempio Area = "CRM Lead-to-Opportunity") ===
# Funzionale
ws_summary['B16'] = "=COUNTIF('Test book - Funzionale'!B2:B500,\"CRM Lead-to-Opportunity\")"
ws_summary['C16'] = "=COUNTIFS('Test book - Funzionale'!B2:B500,\"CRM Lead-to-Opportunity\",'Test book - Funzionale'!H2:H500,\"passed\")"
# Tecnico
ws_summary['D16'] = "=COUNTIF('Test book - Tecnico'!B2:B500,\"CRM Lead-to-Opportunity\")"
ws_summary['E16'] = "=COUNTIFS('Test book - Tecnico'!B2:B500,\"CRM Lead-to-Opportunity\",'Test book - Tecnico'!H2:H500,\"passed\")"
```

**Nota**: le righe intro processo nel foglio Funzionale hanno colonna D
vuota → `COUNTA('Test book - Funzionale'!D2:D500)` conta correttamente
solo i test reali, ignorando le intro.

---

## Istruzioni generazione

1. Leggere la skill `xlsx` per le istruzioni tecniche openpyxl
2. Usare **openpyxl** (non pandas) per preservare formule e formattazione
3. Tutti i valori `Test Result` iniziali = `"to be tested"` (mai blank)
4. Salvare in `outputs/[Cliente]_UAT_test_book_v[N].xlsx`
5. Dopo la generazione, eseguire (se disponibile) `scripts/recalc.py` per
   forzare il ricalcolo delle formule a livello cella

---

## Processo di intake — OBBLIGATORIO prima della generazione

Non generare il file finché non hai completato tutti e 5 gli step.
**Gestisci un'area alla volta. Non anticipare la generazione.**

### Step 1 — Parametri base

Se non già forniti, chiedere:

- **Cliente** — ragione sociale (usato nel nome file)
- **Versione Odoo Enterprise** — obbligatoria, **nessun default**
- **Versione file** — es. v1, v2, v3 (default: v1)
- **Lingua test case** — Inglese (default) o Italiano

### Step 2 — Definizione aree

Chiedere: *"Quali aree (processi) vuoi includere nel test book?"*

Proporre le aree standard:

```
1. Login & Navigation
2. Anagrafiche
3. CRM — Lead-to-Opportunity
4. Offerta
5. Contratto & Firma digitale
6. Order-to-Cash
7. Procure-to-Pay
8. Magazzino & Logistica
9. Contabilità & Reporting
10. Permessi e sicurezza
```

L'utente può: confermare tutte, selezionarne un sottoinsieme, rinominarne,
aggiungerne di custom (es. "Integrazione SAP", "EDI/SDI", "Sign avanzato",
"Cron e scheduled actions").

Assegnare ID progressivi alle aree confermate.

### Step 3 — Test case per area (una alla volta)

Per ogni area confermata, chiedere:

> *"Per l'area **[nome]**: vuoi usare i test case standard, definirli tu, o un mix?"*

- **Standard** → usare `references/test-case-library.md`
- **Custom** → l'utente li elenca in formato libero, Claude li struttura
  e classifica F/T
- **Mix** → partire dagli standard, chiedere aggiunte/rimozioni/modifiche

Per ogni test case, classificare **F (Funzionale)** o **T (Tecnico)**.
Vedere "Filosofia: Funzionale vs Tecnico" per il criterio.

### Step 4 — Descrizione processo per area (solo F)

Per ogni area con almeno un test F, chiedere/proporre la **descrizione
processo non tecnica** (3-5 frasi) che andrà nell'intro del foglio
Funzionale.

Esempi:

> **Area 3 — CRM Lead-to-Opportunity**: Il commerciale riceve una richiesta
> da un potenziale cliente (tramite form web, telefono o email). La registra
> come Lead in Odoo, raccoglie le informazioni essenziali e qualifica il
> contatto. Quando il Lead diventa concreto, viene convertito in Opportunità
> e assegnato al team commerciale per la preparazione dell'offerta.

> **Area 5 — Contratto & Firma digitale**: Una volta accettata l'offerta,
> il sistema genera il contratto in PDF con i dati del cliente, le clausole
> e i campi firma. Il contratto viene inviato al cliente via email tramite
> il modulo Sign. Il cliente firma online, poi firma anche l'interno Avvale,
> e il contratto risulta automaticamente "Firmato" in Odoo.

Se la libreria standard ha già una descrizione per l'area, proporre quella
e chiedere conferma/modifiche.

### Step 5 — Riepilogo e conferma

Mostrare tabella riepilogativa prima di generare:

| Area                       | F (Funz.) | T (Tec.) | Totale | Tipo     |
|----------------------------|-----------|----------|--------|----------|
| Login & Navigation         | 2         | 3        | 5      | standard |
| CRM Lead-to-Opportunity    | 4         | 2        | 6      | mix      |
| Contratto & Firma          | 6         | 4        | 10     | standard |
| Integrazione SAP           | 0         | 5        | 5      | custom   |
| **Totale**                 | **12**    | **14**   | **26** |          |

Chiedere: *"Confermo e genero il file?"*
Generare **solo** dopo risposta affermativa esplicita.

---

## Dipendenze skill

| Condizione                                    | Skill                                                  |
|-----------------------------------------------|--------------------------------------------------------|
| Sempre                                        | `xlsx` (generazione file)                              |
| Input è test book esistente da aggiornare     | `xlsx` in modalità read → modifica → salva             |
| Input include AF o specifiche funzionali      | `functional-analysis` (estrarre processi end-to-end)   |

---

## Reference files

- `references/test-case-library.md` → libreria test case standard
  organizzata per processo, con descrizione intro e classificazione F/T
  per ogni test. Caricare **solo** quando l'utente sceglie "standard" o
  "mix" per un'area nello Step 3. Non caricare se l'utente definisce tutti
  i test case custom.

---

## Anti-pattern da evitare

- **Test funzionali troppo tecnici** — "Verifica che `state` sia `draft`":
  questo è T, non F. Riformulare come "Verifica che la nuova offerta
  risulti in stato Bozza e non sia inviata".
- **Test funzionali atomici sconnessi** — il foglio Funzionale deve
  raccontare il processo. Anche se i test restano brevi (un'azione per
  riga), devono seguire l'ordine del workflow reale (Lead → Opportunità
  → Offerta → Firma → Contratto firmato).
- **Intro processo generiche o copiate dal manuale Odoo** — devono
  riflettere il contesto cliente specifico estratto dall'AF.
- **Test duplicati F+T** — se un test verifica la stessa cosa in modo
  funzionale e tecnico, tenerne uno solo (preferenza T se il check è
  un vincolo DB, F se è un'azione utente).
- **Riempire il foglio Funzionale con > 150 test** — workshop UAT con
  cliente realistico ~1 giorno. Se servono più test, spostarli su Tecnico
  o splittarli su più sessioni.
