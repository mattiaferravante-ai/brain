Genera il Manuale Utente strutturato per un modulo Odoo Enterprise.

Segui le istruzioni in `Work/Skills/user-manual/SKILL.md`.

**Prerequisito brand (obbligatorio):** carica prima la skill `avvale-brand`
leggendo `Work/Skills/avvale-brand/avvale-brand/tokens.json` e
`Work/Skills/avvale-brand/avvale-brand/references/docx_brand.md`.

Argomenti (nell'ordine):
1. **progetto** — percorso relativo dentro Work/ (es. `Clients/TEA_contratti`)
2. **modulo** *(opzionale)* — nome del modulo/area (es. `Gestione Offerte e Contratti`)

Esempi:
- `/user-manual Clients/TEA_contratti` → Claude chiede le info mancanti
- `/user-manual Clients/TEA_contratti "Gestione Offerte e Contratti"`

Output atteso:
1. File `.docx` salvato in `Work/<progetto>/` (o sottocartella `ManualeUtente/`)
2. README del progetto aggiornato con riferimento al manuale generato
