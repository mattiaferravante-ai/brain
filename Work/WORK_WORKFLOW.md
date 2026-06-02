# Work Workflow — Avvale S.p.A.

Regole operative per i progetti Odoo gestiti nell'ambito lavorativo.

---

## 1. Struttura documentale per progetto

Ogni progetto cliente ha una cartella in `Work/Clients/NomeCliente_NomeProgetto/` con:

```
NomeCliente_NomeProgetto/
├── README.md               ← stack, contatti, URL ambienti, note generali
├── AF/                     ← Analisi Funzionali (usa skill functional-analysis)
├── UAT/                    ← Test Book (usa skill uat-testbook)
├── MeetingNotes/           ← Verbali meeting (YYYY-MM-DD_topic.md)
└── TechNotes/              ← Workaround, config, SQL, script
```

---

## 2. Naming convention

| Tipo documento      | Formato nome file                              |
|---------------------|------------------------------------------------|
| Analisi Funzionale  | `AF_ModuloOArgomento_v1.docx`                  |
| UAT Test Book       | `UAT_ModuloOArgomento_v1.xlsx`                 |
| Meeting Notes       | `YYYY-MM-DD_topic.md`                          |
| Tech Notes          | `argomento_tecnico.md`                         |

---

## 3. Tool AI disponibili

- **functional-analysis** skill → genera `.docx` AF stile Avvale
- **uat-testbook** skill → genera `.xlsx` UAT con fogli Funzionale/Tecnico
- **odoo-permission-builder** skill → genera `ir.rule` e access rights XML

---

## 4. Ambienti standard Odoo

Da documentare in ogni `README.md` di progetto:
- URL prod / staging / dev
- Versione Odoo
- Moduli installati custom
- Credenziali (riferimento a password manager, mai nel Brain)
