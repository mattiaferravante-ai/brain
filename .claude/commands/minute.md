Genera il verbale strutturato di una riunione a partire da una trascrizione grezza.

Segui le istruzioni in `Work/Skills/minute.md`.

Argomenti (nell'ordine):
1. **progetto** — percorso relativo dentro Work/ (es. `Avvale/projects/ClienteRossi`)
2. **data** *(opzionale)* — data della riunione in formato YYYY-MM-DD (default: oggi)
3. **tipo** *(opzionale)* — `cliente` (default) o `interno`

Dopo gli argomenti, l'utente incollerà la trascrizione grezza nel messaggio.

Esempi:
- `/minute Avvale/projects/ClienteRossi` → poi incolla la trascrizione
- `/minute Avvale/projects/ClienteRossi 2026-05-28 interno`

Output atteso:
1. File verbale salvato in `Work/<progetto>/MeetingNotes/YYYY-MM-DD_meeting.md`
2. README del progetto aggiornato con sezione "Ultimo meeting"
3. Checklist action items mostrata a schermo
