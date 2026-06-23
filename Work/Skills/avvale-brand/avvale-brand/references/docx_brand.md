# Word (.docx) — Avvale brand application

Riferimento per documenti testuali brandizzati Avvale (proposal lunghi, report, executive summary, business case in formato Word).

## Setup pagina

- **Formato**: A4 (210 × 297 mm).
- **Margini**: 2.5 cm top/bottom, 2.5 cm sx/dx.
- **Orientamento**: portrait. Solo per allegati con tabelle larghe puoi usare landscape.

## Tipografia

- **Font**: Archivo. Fallback: Inter, Helvetica, Arial.
- Imposta il font su tutti gli stili (Normal, Heading 1-3, Title) — non lasciare Calibri o Times di default.

| Stile        | Peso         | Size  | Colore             | Note                              |
|--------------|--------------|-------|--------------------|-----------------------------------|
| Title        | Extrabold    | 32 pt | Raisin Black       | Solo cover                        |
| Subtitle     | Regular      | 16 pt | Celadon Green      | Cover                             |
| Heading 1    | Bold         | 20 pt | Celadon Green      | Sezioni principali                |
| Heading 2    | Bold         | 16 pt | Raisin Black       | Sotto-sezioni                     |
| Heading 3    | Bold         | 13 pt | Raisin Black       |                                   |
| Body         | Regular      | 11 pt | Raisin Black       | Interlinea 1.4                    |
| Caption      | Italic       | 9 pt  | Raisin 60%         | Sotto figure/tabelle              |
| Footer       | Regular      | 9 pt  | Raisin 60%         | Numero pagina + nome documento    |

## Header e footer

- **Header**: logo Avvale orizzontale positivo (`logo_pos.png`) in alto a sinistra, altezza ~12 mm. Linea sottile sotto (1 pt, grigio `#E5E5E5`).
- **Footer**: a sinistra il nome del documento + data; a destra il numero di pagina ("Pag. 1 di N"). Tutto Archivo Regular 9pt, Raisin 60% opacità.
- Cover: header e footer **disattivati** sulla cover.

## Cover page

Layout consigliato:
1. Logo Avvale negativo grande, in alto.
2. Sotto, blocco titolo:
   - Eyebrow (es. "PROPOSAL", "BUSINESS CASE") — Archivo Bold caps 11pt, Celadon Green.
   - Titolo del documento — Archivo Extrabold 32pt, Raisin Black.
   - Sottotitolo opzionale — Archivo Regular 16pt, Celadon Green.
3. In basso: nome cliente, data, autore. Archivo Regular 11pt.
4. Sfondo: bianco o Raisin Black con logo negativo.

## Tabelle

- Header row: sfondo Celadon Green `#248B7E`, testo bianco, Archivo Bold 11pt.
- Righe alternate: bianco e `#F5F5F5`.
- Bordi: solo orizzontali, 0.5pt grigio `#CCCCCC`.
- Padding cella: 4 pt verticale, 8 pt orizzontale.

## Liste

- Bullet: usa il carattere `•` (U+2022), colore Celadon Green se vuoi un accento.
- Liste numerate: numero in Archivo Bold, contenuto Regular.
- Indentazione: 0.5 cm per livello.

## Citazioni / callout

- Quote: rientro 1 cm a sinistra, barra verticale 3pt Celadon Green a sinistra, testo Archivo Italic Regular 11pt.
- Box informativo: sfondo Pistachio al 15% (`#AACE7C` con opacità) o `#F5F5F5`, padding 12pt, titolo Bold 11pt Celadon Green.

## Immagini

- Centra le immagini orizzontalmente.
- Caption sotto, Archivo Italic 9pt, "Fig. N — descrizione".

## Don'ts docx

- Non lasciare il font Calibri di default da nessuna parte — Word lo riapplica subdolamente quando incolli testo. Re-imposta `Normal` style.
- Non usare i colori "Office Theme" — sostituisci sempre con HEX della palette Avvale.
- Non usare WordArt, ombreggiature pesanti, bordi page-border decorativi.
- Non usare giustificato pieno per body lunghi (crea river di spazi). Allineamento a sinistra.

## Implementazione

Usa `python-docx` per generare. Struttura tipica:

```python
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Imposta font default
style = doc.styles['Normal']
style.font.name = 'Archivo'
style.font.size = Pt(11)
style.font.color.rgb = RGBColor(0x23, 0x1C, 0x1D)

# Heading 1
h1 = doc.styles['Heading 1']
h1.font.name = 'Archivo'
h1.font.bold = True
h1.font.size = Pt(20)
h1.font.color.rgb = RGBColor(0x24, 0x8B, 0x7E)
```

Ricordati di applicare il font esplicitamente anche tramite `rPr/rFonts` XML quando python-docx non lo propaga (succede a volte sui titoli e nelle tabelle).
