# PowerPoint (.pptx) — Avvale brand application

Riferimento operativo per costruire deck Avvale (pitch, proposal, business case). Da leggere quando devi generare un .pptx.

## Setup di base

- **Formato slide**: 16:9 widescreen (13.333" × 7.5"). Mai 4:3.
- **Margini**: 0.5" su tutti i lati (sicurezza); contenuto dentro 0.7".
- **Font**: Archivo, fallback Inter/Helvetica/Arial. In python-pptx usa il nome esatto `Archivo` per il `font.name`.
- **Sfondo**: bianco (`#FFFFFF`) per slide standard. Raisin Black (`#231C1D`) per cover/section divider/closing slide.

## Slide master — struttura tipica

Un deck Avvale "minimo viable" ha:

1. **Cover** — titolo del progetto, nome cliente, data, logo Avvale (negativo, in alto a sx) su sfondo Raisin Black `#231C1D` o Celadon Green `#248B7E`. Marchio (cross) come elemento decorativo grande in basso a destra, opacità 100%.
2. **Agenda** — bullet o numerata, font Bold per le voci, accenti in Celadon Green.
3. **Section divider** — sfondo scuro (Raisin Black o Celadon Green), titolo sezione grande, numero sezione, marchio come watermark.
4. **Content slide** — sfondo bianco, titolo in alto (Archivo Bold 24pt, Raisin Black o Celadon Green), body sotto (Archivo Regular 16pt). Logo orizzontale piccolo nel footer.
5. **Closing / contatti** — sfondo Celadon Green o Raisin Black, "Thank you" o claim, contatti, logo Avvale negativo.

## Palette colori in pptx

Usa questi RGB (per python-pptx `RGBColor`):

```
PURE_WHITE      = (255, 255, 255)
RAISIN_BLACK    = (35, 28, 29)
CELADON_GREEN   = (36, 139, 126)   # signature
KEPPEL          = (71, 177, 163)
GREEN_RYB       = (90, 176, 49)
PISTACHIO       = (170, 206, 124)
# secondary
ACQUA_BLUE      = (152, 159, 206)
RED_SALSA       = (235, 87, 88)
ENGLISH_VIOLET  = (87, 75, 98)
```

## Tipografia

| Elemento               | Pesi          | Size (pt) | Colore                     |
|------------------------|---------------|-----------|----------------------------|
| Cover title            | Extrabold     | 48–54     | White (su scuro)           |
| Cover subtitle         | Regular       | 20–24     | White                      |
| Section divider title  | Extrabold     | 40–48     | White                      |
| Slide title            | Bold          | 24–28     | Celadon Green o Raisin     |
| Subtitle / eyebrow     | Bold (caps)   | 11–13     | Celadon Green              |
| Body                   | Regular       | 14–18     | Raisin Black               |
| Bullet                 | Regular       | 14–16     | Raisin Black               |
| KPI number             | Extrabold     | 44–60     | Celadon Green              |
| KPI label              | Regular       | 11–13     | Raisin Black               |
| Footer / page number   | Regular       | 9         | Raisin Black 60% opacity   |

## Logo nelle slide

- **Cover**: logo negativo (`logo_neg.png`) in alto a sinistra. Altezza ~0.6" (mantieni proporzioni). Clearspace minimo intorno = altezza del marchio.
- **Content slide**: logo positivo (`logo_pos.png`) nel footer in basso a sinistra. Altezza ~0.35".
- **Section divider su sfondo scuro**: logo negativo in alto a sinistra.
- **Closing slide**: logo negativo grande, centrale, con clearspace ampio.

Mai distorcere: in python-pptx imposta solo `height` e lascia che `width` venga calcolato proporzionalmente — oppure pre-calcola width = height × (orig_w / orig_h).

## Grafici

- Usa la palette Avvale anche nei grafici. **Mai** la palette di default Office.
- Ordine consigliato dei colori per serie:
  1. Celadon Green `#248B7E`
  2. Raisin Black `#231C1D`
  3. Keppel `#47B1A3`
  4. Pistachio `#AACE7C`
  5. Acqua Blue `#989FCE`
  6. English Violet `#574B60`
- Linee griglia: grigio chiaro `#E5E5E5`, sottili.
- Etichette assi: Archivo Regular 10pt, Raisin Black.
- Titolo grafico: Archivo Bold 14pt, allineato a sinistra.
- Evita 3D, ombre, gradienti pesanti.

## Tabelle

- Header row: sfondo Celadon Green `#248B7E`, testo bianco, Archivo Bold 12pt.
- Righe alternate: bianco e Pistachio molto trasparente (`#AACE7C` al 15% opacità) o bianco e `#F5F5F5`.
- Bordi: solo orizzontali, grigio chiaro `#E5E5E5`. Niente bordi verticali pesanti.
- Padding cella: almeno 6pt sopra/sotto, 10pt sx/dx.

## Elementi grafici

- **Pictogram (cross)** — usabile in grande come watermark su section divider. Posizionalo in basso/destra, parzialmente fuori slide. Tonalità chiara su scuro: usa `pictogram_white.png` con opacità 20-40%.
- **Pattern background** — `bg_pattern_black.png` o `bg_pattern_white.png` per slide di copertina di sezione.
- **Symbol arrow / quote** — per testimonianze o callout.

## Don'ts specifici pptx

- Non usare le shape "SmartArt" di PowerPoint con stile default — sembrano fuori brand.
- Non usare bullet animati di sistema (☑, ➜, etc.). Se servono bullet, usa il punto Avvale: bullet Celadon Green o un piccolo quadrato.
- Non centrare orizzontalmente i bullet o il body — sempre allineato a sinistra.
- Non riempire la slide con testo: max ~40 parole per slide content. Se serve più testo, è un docx, non una slide.

## Implementazione: usa lo script

Per generare un deck rapidamente, usa `scripts/build_pptx.py` (vedi `scripts/README.md`). Lo script:
- crea il file pptx con master e palette pre-impostati,
- accetta un dict di slide (cover, agenda, sections, content, closing),
- inserisce automaticamente logo, footer, slide number,
- restituisce il path del file generato.

Quando il caso d'uso non rientra nei pattern dello script (es. proposta molto custom, deck con grafici complessi), puoi costruire manualmente con `python-pptx` rispettando questa reference.
