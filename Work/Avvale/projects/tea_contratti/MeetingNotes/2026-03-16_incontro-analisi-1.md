# Meeting Notes — Incontro di Analisi 1

**Data:** 2026-03-16  
**Cliente:** TEA Ambiente e Ecologia  
**Progetto:** tea_contratti  
**Partecipanti:** Alessandro Caccialanza (Avvale), Matteo Lucchesi (Avvale), Michele Calvani (PM Avvale), Mattia Ferravante (Avvale), Andrea Bassoli (TEA — Resp. Commerciale), Luisa Fiorini (TEA), Noemi Menegazzo (TEA — Commerciale), Claudia Grazioli (TEA — Backoffice)  
**Tipo:** Analisi AS-IS

---

## Agenda

1. Processo AS-IS gestione offerte
2. Requisiti funzionali CRM Odoo
3. Flusso approvazione e firma
4. Gestione comunicazioni e alias email

---

## Discussione

### Processo AS-IS — Tracciamento offerte via Excel

Il file Excel è lo strumento attuale per tracciare tutte le commesse: commerciale incaricato, cliente, data arrivo, canale (email/portale/telefono), tipo rifiuti, impianto di destino, operazione R/D, stato avanzamento.

- Ogni riga = un codice rifiuto → più righe per la stessa offerta
- Numero protocollo progressivo assegnato dal backoffice (punto aperto: chi lo genera)
- Volumi: ~400-500 offerte/anno servizi standard, ~100 contratti impianti (TMB/Discarica)
- 90% attività = richieste in entrata da clienti esistenti, 10% procacciamento attivo

### Tipologie di output contrattuale

| Tipo | Caratteristiche |
|------|----------------|
| Offerta RS (Rifiuti Speciali) | Flusso standard, tariffe unitarie €/kg o €/viaggio |
| Offerta TMB | Contratto impianto, validità annuale |
| Contratto Discarica | 17-20 pagine, clausole complesse, allegati |

Nessuna di queste è un ordine di vendita Odoo standard: sono offerte a tariffe unitarie. La fatturazione avviene mensilmente a consuntivo sul peso effettivo (fuori da Odoo, gestita da ufficio FA).

### Requisiti principali emersi

- Listino prezzi: combinazione CER + impianto di destino → costo acquisto fornitore automatico
- Ricarico cliente: percentuale (15-20%) applicata sul costo fornitore, modificabile manualmente
- Minimo fatturabile impianto e verso cliente (non sempre coincidenti)
- Firma digitale cliente tramite Odoo Sign (requisito esplicito)
- Allegati standard: informativa privacy, condizioni generali, schede di caratterizzazione
- Follow-up automatico per offerte senza risposta

### Flusso di approvazione

```
Commerciale crea offerta → Backoffice assegna protocollo → Responsabile commerciale (Andrea) firma → Invio al cliente
```

- La firma di Andrea è una firma legale che arriva al cliente (non solo approvazione interna)
- Post-accettazione: backoffice inserisce contratto su VMS e coordina logistica (fuori Odoo)

### Gestione comunicazioni

- Alias email: `commercialeambiente@aspa.it` (molto trafficata, ~50 email/giorno)
- Decisione: inoltro selettivo a Odoo, non automatico — troppi messaggi non pertinenti
- Proposta: dare l'alias Odoo ai clienti abituali per le nuove richieste

### Struttura anagrafica clienti

- Sede legale ≠ sede di ritiro (fondamentale per documenti di trasporto e calcolo chilometrico)
- Costo trasporto calcolato dal punto di prelievo all'impianto + ritorno

---

## Decisioni prese

- Odoo gestisce il processo fino alla firma del contratto; post-accettazione fuori da Odoo
- Nessuna integrazione con VMS nella prima fase
- Inoltro email a Odoo selettivo e manuale
- Firma digitale cliente via Odoo Sign è un requisito

---

## Action Items

| # | Azione | Responsabile | Scadenza |
|---|--------|--------------|----------|
| 1 | Analizzare modulo lead/CRM Odoo | Alessandro Caccialanza | prossimo incontro |
| 2 | Fornire lista tipologie di trasporto | Noemi Menegazzo | — |
| 3 | Condividere template offerta tipo | Noemi Menegazzo | — |
| 4 | Condividere quotazione fasce chilometriche | Noemi Menegazzo | — |
| 5 | Analizzare contratto Discarica complesso (17-20 pp) | Alessandro Caccialanza | — |
| 6 | Verificare generazione automatica numero protocollo (punti controversi interni) | Claudia Grazioli | — |
| 7 | Valutare portale clienti con ufficio privacy | Luisa Fiorini | — |
| 8 | Verificare integrazione mappe/distanze kilometriche in Odoo | Mattia Ferravante / Alessandro | — |
| 9 | Inviare riepilogo punti discussi | Michele Calvani | 2026-03-17 mattina |

---

## Note aperte / Da chiarire

- Generazione numero protocollo: automatica da Odoo o manuale dal gestionale VMS?
- Portale clienti: fattibile ma richiede valutazione privacy
- Calcolo distanze Google Maps: verificare se solo nel modulo logistica

---

*Next meeting: 2026-03-19*
