# Immagini — Avvale brand application

Riferimento per la creazione di immagini brandizzate Avvale (social post, cover LinkedIn, banner, infografiche, illustrazioni, immagini AI-generate).

## Quando si applica

- Post LinkedIn, Twitter/X, Instagram, Facebook con grafica.
- Cover e thumbnail (LinkedIn, Facebook, Twitter, YouTube).
- Banner per landing page, header email.
- Infografiche standalone (PNG/JPG/SVG).
- Immagini generate da modelli AI (DALL-E, Midjourney, Imagen) destinate a comunicazione Avvale.

## Formati e dimensioni standard

| Uso                          | Dimensioni (px)        | Aspect ratio | Note                          |
|------------------------------|------------------------|--------------|-------------------------------|
| LinkedIn post (single image) | 1200 × 627             | ~1.91:1      | minimo 1080 × 566             |
| LinkedIn cover personale     | 1584 × 396             | 4:1          |                               |
| LinkedIn cover company       | 1128 × 191             | 5.9:1        |                               |
| Twitter/X post               | 1600 × 900             | 16:9         |                               |
| Twitter/X header             | 1500 × 500             | 3:1          |                               |
| Facebook post                | 1200 × 630             | 1.91:1       |                               |
| Facebook cover               | 820 × 312              | 2.63:1       |                               |
| Instagram square             | 1080 × 1080            | 1:1          |                               |
| Instagram portrait           | 1080 × 1350            | 4:5          | meglio del quadrato in feed   |
| Instagram story / Reels      | 1080 × 1920            | 9:16         | margini 250 px su top/bottom  |
| YouTube thumbnail            | 1280 × 720             | 16:9         |                               |
| Banner header generico       | 1920 × 600             | 3.2:1        |                               |

Esporta in **PNG** (qualità) o **JPG** (peso, foto). SVG solo per illustrazioni vettoriali.

## Composizione brand

### Sfondi consigliati
- **Bianco `#FFFFFF`** — pulizia, default per documenti factual.
- **Raisin Black `#231C1D`** — premium, autorevolezza.
- **Celadon Green `#248B7E`** — momenti signature, lanci, annunci.
- **Pattern** — `bg_pattern_white.png` / `bg_pattern_black.png` / `bg_pattern_pink.png` come sfondo "texture".
- **Gradient** — solo monocolore (es. Celadon Green → Keppel). Mai gradienti multicolore arcobaleno.

### Logo nelle immagini
- Sempre presente sulle immagini "ufficiali" Avvale.
- Posizionamento standard: angolo in alto a sinistra (cover) o in basso a destra (post). Mai centrato a meno di compositions tipo "card formal".
- Dimensione: sempre ≥ 55 px (orizzontale) o 42 px (stacked). Nei banner larghi, almeno il 5% della larghezza totale.
- Versione coerente con lo sfondo (negativo su scuro, positivo su chiaro).
- Padding: clearspace ≥ altezza del marchio, anche al bordo dell'immagine.

### Pictogram come elemento visivo
- Il marchio (cross) può essere usato in **grande** come elemento decorativo: esce dal margine, opacità 20–60%, posizionato come "watermark".
- Rotazione consentita solo a `-28°` se usato come pattern ripetuto.
- Mai usare il pictogram al posto del logo completo nelle immagini "first-impression".

### Tipografia su immagine
- Solo **Archivo**. Pesi: Bold o Extrabold per titoli (servono per leggibilità su immagine), Regular per body brevi.
- Min size leggibile: 24 px (mobile), 16 px (desktop).
- Contrasto: testo bianco su scuro o Raisin Black su chiaro. Mai testo Celadon su sfondo Celadon.
- Evita overlay di testo su foto piene di dettaglio: usa una shape Raisin Black con opacità 70–85% sotto il testo.

### Foto e illustrazioni
- **Foto**: autentiche, pulite, professionali. Persone in situazioni di lavoro reali (no stock cliché tipo handshake/lampadina/freccia).
- **Color treatment**: foto in bianco e nero o leggermente desaturate funzionano molto bene con la palette Avvale. Evita foto sature con tonalità che competono con Celadon Green.
- **Illustrazioni**: stile flat, geometrico, con palette Avvale. No 3D rendering iperrealistici, no clipart.
- **Icone**: stile lineare (line icons), peso 1.5–2 px, colore Celadon Green o Raisin Black. Mai icone color-block multi-colore.

