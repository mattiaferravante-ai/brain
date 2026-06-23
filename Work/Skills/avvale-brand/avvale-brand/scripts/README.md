# avvale-brand / scripts

Questa skill è un **design system**: non produce direttamente deliverable. La cartella `scripts/` contiene solo helper a supporto di altre skill di produzione documenti.

## `load_tokens.py`

Helper per caricare `tokens.json` da un'altra skill. Espone:

- `load_tokens(skill_root)` → restituisce il dict completo dei token.
- `rgb_tuple(color_token)` → converte un token (dict o HEX string) in `(r, g, b)`.
- `asset_path(skill_root, relative)` → risolve il path assoluto di un asset.
- `chart_palette(tokens)` → lista RGB ordinata per le serie dei grafici.
- `font_stack(tokens)` → lista `[primary, ...fallbacks]`.

### Esempio: integrare i token in una skill pptx

```python
from pathlib import Path
import sys
AVVALE = Path("<absolute-path>/avvale-brand")
sys.path.insert(0, str(AVVALE / "scripts"))
from load_tokens import load_tokens, rgb_tuple, asset_path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

tokens = load_tokens(AVVALE)
CELADON = RGBColor(*rgb_tuple(tokens["color"]["primary"]["celadon_green"]))
RAISIN  = RGBColor(*rgb_tuple(tokens["color"]["primary"]["raisin_black"]))
FONT    = tokens["typography"]["primary_family"]
LOGO    = asset_path(AVVALE, tokens["logo"]["paths"]["horizontal_positive"])

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
# ...applica CELADON, RAISIN, FONT, LOGO alle slide...
```

## Smoke test

```bash
python load_tokens.py /path/to/avvale-brand
```

Stampa:

```
Brand: Avvale
Font stack: Archivo, Inter, Helvetica, Arial
Signature color: #248B7E
Chart palette: ['#248B7E', '#231C1D', '#47B1A3', '#AACE7C', '#989FCE', '#574B60', '#5AB031']
```
