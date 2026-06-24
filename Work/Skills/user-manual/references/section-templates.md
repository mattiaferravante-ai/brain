# Section Templates — Manuale Utente

Blocchi di testo standard riutilizzabili. Adattare i placeholder `[...]`
al contesto del cliente. La PARTE 2 è quasi identica per tutti i manuali —
usare il testo qui sotto come base e personalizzare solo gli esempi.

---

## Registro Versioni

| Rev  | Descrizione                                         | Data       |
|------|-----------------------------------------------------|------------|
| 1.0  | Prima emissione – Manuale Utente [Modulo]           | [Mese AAAA]|

---

## PARTE 2 – ODOO: BASI OPERATIVE (testo standard)

### 2.1 Accesso e navigazione

Accedere all'URL del sistema con email aziendale e password. Le app
disponibili appaiono nella schermata home. Per tornare alla home in
qualsiasi momento: cliccare il logo Odoo in alto a sinistra. Ogni app
mantiene la cronologia di navigazione (breadcrumb) visibile in alto.

### 2.2 Il Chatter — Comunicazione sul record

Il chatter è il pannello di comunicazione che appare nella parte inferiore
di ogni record (lead, offerta, contatto, ordine). Consente di tracciare tutta
la comunicazione interna ed esterna direttamente sul record.

| Azione           | Destinatari                                             | Quando usarla                                                      |
|------------------|---------------------------------------------------------|--------------------------------------------------------------------|
| Invia messaggio  | Email inviata al cliente + tracciata sul record         | Per comunicare ufficialmente con il cliente                        |
| Registra nota    | Solo utenti Odoo interni — NON inviata al cliente       | Per appunti interni, aggiornamenti di stato, note per i colleghi   |
| Allega file      | Documenti, PDF, immagini caricati sul record            | Per caricare materiale correlato alla trattativa                   |

NOTA: 'Invia messaggio' esce via email al cliente. 'Registra nota' è
esclusivamente interna e non viene mai recapitata al cliente.

### 2.3 Attività e promemoria

Le attività pianificano azioni future su un record. Tipi disponibili:
Chiamata, Email, Riunione, Scadenza.

Per creare un'attività: aprire il record → cliccare l'icona orologio (o il
pulsante 'Attività') → scegliere tipo, data scadenza e responsabile → Salva.

Le attività appaiono nel Calendario e nella vista Kanban del CRM con badge
colorato:
- **Verde**: attività futura
- **Arancio**: attività in scadenza oggi
- **Rosso**: attività scaduta — richiede attenzione immediata

### 2.4 Ricerca e filtri

Ogni lista dispone di una barra di ricerca in alto. Utilizzare:
- **Filtri**: per restringere i risultati per condizione (es. 'Le mie lead',
  'Proposte inviate')
- **Raggruppa per**: per organizzare i risultati per cliente, fase,
  responsabile
- **Preferiti**: per salvare combinazioni di filtri usate frequentemente

---

## Template: tabella fasi pipeline (PARTE 3)

| #  | Fase                  | Come si avanza                     | Note                                                     |
|----|-----------------------|------------------------------------|----------------------------------------------------------|
| 1  | [Nome fase 1]         | Manuale                            | [condizione necessaria]                                  |
| 2  | [Nome fase 2]         | Manuale                            | [cosa raccogliere / verificare]                          |
| 3  | [Nome fase 3]         | Manuale + Auto                     | Il sistema [azione automatica] quando l'utente [azione]  |
| 4  | [Nome fase 4]         | AUTOMATICO                         | Impostato da Odoo quando [evento trigger]                |
| 5  | [Nome fase 5]         | AUTOMATICO                         | Impostato da Odoo quando [evento trigger]                |
| 6  | [Nome fase finale]    | Manuale                            | Solo se [condizione di completezza]                      |

---

## Template: sottosezione PARTE 4 (processo passo per passo)

```
### 4.N  [Titolo azione o fase]

[1-2 frasi di contesto: quando si arriva qui e perché]

[Passi operativi in ordine:]
- [Passo 1]: [istruzione]
- [Passo 2]: [istruzione]
- ...

[Tabella esiti se applicabile:]
| Scenario / Azione     | Cosa succede                                         |
|-----------------------|------------------------------------------------------|
| [Caso 1]              | [Effetto 1]                                          |
| [Caso 2]              | [Effetto 2]                                          |

NOTA:  [avvertenza critica, se presente]

SUGGERIMENTO:  [consiglio pratico, se presente]
```

---

## Template: flusso sintetico per variante (PARTE 5)

```
### 5.N  [Nome variante]

| Step | Fase              | Tipo           | Azione                                                  |
|------|-------------------|----------------|---------------------------------------------------------|
| 1    | [Fase 1]          | Manuale        | [Azione chiave — max 15 parole]                         |
| 2    | [Fase 2]          | Manuale        | [Azione chiave]                                         |
| 3    | [Fase 3]          | Manuale + Auto | [Azione utente] → sistema [effetto automatico]          |
| 4    | [Fase 4]          | AUTOMATICO     | [Evento trigger] → lead / record avanza automaticamente |
| 5    | [Fase 5]          | AUTOMATICO     | [Evento trigger] → [effetto]                            |
| 6    | [Fase finale]     | Manuale        | Completare [condizione] → avanzare manualmente          |
```

---

## Template: appendice Key User (A.N)

```
### A.N  [Nome configurazione]

**Percorso:** [App] → [Menu] → [Sottomenu]

| Menu / Sezione        | Contenuto                              | Operazioni consentite     |
|-----------------------|----------------------------------------|---------------------------|
| [Voce menu 1]         | [Cosa contiene]                        | [Chi può fare cosa]       |
| [Voce menu 2]         | [Cosa contiene]                        | [Chi può fare cosa]       |

[Istruzioni per le operazioni più comuni: Crea, Modifica, Elimina]

NOTA:  [Eventuali vincoli: impatto su altri record, chi consultare prima
di modificare, operazioni irreversibili]
```

---

## Nota metodologica (da inserire in testa al documento se ci sono assunzioni)

> **Nota**: Le seguenti assunzioni sono state applicate in assenza di
> indicazioni esplicite: [elenco assunzioni]. Eventuali variazioni rispetto
> alla configurazione reale del sistema potranno richiedere aggiornamenti
> al presente documento.
