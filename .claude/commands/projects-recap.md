Genera un recap di tutti i progetti attivi con stato e scadenze.

## Comportamento

1. Scansiona `Work/Avvale/projects/` cercando sottocartelle che abbiano un `README.md`
2. Per ogni progetto con stato `#active`, leggi:
   - `README.md` → Cliente, Odoo, Inizio, Durata stimata, PM Avvale, Referente cliente
   - Sezione `## Scadenze` del `README.md` → lista scadenze (milestone, go-live, UAT, ecc.)
   - `PROJECT_SUMMARY.md` → sezione `## Punti aperti` per blocchi attivi
3. Genera un output strutturato in tre blocchi:

---

### Blocco 1 — Tabella progetti attivi

| Progetto | Cliente | Inizio | Durata | PM | Stato |
|----------|---------|--------|--------|----|-------|
| ...      | ...     | ...    | ...    | ...| ...   |

### Blocco 2 — Scadenze per progetto

Per ogni progetto attivo mostra le scadenze dalla sezione `## Scadenze` del README.
Se la sezione è vuota o assente: scrivi `— nessuna scadenza registrata`.

### Blocco 3 — Punti aperti critici

Per ogni progetto attivo mostra i punti aperti non risolti da `PROJECT_SUMMARY.md`.
Se sono più di 5, mostra solo i primi 5 e indica quanti altri ce ne sono.
Se la sezione è vuota: ometti il progetto dal blocco.

---

## Note

- Considera attivo solo chi ha `#active` nel README
- Ordina i progetti per data di inizio (prima i più recenti)
- Se non ci sono progetti attivi: di' "Nessun progetto attivo trovato in Work/Avvale/projects/"
- Non modificare nessun file, è un comando di sola lettura
