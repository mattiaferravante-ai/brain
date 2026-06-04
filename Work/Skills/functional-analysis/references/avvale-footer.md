# Avvale Footer Standard

## Testo footer societario (riga unica)

```
© Avvale  |  Avvale S.p.A.  –  Via Melzi D'Eril 34, 20154 Milano (MI) - Italia
T +39 02 87311  –  REA di Milano 1726950  –  C.F. e P.I. IT04113150967
Capitale Sociale Euro 2.674.073,00 i.v.  –  www.avvale.com
```

## Note d'uso

- Il footer societario va nel **footer di pagina**, allineato a sinistra
- Il numero di pagina va **centrato** o a destra nello stesso footer
- Font: **Arial 8pt**, colore `#595959`
- Non ripetere il footer sulla pagina di copertina (usare `titlePage: true`)

## Implementazione docx-js (TypeScript / JS)

```javascript
const footer = new Footer({
  children: [
    new Paragraph({
      children: [
        new TextRun({
          text: "© Avvale  |  Avvale S.p.A.  – Via Melzi D'Eril 34, 20154 Milano (MI)",
          font: "Arial", size: 16, color: "595959"
        }),
      ],
      alignment: AlignmentType.LEFT,
    }),
    new Paragraph({
      children: [
        new TextRun({
          text: "Do not duplicate without written permission",
          font: "Arial", size: 16, color: "595959", italics: true
        }),
        new TextRun({ children: ["\t\tPagina "], font: "Arial", size: 16 }),
        new TextRun({ children: [new PageNumber()], font: "Arial", size: 16 }),
      ],
      tabStops: [{ type: TabStopType.RIGHT, position: 9026 }],
    }),
  ],
});
```

## Header standard

```javascript
const header = new Header({
  children: [
    new Paragraph({
      children: [
        new TextRun({
          text: "[TITOLO DOCUMENTO]  –  Rev. 01.0",
          font: "Arial", size: 18, color: "2D7206"
        }),
      ],
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "3B9408" } },
      alignment: AlignmentType.RIGHT,
    }),
  ],
});
```

## Implementazione python-docx (in alternativa)

```python
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_footer(section):
    footer = section.footer
    p1 = footer.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p1.add_run(
        "© Avvale  |  Avvale S.p.A. – Via Melzi D'Eril 34, "
        "20154 Milano (MI)  –  www.avvale.com"
    )
    run.font.name = "Arial"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    # Riga 2: numero pagina centrato
    p2 = footer.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    p2._p.append(fld)
```
