# Gap Analysis Patterns — Moduli Odoo Enterprise Standard

Pattern ricorrenti di gap per i moduli più comuni nelle implementazioni Avvale.
Usare come punto di partenza, adattare al contesto specifico del cliente.

---

## CRM (Gestione Lead e Opportunità)

| ID     | AS-IS tipico                                       | TO-BE Odoo                                           | Tipo     |
|--------|----------------------------------------------------|------------------------------------------------------|----------|
| CRM-01 | Email personali / casella condivisa non strutturata | Alias email team → creazione automatica Lead         | Config   |
| CRM-02 | Excel per tracciare opportunità                    | Pipeline CRM con stage personalizzabili              | Standard |
| CRM-03 | Nessuna visibilità sul backlog del team            | Dashboard e filtri per commerciale / stage           | Standard |
| CRM-04 | Approvazione offerte via email                     | Workflow approvazione interno con notifica           | Config   |
| CRM-05 | Storico conversazioni non tracciato                | Chatter per-lead con log automatico                  | Standard |
| CRM-06 | Report manuali su Excel                            | Report nativi CRM + filtri per periodo/commerciale   | Standard |

---

## Vendite (Preventivi, Ordini, Contratti)

| ID     | AS-IS tipico                                  | TO-BE Odoo                                              | Tipo            |
|--------|-----------------------------------------------|---------------------------------------------------------|-----------------|
| VEN-01 | Preventivi su Word/Excel con stampa unione    | Template QWeb parametrici per tipologia contratto       | Custom          |
| VEN-02 | Prezzi inseriti manualmente                   | Listino prezzi cliente per prodotto/categoria           | Config          |
| VEN-03 | Prezzi fornitore su Excel separato            | Listino acquisto per fornitore/prodotto                 | Config          |
| VEN-04 | Nessun versionamento offerte                  | Revisioni preventivo con stato Bozza/Inviato/Confermato | Standard        |
| VEN-05 | Firma contratto cartacea o via email          | Sign Odoo (modulo Enterprise) — invio per firma digitale | Standard        |
| VEN-06 | Allegati gestiti su cartelle locali o Drive   | Gestione allegati su record Odoo + link Drive           | Standard+Config |
| VEN-07 | Sconti applicati liberamente senza controllo  | Discount engine con soglie e approvazione               | Config/Custom   |

---

## Contabilità e Fatturazione

| ID     | AS-IS tipico                            | TO-BE Odoo                                  | Tipo          |
|--------|-----------------------------------------|---------------------------------------------|---------------|
| CON-01 | Fatturazione manuale da Excel           | Fatture generate da ordine di vendita       | Standard      |
| CON-02 | Riconciliazione bancaria manuale        | Bank reconciliation automatica con regole   | Config        |
| CON-03 | FE Italia non integrata                 | Modulo `l10n_it_edi` + invio SDI            | Standard (IT) |
| CON-04 | Nessuna analitica                       | Piano dei conti analitico multi-asse        | Config        |
| CON-05 | Report custom su Excel                  | Report contabili nativi + filtri periodo    | Standard      |
| CON-06 | Cespiti gestiti su Excel                | Modulo Assets Odoo Enterprise               | Standard      |

---

## Acquisti

| ID     | AS-IS tipico                          | TO-BE Odoo                              | Tipo     |
|--------|---------------------------------------|-----------------------------------------|----------|
| ACQ-01 | RdA via email o verbale               | RdA con workflow approvazione           | Config   |
| ACQ-02 | Prezzi fornitore non centralizzati    | Listino acquisto per fornitore          | Config   |
| ACQ-03 | Nessun tracking ordini aperti         | Dashboard OdA con stato e scadenze      | Standard |
| ACQ-04 | Approvazione manuale via firma fisica | Workflow approvazione multi-livello     | Config   |

---

## Inventario / Magazzino

| ID     | AS-IS tipico                          | TO-BE Odoo                                       | Tipo     |
|--------|---------------------------------------|--------------------------------------------------|----------|
| INV-01 | Excel per giacenze                    | Inventario Odoo con location multi-livello       | Standard |
| INV-02 | Riordino manuale                      | Reordering rules (min/max) + buy/manufacture     | Config   |
| INV-03 | Tracciabilità lotti su carta          | Lotti/seriali nativi + tracciabilità a valle     | Standard |
| INV-04 | Packaging non gestito                 | Packaging logic con conversione UoM              | Config   |

---

## Sign / Firma elettronica

| ID     | AS-IS tipico                                   | TO-BE Odoo                                        | Tipo          |
|--------|------------------------------------------------|---------------------------------------------------|---------------|
| SGN-01 | Contratto stampato, firmato, scansionato       | Invio contratto via Sign Odoo + firma digitale    | Standard      |
| SGN-02 | Nessuna evidenza legale della firma            | Audit trail Sign + IP/timestamp                   | Standard      |
| SGN-03 | Template contratti su Word                     | Template Sign con campi dinamici (partner, prodotti) | Config       |
| SGN-04 | Notifica firma via email manuale               | Automazione Sign — notifica completamento al PM   | Config        |
| SGN-05 | Integrazione con CRM / Vendite assente         | Trigger Sign da Sale Order / Lead                 | Config/Custom |

---

## Moduli Custom / OCA frequenti in Avvale

| Esigenza                            | Soluzione consigliata                            | Tipo          |
|-------------------------------------|--------------------------------------------------|---------------|
| Firma digitale documenti            | **Sign Odoo Enterprise** (preferito) o DocuSign  | Standard / Custom |
| Gestione allegati strutturata       | OCA `document_page`                              | OCA           |
| Campi custom su oggetti nativi      | Odoo Studio (Enterprise) o sviluppo custom       | Custom        |
| Notifiche WhatsApp                  | Integrazione WhatsApp Cloud API                  | Custom        |
| EDI / integrazione sistemi terzi    | Middleware + API REST/OData                      | Custom        |
| Analytic multi-asse                 | Configurazione nativa Odoo Enterprise            | Config        |
| Integrazione SAP / Tagetik          | Connector custom + API                           | Custom        |
| E-invoicing Croazia FINA            | Modulo custom + endpoint FINA                    | Custom        |

> **Nota**: non includere in questo file pattern specifici per paese
> (localizzazioni, e-invoicing, compliance fiscale locale). Quelli vanno
> documentati nel singolo documento di AF sotto "Configurazioni di Sistema",
> contestualizzati al cliente.

---

## Note metodologiche per la gap analysis

- Classificare sempre il gap **prima** di stimare l'effort
- Un gap `Config` non deve mai diventare `Custom` senza approvazione cliente
- Gap `Out of scope` → documentare sempre con "previsto Fase X" o "non in roadmap"
- Se un gap è riconducibile a un modulo OCA: indicare il nome **esatto** del repo
- Per gap `Custom` con effort Alto: suggerire sempre di aprire un OP per
  stima dettagliata
- Effort `Alto` su singola riga della gap analysis → considerare di scomporlo
  in più gap atomici per migliorare la stima
