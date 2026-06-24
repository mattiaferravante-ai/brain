# Odoo 19 — Note tecniche e breaking changes

Note estratte da progetti reali su Odoo 19 Enterprise. Aggiornare man mano che emergono nuovi casi.

**Fonte primaria:** tea_contratti (modulo `tea_quotations`, schema `19.0.1.4.0`)

---

## Breaking changes rispetto a 17/18

### SQL Constraints
**Prima (≤18):**
```python
_sql_constraints = [('unique_col', 'UNIQUE(col)', 'Messaggio errore')]
```
**Odoo 19:**
```python
from odoo import models
models.Constraint("UNIQUE(col)", "Messaggio errore")
```
Usare `models.Constraint` nella lista `_constraints` — la sintassi `_sql_constraints` è deprecata.
> ⚠️ Se il campo contiene NULL, usare constraint Python invece di SQL UNIQUE (i NULL sono trattati come distinti in PostgreSQL → constraint SQL non funziona come atteso).

---

### Filtro prodotti nelle search view
**Prima:**
```xml
<filter name="consumable" .../>
```
**Odoo 19:**
```xml
<filter name="goods" .../>
```
Il dominio `consumable` non esiste più come nome filtro standard.

---

### `uom_po_id` rimosso
Il campo `uom_po_id` su `product.template` / `product.product` non esiste in Odoo 19. Se il tuo modulo lo referenzia (es. in XML data, domain, o codice Python), rimuovilo o sostituiscilo con `uom_id`.

---

### Gruppo sicurezza CRM
**Prima:**
```
crm.group_crm_manager  ← non esiste in Odoo 19
```
**Odoo 19 — usare:**
```
sales_team.group_sale_manager
```
Usare questo gruppo per ACL e record rules sui modelli CRM/sales.

---

### Dipendenza `l10n_it_edi` per codice fiscale
Il campo `l10n_it_codice_fiscale` su `res.partner` richiede il modulo `l10n_it_edi` come dipendenza esplicita nel `__manifest__.py`. Senza di esso il campo non esiste a runtime.

---

### `supplier_rank` richiede modulo `account`
`res.partner.supplier_rank` è definito nel modulo `account`. Se il tuo modulo lo usa in domain o codice senza dipendere da `account`, aggiungi `account` alle dipendenze.

---

## Pattern specifici Odoo 19

### Sequenze con schema custom per outlet/filiale
Per numerazione tipo `DI/DIEV + YY + outlet + seriale` con reset per FY (aprile in India):
```python
# ir.sequence con prefix dinamico + padding
seq = self.env['ir.sequence'].search([('code', '=', 'mio.modulo.sequence')])
# Il reset FY (aprile) richiede logica custom su ir.sequence.date_range
```
Valutare `ir.sequence.date_range` per gestire finestre cross-FY (registrazione entro fine FY precedente).

---

### Odoo Sign — hook post-firma
Per triggerare automazioni quando un documento viene firmato:
```python
# Override su sign.request
def _sign(self):
    res = super()._sign()
    # logica custom post-firma
    return res
```
Questo è il punto di ingresso per automazioni tipo "accettazione offerta → cambio stato CRM".

---

### Font PDF compatibile con Calibri Light
**Carlito** (Apache 2.0) è metricamente compatibile con Calibri Light — usalo come sostituto nei report QWeb/PDF. Non richiede licenza Microsoft.

---

## Architettura moduli

### Modello standalone vs ereditarietà
Preferire un modello standalone (es. `tea.offer`) linkato via `M2O` a `crm.lead` piuttosto che ereditare `crm.lead` direttamente, quando:
- Il modello ha una state machine propria
- Deve avere viste/menu separati
- Potrebbero esserci multiple istanze per la stessa lead

Ereditare il modello base (delegation/prototype inheritance) solo quando si aggiungono campi/comportamenti al modello esistente senza creare un'entità separata.

---

### Disabilitare creazione diretta da un modello
```xml
<!-- Nel manifest o security: disabilita il pulsante "Nuovo" nel tree view -->
<record model="ir.actions.act_window" ...>
    <field name="context">{'no_create': True}</field>
</record>
```
Oppure via `@api.model create()` con raise `UserError` se manca il campo obbligatorio (es. `lead_id`).

---

## Integrazioni

### E-invoicing Italia (`l10n_it_edi`)
- Dipendenza obbligatoria per: `l10n_it_codice_fiscale`, `l10n_it_pec`, `l10n_it_sdi_code`
- Il formato SDI richiede che il partner abbia PEC o codice destinatario compilato
- Utile per detect persona fisica vs società: `len(cf) == 16` → persona fisica

### E-invoicing Croazia (FINA)
- Formato XML specifico FINA (non UBL standard)
- Moduli custom per la generazione — nessun modulo standard Odoo
- Vedi progetti con scope Croazia per riferimenti

---

*Aggiornato: 2026-06-24 | Fonte: tea_contratti, piaggio_cdms_india*
