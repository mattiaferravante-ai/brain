---
name: avvale-brand
description: "Brand identity e design system di Avvale (gruppo Techedge) — la fonte unica di verità per logo, palette colori, tipografia Archivo, asset grafici, regole di composizione e tone of voice. Carica e applica questa skill ogni volta che stai creando, modificando o impaginando un qualsiasi materiale per Avvale (presentazione pptx, documento Word docx, report Excel xlsx, pdf, immagine, one-pager, post social, banner, infografica) e ogni volta che stai usando un'altra skill di produzione (pptx, docx, xlsx, pdf, image generation) in un contesto in cui l'output rappresenta Avvale o un cliente di Avvale. Trigger anche con menzioni indirette come 'Avvale', 'Techedge', 'il mio cliente / la mia azienda' quando l'utente lavora in Avvale, 'applica il nostro brand', 'rendilo brandizzato', 'metti il logo Avvale', 'usa i nostri colori', 'crea un'immagine per Avvale'. Questa skill non genera direttamente i deliverable — fornisce design tokens, asset e linee guida da iniettare a monte di altre skill di produzione."
---

# Avvale — Brand Identity & Design System

Questa skill è la **fonte unica di verità** per la brand identity di Avvale (gruppo Techedge). Il suo scopo è dare a Claude, e alle altre skill di produzione documenti, un punto di partenza coerente: design tokens, asset e regole.

> Non costruisce deliverable: alimenta altre skill (pptx, docx, xlsx, pdf, ecc.) con i criteri di brand corretti.

## Quando questa skill è attiva

Caricala — e applica i suoi contenuti — ogni volta che si verifica almeno una di queste condizioni:

- L'utente sta producendo materiale che rappresenta Avvale o un suo cliente.
- L'utente menziona "Avvale", "Techedge", "il nostro brand", "il mio team", "la mia azienda" e lavora in Avvale.
- Stai per richiamare un'altra skill di produzione (pptx, docx, xlsx, pdf, web design, copywriting, ecc.) e l'output finale sarà un materiale Avvale.

In questi casi: **leggi prima i token e le guidelines di questa skill**, poi passa quei valori (colori, font, asset, regole) come input vincolanti alla skill di produzione.

## Cosa contiene la skill

```
avvale-brand/
├── SKILL.md                       # questo file: indice + regole top-level
├── tokens.json                    # design tokens machine-readable
├── assets/
│   ├── logo/                      # 6 PNG: positivo/negativo × orizzontale/portrait/payoff
│   ├── graphic-elements/          # pictogram, simboli, pattern background
│   └── colors.json                # palette in JSON con HEX/RGB/CMYK
└── references/
    ├── brand_guidelines.md        # documento esteso (logo, type, colori, tono)
    ├── pptx_brand.md              # specifiche operative per .pptx
    ├── docx_brand.md              # specifiche operative per .docx
    ├── xlsx_brand.md              # specifiche operative per .xlsx
    ├── pdf_brand.md               # specifiche operative per .pdf
    ├── image_brand.md             # specifiche operative per immagini (social, banner, AI gen)
    └── qa_checklist.md            # checklist finale prima di consegnare
```

## Flusso d'uso (quando un'altra skill produrrà il deliverable)

1. **Carica i token** — leggi `tokens.json` (machine-readable) per avere subito a portata: palette, font, dimensioni minime logo, paths degli asset.
2. **Carica le guidelines** — leggi `references/brand_guidelines.md` per capire il "perché" e gli usi corretti.
3. **Carica la reference di formato** giusta in base al deliverable target:
   - `.pptx` → `references/pptx_brand.md`
   - `.docx` → `references/docx_brand.md`
   - `.xlsx` → `references/xlsx_brand.md`
   - `.pdf`  → `references/pdf_brand.md`
   - immagini (social, banner, infografiche, AI image gen) → `references/image_brand.md`
