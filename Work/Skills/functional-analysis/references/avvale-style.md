# Avvale Style Guide — Colori e Tipografia

## Palette colori

| Uso | Nome | Hex | RGB |
|---|---|---|---|
| Header tabelle | Verde Avvale | `#3B9408` | 59, 148, 8 |
| Sfondo alternato righe | Verde Avvale chiaro | `#D9EAD3` | 217, 234, 211 |
| Accento heading / bordo | Verde Avvale scuro | `#2D7206` | 45, 114, 6 |
| Bordi tabelle | Grigio chiaro | `#CCCCCC` | 204, 204, 204 |
| Testo body | Nero | `#000000` | — |
| Testo secondario / note | Grigio scuro | `#595959` | — |
| Sfondo copertina (opzionale) | Bianco | `#FFFFFF` | — |

## Tipografia

| Elemento | Font | Size (pt) | Stile |
|---|---|---|---|
| Body / default | Arial | 11 | Normal |
| H1 | Arial | 16 | Bold, verde scuro `#2D7206` |
| H2 | Arial | 13 | Bold, verde `#3B9408` |
| H3 | Arial | 11 | Bold, grigio `#595959` |
| Caption tabelle | Arial | 9 | Italic |
| Header tabella | Arial | 10 | Bold, bianco |
| Testo tabella | Arial | 10 | Normal |
| Footer | Arial | 8 | Normal |
| Copertina titolo | Arial | 22 | Bold |
| Copertina sottotitolo | Arial | 14 | Normal |

## Spacing paragrafi

```javascript
// Body
spacing: { before: 120, after: 120, line: 276 }  // ~1.15 interlinea

// Dopo heading H1
spacing: { before: 360, after: 180 }

// Dopo heading H2
spacing: { before: 240, after: 120 }

// Celle tabella
margins: { top: 80, bottom: 80, left: 120, right: 120 }
```

## Heading border (linea decorativa sotto H1)

```javascript
paragraph: {
  border: {
    bottom: { style: BorderStyle.SINGLE, size: 6, color: "3B9408", space: 1 }
  }
}
```

## Stili docx-js da dichiarare

```javascript
paragraphStyles: [
  {
    id: "Heading1", name: "Heading 1",
    run: { size: 32, bold: true, font: "Arial", color: "2D7206" },
    paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 }
  },
  {
    id: "Heading2", name: "Heading 2",
    run: { size: 26, bold: true, font: "Arial", color: "3B9408" },
    paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 }
  },
  {
    id: "Heading3", name: "Heading 3",
    run: { size: 22, bold: true, font: "Arial", color: "595959" },
    paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 }
  },
]
```

## Equivalenti python-docx (in caso di generazione via python-docx)

```python
from docx.shared import Pt, RGBColor, Cm

# Colori Avvale
COLOR_GREEN        = RGBColor(0x3B, 0x94, 0x08)   # header tabelle
COLOR_GREEN_DARK   = RGBColor(0x2D, 0x72, 0x06)   # H1
COLOR_GREEN_LIGHT  = "D9EAD3"                     # shading righe alternate (hex string)
COLOR_GRAY_BORDER  = "CCCCCC"
COLOR_GRAY_TEXT    = RGBColor(0x59, 0x59, 0x59)

# Page setup
PAGE_WIDTH   = Cm(21.0)    # A4
PAGE_HEIGHT  = Cm(29.7)
MARGIN_ALL   = Cm(2.54)

# Font sizes
H1_SIZE = Pt(16)
H2_SIZE = Pt(13)
H3_SIZE = Pt(11)
BODY    = Pt(11)
TABLE   = Pt(10)
FOOTER  = Pt(8)
```
