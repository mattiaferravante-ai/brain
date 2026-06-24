---
name: user-manual
description: >
  Genera Manuali Utente Odoo Enterprise strutturati e pronti per delivery,
  seguendo il formato standard Avvale S.p.A. Usa SEMPRE questa skill quando
  l'utente chiede di creare, redigere, completare o aggiornare un manuale
  utente, una guida operativa, una guida end-user, una documentazione utente,
  o qualsiasi documento che spiega come usare Odoo a un utente finale o a
  un key user. Triggera anche per: "scrivi il manuale per", "prepara la guida
  utente di", "crea la documentazione utente per", "manuale operativo per",
  "guida key user per", "documenta come si usa il modulo X".
  Output principale: file .docx pronto per consegna al cliente.
---

# User Manual Generator — Avvale Standard

## Scopo

Produrre Manuali Utente Odoo Enterprise conformi allo standard Avvale:
scritti in linguaggio operativo (non tecnico), strutturati per flusso di
lavoro reale, pronti per delivery cliente.

## Identità e contesto

Il Manuale Utente è un documento destinato all'**utente finale** del cliente
(Commerciale, Operatore, Key User), non al team IT. Deve rispondere alla
domanda: *"Come si usa questo sistema nel mio lavoro quotidiano?"*

- Lingua: **Italiano** (default)
- Formato: **.docx** (Word), generato via skill `docx`
- Tone of voice: operativo, diretto, non tecnico. Descrivere le azioni
  in termini di quello che l'utente vede e fa, non come funziona il sistema
  internamente.

---

## Informazioni minime obbligatorie

Se non fornite, chiedere prima di procedere:

1. **Cliente** — ragione sociale
2. **Modulo / Area** — es. "Gestione Offerte e Contratti", "CRM Commerciale"
3. **Versione Odoo** — obbligatoria, nessun default
4. **Ruoli utente** — nomi e breve descrizione delle responsabilità
5. **App installate** — le app Odoo accessibili al cliente per questo perimetro
6. **Flussi da documentare** — processi principali (es. lead → offerta → firma)
7. **Varianti di processo** — tipologie (es. Rifiuti Speciali / TMB / Discarica) se presenti
8. **Sezione Key User** — includere Appendice Key User? (default: sì se modulo ha configurazione)

---

## Struttura standard del documento

Seguire esattamente questo ordine. Non omettere parti — se una parte non è
applicabile, inserire: *"N/A – non in scope per questa versione."*

### Copertina (non numerata)

- Logo Avvale → path da `avvale-brand` → `tokens.logo.paths.pos`
- Eyebrow: `MANUALE UTENTE` — Archivo Bold 11pt caps, Celadon Green
- Titolo: `[Cliente] – [Modulo] – Manuale Utente – Odoo [versione] Enterprise`
- Tabella metadati (allineata, font Regular):

| Campo          | Valore                                      |
|----------------|---------------------------------------------|
| Documento      | Manuale Utente – [Modulo]                   |
| Cliente        | [Ragione sociale]                           |
| Versione       | Rev. X.Y                                    |
| Data           | [Mese AAAA]                                 |
| Classificazione| Confidential                                |
| Redatto da     | Avvale S.p.A.                               |

- Footer Avvale → skill `avvale-brand` → `references/docx_brand.md`

### Registro Versioni

| Rev  | Descrizione                                        | Data       |
|------|----------------------------------------------------|------------|
| 1.0  | Prima emissione – [titolo manuale completo]        | [Mese AAAA]|

Versioning: `1.0` → prima emissione, `1.x` → aggiornamenti post-delivery.

### Indice

TOC automatico su pagina separata dopo Registro Versioni.

---

### PARTE 1 – LE APP E I RUOLI

#### 1.1 Applicazioni disponibili

Tabella: **App | Utilizzo**

