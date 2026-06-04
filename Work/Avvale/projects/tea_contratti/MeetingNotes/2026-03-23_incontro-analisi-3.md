# Meeting Notes — Incontro di Analisi 3

**Data:** 2026-03-23  
**Cliente:** TEA Ambiente e Ecologia  
**Progetto:** tea_contratti  
**Partecipanti:** Alessandro Caccialanza (Avvale), Matteo Lucchesi (Avvale), Michele Calvani (PM Avvale), Mattia Ferravante (Avvale), Andrea Bassoli (TEA — Resp. Commerciale), Luisa Fiorini (TEA), Noemi Menegazzo (TEA — Commerciale), Claudia Grazioli (TEA — Backoffice)  
**Tipo:** Analisi AS-IS — Modulo CRM, Struttura Contratti, Gestione Prodotti

---

## Agenda

1. Analisi modulo CRM Odoo standard
2. Progettazione oggetto "contratto" custom
3. Pipeline CRM e stati custom
4. Struttura prodotti/listino: HP, stato fisico, operazioni R/D
5. Revisione documenti tecnici

---

## Discussione

### Decisione architetturale CRM — NO quotation standard

Odoo gestisce le opportunità tramite quotation → ordini di vendita. Il flusso TEA non è un ordine di vendita ma un contratto a tariffe unitarie con fatturazione a consuntivo.

**Decisione: creare oggetto custom "contratto"** (→ poi implementato come `tea.offer`) invece di usare le quotation standard. L'oggetto sarà simile al listino prezzi fornitore Odoo, con campi aggiuntivi per impianto e logica markup.

### Pipeline CRM custom

| Stage | Seq | Note |
|-------|-----|------|
| Nuovo | 10 | Lead ricevuta, tipologia obbligatoria |
| Preso in carico | 15 | Raccolta dati |
| Elaborazione proposta | 20 | **Blocco**: per RS, documentazione (foto/sopralluogo/info) deve essere completata |
| Proposta inviata | 30 | **Automatico** al momento dell'invio firma digitale |
| Attesa documenti | 40 | Stato intermedio post-accettazione per backoffice |
| Offerta accettata | 50 | Tutti i documenti completi (Won) |

- **Blocco su Elaborazione proposta**: non si può avanzare finché Andrea non ha firmato (approvazione interna)
- **Stato intermedio "Attesa documenti"**: concordato esplicitamente per gestire offerte accettate ma in attesa di documentazione da backoffice
- Bottone "Won" standard nascosto: la transizione a Won avviene tramite stage "Offerta accettata"

### Struttura lead/offerte

- 1 lead = 1 contratto (se cliente ha 2 contratti slegati → 2 lead separate)
- Più versioni offerta sulla stessa lead (es. richiesta sconto → stessa lead, nuova quotation)
- Assegnatario (sales person) tracciato dall'inizio alla fine anche quando subentrano altri ruoli

### Struttura prodotti e listino fornitore

| Elemento | Dove vive | Note |
|----------|-----------|------|
| Stato fisico (S1-S4) | Proprietà del prodotto (`product.template`) | Discriminante per il prezzo |
| HP (classificazioni pericolo) | Dato sulla riga del listino fornitore | Non sull'anagrafica prodotto |
| Operazione R/D | Dato interno per backoffice | Solitamente non stampato in offerta |
| Codice CER | Nome principale prodotto | Campo `name` = codice interno (es. 020104RETIS2) |

- HP: un rifiuto pericoloso può avere combinazioni HP diverse → HP è dato della riga listino, non del prodotto
- Stato fisico: proprietà intrinseca del prodotto (solido/liquido/fangoso)
- Operazione R/D: necessaria per Claudia per documenti di trasporto VMS; raramente stampata nell'offerta

### Documenti e allegati

| Tipo documento | Dove allegare |
|----------------|---------------|
| Scheda di caratterizzazione/omologa | Al prodotto (univoca per CER × impianto × stato fisico) |
| Condizioni generali | Template email offerta |
| Informativa privacy | Template email offerta |
| Dati fatturazione elettronica (SDI/PEC) | Modulo allegato post-accettazione |

- Schede omologa: caricate da Noemi come allegati al prodotto per ogni combinazione
- Forma di cortesia (Egregio/Spett.): automatica da tipo cliente (privato/azienda), modificabile manualmente

### Trasporto e struttura offerta

- Autocarro ragno: riga singola per ogni codice CER
- Furgone: riga cumulativa (trasporto cumulativo per più CER) oppure riga singola se quantità nota
- Calcolo fascia chilometrica: specifico per singola riga contratto (non standardizzabile a priori)
- Extra sosta: voce fissa generica, addebitata se carico/scarico supera 1h inclusa

---

## Decisioni prese

- NO quotation standard Odoo → oggetto custom `tea.offer` (contratto)
- Pipeline CRM custom con 6 stage + blocchi di transizione
- Blocco su "Qualified" (Elaborazione proposta): richiede firma approvatore prima del passaggio
- Stato intermedio "Attesa documenti" (On Hold) tra Proposition e Won
- HP = dato sulla riga listino fornitore, NON attributo del prodotto
- Stato fisico = proprietà del prodotto (campo Selection)
- Operazione R/D = dato interno backoffice, flag per stampa solo su contratti impianto
- Codice CER = nome prodotto (campo `name`)
- Permessi Claudia (backoffice) = stessi dei commerciali

---

## Action Items

| # | Azione | Responsabile | Scadenza |
|---|--------|--------------|----------|
| 1 | Prototipo modulo contratti per prossimo incontro | Mattia Ferravante | incontro successivo |
| 2 | Aggiungere filtri ricerca lead per zona/provincia (punto aperto) | Alessandro Caccialanza | — |
| 3 | Implementare blocco firma Qualified → Proposition | Alessandro Caccialanza | — |
| 4 | Aggiungere stato intermedio On Hold (Attesa documenti) | Alessandro Caccialanza | — |
| 5 | Configurare permessi Claudia = commerciali | Alessandro Caccialanza | — |
| 6 | Verificare stato risposta protocollo | Noemi Menegazzo | ASAP |
| 7 | Rivedere file base dati: eliminare duplicati CER/operazione | Noemi Menegazzo | — |
| 8 | Ottenere approvazione manager per condivisione contratti complessi | Noemi Menegazzo | — |
| 9 | Caricare allegati contrattuali standard + esempio schede omologa | Noemi Menegazzo | entro incontro successivo |
| 10 | Anticipare dubbi alle colleghe prima del prossimo meeting | Tutti | — |

---

## Note aperte / Da chiarire

- Filtri ricerca lead per zona/provincia (non standard Odoo)
- Numero protocollo: ancora aperto
- Automazione contratti complessi (Discarica 17-20 pp): da valutare approccio con file stampa unione Word/Excel
- Gestione scaglioni trasporto furgone: inserimento manuale o automatico

---

*Next meeting: incontro penultimo (data da confermare)*
