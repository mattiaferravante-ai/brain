# Skill: new-project

Crea la struttura cartelle per un nuovo progetto all'interno del Brain (Work).

## Trigger

Ogni volta che si vuole creare un nuovo progetto, una nuova sezione, un nuovo cliente, un nuovo engagement Avvale.

## Parametri

- **area:** percorso relativo dentro `Work/` dove creare il progetto (es. `Avvale/projects`, `Clients`)
- **nome:** nome del progetto/cliente (es. `AziendaXYZ`, `MigrazioneCRM`)
- **tipo:** `full` (default) | `minimal`

## Comportamento

1. Costruisci il percorso: `Work/<area>/<nome>/`
2. Crea le sottocartelle in base al tipo:
   - **full:** `AF/`, `UAT/`, `MeetingNotes/`, `TechNotes/`
   - **minimal:** solo `README.md`, nessuna sottocartella
3. Crea `README.md` nella cartella del progetto (vedi template sotto)
3b. Per tipo `full`, crea anche `PROJECT_SUMMARY.md` copiando e adattando il template da `Work/Templates/PROJECT_SUMMARY_template.md` (sostituisci `<NomeProgetto>` con il nome reale)
4. Aggiorna il `README.md` della cartella padre (`Work/<area>/`) aggiungendo una riga nella sezione Progetti
5. Se non esiste la sezione "Progetti" nel README padre, creala
6. Aggiorna `Work/README.md` solo se si tratta di una nuova area di primo livello (non già presente)

## Template README progetto (full)

```markdown
# <NomeProgetto>

<!-- descrizione breve del progetto -->

## Stack

- Odoo: <!-- versione -->
- Moduli: <!-- es. Contabilità, Magazzino, ... -->

## Contatti

- PM: 
- Referente cliente: 

## Sottocartelle

- `AF/` — Analisi Funzionali
- `UAT/` — Test Book e risultati
- `MeetingNotes/` — Verbali meeting
- `TechNotes/` — Note tecniche, workaround, configurazioni

## Stato

`#active` | `#completed` | `#on-hold`

## Tag

`#avvale` `#odoo` `#work`
```

## Template README progetto (minimal)

```markdown
# <NomeProgetto>

<!-- descrizione breve -->

## Tag

`#work` `#odoo`
```

## Note

- Usa sempre nomi in CamelCase o kebab-case per le cartelle (es. `AziendaXYZ`, `migrazione-crm`)
- Dopo la creazione, mostra il tree della struttura creata
- Ricorda di fare commit con messaggio: `brain: add project <nome>`
