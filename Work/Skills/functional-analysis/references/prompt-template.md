# Prompt Template — Richiesta AF Avvale

## Template per richiesta NUOVA Analisi Funzionale

```
Cliente: [nome cliente]
Odoo: Enterprise [versione]   ← obbligatorio, nessun default
Modulo / area: [es. CRM – Gestione Lead e Preventivi]
Tipo richiesta: NUOVO
Revisione target: [es. 01.0]
Data documento: [GG/MM/AAAA]
Destinatario: [Cliente / Interno / Entrambi]
Lingua: [Italiano (default) / Inglese]

Input allegato: [appunti workshop / trascrizione / brief verbale / nessuno]
Natura input: [descrivere brevemente]

Sezioni da generare:
- [ ] Copertina
- [ ] Registro Versioni
- [ ] Indice
- [ ] AS-IS
- [ ] TO-BE
- [ ] Gap Analysis
- [ ] Configurazioni di Sistema
- [ ] Open Points

Note specifiche: [eventuali vincoli, decisioni note, dipendenze, OP da considerare]
```

---

## Template per richiesta AGGIORNAMENTO AF esistente

```
Cliente: [nome cliente]
Odoo: Enterprise [versione]
Modulo / area: [es. CRM – Gestione Lead e Preventivi]
Tipo richiesta: AGGIORNAMENTO
Revisione corrente: [es. 01.1]  →  nuova revisione: [es. 01.2]
Data documento: [GG/MM/AAAA]

AF allegata: [allegare il .docx esistente]
Input modifiche: [allegare appunti / trascrizione con le novità]

Sezioni da aggiornare:
- [es. TO-BE § Gestione Lead]
- [es. Gap Analysis — chiudere GAP-003]
- [es. Open Points — chiudere OP-002]

Sezioni invariate: mantieni esattamente come sono.
Note specifiche: [es. "chiuso OP-003, aggiunto flusso approvazione"]
```

---

## Comportamento atteso dalla skill

1. **Validare i campi obbligatori**: Cliente, Versione Odoo Enterprise, Modulo.
   Se ne manca uno e non è inferibile dall'allegato → chiedere **solo quello**.
2. **Per richieste NUOVE**: generare tutte le sezioni richieste seguendo lo
   standard. Non saltare sezioni — usare "N/A – non in scope per questa fase"
   quando applicabile.
3. **Per richieste AGGIORNAMENTO**:
   - Leggere prima il .docx esistente (skill `docx`) per estrarre struttura
     e contenuti.
   - Applicare **solo il delta** indicato nel campo "Sezioni da aggiornare".
   - Mantenere identiche le sezioni non menzionate.
   - Incrementare il numero di revisione nel Registro Versioni con riga nuova.
4. **Dichiarare assunzioni** in testa al documento quando si è proceduto
   senza informazioni complete.
