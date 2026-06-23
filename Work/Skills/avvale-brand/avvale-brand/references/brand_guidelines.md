# Avvale — Brand Guidelines (operative)

Estratto operativo del brand book ufficiale Avvale (gruppo Techedge), pensato per essere consumato da un LLM che deve generare documenti.

## Logo

### Versioni
- **Horizontal logo** (default, da usare nella maggior parte dei casi).
- **Stacked logo** — solo quando lo spazio orizzontale non è sufficiente.
- **Strapline version** — con "TECHEDGE GROUP" sotto, per esplicitare l'appartenenza al gruppo (es. comunicazioni corporate, primo contatto con un cliente).
- **Positive (su sfondo chiaro)** e **negative (su sfondo scuro/colorato)** — scegli sempre la variante che massimizza il contrasto.

I file sono in `assets/logo/`. Non ricrearli, non ridisegnarli.

### Clearspace
- Logo orizzontale: spazio libero tutto attorno = altezza del marchio (`X`).
- Logo stacked: spazio libero = `0.75 × X`.

In pratica: prima di posizionare il logo, "padding" almeno pari all'altezza del marchio.

### Dimensioni minime
| Versione   | Print min | Digital min |
|------------|-----------|-------------|
| Horizontal | 20 mm     | 55 px       |
| Stacked    | 15 mm     | 42 px       |

### Marchio (mark) come elemento grafico
- Il **marchio** (la croce) può essere usato da solo come elemento grafico decorativo o come pattern.
- Quando usato come pattern, mantenere rotazione di **-28°**.
- Quando usato come elemento singolo (es. esce dal margine della slide), il centro del marchio e i quattro bracci della croce devono restare visibili.
- Il **logotype** "avvale" da solo (senza marchio) **non è ammesso**.

### Don'ts (tassativi)
- Non distorcere, scalare in modo non proporzionale, ruotare il logo (orizzontale/stacked).
- Non cambiare i colori del logo.
- Non aggiungere outline, glow, ombre, gradienti o effetti.
- Non posizionare il logo su sfondi che non garantiscono contrasto.
- Non ricreare il logotype con altri font: usa sempre i file approvati.

## Tipografia

