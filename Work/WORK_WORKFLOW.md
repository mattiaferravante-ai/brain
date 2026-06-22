# Work Workflow — Avvale S.p.A.

Regole operative per i progetti Odoo gestiti nell'ambito lavorativo.

---

## 1. Struttura documentale per progetto

I progetti Avvale vivono in `Work/Avvale/projects/NomeProgetto/`.  
Altri clienti/progetti vanno in `Work/Clients/NomeProgetto/`.

Usa `/new-project Avvale/projects NomeProgetto` per creare la struttura completa.

Template di riferimento: [[PROJECT_SUMMARY_template]] | [[TEMPLATE_MeetingNotes]]

```
NomeProgetto/
├── README.md               ← stack, contatti, URL ambienti, stato progetto, ultimo meeting
├── PROJECT_SUMMARY.md      ← riepilogo cumulativo: requisiti, decisioni, processi, stakeholders
├── AF/                     ← Analisi Funzionali (usa skill functional-analysis)
├── UAT/                    ← Test Book (usa skill uat-testbook)
├── MeetingNotes/           ← Verbali meeting (YYYY-MM-DD_meeting.md)
└── TechNotes/              ← Workaround, config, SQL, script
```

---

## 2. Pipeline standard: Meeting → AF

Il flusso per costruire un'Analisi Funzionale parte dalle trascrizioni delle riunioni:

```
Trascrizione riunione
      ↓
/minute Avvale/projects/NomeProgetto
      ↓
MeetingNotes/YYYY-MM-DD_meeting.md   ← verbale strutturato
PROJECT_SUMMARY.md                   ← aggiornato in append (requisiti, decisioni, processi...)
README.md                            ← aggiornato con "Ultimo meeting"
      ↓
(ripeti per ogni meeting)
      ↓
/functional-analysis Avvale/projects/NomeProgetto
      ↓
AF/AF_Modulo_v1.docx
```

**Correggere info nel PROJECT_SUMMARY:**
- Correzione puntuale → chiedi a Claude ("nel PROJECT_SUMMARY di X, cambia Y con Z")
- Modifica estesa → edita direttamente in Obsidian (è markdown normale)

---

## 3. Naming convention

| Tipo documento      | Formato nome file                              |
|---------------------|------------------------------------------------|
| Analisi Funzionale  | `AF_ModuloOArgomento_v1.docx`                  |
| UAT Test Book       | `UAT_ModuloOArgomento_v1.xlsx`                 |
| Meeting Notes       | `YYYY-MM-DD_meeting.md`                        |
| Tech Notes          | `argomento_tecnico.md`                         |
| Project Summary     | `PROJECT_SUMMARY.md` (fisso, uno per progetto) |

---

## 4. Tool AI disponibili

| Skill | Trigger | Output |
|-------|---------|--------|
| `/new-project` | Nuovo progetto/cliente | Struttura cartelle + README + PROJECT_SUMMARY |
| `/minute` | Trascrizione riunione | Verbale + aggiornamento PROJECT_SUMMARY + README |
| `/functional-analysis` | Pronto per AF | `.docx` AF stile Avvale |
| `/uat-testbook` | Pronto per UAT | `.xlsx` UAT con fogli Funzionale/Tecnico |
| `/odoo-permission-builder` | Record rules / permessi | XML `ir.rule` e access rights |

---

## 5. Ambienti standard Odoo

Da documentare in ogni `README.md` di progetto:
- URL prod / staging / dev
- Versione Odoo
- Moduli installati custom
- Credenziali (riferimento a password manager, mai nel Brain)
