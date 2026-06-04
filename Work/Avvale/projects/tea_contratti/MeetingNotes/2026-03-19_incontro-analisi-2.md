# Meeting Notes — Incontro di Analisi 2

**Data:** 2026-03-19  
**Cliente:** TEA Ambiente e Ecologia  
**Progetto:** tea_contratti  
**Partecipanti:** Alessandro Caccialanza (Avvale), Matteo Lucchesi (Avvale), Michele Calvani (PM Avvale), Mattia Ferravante (Avvale), Andrea Bassoli (TEA — Resp. Commerciale), Luisa Fiorini (TEA), Noemi Menegazzo (TEA — Commerciale), Claudia Grazioli (TEA — Backoffice)  
**Tipo:** Analisi AS-IS — Utenti, Clienti, Prodotti

---

## Agenda

1. Struttura utenti e permessi
2. Anagrafica clienti e migrazione dati
3. Listino prodotti e logica prezzi
4. Revisione documento ESIS

---

## Discussione

### Utenti e ruoli

| Utente | Ruolo | Note |
|--------|-------|------|
| Noemi Menegazzo | Commerciale | Operativo |
| (terzo commerciale) | Commerciale | In arrivo ad aprile 2026 |
| Claudia Grazioli | Backoffice | Accede per documentazione post-accettazione |
| Andrea Bassoli | Approvatore | Unico che sblocca/firma offerte prima invio cliente |

- Tutti gli utenti: stessi accessi, nessuna segregazione dati, visibilità completa su lead e offerte
- Claudia ha bisogno di **notifiche email** quando un contratto viene firmato dal cliente (per avviare inserimento su VMS)
- Andrea: notifiche approvazione via email (non solo notifiche interne Odoo)

### Anagrafica clienti e migrazione

- Dati su gestionale VMS, ~5000 anagrafiche totali → **migrazione solo ~500 clienti attivi** (anno precedente)
- Export VMS disponibile: ragione sociale, P.IVA, CF, PEC, indirizzo sede legale (dati parziali)
- Dati necessari per offerta: ragione sociale, sede legale, unità produttiva, P.IVA, contatto referente (tel + email)
- Dati fatturazione (SDI, PEC): richiesti post-accettazione tramite moduli allegati all'offerta
- Ogni cliente può avere **più unità produttive** → offerta separata per ogni sede/cantiere (con calcolo trasporto dedicato)
- Per clienti con più unità locali attive: un'unica offerta cumulativa intestata alla sede legale con righe per ogni sede
- **Clienti pubblici**: stesso flusso offerta, poi gestione affidamento su piattaforme esterne; impegno di spesa allegato e lead chiuso
- **Clienti interni gruppo**: stesso flusso, salvo contratti inter-company specifici

### Listino prodotti e logica prezzi

- Chiave univoca listino fornitore: **CER + stato fisico + impianto di destino**
- Scadenza listini: prevalentemente annuale (31/12), alcuni semestrale (30/06)
- Ricarico cliente: 15-20% sul costo fornitore, modificabile manualmente dal commerciale
- Minimo fatturabile lato fornitore e lato cliente **non coincidono** (microraccolte aggregate)
  - Due tipologie: per rifiuto/formulario O cumulativo su tutti i rifiuti
  - Campo libero in Odoo, fleggabile o meno nell'offerta

### Costi di trasporto

| Mezzo | Calcolo | Logica offerta |
|-------|---------|----------------|
| Autocarro ragno | Fasce chilometriche | Tariffa €/viaggio per fascia |
| Furgone | Scaglioni €/m³ | Tabella scaglioni O riga singola se quantità nota |

- Costo trasporto: riga separata (non inclusa nel prezzo CER)
- Calcolo: punto di prelievo → impianto → ritorno trasportatore

### Gestione contratti e revisioni

- **Nuovi servizi** dello stesso cliente → nuova offerta con protocollo separato
- **Revisioni** (sconti, variazioni tonnellaggio) → versioni dello stesso contratto, tracciabili
- Fatturazione: mensile a consuntivo (peso effettivo a destino) — fuori da Odoo

---

## Decisioni prese

- Migrazione: solo 500 clienti attivi, non l'intera anagrafica VMS
- Chiave listino: CER + stato fisico + impianto (combinazione univoca)
- Accettazione firma: sia digitale (Odoo Sign) che cartacea (PDF scaricabile + firma manuale)
- La pipeline deve consentire avanzamento manuale anche senza firma digitale
- Tag Odoo standard per segmentazione clienti per settore (edilizia, officina, ecc.)

---

## Action Items

| # | Azione | Responsabile | Scadenza |
|---|--------|--------------|----------|
| 1 | Revisione documento AF base | Noemi Menegazzo | prossimo incontro |
| 2 | Contattare nuovo commerciale esterno (serve utenza Odoo?) | Noemi Menegazzo | ASAP |
| 3 | Inviare export VMS (clienti attivi) | Noemi Menegazzo | — |
| 4 | Inviare esempio offerta con più unità locali | Noemi Menegazzo | entro giornata |
| 5 | Preparare listino completo: CER + stato fisico + impianto | Noemi Menegazzo | — |
| 6 | Inviare export servizi anno scorso (codici + destinazioni) | Noemi Menegazzo | entro giornata |
| 7 | Inviare template offerta standard con minimo fatturabile cumulativo e dettagli trasporto | Noemi Menegazzo | entro giornata |
| 8 | Aggiornare AS-IS con 3 commerciali + 1 backoffice | Mattia Ferravante | — |

---

## Note aperte / Da chiarire

- Numero protocollo: ancora aperto (Claudia sta verificando internamente)
- Commerciale esterno: da valutare se ha bisogno di accesso Odoo
- Termini di pagamento variabili per clienti fornitori (90gg) e contratti impianti (semestrali)

---

*Next meeting: 2026-03-23*
