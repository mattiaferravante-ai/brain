# Section Templates — Blocchi Riutilizzabili

Usare questi blocchi come punto di partenza, adattando i placeholder `[...]`.

---

## Template: Registro Versioni

| Rev  | Descrizione                    | Data       |
|------|--------------------------------|------------|
| 00.1 | Bozza Workshop 1               | GG/MM/AAAA |
| 00.2 | Bozza Workshop 2               | GG/MM/AAAA |
| 01.0 | Prima versione ufficiale       | GG/MM/AAAA |
| 01.1 | Revisione post-delivery        | GG/MM/AAAA |

---

## Template: Apertura sezione AS-IS

```
[Cliente] gestisce annualmente circa [X] [operazioni/contratti/ordini].
Il team [commerciale/operativo/amministrativo] è composto da [N] persone: [ruoli].

Il processo attuale è suddiviso nelle seguenti fasi principali:
- [Fase 1]
- [Fase 2]
- [Fase 3]

Gli strumenti attualmente in uso sono: [Excel / email / sistema legacy / altro].

I principali pain point rilevati in fase di workshop sono:
- [Pain point 1]
- [Pain point 2]
```

---

## Template: Apertura sezione TO-BE

```
La soluzione TO-BE prevede l'implementazione di Odoo Enterprise [versione],
modulo [nome modulo], per coprire i seguenti processi:
- [Processo 1]
- [Processo 2]

Vengono di seguito dettagliate le aree funzionali previste.
```

---

## Template: Blocco Utenti e Ruoli

```markdown
### Utenti e Ruoli

Vengono definiti i seguenti profili utente:

| Profilo       | Accessi principali                         | Restrizioni               |
|---------------|--------------------------------------------|---------------------------|
| [Ruolo 1]     | [Cosa può fare]                            | [Cosa non può fare]       |
| [Ruolo 2]     | [Cosa può fare]                            | [Cosa non può fare]       |
```

---

## Template: Blocco Processo Operativo Step-by-Step

```markdown
### [Nome Processo]

**Attori**: [Ruoli coinvolti]
**Trigger**: [Cosa avvia il processo]
**Output**: [Risultato finale]

| Step | Azione utente | Menu path                    | Risultato sistema |
|------|---------------|------------------------------|-------------------|
| 1    | [Azione]      | [Modulo > Voce > Sotto-voce] | [Cosa succede]    |
| 2    | [Azione]      | [Menu path]                  | [Risultato]       |
| 3    | [Azione]      | [Menu path]                  | [Risultato]       |

**Regole di validazione:**
- [Regola 1 — es. campo X obbligatorio prima di passare allo stato Y]
- [Regola 2]

**Messaggi di errore comuni:**
- [Errore] → [Causa] → [Soluzione]
```

---

## Template: Gap Analysis completa

| ID      | Area      | Processo AS-IS               | Soluzione TO-BE           | Tipo     | Effort  | Note              |
|---------|-----------|------------------------------|---------------------------|----------|---------|-------------------|
| GAP-001 | [Modulo]  | [Come funziona oggi]         | [Come funzionerà in Odoo] | Standard | Basso   | -                 |
| GAP-002 | [Modulo]  | [Come funziona oggi]         | [Configurazione Odoo]     | Config   | Basso   | -                 |
| GAP-003 | [Modulo]  | [Come funziona oggi]         | [Sviluppo custom / OCA]   | Custom   | Medio   | [Nome modulo OCA] |
| GAP-004 | [Modulo]  | [Processo non supportato]    | Non in scope              | Out      | —       | Fase 2            |

**Leggenda effort:**
- Basso: < 0,5 gg
- Medio: 0,5–2 gg
- Alto: > 2 gg

---

## Template: Configurazioni di Sistema

```markdown
### [Nome Modulo]

| Menu path                         | Parametro                   | Valore / Logica          | Dipendenze        |
|-----------------------------------|-----------------------------|--------------------------|-------------------|
| [Modulo > Configurazione > Voce]  | [Nome parametro]            | [Valore o regola]        | [Pre-requisito]   |
| [Menu path]                       | [Parametro]                 | [Valore]                 | -                 |
```

---

## Template: Open Points

| ID     | Descrizione                                    | Responsabile       | Data limite | Stato  |
|--------|------------------------------------------------|--------------------|-------------|--------|
| OP-001 | [Questione aperta o decisione pendente]        | [Nome / Azienda]   | GG/MM/AAAA  | Aperto |
| OP-002 | [Informazione mancante da cliente]             | [Nome / Azienda]   | GG/MM/AAAA  | Chiuso |

Stati ammessi: `Aperto`, `In analisi`, `Risolto`, `Chiuso`, `Rinviato`.

---

## Template: Nota di assunzione (inizio documento)

```
> **Nota metodologica**: Le informazioni contenute in questo documento sono basate
> sui workshop effettuati in data [date]. Le seguenti assunzioni sono state applicate
> in assenza di indicazioni esplicite:
> - Versione Odoo Enterprise: [versione]
> - Lingua sistema: [IT/EN]
> - [Altra assunzione]
>
> Eventuali variazioni rispetto a queste assunzioni potranno impattare lo scope
> e i tempi di implementazione.
```

---

## Template: Sezione "N/A"

Quando una sezione non è applicabile, **non rimuoverla**: lasciarla nel
documento con la nota standard:

```
N/A – non in scope per questa fase.
```
