---
name: functional-analysis
description: >
  Genera documenti di Analisi Funzionale Odoo Enterprise strutturati e pronti
  per delivery, seguendo il formato e lo stile Avvale S.p.A. Usa SEMPRE questa
  skill quando l'utente chiede di creare, redigere, completare o aggiornare
  un'analisi funzionale, un documento AS-IS / TO-BE, una gap analysis, un
  documento di specifiche funzionali, o qualsiasi deliverable documentale per
  un progetto Odoo. Triggera anche per richieste tipo: "scrivi l'analisi
  funzionale di", "documenta il processo di", "prepara il documento per il
  modulo X", "crea l'AF per", "aggiorna l'analisi di", "fai la gap analysis di".
  Output principale: file .docx pronto per consegna al cliente o revisione
  interna.
---

# Functional Analysis Generator — Avvale Standard

## Scopo

Produrre documenti di Analisi Funzionale Odoo Enterprise conformi allo standard
Avvale: strutturati, professionali, pronti per delivery cliente o revisione
interna.

## Identità e contesto

Avvale S.p.A. è una società di consulenza ERP. I documenti prodotti sono
destinati sia al cliente (Key User / PM) che al team interno Avvale. Lavora
**esclusivamente** con Odoo **Enterprise**. La versione specifica viene
**sempre** fornita nel prompt — non assumere mai una versione di default.

## Comportamento generale

- Lingua output: **Italiano** (salvo indicazione contraria)
- Formato output principale: **.docx** (Word), generato via skill `docx`
- Se la versione Odoo non è fornita → chiederla prima di procedere
- Se il perimetro non è chiaro → porre **massimo 2 domande** di chiarimento
  prima di procedere con assunzioni dichiarate esplicitamente

---

## Input accettati

| Tipo input | Come gestirlo |
|---|---|
| Testo libero / note workshop | Strutturare secondo le sezioni standard |
| File Excel allegato | Leggere con skill `xlsx` prima di procedere |
| File .docx esistente da aggiornare | Leggere con skill `docx` (unpack) e modificare |
| Brief verbale dell'utente | Porre le domande di intake (vedi sotto) |
| Nessun input | Chiedere le informazioni minime obbligatorie |

---

## Informazioni minime obbligatorie

Se non fornite, chiedere prima di procedere:

1. **Cliente** — ragione sociale
2. **Progetto / Modulo** — es. "CRM - Gestione Preventivi", "Contabilità IT"
3. **Versione Odoo** — **obbligatoria, nessun default**. Avvale lavora
   esclusivamente con Odoo **Enterprise**.
4. **Perimetro** — cosa è in scope (moduli, processi, flussi)
5. **Destinatario** — cliente (key user/PM) e/o interno Avvale
6. **Lingua** — default: Italiano

Assunzioni ragionevoli: dichiararle sempre in testa al documento generato.

---

## Prompt di intake atteso (richiesta utente standard)

Per ogni richiesta di generazione AF, l'utente fornirà tipicamente:

- Cliente, Versione Odoo Enterprise, Modulo/area
- Tipo di richiesta: **NUOVO** o **AGGIORNAMENTO**
- Revisione target e data
- Input allegato e sua natura (appunti / trascrizione / mix)
- Sezioni da generare o aggiornare
- Note specifiche

Se uno di questi campi manca e non è inferibile dall'allegato, chiedi **solo
quello mancante** — non bloccare l'intera generazione.

Per richieste di **AGGIORNAMENTO**: leggere prima il .docx allegato per
estrarre la struttura esistente, poi applicare **solo il delta indicato**.
Le sezioni non menzionate vanno mantenute identiche all'originale.

Template prompt utente → vedere `references/prompt-template.md`.

---

## Struttura standard del documento

Seguire **esattamente** questo ordine di sezioni. Non omettere sezioni — se una
sezione non è applicabile, inserire la nota: *"N/A – non in scope per questa
fase."*

### 1. Copertina (non numerata)
- Logo Avvale (placeholder se non disponibile)
- Titolo: `[Cliente] – [Area] – [Modulo Odoo] – Analisi Funzionale`
- Data, versione, classificazione (Public / Internal / Confidential)
- Footer Avvale standard (vedi `references/avvale-footer.md`)

### 2. Registro Versioni del Documento

Tabella con colonne: **Rev | Descrizione | Data**

Versioning convention:
- `00.x` → bozze da workshop (00.1, 00.2, ...)
- `01.0` → prima versione ufficiale
- `01.x` → revisioni post-delivery

### 3. Indice

Generato automaticamente con `TableOfContents` docx-js, su pagina separata
dopo Registro Versioni.

### 4. Processo AS-IS

Descrivere il processo attuale del cliente **prima** dell'implementazione Odoo.

Struttura consigliata per ogni sotto-processo:
- Contesto e volumi (es. "X operazioni/anno", "team di N persone")
- Attori coinvolti e ruoli
- Flusso operativo (bullet point o prosa strutturata)
- Strumenti attuali (Excel, email, sistemi legacy)
- Pain point espliciti

> **Nota**: l'AS-IS deve essere **descrittivo**, non valutativo. Rimandare le
> considerazioni critiche alla Gap Analysis.

### 5. Sistema TO-BE

Descrivere il futuro stato con Odoo implementato.

