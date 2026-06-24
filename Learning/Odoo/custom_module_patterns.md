# Pattern architetturali — Moduli Custom Odoo

Pattern ricorrenti per strutturare moduli Odoo custom. Indipendenti dalla versione salvo dove indicato.

---

## State machine su modello custom

Pattern per gestire un flusso multi-stato (es. offerta, richiesta approvazione):

```python
class MioModello(models.Model):
    _name = 'mio.modello'

    state = fields.Selection([
        ('draft', 'Bozza'),
        ('approval', 'In approvazione'),
        ('approved', 'Approvato'),
        ('sent', 'Inviato'),
        ('accepted', 'Accettato'),
        ('refused', 'Rifiutato'),
    ], default='draft')

    def action_send_to_approval(self):
        self.write({'state': 'approval'})

    def action_approve(self):
        self.write({'state': 'approved'})
```

**Regola:** ogni transizione di stato = un metodo `action_*` dedicato, mai aggiornare lo stato direttamente dall'esterno.

---

## Pipeline CRM con blocchi di transizione

Per customizzare la pipeline CRM con stage bloccate condizionalmente:

```python
# Override di crm.lead
def write(self, vals):
    if 'stage_id' in vals:
        # Verifica condizioni prima di permettere la transizione
        new_stage = self.env['crm.stage'].browse(vals['stage_id'])
        if not self._can_advance_to(new_stage):
            raise UserError(_("Condizioni non soddisfatte per avanzare a %s") % new_stage.name)
    return super().write(vals)
```

---

## Unicità con constraint Python (non SQL UNIQUE)

Usare quando la chiave di unicità include campi Many2many o quando i NULL devono essere trattati come uguali:

```python
@api.constrains('field_a', 'field_b')
def _check_unique(self):
    for rec in self:
        domain = [
            ('field_a', '=', rec.field_a.id),
            ('field_b', '=', rec.field_b.id),
            ('id', '!=', rec.id),
        ]
        if self.search_count(domain):
            raise ValidationError(_("Combinazione già esistente."))
```

**Quando usarlo:** chiavi composite con M2M, quando NULL deve essere trattato come uguale ad altri NULL (SQL UNIQUE considera NULL ≠ NULL).

---

## Notifiche email automatiche

```python
# Nel metodo che triggera la notifica
template = self.env.ref('mio_modulo.email_template_id')
template.send_mail(self.id, force_send=True)
```

Template XML:
```xml
<record id="email_template_id" model="mail.template">
    <field name="name">Nome Template</field>
    <field name="model_id" ref="model_mio_modello"/>
    <field name="subject">Oggetto: ${object.name}</field>
    <field name="email_to">${object.partner_id.email}</field>
    <field name="body_html" type="html">...</field>
</record>
```

---

## Cron giornaliero

```xml
<record id="cron_reminder" model="ir.cron">
    <field name="name">Reminder giornaliero</field>
    <field name="model_id" ref="model_mio_modello"/>
    <field name="state">code</field>
    <field name="code">model.action_send_reminders()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
    <field name="active">True</field>
</record>
```

---

## Struttura `__manifest__.py` tipica

```python
{
    'name': 'Nome Modulo',
    'version': '19.0.1.0.0',  # OCA semver: odoo_version.major.minor.patch.hotfix
    'category': 'Sales/CRM',
    'depends': [
        'account',        # se usi supplier_rank o contabilità
        'crm',
        'l10n_it_edi',    # se usi l10n_it_codice_fiscale
        'product',
        'sale_crm',
        'sign',           # se usi Odoo Sign
        'uom',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/mio_modello_views.xml',
        'data/email_templates.xml',
        'data/ir_cron.xml',
    ],
}
```

---

## Record rules — pattern ricorrenti

```xml
<!-- Accesso solo ai propri record (salesperson) -->
<record id="rule_own_records" model="ir.rule">
    <field name="name">Accesso ai propri record</field>
    <field name="model_id" ref="model_mio_modello"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
</record>

<!-- Manager: accesso a tutto -->
<record id="rule_manager_all" model="ir.rule">
    <field name="name">Manager — accesso completo</field>
    <field name="model_id" ref="model_mio_modello"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
</record>
```

**Nota Odoo 19:** usare `sales_team.group_sale_manager`, non `crm.group_crm_manager` (non esiste).

---

## Report QWeb PDF

Struttura base per un report stampabile:

```xml
<report
    id="report_mio_documento"
    model="mio.modello"
    string="Stampa Documento"
    report_type="qweb-pdf"
    name="mio_modulo.report_mio_documento_template"
    file="mio_modulo.report_mio_documento_template"
    print_report_name="'Documento - %s' % (object.name)"
/>

<template id="report_mio_documento_template">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <div class="page">
                    <!-- contenuto -->
                </div>
            </t>
        </t>
    </t>
</template>
```

**Font PDF:** usare **Carlito** (Apache 2.0) come sostituto di Calibri Light — metricamente identico, nessuna licenza Microsoft richiesta.

---

*Aggiornato: 2026-06-24*
