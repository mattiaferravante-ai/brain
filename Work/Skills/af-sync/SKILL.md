# Skill: af-sync

Rilegge l'Analisi Funzionale .docx di un progetto e sincronizza `PROJECT_SUMMARY.md` con il contenuto aggiornato.

## Trigger

`/af-sync [progetto]`

Esempi:
- `/af-sync tea_contratti`
- `/af-sync` (se sei già nella cartella del progetto)

## Input

- **progetto** *(opzionale)* — nome della cartella progetto dentro `Work/Avvale/projects/` o `Work/Clients/`. Se omesso, usa il progetto corrente dal contesto della conversazione.

## Comportamento

### 1. Individua il file AF

Cerca nella cartella `AF/` del progetto il file `.docx` con il numero di revisione più alto (es. `*_AF_*.docx`). Se ce n'è più di uno, usa quello con la data di modifica più recente.

### 2. Estrai il testo dal .docx

Esegui questo snippet Python per estrarre il testo leggibile:

```python
import zipfile, re, sys

def extract_docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    # Estrai testo dai tag <w:t> preservando le interruzioni di paragrafo
    paragraphs = re.split(r'<w:p[ >]', xml)
    lines = []
    for para in paragraphs:
        texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', para)
        line = "".join(texts).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)

print(extract_docx_text(sys.argv[1]))
```

Salva lo script in un file temporaneo ed eseguilo con `python <tmp_script> "<path_af_docx>"`.

### 3. Analizza il contenuto estratto

Leggi il testo estratto e identifica le sezioni presenti nell'AF:
- Registro Versioni (versione, data, autore, descrizione modifiche)
- AS-IS (processo attuale, attori, criticità)
- TO-BE (requisiti funzionali per area: utenti, anagrafiche, configurazioni, processi, automazioni, report)
- Gap Analysis (gap identificati e soluzioni proposte)
- Configurazioni di Sistema
- Open Points / Punti aperti

### 4. Confronta con PROJECT_SUMMARY.md

Leggi il `PROJECT_SUMMARY.md` esistente e identifica:
- Informazioni **nuove** presenti nell'AF ma non nel summary
- Informazioni **aggiornate** (es. gap risolti, nuovi requisiti, decisioni prese)
- Open points **chiusi** nell'AF che nel summary appaiono ancora aperti

### 5. Aggiorna PROJECT_SUMMARY.md

Aggiorna le sezioni pertinenti di `PROJECT_SUMMARY.md`:
- Aggiungi/aggiorna requisiti emersi dalle sezioni TO-BE
- Aggiorna le decisioni chiave (sezione "Decisioni chiave")
- Chiudi i punti aperti risolti (con `~~testo~~`)
- Aggiorna la sezione "Documenti Knowledge Base" con il nome/revisione corretto del file AF
- Aggiorna la data di ultimo aggiornamento

### 6. Report finale

Mostra un riepilogo di:
- File AF letto (nome, revisione, data modifica)
- N. modifiche applicate a PROJECT_SUMMARY.md
- Elenco puntato delle sezioni aggiornate
- Eventuali informazioni nell'AF che sembrano in conflitto con il summary (da risolvere manualmente)

## Note operative

- NON sovrascrivere informazioni già presenti nel summary con versioni meno dettagliate dall'AF
- Se l'AF contiene nomi tecnici (modelli, field names), riportali nella sezione "Note tecniche" del summary, non nei requisiti funzionali
- Se il progetto è in fase UAT, evidenzia eventuali gap ancora aperti
- Dopo la sincronizzazione, sei pronto per ricevere comandi come `/functional-analysis` per generare la prossima versione dell'AF

## Output

Nessun file nuovo generato. Modifica in-place `PROJECT_SUMMARY.md` e mostra il report delle modifiche.