## Image generation (AI)

Quando generi immagini con un modello (DALL-E, Imagen, Midjourney, ecc.) per Avvale:

### Prompt — checklist
Includi sempre:
1. **Stile**: "minimalist", "editorial", "clean professional photography" o "flat geometric illustration".
2. **Palette**: cita esplicitamente i colori "deep teal `#248B7E`, off-black `#231C1D`, white". Aggiungi pistachio/keppel se vuoi accenti chiari.
3. **Composizione**: "lots of negative space", "asymmetric composition with strong horizontal lines".
4. **Tono**: "consultancy", "enterprise tech", "B2B premium". Evita "playful", "cartoon", "fantasy".
5. **Esclusioni**: "no people stock photo cliché, no handshake, no lightbulb, no neon glow, no rainbow gradient".

### Esempio di prompt
> Editorial photograph for an enterprise tech consultancy. Modern data center seen from a low angle, lit with a deep teal accent (#248B7E) on off-black machinery. Cinematic, lots of negative space on the left side for headline copy. Minimalist, B2B, premium. No people, no stock cliché, no rainbow gradient.

### Post-processing dell'immagine generata
1. Verifica che i colori dominanti siano in palette (usa un picker se serve).
2. Aggiungi il logo Avvale in PNG (versione coerente con lo sfondo).
3. Ritocca contrasto se necessario per assicurare leggibilità del logo.
4. Esporta nel formato/dimensione del canale di destinazione.

## Composizione tipo: post LinkedIn (1200 × 627)

```
+------------------------------------------+
| [logo Avvale neg] (top-left, 100 px)     |
|                                          |
|   TITOLO IN ARCHIVIO BOLD 60 px          |
|   bianco · max 2 righe · allineato sx    |
|                                          |
|   sottotitolo 28 px · regular            |
|                                          |
|                  [pictogram_white.png    |
|                   opacità 15%, esce      |
|                   dal margine destro]    |
+------------------------------------------+
sfondo: Raisin Black (#231C1D) o Celadon Green (#248B7E)
```

## Don'ts immagini

- Mai filtri Instagram/preset "moody" che virano i colori.
- Mai testo su sfondo a basso contrasto (verde su verde, bianco su pistachio chiaro).
- Mai lasciare il logo "schiacciato" su un bordo senza clearspace.
- Mai più di 2 colori della palette + neutro nello stesso post.
- Mai aggiungere watermark o copyright "© Avvale" — il logo basta.
- Mai usare emoji come "decoro" sull'immagine (vanno solo nel testo del post, e con misura).

## Implementazione tipica

Per generare immagini programmaticamente (es. con Pillow + matplotlib + numpy), carica i token e gli asset come per qualsiasi altra skill:

```python
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys, json

AVVALE = Path("<path>/avvale-brand")
sys.path.insert(0, str(AVVALE / "scripts"))
from load_tokens import load_tokens, rgb_tuple, asset_path

t = load_tokens(AVVALE)
celadon = rgb_tuple(t["color"]["primary"]["celadon_green"])
raisin  = rgb_tuple(t["color"]["primary"]["raisin_black"])
font_p  = "/path/to/Archivo-Bold.ttf"  # o registra con fontconfig

img = Image.new("RGB", (1200, 627), color=raisin)
draw = ImageDraw.Draw(img)

logo = Image.open(asset_path(AVVALE, t["logo"]["paths"]["horizontal_negative"])).convert("RGBA")
logo.thumbnail((220, 80))
img.paste(logo, (60, 50), logo)

draw.text((60, 220), "Data platform.\nIn 12 settimane.",
          font=ImageFont.truetype(font_p, 60), fill="white")

img.save("out.png")
```

## Checklist immagine prima della pubblicazione

- [ ] Logo presente, in versione coerente con lo sfondo.
- [ ] Logo ha clearspace e dimensione minima rispettati.
- [ ] Colori dominanti in palette (bianco / Raisin / Celadon + max 1 accento).
- [ ] Testo in Archivo, leggibile (contrasto ≥ 4.5:1).
- [ ] Dimensioni corrette per il canale (vedi tabella all'inizio).
- [ ] Nessun cliché stock o effetto pacchiano.
- [ ] File salvato come `avvale_<canale>_<oggetto>_<YYYYMMDD>.png`.
