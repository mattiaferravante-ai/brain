# PDF — Avvale brand application

Riferimento per la creazione di PDF brandizzati Avvale.

## Approccio

I PDF Avvale possono nascere in due modi:

1. **Conversione da pptx/docx**: il modo migliore e più frequente. Costruisci il deliverable in pptx o docx applicando le rispettive reference brand, poi esporta in PDF. Questa via mantiene automaticamente font, colori, logo.
2. **Generazione diretta**: per documenti puramente PDF (es. one-pager grafici, brochure tecniche stampabili). Usa `reportlab` o `pdfkit` (HTML→PDF) applicando manualmente i criteri sotto.

## Setup

- **Formato**: A4 portrait di default. Landscape solo se i contenuti lo richiedono (es. infografiche orizzontali).
- **Margini**: 20 mm su tutti i lati.
- **Font incorporati**: Archivo. Quando usi reportlab, registra il font da `.ttf` se disponibile, altrimenti fallback Helvetica con avviso.

## Tipografia (riassunto)

| Elemento     | Peso        | Size  | Colore         |
|--------------|-------------|-------|----------------|
| Title cover  | Extrabold   | 28-32 | Raisin / White |
| H1           | Bold        | 18-20 | Celadon Green  |
| H2           | Bold        | 14    | Raisin Black   |
| Body         | Regular     | 10-11 | Raisin Black   |
| Caption      | Italic      | 8-9   | Raisin 60%     |
| Footer       | Regular     | 8     | Raisin 60%     |

Interlinea body: 1.4.

## Cover e header

- Cover: logo Avvale negativo grande in alto, titolo, sottotitolo, data, cliente. Sfondo Raisin Black o bianco.
- Header (dalla pag. 2 in poi): logo positivo orizzontale piccolo a sinistra, linea sottile sotto.
- Footer: numero pagina a destra, nome documento a sinistra, in Archivo Regular 8pt grigio.

## Esempio reportlab (canvas)

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Registra Archivo se .ttf disponibile, altrimenti fallback
try:
    pdfmetrics.registerFont(TTFont('Archivo', '/path/to/Archivo-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('Archivo-Bold', '/path/to/Archivo-Bold.ttf'))
    BODY_FONT = 'Archivo'
    BOLD_FONT = 'Archivo-Bold'
except Exception:
    BODY_FONT = 'Helvetica'
    BOLD_FONT = 'Helvetica-Bold'

CELADON = HexColor('#248B7E')
RAISIN  = HexColor('#231C1D')

c = canvas.Canvas('out.pdf', pagesize=A4)
# ... disegna logo, titoli, body
c.save()
```

## Conversione pptx → pdf

Su macOS con LibreOffice installato:
```bash
soffice --headless --convert-to pdf out.pptx --outdir output_dir/
```

Oppure usa `python-pptx` per costruire e poi convertire con `comtypes` su Windows o Keynote/PowerPoint AppleScript su Mac.

## Conversione docx → pdf

```bash
soffice --headless --convert-to pdf out.docx --outdir output_dir/
```

Verifica il PDF risultante: a volte il rendering della tabella o dei grafici cambia leggermente. Se il documento è critico (proposal cliente), apri il PDF e controlla almeno la cover e una pagina con tabelle.

## Don'ts

- Non lasciare font Helvetica/Times nel PDF se hai dichiarato Archivo nel docx/pptx — significa che il font non è stato incorporato. Usa `--export-pdf-with-fonts` (LibreOffice) o disabilita la sostituzione font in Word.
- Non usare PDF "scannerizzati" o ricostruiti da immagini per documenti commerciali ufficiali — perdi la searchability e la qualità.
- Non superare 10 MB per PDF inviati via email cliente. Comprimi le immagini se il file è troppo grande.

## Checklist conversione

Prima di consegnare un PDF:
- [ ] Apri il PDF e verifica che il logo si veda nitido.
- [ ] Controlla che il font sia Archivo (oppure il fallback dichiarato) e non sia stato sostituito dall'engine.
- [ ] Verifica che i colori della palette (specialmente Celadon Green) siano resi correttamente.
- [ ] Verifica la numerazione pagina e il footer.
- [ ] Apri su un secondo strumento (es. anteprima Mac e Acrobat Reader) per assicurarti che si visualizzi uniformemente.