Per ogni app: nome app Odoo (grassetto) + descrizione funzionale in linguaggio
utente (es. "Gestione lead e pipeline commerciale — punto di ingresso per ogni
nuova trattativa"). Non includere dettagli tecnici sui moduli.

#### 1.2 Ruoli utente

Tabella: **Ruolo | Chi è | Cosa può fare**

- Descrivere i ruoli in termini di attività concrete, non di gruppi tecnici Odoo
- Massimo 4-5 ruoli. Se ce ne sono di più, raggrupparli per area funzionale
- Indicare sempre chi assegna i ruoli (es. "Il ruolo viene assegnato
  dall'amministratore al momento della creazione dell'utente")

---

### PARTE 2 – ODOO: BASI OPERATIVE

Sezione fissa per tutti i manuali. Adattare solo gli esempi al contesto cliente.
Vedere `references/section-templates.md` per il testo standard.

Sottosezioni obbligatorie:

#### 2.1 Accesso e navigazione

- URL di accesso e credenziali
- Home page Odoo, breadcrumb, logo per tornare alla home

#### 2.2 Il Chatter — Comunicazione sul record

Tabella: **Azione | Destinatari | Quando usarla**
- Invia messaggio (email al cliente, tracciata)
- Registra nota (solo interna, NON inviata al cliente)
- Allega file
- NOTA di warning: distinguere chiaramente Invia messaggio vs Registra nota

#### 2.3 Attività e promemoria

- Come creare un'attività (passi operativi)
- Tipi disponibili: Chiamata, Email, Riunione, Scadenza
- Significato colori badge: Verde (futura), Arancio (oggi), Rosso (scaduta)

#### 2.4 Ricerca e filtri

- Barra di ricerca, Filtri, Raggruppa per, Preferiti
- Esempio concreto con i filtri più usati nel contesto del cliente

---

### PARTE 3 – PIPELINE / FLUSSO PRINCIPALE

Nome sezione: `PARTE 3 – PIPELINE [NOME]: LE [N] FASI` (adattare al modulo).

Tabella fasi: **# | Fase | Come si avanza | Note**

Colonna "Tipo":
- `Manuale` — l'utente sposta la card o clicca un pulsante
- `AUTOMATICO` — il sistema avanza la fase senza intervento utente
- `Manuale + Auto` — l'utente compie un'azione che scatena l'avanzamento

Indicare sempre:
- In quale momento avviene l'avanzamento automatico (es. "quando il cliente firma")
- Quando una fase può essere saltata o non è percorribile
- Come si gestisce il caso negativo (perso, rifiutato, archiviato)

---

### PARTE 4 – PROCESSO [MODULO]: PASSO PER PASSO

Nome sezione: `PARTE 4 – PROCESSO [NOME]: PASSO PER PASSO`

Sottosezioni numerate `4.1`, `4.2`, ... per ogni macro-passo del flusso
principale. Ogni sottosezione copre una fase o un'azione specifica.

#### Pattern per ogni sottosezione

Titolo: `4.N  [Fase o Azione]`

Struttura contenuto:
1. **Contesto** — breve intro su quando/perché si arriva qui (1-2 frasi)
2. **Azioni operative** — bullet point con passi esatti nell'ordine in cui
   l'utente li esegue. Usare verbi all'imperativo: Cliccare, Selezionare,
   Compilare, Salvare. Indicare sempre il percorso menu quando cambia contesto.
3. **Tabella effetti** (se una sezione ha più esiti possibili):
   `Azione | Effetto` oppure `Scenario | Cosa succede`
4. **NOTA:** per avvertenze critiche (blocchi di sistema, dati non modificabili
   dopo il salvataggio, azioni irreversibili)
5. **SUGGERIMENTO:** per consigli pratici e best practice (opzionale)

#### Convenzioni testo

- Percorsi menu: `App → Menu → Sottomenu` (monospace o grassetto)
- Pulsanti e campi UI: `'Nome pulsante'` tra virgolette singole e grassetto
- Chip/stato colorato: descrivere sempre con il colore + significato:
  Verde = ..., Blu = ..., Giallo = ..., Rosso = ...
- Automazioni: evidenziare AUTOMATICO in maiuscolo o con nota dedicata

---

### PARTE 5 – FLUSSO SINTETICO PER TIPOLOGIA

Includere solo se il processo ha varianti per tipologia (es. prodotti/clienti
diversi che seguono flussi leggermente diversi).

Per ogni variante: tabella `Step | Fase CRM | Tipo | Azione`

- Tipo: `Manuale`, `AUTOMATICO`, `Manuale + Auto`
- Azione: descrizione sintetica (max 15 parole) dell'azione chiave per lo step
- Limitare a 6-8 step per variante — questa è una quick reference, non il
  manuale completo
- Rinviare a PARTE 4 per i dettagli

---

### APPENDICE – GUIDA KEY USER

Includere quando il perimetro comprende operazioni di configurazione eseguite
dal Key User / Admin.

Titolo: `APPENDICE – GUIDA KEY USER`

Sottosezioni `A.1`, `A.2`, ...

#### Pattern per ogni sottosezione Key User

```
#### A.N  [Nome configurazione]

**Percorso:** App → Menu → Sottomenu

[Tabella o lista delle operazioni disponibili]

[Istruzioni per le operazioni CRUD più comuni: Crea, Modifica, Elimina]

NOTA: [eventuali vincoli di sistema, impatto sulle altre configurazioni,
chi deve essere consultato prima di modificare]
```

Voci tipiche dell'appendice (adattare al modulo):
- Gestione anagrafiche (prodotti, clienti, categorie)
- Configurazione listini / prezzi
- Gestione utenti e permessi (ruoli, gruppi, accessi)
- Template documenti
- Automazioni e azioni pianificate (cron)
- Parametri di sistema / configurazione modulo

---

## Callout standard

Usare in modo consistente in tutto il documento:

```
NOTA:  [testo avvertenza — bloccante o criticamente importante per l'utente]

SUGGERIMENTO:  [consiglio pratico, non obbligatorio]
```

Formattazione:
- `NOTA:` → Box con sfondo Pistachio 15% (`#AACE7C` opacità 15%), bordo
  sinistro 3pt Celadon Green, testo Regular 11pt Raisin Black
- `SUGGERIMENTO:` → Box con sfondo `#F5F5F5`, bordo sinistro 3pt `#47B1A3`
  (Keppel), testo Regular 11pt Raisin Black
- Entrambi usano il prefisso in Archivo Bold caps come label

---

## Istruzioni per la generazione .docx

> **Prerequisito brand**: caricare skill `avvale-brand` prima di generare.
> Leggere `tokens.json` e `references/docx_brand.md`.

1. Leggere la skill `docx` per le istruzioni tecniche di generazione
2. Formato pagina: **A4** (11906 × 16838 DXA)
3. Margini: **1440 DXA** (≈ 2,54 cm) su tutti i lati
4. Font: **Archivo** — fallback: Inter → Helvetica → Arial
5. Palette colori → `avvale-brand` → `tokens.json` (signature: Celadon Green `#248B7E`)
6. Header: logo `logo_pos.png` in alto a sinistra (h ≈ 12mm), linea grigia
   sottile (`#E5E5E5` 1pt). Disabilitato sulla cover.
7. Footer: nome documento + data (sinistra), "Pag. X di Y" (destra),
   Archivo Regular 9pt. Disabilitato sulla cover.
8. TOC automatico su pagina separata

### Heading levels

- H1 (`PARTE N`) → Archivo Bold 20pt, Celadon Green `#248B7E`
- H2 (es. `4.1 Titolo`) → Archivo Bold 16pt, Raisin Black `#231C1D`
- H3 (es. `A.1 Titolo`) → Archivo Bold 13pt, Raisin Black `#231C1D`

### Tabelle

- Header row: sfondo Celadon Green `#248B7E`, testo bianco, Archivo Bold 11pt
- Righe alternate: `#F5F5F5` / bianco
- Bordi orizzontali: 0.5pt grigio `#CCCCCC`
- Padding cella: 4pt verticale, 8pt orizzontale

### Testo body

- Archivo Regular 11pt, Raisin Black `#231C1D`, interlinea 1.4
- Bullet: `•` U+2022, allineamento sinistra, indentazione 0.5cm per livello

---

## Processo di intake

Se le informazioni non sono complete, fare al massimo **2 domande** prima
di procedere con assunzioni dichiarate esplicitamente.

Per richieste di **aggiornamento**: leggere il .docx esistente per estrarre
la struttura attuale, poi applicare solo il delta indicato. Le sezioni non
menzionate vanno mantenute identiche all'originale.

---

## Dipendenze skill

| Condizione                              | Skill da invocare               |
|-----------------------------------------|---------------------------------|
| Sempre (output)                         | `docx`                          |
| Sempre (brand)                          | `avvale-brand` (prerequisito)   |
| Input è .docx esistente da aggiornare   | `docx` in modalità read/edit    |
| Input include AF o PROJECT_SUMMARY.md   | Leggerli per estrarre i flussi  |

---

## Reference files

- `references/section-templates.md` → testo standard per Parte 2 (basi
  operative Odoo) e blocchi riutilizzabili per le altre sezioni
- skill `avvale-brand` → palette, font, logo, footer (caricare sempre prima)

---

## Anti-pattern da evitare

- **Linguaggio tecnico Odoo** — non scrivere "model `tea.offer`", "campo
  `state`", "scheduled action". Descrivere cosa vede e fa l'utente.
- **Sezioni senza azioni concrete** — ogni sezione deve chiudersi con almeno
  un'istruzione operativa (cosa cliccare, cosa compilare).
- **NOTA usata per tutto** — riservare NOTA solo a blocchi critici.
  I consigli vanno in SUGGERIMENTO o in body text normale.
- **Flusso non sequenziale** — la PARTE 4 deve seguire il processo nell'ordine
  reale in cui lo esegue l'utente, non nell'ordine dei moduli Odoo.
- **Varianti mischiate nella PARTE 4** — se ci sono varianti di processo
  (es. tipologie diverse), documentare il flusso comune in PARTE 4 e le
  differenze per variante nella PARTE 5 (Flusso sintetico). Non intrecciare.
