# Excel (.xlsx) — Avvale brand application

Riferimento per fogli Excel brandizzati Avvale (report dati, dashboard, modelli economici, listini).

## Setup

- **Font default cella**: Archivo Regular 11. Se Archivo non disponibile su Excel, fallback Inter o Calibri (l'unico contesto in cui Calibri è tollerato — ma indicalo nelle note del file).
- **Colore griglia**: lascia default oppure off su sheet di presentazione.
- **Sfondo**: bianco. Aggiungi una "fascia brand" in alto come header (rows 1-3) con sfondo Celadon Green o Raisin Black.

## Struttura tipica di un report

| Sezione                        | Descrizione                                                |
|--------------------------------|------------------------------------------------------------|
| Foglio "Cover" o intro         | Logo Avvale in alto, titolo report, data, autore           |
| Foglio "Executive summary"     | KPI principali in evidenza, breve commento                 |
| Foglio "Data" / "Detail"       | Tabelle dati, formule, dropdown                            |
| Foglio "Methodology" (opt.)    | Note metodologiche                                         |

## Header tabella

- Riga header: sfondo Celadon Green `#248B7E`, testo bianco, Archivo Bold 11pt, allineamento centrato.
- Filtro: attivo sull'header.
- Freeze panes: prima riga + prima colonna se la tabella supera ~20 righe o ~6 colonne.

## Stile celle

- **Numeri**: separatore migliaia, 0 o 2 decimali in base al contesto. Negativi in rosso (Red Salsa `#EB5758`).
- **Percentuali**: 1 decimale, formato `0.0%`.
- **Date**: `dd/mm/yyyy` (Italia) o `yyyy-mm-dd` (internazionale).
- **Valute**: simbolo `€` o `$`, separatore migliaia.

## Conditional formatting

- Per heatmap, usa scala bicolore: bianco → Celadon Green per valori positivi, bianco → Red Salsa per valori critici.
- Per "data bar", usa Celadon Green o Keppel.
- Evita le scale tricolori predefinite di Excel (rosso/giallo/verde) che hanno colori fuori brand.

## KPI cards (in dashboard)

Layout consigliato per un KPI:
- Cella superiore (merge 3 colonne): label in Archivo Bold 11pt, Raisin Black, sfondo Pistachio `#AACE7C` al 30%.
- Cella inferiore (stessa larghezza): valore numerico in Archivo Extrabold 28pt, Celadon Green, allineamento centrato, sfondo bianco.
- Bordo esterno: 1pt grigio `#E5E5E5`.

## Grafici (chart)

- Stessi principi del pptx: usa solo la palette Avvale.
- Ordine colori serie: Celadon Green → Keppel → Pistachio → Raisin Black → Acqua Blue → English Violet.
- Disabilita la legenda 3D, le ombre, i gradienti.
- Titolo grafico in Archivo Bold 14pt.

## Header / footer di stampa

Se il file verrà stampato:
- Header sx: nome documento; centro: nulla; dx: logo Avvale.
- Footer sx: data; centro: "Pag. &P di &N"; dx: confidenzialità (es. "Confidential — Avvale").
- Margini stampa: 1.5 cm su tutti i lati.

## Implementazione

Usa `openpyxl`. Pattern tipico:

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

wb = Workbook()
ws = wb.active

CELADON = "FF248B7E"
RAISIN  = "FF231C1D"
WHITE   = "FFFFFFFF"

header_fill = PatternFill("solid", fgColor=CELADON)
header_font = Font(name="Archivo", bold=True, size=11, color=WHITE)
body_font   = Font(name="Archivo", size=11, color=RAISIN[2:])
```

Nota: `PatternFill` vuole `fgColor` con prefisso `FF` per l'alpha.

## Don'ts xlsx

- Non lasciare lo sfondo "Office theme blue" sulle tabelle Excel (la "Format as Table" applica un blu di default — sostituiscilo).
- Non usare grafici a torta con più di 5 fette.
- Non lasciare merge cells "decorativi" sparsi (rendono pivot e filtri inutilizzabili).