Struttura per ogni area funzionale:
- **Utenti e Ruoli** — profili, permessi, segregation of duties
- **Anagrafiche** — struttura dati master (clienti, fornitori, prodotti, ...)
- **Configurazioni** — parametri di sistema, listini, template, workflow
- **Processi operativi** — flusso step-by-step in Odoo con menu path
- **Automazioni** — regole automatiche, scheduled actions, notifiche
- **Report e stampe** — output documentali, template QWeb

#### Pattern processo operativo

Per ogni processo usare questo pattern:

```
[MENU PATH] → [AZIONE UTENTE] → [RISULTATO SISTEMA]
```

Esempio: `CRM > Lead > Nuova` → Compilare cliente e tipologia → Sistema crea
Lead in stato "Nuova".

Tabella step obbligatoria: **Step | Azione utente | Menu path | Risultato sistema**

Includere sempre:
- regole di validazione
- messaggi di errore comuni
- attori coinvolti
- trigger e output del processo

### 6. Gap Analysis

Tabella comparativa AS-IS vs TO-BE con classificazione gap:

| ID | Area | Processo AS-IS | Soluzione TO-BE | Tipo | Effort | Note |
|---|---|---|---|---|---|---|
| GAP-001 | CRM | Excel manuale | Lead Odoo | Standard | Basso | - |
| GAP-002 | Firma | Cartaceo | Sign Odoo / DocuSign | Custom | Medio | OCA o sviluppo |

**Tipi di gap:**
- `Standard` — coperto nativamente da Odoo Enterprise
- `Config` — risolvibile con configurazione, nessuno sviluppo
- `Custom` — richiede sviluppo o modulo OCA
- `Out of scope` — non in perimetro (documentare con "previsto Fase X" o "non in roadmap")

**Effort:**
- Basso: < 0,5 gg
- Medio: 0,5–2 gg
- Alto: > 2 gg

> **Importante**: non includere mai pattern di localizzazione country-specific
> (e-invoicing, compliance fiscale locale) nella gap analysis generica —
> documentarli nella sezione "Configurazioni di Sistema" contestualizzati al
> cliente specifico.

Pattern di gap ricorrenti per modulo → `references/gap-analysis-patterns.md`.

### 7. Configurazioni di Sistema

Elenco delle configurazioni da eseguire in Odoo, raggruppate per modulo.

Per ogni configurazione:
- Menu path
- Parametro / voce da configurare
- Valore / logica da applicare
- Dipendenze (es. "dopo aver configurato X")

### 8. Open Points

Tabella delle questioni aperte, decisioni pendenti o informazioni mancanti.

| ID | Descrizione | Responsabile | Data limite | Stato |
|---|---|---|---|---|
| OP-001 | Confermare gestione firma digitale | Cliente – Mario Rossi | 30/04/2026 | Aperto |

---

## Istruzioni per la generazione .docx

1. Leggere prima la skill `docx` per le istruzioni tecniche di generazione
2. Usare **A4** come formato pagina (11906 × 16838 DXA)
3. Margini: **1440 DXA** (≈ 2,54 cm) su tutti i lati
4. Font: **Arial** come font di sistema
5. Palette colori Avvale → `references/avvale-style.md`
6. Intestazione: titolo documento + numero revisione (destra) | logo (sinistra),
   bordo inferiore `#3B9408`
7. Footer: copyright Avvale + dati societari → `references/avvale-footer.md`
8. TOC automatico su pagina separata dopo Registro Versioni
9. Numerazione pagine: footer centrato, formato "Pagina X di Y"

### Tabelle standard
- Header row: sfondo `#3B9408` (verde Avvale), testo bianco bold
- Righe alternate: `#D9EAD3` / bianco
- Bordi: `#CCCCCC`, `BorderStyle.SINGLE`, size 1
- Sempre `ShadingType.CLEAR` (mai SOLID)

### Heading levels
- H1 → sezioni principali (AS-IS, TO-BE, Gap Analysis, …) — Arial 16pt bold `#2D7206`
- H2 → sotto-sezioni (es. "Gestione Lead", "Anagrafica CER") — Arial 13pt bold `#3B9408`
- H3 → dettagli (es. "Campi obbligatori", "Regole di validazione") — Arial 11pt bold `#595959`

---

## Assunzioni

Quando mancano informazioni, procedere con assunzioni ragionevoli **dichiarate
esplicitamente** in una nota all'inizio del documento:

> **Nota metodologica**: Le seguenti assunzioni sono state applicate in assenza
> di indicazioni esplicite: [elenco assunzioni]. Eventuali variazioni potranno
> impattare scope e tempi.

---

## Dipendenze skill

| Condizione | Skill da invocare |
|---|---|
| Output finale | `docx` (sempre) |
| Input è file Excel | `xlsx` (prima di procedere) |
| Input è .docx esistente | `docx` in modalità edit (unpack → modifica → repack) |
| Input è PDF | `pdf` |

---

## Reference files

Leggere i reference solo quando servono per il task corrente, non tutti per
default:

- `references/avvale-style.md` → palette colori, tipografia, esempi heading,
  spacing paragrafi, stili docx-js
- `references/avvale-footer.md` → testo footer societario standard +
  implementazione docx-js header/footer
- `references/section-templates.md` → blocchi di testo riutilizzabili per
  ogni sezione ricorrente (registro versioni, AS-IS, TO-BE, processo, gap,
  open points, nota di assunzione)
- `references/gap-analysis-patterns.md` → pattern comuni di gap per moduli
  Odoo standard (CRM, Vendite, Contabilità, Acquisti) + moduli OCA frequenti
- `references/prompt-template.md` → template di intake per richieste di
  aggiornamento AF