4. **Passa i tokens alla skill di produzione** — quando invochi (o agisci come) una skill `pptx` / `docx` / `xlsx` / `pdf`, esplicita che deve usare:
   - palette: vedi `tokens.colors`,
   - font: `Archivo` (con fallback dichiarato),
   - logo: dai i path da `tokens.logo.paths.*`,
   - regole layout: vedi le specifiche in `references/<formato>_brand.md`.
5. **A fine lavoro**, controlla il deliverable contro `references/qa_checklist.md`.

## Regole non negoziabili (top-level)

Queste sono le regole che, se ignorate, fanno sembrare il materiale "non Avvale". Devono essere applicate sempre, indipendentemente dalla skill di produzione:

- **Logo**: usa solo i file in `assets/logo/`. Mai ricrearlo, mai distorcerlo, mai ricolorarlo, mai aggiungere effetti (outline/glow/ombra). Il logotype "avvale" da solo (senza marchio) non è ammesso.
- **Tipografia**: solo **Archivo** (https://fonts.google.com/specimen/Archivo). Pesi consentiti: Thin, Regular, Bold, Extrabold (anche Italic). Fallback in ordine: Inter → Helvetica → Arial. Mai font "creativi" diversi.
- **Colore signature**: **Celadon Green `#248B7E`**. È il colore-firma di Avvale: deve comparire come accento (titoli, KPI, prima serie nei grafici). Non sostituirlo con altri verdi della palette.
- **Sfondi**: bianco `#FFFFFF`, Raisin Black `#231C1D`, o un colore della palette primaria. Mai colori arbitrari fuori palette (es. blu Office default).
- **Contrasto**: testo Raisin Black su bianco, oppure bianco su Raisin Black/Celadon Green. Mai verde su verde.
- **Tone of voice**: consulenziale, asciutto, concreto. Niente buzzword vacue ("revolutionary", "best-in-class", "rivoluzionario"). Niente emoji nei materiali formali.

## Riassunto operativo (quick reference)

| Cosa                | Valore                                                      |
|---------------------|-------------------------------------------------------------|
| Font                | Archivo (Thin / Regular / Bold / Extrabold, ± italic)        |
| Fallback font       | Inter → Helvetica → Arial                                    |
| Colore signature    | Celadon Green `#248B7E`                                      |
| Neri/scuri          | Raisin Black `#231C1D`                                       |
| Verdi accento       | Keppel `#47B1A3`, Green RYB `#5AB031`, Pistachio `#AACE7C`   |
| Logo default        | `assets/logo/logo_pos.png` (orizzontale positivo)            |
| Logo su scuro       | `assets/logo/logo_neg.png`                                   |
| Pictogram (cross)   | `assets/graphic-elements/pictogram_black.png` / `_white.png` |
| Min size logo       | 55 px digitale (orizzontale), 42 px (stacked)                |
| Clearspace logo     | altezza del marchio (`X`); stacked = `0.75 × X`              |
| Pattern rotazione   | `-28°` (per il marchio usato come pattern)                   |

## Tone of voice — pillole

Avvale è una società di consulenza e system integration tech, parte del gruppo Techedge. Parla a CFO, CIO, COO, direttori innovation di grandi aziende.

- **Voce**: consulenziale, esperta, concreta, asciutta.
- **In italiano**: registro professionale ("voi/lei" col cliente, "noi" per Avvale). Frasi brevi, verbi attivi.
- **In inglese**: business English neutro, no slang, no marketing-speak.
- **Vocabolario**: usa termini tecnici precisi quando servono ("data platform", "ERP migration", "MLOps") senza nasconderli dietro buzzword vuote.
- **Misurabilità**: parla di outcome misurabili, non di feature. "Riduciamo il time-to-insight da 3 settimane a 48 ore" è meglio di "soluzione innovativa di analytics".
- **5 parole chiave**: concreto, competente, diretto, affidabile, misurabile.

## Per approfondire

- Token machine-readable → `tokens.json`
- Linee guida estese (con motivazioni e esempi) → `references/brand_guidelines.md`
- Specifiche operative per formato → `references/{pptx,docx,xlsx,pdf}_brand.md`
- QA finale → `references/qa_checklist.md`
