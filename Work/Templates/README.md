# 📁 Templates

Template riutilizzabili per tutti i progetti Odoo/Avvale.

| File | Uso |
|------|-----|
| `TEMPLATE_ProjectREADME.md` | README di ogni progetto cliente (copia in `Clients/NomeProgetto/`) |
| `TEMPLATE_MeetingNotes.md` | Verbale meeting (copia in `Clients/NomeProgetto/MeetingNotes/`) |
| `TEMPLATE_TechNote.md` | Nota tecnica / workaround (copia in `Clients/NomeProgetto/TechNotes/`) |
| `PROJECT_SUMMARY_template.md` | Riepilogo cumulativo di progetto — aggiornato da `/minute`, input per `/functional-analysis` |

## Documenti generati da AI

Per AF e UAT **non usare template statici** — generarli direttamente con le skill:

- **Analisi Funzionale** → chiedi a Claude con `functional-analysis` skill
- **UAT Test Book** → chiedi a Claude con `uat-testbook` skill
- **Record Rules XML** → chiedi a Claude con `odoo-permission-builder` skill