- **Font ufficiale**: **Archivo** (Google Fonts: https://fonts.google.com/specimen/Archivo).
- **Pesi consentiti**: Thin, Regular, Bold, Extrabold (anche Italic). Non usare pesi diversi.
- **Fallback** se Archivo non installato: Inter → Helvetica → Arial. In docx/pptx, dichiara la sostituzione nei commenti del documento se necessaria.
- **Gerarchia tipica**:
  - Title (cover): Archivo Extrabold, 48–60 pt
  - Section header: Archivo Bold, 28–36 pt
  - Slide title: Archivo Bold, 24–28 pt
  - Body: Archivo Regular, 14–18 pt
  - Caption / footer: Archivo Regular, 9–11 pt
- Non usare *all caps* in modo aggressivo. Va bene per label brevi (es. "CASE STUDY", "AGENDA").

## Colori

### Palette primaria
| Nome             | HEX       | RGB             | CMYK              | Quando usarlo                                  |
|------------------|-----------|-----------------|-------------------|------------------------------------------------|
| Pure White       | `#FFFFFF` | 255,255,255     | 0,0,0,0           | sfondo principale, testo su scuro              |
| Raisin Black     | `#231C1D` | 36,29,30        | 70,69,59,80       | testo body, sfondi scuri "premium"             |
| Celadon Green    | `#248B7E` | 36,139,126      | 80,23,54,7        | **colore signature**: titoli, accenti, KPI     |
| Keppel           | `#47B1A3` | 71,177,163      | 69,5,43,0         | accento secondario, hover, illustrazioni       |
| Green RYB        | `#5AB031` | 90,176,49       | 68,0,100,0        | accento "growth", grafici positivi             |
| Pistachio        | `#AACE7C` | 170,206,124     | 41,0,64,0         | sfondi tenui, callout, illustrazioni           |

### Palette secondaria (uso parsimonioso)
| Nome             | HEX       | RGB             |
|------------------|-----------|-----------------|
| Acqua Blue       | `#989FCE` | 152,159,206     |
| Almond           | `#FFECD1` | 255,236,209     |
| Lilac Luster     | `#B79FAD` | 183,159,173     |
| English Violet   | `#574B60` | 87,75,98        |
| Red Salsa        | `#EB5758` | 235,87,88       |
| Bittersweet      | `#412647` | 65,38,71        |
| Champagne Pink   | `#EADDD6` | 234,221,214     |

I colori secondari **non sono obbligatori**. Vanno usati con parsimonia in report, illustrazioni, marketing — e sempre coerenti con la palette primaria. Per documenti commerciali/corporate ufficiali, **resta sulla palette primaria**.

### Regole d'uso colore
- Il **colore signature** è Celadon Green `#248B7E`. È il colore "Avvale" — usalo per definire l'identità del documento (titoli, linee di accento, primo elemento di un grafico).
- Per documenti business: massimo **3 colori** dalla palette primaria + bianco e Raisin Black come neutri.
- **Mai** introdurre colori fuori palette (es. blu Microsoft Office di default). Se devi visualizzare 6+ categorie in un grafico, scegli 6 colori dalla palette primaria e secondaria mantenendo Celadon Green come primo.
- **Contrasto**: testo Raisin Black su Pure White, oppure Pure White su Raisin Black/Celadon Green. Evita testo verde su verde.

## Tone of voice

- **Voce**: consulenziale, esperta, asciutta. Parliamo a CFO, CIO, COO, direttori IT/innovation di grandi aziende.
- **Tono**: professionale ma non distaccato. Sicuro senza essere arrogante. Concreto, non visionario.
- **Vocabolario**: usa termini tech precisi quando servono (es. "data platform", "ERP migration", "MLOps") senza nasconderli dietro buzzword. Evita marketing-speak ("revolutionary", "world-class", "best-in-class").
- **Forma**: frasi brevi, verbi attivi. Liste puntate per i benefit, non paragrafi monolitici.
- **Italiano**: registro professionale formale ("voi" plurale per il cliente, "noi" per Avvale). Evita anglicismi quando esiste un equivalente italiano standard.
- **Inglese**: business English neutro, evita locuzioni regionali.

### Esempi
**Buono (IT)**: "Costruiamo la vostra data platform in 12 settimane, con governance e modello di costo trasparenti dal primo giorno."

**Cattivo (IT)**: "Trasformiamo il vostro business con soluzioni innovative best-in-class che rivoluzioneranno il modo in cui pensate ai dati."

**Buono (EN)**: "We help banks migrate core systems to the cloud while keeping compliance and downtime under control."

**Cattivo (EN)**: "We empower financial institutions to embrace cutting-edge cloud transformation journeys."

## Layout e composizione

- **Ariosità**: lascia spazio bianco. Una slide pulita Avvale ha più aria di una slide McKinsey.
- **Allineamento**: a sinistra per body e titoli; centrale solo per cover e divider.
- **Griglia**: pensa in colonne (12-col su pptx widescreen). Non riempire i bordi: lascia margini interni di almeno 0.5" / 1.3 cm.
- **Foto**: usa foto autentiche, neutre, professionali. No stock cliché (mani che si stringono, lampadine, frecce).
- **Pictogram**: il marchio Avvale può essere usato in grande dimensione, fuori margine, in tonalità chiara su sfondo scuro o viceversa, come "watermark" su slide di sezione.

## Brand voice in 5 parole-chiave
- **Concreto** (concrete)
- **Competente** (expert)
- **Diretto** (direct)
- **Affidabile** (trustworthy)
- **Misurabile** (measurable)
