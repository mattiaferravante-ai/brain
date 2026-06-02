# Skill: generate-cv

Genera il curriculum di Mattia Ferravante a partire da `Work/PROFESSIONAL_PROFILE.md` come source of truth.

## Trigger

Ogni volta che si parla di: generare il CV, aggiornare il curriculum, creare una versione del curriculum, CV in inglese/italiano, CV per una specifica posizione.

## Comportamento

1. Leggi `Work/PROFESSIONAL_PROFILE.md` per esperienza, competenze, carriera
2. Leggi `Personal/PERSONAL_PROFILE.md` per formazione e dati anagrafici
3. Genera il CV nel formato richiesto (vedi opzioni sotto)
4. Salva l'output in `Work/CV/` con naming: `CV_Ferravante_[lingua]_[YYYY-MM].md`

## Parametri

- **lingua:** `it` (default) | `en`
- **target:** ruolo o posizione specifica (es. "Odoo Senior Consultant", "ERP Project Manager") — adatta il tono e le priorità
- **formato:** `standard` (default) | `breve` (1 pagina) | `dettagliato`

## Struttura output CV

```
# Mattia Ferravante
[contatti: email, telefono, città]

## Profilo professionale
[2-3 righe che sintetizzano chi è e il suo valore]

## Esperienza professionale
[cronologica inversa — per ogni ruolo: azienda, periodo, titolo, bullet point responsabilità]

## Competenze tecniche
[raggruppate per area: ERP/Odoo, Programmazione, Database, OS/Tools]

## Formazione
[cronologica inversa]

## Lingue
[Italiano: madrelingua | Inglese: buono]

## Certificazioni
[Odoo 19 Functional]
```

## Note

- Il profilo Avvale va descritto mettendo in evidenza il ruolo di **Lead Process Specialist**: raccolta requisiti, AF, UAT, progettazione processi, interfaccia dev team
- Il background contabile (Motip Dupli) è un differenziante per ruoli in ambito ERP finance — valorizzarlo
- Il gap 2021-2022 non va lasciato vuoto: descriverlo come "Formazione intensiva — Python, Data Science, pivot di carriera"
- Output in Markdown, convertibile in PDF/DOCX
