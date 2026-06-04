# Test Case Library — UAT Avvale (Odoo Enterprise)

Libreria di test case standard organizzata per **processo di business
end-to-end**, non per modulo Odoo. Ogni area contiene:

1. Una **descrizione processo** non tecnica (intro per foglio Funzionale)
2. Una tabella di test case atomici con classificazione **Audience (F/T)**

> **Uso**: caricare questo file solo se l'utente sceglie "standard" o "mix"
> per un'area nello Step 3 della skill `uat-testbook`. La libreria è un
> punto di partenza — l'utente può modificare, aggiungere o rimuovere
> qualsiasi test case durante l'intake.

Formato test case: colonne `Step ID | Title | Pre-requisite | Test Step
description | Expected result | Audience (F/T)`.

**Legenda Audience**:
- **F** = Funzionale → foglio "Test book - Funzionale" (cliente)
- **T** = Tecnico → foglio "Test book - Tecnico" (QA interno)

---

## Area 1 — Login & Navigation

**Descrizione processo (intro foglio Funzionale)**:

L'utente accede a Odoo con le proprie credenziali aziendali e visualizza
la dashboard configurata per il suo ruolo. Da qui può navigare nei moduli
abilitati, modificare le proprie preferenze (lingua, fuso orario) e
ricercare rapidamente qualunque record. Il logout è esplicito e protegge
la sessione.

| Step ID | Title              | Pre-requisite                                | Test Step description                                                                                  | Expected result                                                                                          | Audience |
|---------|--------------------|----------------------------------------------|--------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|----------|
| 1       | Login OK           | Utente attivo con credenziali valide         | Aprire URL Odoo → inserire username e password validi → cliccare "Log in"                              | L'utente accede a Odoo e visualizza la dashboard di default secondo il proprio gruppo                    | F        |
| 2       | Navigazione moduli | Utente loggato                               | Click su menu principale → verificare elenco app abilitate → aprire 2-3 app del perimetro              | Solo le app del perimetro UAT sono visibili; ogni modulo si apre senza errore                            | F        |
| 3       | My Profile         | Utente loggato                               | Click avatar → "My Profile" → modificare firma email → Save                                            | Modifiche salvate; firma applicata nei messaggi outbound                                                  | F        |
| 4       | Lingua interfaccia | Utente loggato                               | Preferences → cambiare lingua → ricaricare pagina                                                       | L'interfaccia viene mostrata nella lingua selezionata                                                    | F        |
| 5       | Logout             | Utente loggato                               | Click avatar → "Log out"                                                                                | Disconnessione e redirect alla pagina di login                                                            | F        |
| 6       | Login KO password  | Utente attivo                                | URL Odoo → username valido + password errata → "Log in"                                                | Errore "Wrong login/password"; nessun accesso                                                            | T        |
| 7       | Reset password     | Utente con email valida                      | Login screen → "Reset Password" → email → verifica link                                                | Email ricevuta entro 5 minuti; link funzionante                                                          | T        |
| 8       | Sessione scaduta   | Utente loggato                               | Lasciare sessione idle oltre il timeout configurato → tentare azione                                    | Sistema richiede ri-login                                                                                | T        |

---

## Area 2 — Anagrafiche (Master data)

**Descrizione processo (intro foglio Funzionale)**:

Prima di poter operare, occorre caricare le anagrafiche di base: clienti,
fornitori, prodotti e listini. Le anagrafiche cliente includono ragione
sociale, partita IVA, indirizzi e referenti. I prodotti hanno categoria,
prezzo e regole di tassazione. I listini permettono di applicare prezzi
o sconti differenziati per cliente o gruppo. Una volta caricate, queste
anagrafiche alimentano automaticamente tutti i documenti operativi.

| Step ID | Title                              | Pre-requisite                                | Test Step description                                                                                       | Expected result                                                                                                  | Audience |
|---------|------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------|
| 1       | Crea cliente (Contact)             | Utente con permessi Contacts Manager         | Contacts → Create → compilare ragione sociale, P.IVA, indirizzo, email → Save                              | Record creato; ricercabile per nome, P.IVA e codice                                                              | F        |
| 2       | Crea contatto referente            | Partner aziendale esistente                  | Aprire partner → "Contacts & Addresses" → Create → tipo "Contact" → nome, email, telefono → Save           | Referente collegato al partner azienda; visibile nelle sue Addresses                                              | F        |
| 3       | Crea prodotto Service              | Utente con product.group_product_manager     | Inventory > Products → Create → Tipo "Service" → categoria → prezzo listino → Save                         | Prodotto disponibile in Sales / Purchase                                                                          | F        |
| 4       | Crea listino prezzi cliente        | Esiste un cliente target                     | Sales → Configuration → Pricelists → Create → riga sconto 10% per prodotto X → applicare a cliente Y       | SO per cliente Y con prodotto X applica sconto 10%                                                               | F        |
| 5       | Import massivo contatti via Excel  | File Excel con 10 record di test             | Contacts → Favorites → Import records → upload file → mappare colonne → Test → Import                       | 10 record importati senza errori                                                                                  | F        |
| 6       | Validazione P.IVA duplicata        | Esiste partner con P.IVA = X                 | Contacts → Create → stessa P.IVA → Save                                                                     | Warning di P.IVA duplicata (se attivato) o conferma esplicita                                                    | T        |
| 7       | Vincolo P.IVA formato              | -                                            | Contacts → Create → P.IVA con caratteri non validi → Save                                                   | Sistema blocca il save con errore di formato                                                                      | T        |
| 8       | ACL Contacts read-only             | Utente con gruppo Contacts Read              | Aprire contatto → tentare modifica                                                                          | Bottoni Edit nascosti; salvataggio impossibile                                                                    | T        |

---

## Area 3 — CRM: Lead-to-Opportunity

**Descrizione processo (intro foglio Funzionale)**:

Il commerciale riceve una richiesta da un potenziale cliente (form web,
telefono, email, fiera). La registra in Odoo come Lead, raccoglie le
informazioni essenziali (azienda, contatto, esigenza) e qualifica il
contatto. Quando il Lead diventa concreto, viene convertito in
Opportunità all'interno della pipeline commerciale e assegnato al sales
owner per la preparazione dell'offerta. Ogni Opportunità ha uno stage,
una stima di valore e una data di chiusura prevista.

| Step ID | Title                              | Pre-requisite                                | Test Step description                                                                                       | Expected result                                                                                                  | Audience |
|---------|------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------|
| 1       | Crea Lead manuale                  | Utente con gruppo CRM/User                   | CRM → Leads → Create → compilare nome, azienda, email, telefono, descrizione esigenza → Save                | Lead creato in stato iniziale; ricercabile e visibile in lista                                                   | F        |
| 2       | Crea Lead da modulo web            | Form web pubblico configurato                | Compilare form web di contatto sul sito → Submit                                                            | Lead creato automaticamente in CRM con dati da form; assegnato al team default                                   | F        |
| 3       | Qualifica e arricchisci Lead       | Lead esistente                               | Aprire Lead → compilare campi qualifica (settore, dimensione azienda, budget) → assegnare salesperson      | Campi aggiornati; salesperson notificato                                                                          | F        |
| 4       | Converti Lead in Opportunity       | Lead qualificato                             | Aprire Lead → bottone "Convert to Opportunity" → confermare partner/azienda → Create                        | Opportunity creata in pipeline allo stage iniziale; Lead archiviato                                              | F        |
| 5       | Avanza stage pipeline              | Opportunity esistente                        | Aprire Opportunity → drag-and-drop o cambio stage in form → "Proposition"                                  | Stage aggiornato; cronologia visibile nel chatter                                                                | F        |
| 6       | Pianifica attività                 | Opportunity esistente                        | Opportunity → Activities → Schedule activity → tipo "Call" → data → Save                                   | Attività in agenda salesperson; notifica generata                                                                | F        |
| 7       | Lost reason                        | Opportunity in pipeline                      | Opportunity → "Mark as Lost" → selezionare lost reason → Confirm                                            | Opportunity in stato Lost; reason registrata per analisi                                                          | F        |
| 8       | Vincolo email Lead                 | -                                            | CRM → Leads → Create → lasciare email vuota → Save                                                          | Save consentito ma warning se la regola lo prevede; o blocco se email obbligatoria                                | T        |
| 9       | ACL multi-team                     | Utente Sales/User di Team A; Opp di Team B   | Login utente A → cercare Opportunity di Team B                                                              | Record di Team B non visibile (record rule applicata)                                                            | T        |
| 10      | Conversione Lead → Partner         | Lead con nuova azienda                       | Convert → "Create new customer" → verificare creazione partner                                              | Partner creato con dati Lead; collegato all'Opportunity                                                          | T        |

---

## Area 4 — Offerta / Quotation

**Descrizione processo (intro foglio Funzionale)**:

Dall'Opportunità qualificata, il commerciale genera l'Offerta selezionando
i prodotti/servizi, le quantità e applicando eventuali sconti o condizioni
particolari. Il listino del cliente precompila automaticamente i prezzi.
L'Offerta può richiedere approvazione interna se supera soglie definite.
Una volta approvata, viene inviata al cliente via email come PDF formattato.
Il cliente può accettarla, rifiutarla o richiedere modifiche.

| Step ID | Title                                  | Pre-requisite                                          | Test Step description                                                                                                      | Expected result                                                                                                              | Audience |
|---------|----------------------------------------|--------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|----------|
| 1       | Crea Offerta da Opportunity            | Opportunity esistente                                  | Aprire Opp → "New Quotation" → confermare cliente → Save                                                                   | Quotation creata e collegata all'Opportunity; numero progressivo                                                              | F        |
| 2       | Aggiungi righe prodotto                | Quotation in Draft                                     | Quotation → aggiungere 3 righe prodotto con quantità e prezzo da listino → Save                                            | Righe inserite; prezzo da listino cliente; totale calcolato                                                                    | F        |
| 3       | Applica sconto                         | Quotation con righe                                    | Modificare sconto % su una riga → Save                                                                                     | Subtotale e totale aggiornati                                                                                                  | F        |
| 4       | Richiedi approvazione                  | Quotation > soglia                                     | Quotation → "Request approval" → seleziona approver → Submit                                                              | Stato "In Approval"; approver notificato                                                                                       | F        |
| 5       | Approva offerta                        | Quotation in "In Approval", utente Approver            | Approver apre Quotation → "Approve"                                                                                        | Stato "Approved"; pronta per invio                                                                                             | F        |
| 6       | Invia preventivo via email             | Quotation approvata                                    | Aprire quotation → "Send by Email" → verificare template → Send                                                            | Email inviata con PDF allegato; messaggio nel chatter; stato "Sent"                                                            | F        |
| 7       | Anteprima PDF offerta                  | Quotation esistente                                    | Aprire quotation → Print → "Quotation"                                                                                     | PDF generato con logo, dati cliente, righe, totali, IVA                                                                        | F        |
| 8       | Accetta offerta (lato cliente)         | Quotation inviata                                      | Cliente apre link portale → "Accept"                                                                                       | Quotation accettata; stato avanza; commerciale notificato                                                                       | F        |
| 9       | Rifiuta offerta con motivo             | Quotation inviata                                      | Cliente apre link portale → "Decline" → motivare                                                                           | Stato "Refused"; motivazione registrata                                                                                        | F        |
| 10      | Sequence numero progressivo            | -                                                      | Creare 3 Quotation consecutive                                                                                             | Numeri progressivi consecutivi senza gap; format come da configurazione                                                        | T        |
| 11      | Vincolo riga negativa                  | Quotation                                              | Inserire riga con quantità o prezzo negativo → Save                                                                        | Save bloccato con errore di vincolo                                                                                            | T        |
| 12      | Ricalcolo prezzo da listino            | Cliente con listino assegnato                          | Cambiare cliente in Quotation esistente → verificare prezzi                                                                 | Prezzi righe ricalcolati automaticamente sul nuovo listino                                                                     | T        |
| 13      | ACL approver self-approval             | Utente è creatore + approver                           | Creare Quotation → Request approval → tentare self-approve                                                                  | Sistema impedisce self-approval (segregation of duties)                                                                        | T        |

---

## Area 5 — Contratto & Firma digitale (Sign)

**Descrizione processo (intro foglio Funzionale)**:

Una volta accettata l'offerta, il sistema genera il contratto in PDF con
i dati del cliente, le clausole standard, i prodotti/servizi negoziati
e i campi firma posizionati. Il contratto viene inviato al cliente via
email tramite il modulo Sign di Odoo. Il cliente apre il link, compila
i campi richiesti, appone la firma online e conferma. Successivamente il
referente interno Avvale firma a sua volta. A firma completata, il
contratto risulta automaticamente "Firmato" in Odoo, il PDF firmato è
allegato al record e il sistema può procedere con la creazione dell'ordine.

| Step ID | Title                                  | Pre-requisite                                          | Test Step description                                                                                                      | Expected result                                                                                                              | Audience |
|---------|----------------------------------------|--------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|----------|
| 1       | Genera contratto da Offerta            | Quotation accettata                                    | Aprire Quotation → "Generate Contract" → template → Generate                                                               | Contratto creato e collegato; clausole e dati popolati dal template                                                            | F        |
| 2       | Anteprima PDF contratto                | Contratto creato                                       | Aprire contratto → Preview                                                                                                 | PDF con loghi, dati cliente, prodotti, clausole e campi firma posizionati                                                      | F        |
| 3       | Invia contratto a firma                | Contratto + email cliente valida                       | Contratto → "Send to Signature" → firmatari (cliente + interno) → Send                                                     | Sign Request creata; email al firmatario; stato "Sent"                                                                         | F        |
| 4       | Cliente firma (lato Sign)              | Sign Request inviata, link ricevuto                    | Aprire link email → compilare campi → firma → Validate                                                                     | Sign Request avanza (firma interna o "Fully signed")                                                                            | F        |
| 5       | Firmatario interno completa            | Sign Request firmata da cliente                        | Utente interno → Sign → My Requests → Sign → Validate                                                                      | Stato "Fully signed"; PDF firmato scaricabile                                                                                  | F        |
| 6       | Contratto aggiornato post-firma        | Sign Request "Fully signed"                            | Aprire contratto Odoo → verificare stato                                                                                   | Stato "Firmato"; PDF firmato allegato                                                                                          | F        |
| 7       | Annulla Sign Request                   | Sign Request inviata, non firmata                      | Aprire Sign Request → "Cancel"                                                                                             | Sign Request annullata; contratto torna in bozza o annullato                                                                   | F        |
| 8       | Rifiuto firma cliente                  | Sign Request inviata                                   | Cliente apre link → "Decline" → motivazione                                                                                | Stato "Refused"; mittente notificato con motivazione                                                                           | F        |
| 9       | Audit trail firma                      | Documento firmato                                      | Aprire Sign firmato → visualizzare audit trail                                                                             | Audit completo: IP, timestamp, identità firmatario per ogni firma                                                              | F        |
| 10      | Promemoria automatico                  | Sign Request da > X giorni                             | Attendere/forzare cron reminder                                                                                            | Email di reminder al firmatario non rispondente                                                                                | T        |
| 11      | Posizionamento campi firma             | Template Sign                                          | Verificare che i campi firma siano posizionati correttamente nel PDF generato (coordinate cm/mm)                            | Campi firma su pagina giusta, posizione corretta                                                                                | T        |
| 12      | Firma multipla in sequenza             | Sign Request 2 firmatari ordinati                      | Firma F1 → verifica stato → F2 riceve email → firma                                                                        | Stato avanza nell'ordine; "Fully signed" al termine                                                                            | T        |
| 13      | Permesso Sign Manager                  | Utente senza gruppo Sign User                          | Tentare apertura modulo Sign                                                                                                | Accesso negato; modulo nascosto dal menu                                                                                       | T        |
| 14      | Validità link Sign scaduto             | Sign Request scaduta                                   | Aprire link Sign dopo scadenza                                                                                              | Sistema mostra messaggio "Link scaduto"; firma non possibile                                                                   | T        |

---

## Area 6 — Order-to-Cash (vendita → consegna → incasso)

**Descrizione processo (intro foglio Funzionale)**:

Dopo la firma del contratto (o l'accettazione dell'offerta), il sistema
crea l'ordine di vendita. Se ci sono prodotti fisici, viene generato il
movimento di magazzino per la spedizione; il magazziniere prepara la
merce, la spedizione viene validata e il cliente riceve il documento di
trasporto. Contestualmente o successivamente, l'amministrazione emette
la fattura, che viene inviata al cliente e tracciata fino all'incasso
e alla riconciliazione bancaria.

| Step ID | Title                                | Pre-requisite                                  | Test Step description                                                                                            | Expected result                                                                                                | Audience |
|---------|--------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------|
| 1       | Crea Sale Order da Offerta firmata   | Contratto firmato                              | Aprire contratto → "Confirm" / azione → verifica creazione SO                                                    | Sale Order confermato collegato al contratto; numero progressivo                                                | F        |
| 2       | Prepara consegna (Delivery)          | SO con prodotti stoccabili                     | Inventory → Transfers → Delivery → aprire transfer → Validate                                                    | Stock scaricato; SO avanza nel flusso                                                                          | F        |
| 3       | Stampa documento di trasporto        | Delivery validato                              | Aprire delivery → Print → DDT                                                                                     | PDF DDT con righe spedite, destinatario, vettore                                                                | F        |
| 4       | Crea fattura cliente da SO           | SO confermato                                  | SO → "Create Invoice" → Regular Invoice → Confirm                                                                 | Fattura "Posted"; scritture contabili coerenti                                                                  | F        |
| 5       | Stampa fattura PDF                   | Fattura confermata                             | Aprire fattura → Print → Invoice                                                                                  | PDF con dati cliente, righe, totali, IVA, numero progressivo                                                    | F        |
| 6       | Invio fattura elettronica            | Fattura confermata, l10n attiva                | Fattura → "Send Electronic Invoice" → coda SDI / FINA                                                            | Fattura inviata al canale fiscale; stato di trasmissione aggiornato                                            | F        |
| 7       | Registra pagamento cliente           | Fattura cliente confermata                     | Fattura → "Register Payment" → banca → Confirm                                                                    | Pagamento registrato; fattura "In Payment" → "Paid" dopo riconciliazione                                       | F        |
| 8       | Riconciliazione bancaria             | Estratto conto importato                       | Bank → Reconcile → match riga con fattura                                                                         | Movimento riconciliato; fattura "Paid"                                                                          | F        |
| 9       | Stato pagamenti scaduti              | Fattura con scadenza superata                  | Aging report clienti                                                                                              | Fattura compare nello scaduto con bucket corretto                                                              | F        |
| 10      | Sequence fatture progressiva         | -                                              | Creare 3 fatture consecutive in stesso anno                                                                       | Numeri progressivi consecutivi senza gap                                                                       | T        |
| 11      | Validazione IVA codice fiscale       | Fattura cliente IT                             | Verificare campo codice fiscale obbligatorio                                                                       | Sistema blocca conferma se mancante (su clienti privati)                                                       | T        |
| 12      | Vincolo data fattura < data SO       | SO con data X                                  | Fatturare con data < data SO                                                                                      | Warning o blocco secondo configurazione                                                                        | T        |

---

## Area 7 — Procure-to-Pay (acquisto → ricezione → pagamento)

**Descrizione processo (intro foglio Funzionale)**:

L'ufficio acquisti riceve una richiesta interna o pianifica un
riapprovvigionamento. Crea una RdA o direttamente un Purchase Order
al fornitore con righe prodotto, quantità, prezzo e tempi di consegna.
L'ordine viene inviato al fornitore. Alla ricezione della merce, il
magazziniere registra l'entrata aggiornando le giacenze. L'amministrazione
registra poi la fattura fornitore associandola al PO e alla ricezione,
e la paga tramite riconciliazione bancaria.

| Step ID | Title                                | Pre-requisite                                  | Test Step description                                                                                            | Expected result                                                                                                | Audience |
|---------|--------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------|
| 1       | Crea RdA (Purchase Request)          | Modulo PR attivo                               | Purchase → Requests → Create → righe prodotto → Submit                                                            | Request creata; approver notificato                                                                            | F        |
| 2       | Approva RdA                          | RdA in attesa                                  | Approver → Approve                                                                                                | RdA approvata; pronta a generare PO                                                                            | F        |
| 3       | Crea Purchase Order                  | Fornitore esistente                            | Purchase → Orders → Create → fornitore + righe → Confirm Order                                                    | PO confermato; numero progressivo                                                                              | F        |
| 4       | Invia PO al fornitore                | PO confermato                                  | PO → "Send by Email"                                                                                              | Email con PDF inviata                                                                                          | F        |
| 5       | Ricezione merce (Receipt)            | PO confermato                                  | Inventory → Receipts → aprire transfer → Validate                                                                 | Stock aggiornato; PO avanza                                                                                    | F        |
| 6       | Crea fattura fornitore (Bill)        | PO + Receipt validato                          | Purchase → PO → "Create Bill" → ref/date → Confirm                                                                | Bill creato e collegato; scritture coerenti                                                                    | F        |
| 7       | Registra pagamento fornitore         | Bill confermato                                | Bill → "Register Payment" → banca → Confirm                                                                       | Pagamento registrato; Bill "Paid" dopo riconciliazione                                                         | F        |
| 8       | 3-way match (PO/Receipt/Bill)        | Bill, PO e Receipt con quantità diverse        | Creare Bill con qta != ricevute                                                                                   | Sistema segnala discrepanza o blocca conferma                                                                  | T        |
| 9       | Vincolo fornitore attivo             | Fornitore archiviato                           | Tentare creazione PO con fornitore archiviato                                                                     | Bloccato o warning                                                                                             | T        |
| 10      | Multi-currency PO                    | Fornitore in valuta estera                     | Creare PO in USD → verifica tasso cambio                                                                          | Tasso applicato secondo configurazione (data PO o data fattura)                                                | T        |

---

## Area 8 — Magazzino & Logistica

**Descrizione processo (intro foglio Funzionale)**:

Il magazziniere gestisce le entrate, le uscite e gli inventari fisici dei
prodotti. Per ogni movimento, il sistema aggiorna automaticamente le
giacenze per location e fornisce report di stock in tempo reale. Per
prodotti tracciati a lotto o numero seriale, la tracciabilità è completa
dalla ricezione alla consegna al cliente finale. Gli inventari fisici
permettono di rettificare le quantità a sistema in base ai conteggi reali.

| Step ID | Title                       | Pre-requisite                                  | Test Step description                                                                              | Expected result                                                              | Audience |
|---------|-----------------------------|------------------------------------------------|----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|----------|
| 1       | Visualizza giacenze         | Prodotti con stock iniziale                    | Inventory → Reporting → Stock                                                                       | Report giacenze per prodotto / location coerente con setup                   | F        |
| 2       | Inventory adjustment        | Permessi inventory manager                     | Inventory → Operations → Physical Inventory → Create → aggiornare quantità → Apply                  | Quantità aggiornata; movimento di rettifica registrato                       | F        |
| 3       | Tracciabilità lotto          | Prodotto con tracking "By Lots"                | Entrata con lotto → Delivery con lotto → Reporting → Traceability                                   | Tracciabilità monte-valle completa                                            | F        |
| 4       | Trasferimento interno       | 2 location attive                              | Inventory → Transfers → Internal → Create → Validate                                                | Stock spostato fra location                                                  | F        |
| 5       | Picking strategy FIFO       | Prodotto con più lotti                         | Creare Delivery → verificare lotti suggeriti                                                        | FIFO applicato; lotto più vecchio assegnato per primo                        | T        |
| 6       | Stock negativo bloccato     | Prodotto a stock 0                             | Tentare Delivery di quantità > stock                                                                | Bloccato o warning secondo configurazione                                    | T        |

---

## Area 9 — Contabilità & Reporting

**Descrizione processo (intro foglio Funzionale)**:

L'ufficio amministrativo registra le scritture contabili a partire dai
documenti operativi (fatture, pagamenti, movimenti bancari) e produce
report di gestione (bilancio, conto economico, scaduto). La distribuzione
analitica consente di attribuire costi e ricavi ai centri di costo o
progetti. A fine periodo, l'amministrazione blocca le scritture per
impedire modifiche retroattive e procede alla dichiarazione fiscale.

| Step ID | Title                                | Pre-requisite                                  | Test Step description                                                                                            | Expected result                                                                                                | Audience |
|---------|--------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|----------|
| 1       | Bilancio di verifica                 | Movimenti contabili presenti                   | Accounting → Reporting → Trial Balance                                                                            | Report bilanciato (Debit = Credit), filtrabile per periodo                                                     | F        |
| 2       | Conto economico                      | Periodo con ricavi e costi                     | Accounting → Reporting → Profit & Loss                                                                            | P&L coerente con scritture; export PDF/Excel                                                                   | F        |
| 3       | Distribuzione analitica              | Piano analitico configurato                    | Su fattura → riga → distribuzione analitica → percentuali → Confirm                                                | Scritture analitiche generate con percentuali indicate                                                          | F        |
| 4       | Report analitico                     | Movimenti analitici presenti                   | Accounting → Reporting → Analytic                                                                                  | Report mostra costi/ricavi per centro analitico                                                                | F        |
| 5       | Chiusura periodo contabile           | Permessi accounting manager                    | Accounting → Lock Date → impostare → Save                                                                          | Modifiche su periodo bloccato impedite con messaggio                                                            | F        |
| 6       | Validazione bilancio sbilanciato     | Scrittura manuale con D ≠ C                    | Inserire scrittura manuale sbilanciata → Post                                                                      | Sistema blocca il post                                                                                          | T        |
| 7       | Multi-currency rounding              | Fattura USD con cambio                          | Verificare rounding scritture in valuta locale                                                                     | Rounding entro tolleranza; eventuale conto di rounding utilizzato                                              | T        |

---

## Area 10 — Permessi e sicurezza

**Descrizione processo (intro foglio Funzionale)**:

Ogni utente ha un ruolo aziendale (commerciale, magazziniere, contabile,
manager, admin) che determina quali moduli può vedere, quali dati può
leggere e quali azioni può eseguire. La segregation of duties impedisce
che lo stesso utente possa, ad esempio, creare e approvare lo stesso
documento. Le aziende multi-company vedono solo i dati della propria
azienda. Tutti gli accessi e le modifiche critiche sono tracciati in audit log.

| Step ID | Title                                 | Pre-requisite                                | Test Step description                                                                                       | Expected result                                                                                  | Audience |
|---------|---------------------------------------|----------------------------------------------|-------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|----------|
| 1       | Visibilità menu Sales User            | Utente test con "Sales / User"               | Login utente test → verificare menu                                                                          | Vede Sales, CRM, Contacts; non vede Accounting Manager o Settings                                | F        |
| 2       | Read-only su modulo                    | Utente con gruppo Read-only                  | Aprire record → tentare modifica → Save                                                                     | Modifica impedita; messaggio di permesso                                                          | F        |
| 3       | Segregation: creator ≠ approver        | Utente A crea, utente B approva              | A crea → tenta approvazione → fallisce → B approva                                                          | Creator non può approvare; approver non vede "Create" se non autorizzato                          | F        |
| 4       | Multi-company restriction              | Utente A su Company A; record di B           | Login A → cercare record di Company B                                                                       | Record di B non visibili                                                                          | T        |
| 5       | Audit log accessi                      | Login module attivo                          | Eseguire login/logout/modifica record → audit log                                                            | Audit log con utente, IP, timestamp, azione                                                       | T        |
| 6       | Record rule custom                     | ir.rule custom su modello X                  | Verificare che utente fuori gruppo non veda record filtrati                                                 | Record rule applicata coerentemente                                                              | T        |

---

# Appendice — Esempio TEA / A&E (waste management, Odoo 19)

Case study reale: cliente TEA — Ambiente & Ecologia, gestione contratti
e offerte per smaltimento rifiuti. Tre tipologie di offerta (TMB,
Discarica, Rifiuti Speciali) con regole di pricing, righe e documentazione
PDF differenziate. Modulo custom `tea_quotations` su Odoo 19 Enterprise.

Le aree sotto si **affiancano** alle aree standard quando si lavora su
progetti waste management o quando si vuole copiare il pattern multi-tipo
con generazione PDF custom + Sign.

---

### Area TEA-A — Anagrafiche rifiuti (CER, HP, Operazioni R/D)

**Descrizione processo (intro foglio Funzionale)**:

Per gestire offerte di smaltimento, occorre caricare le anagrafiche
normative: i codici CER (classificazione europea rifiuti), le frasi HP
(caratteristiche di pericolo) e le operazioni di recupero/smaltimento
(R1-R13 / D1-D15). Queste anagrafiche sono utilizzate nelle righe di
ogni offerta Discarica e Rifiuti Speciali per identificare correttamente
il rifiuto trattato.

| Step ID | Title                          | Pre-requisite               | Test Step description                                                          | Expected result                                                | Audience |
|---------|--------------------------------|-----------------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------|----------|
| 1       | Import lista CER da file       | File con elenco CER ufficiali | Settings → Tecnico → CER → Import                                              | Tutti i CER importati e ricercabili                            | F        |
| 2       | Crea codice HP custom          | Permessi master data        | HP Codes → Create → codice + descrizione                                       | HP creato e disponibile in righe offerta                       | F        |
| 3       | Crea operazione R/D            | -                           | Waste operations → Create                                                       | Operazione disponibile per selezione                          | F        |
| 4       | Vincolo CER duplicato          | CER esistente               | Tentare creazione CER duplicato                                                 | Save bloccato per unique constraint                            | T        |

---

### Area TEA-B — Offerta TMB

**Descrizione processo (intro foglio Funzionale)**:

L'offerta TMB (Trattamento Meccanico Biologico) è la più semplice fra
le tre tipologie: il commerciale seleziona il tipo offerta TMB, compila
i dati di testata (cliente, produttore, validità) e inserisce una o più
righe servizio con prezzo e quantità. Non sono richiesti CER specifici
né documentazione tecnica aggiuntiva. Il PDF generato segue il template
TMB standard.

| Step ID | Title                          | Pre-requisite                | Test Step description                                                          | Expected result                                                | Audience |
|---------|--------------------------------|------------------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------|----------|
| 1       | Crea Offerta TMB da Opp        | Opportunity esistente        | Opp → New Quotation → tipo "TMB" → cliente + produttore → Save                  | Offerta TMB creata; campi tipo-specifici visibili              | F        |
| 2       | Aggiungi servizio              | Offerta TMB                  | Righe servizio → Create → servizio + quantità + prezzo                          | Riga inserita; totale aggiornato                               | F        |
| 3       | Genera PDF TMB                 | Offerta TMB compilata        | Print → Offerta TMB                                                             | PDF con template TMB, dati cliente e righe servizio            | F        |
| 4       | Invia Offerta TMB a firma      | Offerta TMB approvata        | Send to Signature → cliente + interno                                           | Sign Request creata; flusso firma TMB                          | F        |

---

### Area TEA-C — Offerta Discarica

**Descrizione processo (intro foglio Funzionale)**:

L'offerta Discarica gestisce contratti di smaltimento in discarica per
più rifiuti contemporaneamente, suddivisi in Fanghi e Non Fanghi. La
testata include cliente, validità, eventuale fidejussione. L'Allegato 2
elenca i produttori (filtrato sugli indirizzi del cliente). Le righe
identificano i rifiuti con CER, HP e operazione, ciascuno con prezzo
e minimo fatturabile. Il PDF generato segue il formato Discarica a 18
articoli, conforme alla normativa.

| Step ID | Title                          | Pre-requisite                | Test Step description                                                          | Expected result                                                | Audience |
|---------|--------------------------------|------------------------------|---------------------------------------------------------------------------------|----------------------------------------------------------------|----------|
| 1       | Crea Offerta Discarica         | Opp + cliente con indirizzi  | Opp → New Quotation → tipo "Discarica" → cliente → Save                         | Offerta Discarica creata; sezioni Fanghi e Non Fanghi visibili | F        |
| 2       | Compila Allegato 2 produttori  | Cliente con > 1 indirizzo    | Sezione Allegato 2 → selezionare produttori da dropdown filtrato                | Solo indirizzi del cliente disponibili                         | F        |
| 3       | Aggiungi righe Fanghi          | Offerta Discarica            | Sezione Fanghi → aggiungere CER, HP, operazione, prezzo, minimo                 | Righe inserite con dati CER/HP                                  | F        |
| 4       | Aggiungi righe Non Fanghi      | Offerta Discarica            | Sezione Non Fanghi → aggiungere righe                                            | Righe in sezione corretta                                       | F        |
| 5       | Imposta fidejussione           | Offerta Discarica            | Toggle "Fidejussione richiesta" → importo + scadenza                            | Campo visibile in PDF                                           | F        |
| 6       | Genera PDF Discarica           | Offerta compilata             | Print → Offerta Discarica                                                       | PDF 18 articoli con sezioni Fanghi/Non Fanghi e Allegato 2     | F        |
| 7       | Filtro Allegato 2 per company  | Cliente B con suoi indirizzi  | Aprire offerta di cliente A → dropdown produttori                               | Solo indirizzi cliente A visibili (record rule)                 | T        |
| 8       | Vincolo CER + HP coerenti      | CER non pericoloso           | Inserire HP su CER non pericoloso                                                | Warning o blocco secondo configurazione                         | T        |

---

### Area TEA-D — Offerta Rifiuti Speciali (RS)

**Descrizione processo (intro foglio Funzionale)**:

L'offerta Rifiuti Speciali (RS) gestisce contratti di smaltimento dove
ogni riga rappresenta un CER smaltito presso uno specifico impianto.
Per ogni riga, Odoo precompila automaticamente prezzo, minimo fatturabile,
HP e operazione dal listino fornitore valido alla data dell'offerta.
Il commerciale può modificare uno fra **costo**, **markup 20%** o
**prezzo finale**: il sistema ricalcola automaticamente gli altri due
mantenendo coerenza. Il PDF RS è generato dinamicamente con i dati
specifici di ogni impianto.

| Step ID | Title                                  | Pre-requisite                  | Test Step description                                                          | Expected result                                                        | Audience |
|---------|----------------------------------------|--------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------|----------|
| 1       | Crea Offerta RS                        | Opp + listino fornitore        | Opp → New Quotation → tipo "RS" → cliente → Save                                | Offerta RS creata; sezione righe CER vuota                              | F        |
| 2       | Aggiungi riga CER da listino           | Listino fornitore con CER X    | Riga CER → selezionare CER + impianto                                            | Prezzo, minimo, HP e operazione precompilati dal listino               | F        |
| 3       | Modifica markup 20%                    | Riga con costo da listino      | Modificare markup → verificare prezzo finale                                     | Prezzo finale ricalcolato = costo × 1.20                                | F        |
| 4       | Modifica prezzo finale                 | Riga con costo da listino      | Modificare prezzo finale → verificare costo/markup                              | Sistema ricalcola markup; costo invariato                                | F        |
| 5       | rs_protocol auto-generato              | Offerta RS                     | Salvare offerta RS → verificare campo rs_protocol                                | Protocollo generato secondo sequence dedicata                            | F        |
| 6       | Upload PDF custom RS                   | Offerta RS                     | Upload PDF custom → verifica allegato                                            | PDF custom utilizzato per firma invece del template auto                | F        |
| 7       | Genera PDF RS standard                 | Offerta RS senza custom        | Print → Offerta RS                                                                | PDF con righe CER, impianto, prezzo                                     | F        |
| 8       | Listino scaduto → no precompilazione   | Listino con data fine < oggi   | Aggiungere riga CER da listino scaduto                                           | Sistema non precompila; warning di listino non valido                   | T        |
| 9       | Coerenza ricalcolo bidirezionale       | Riga con costo X               | Modificare ciclicamente costo/markup/prezzo                                      | Tutti e tre i valori sempre coerenti                                    | T        |
| 10      | Vincolo prezzi non negativi            | Offerta RS                     | Inserire prezzo o costo negativo                                                  | Save bloccato                                                            | T        |
| 11      | rs_protocol unique                     | -                              | Tentare duplicazione rs_protocol                                                 | Unique constraint blocca                                                 | T        |

---

### Area TEA-E — Workflow approvazione e firma TEA

**Descrizione processo (intro foglio Funzionale)**:

Tutte le offerte TEA (TMB, Discarica, RS) seguono lo stesso workflow:
bozza → richiesta approvazione → approvata → inviata al cliente → accettata
o rifiutata. La firma cliente avviene via Odoo Sign. L'approvazione interna
è necessaria sopra soglie definite. Una volta firmata, l'offerta diventa
contratto operativo e può essere convertita in Sale Order.

| Step ID | Title                                  | Pre-requisite                  | Test Step description                                                          | Expected result                                                        | Audience |
|---------|----------------------------------------|--------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------|----------|
| 1       | Stato draft → approval                 | Offerta bozza > soglia         | Request approval                                                                  | Stato → "approval"; approver notificato                                 | F        |
| 2       | Approva → approved                     | Offerta in approval            | Approver → Approve                                                                | Stato → "approved"; sblocca invio                                       | F        |
| 3       | Invio a cliente → sent                 | Offerta approved               | Send by email                                                                     | Stato → "sent"                                                          | F        |
| 4       | Accettazione cliente → accepted        | Offerta sent + firmata Sign    | Workflow firma completato                                                          | Stato → "accepted"                                                      | F        |
| 5       | Rifiuto cliente → refused_client       | Offerta sent                   | Cliente rifiuta firma                                                              | Stato → "refused_client"                                                | F        |
| 6       | Rifiuto approver → refused_approver    | Offerta in approval            | Approver → Refuse                                                                 | Stato → "refused_approver"; motivazione obbligatoria                    | F        |
| 7       | Conversione in Sale Order              | Offerta accepted               | Converti in SO                                                                     | SO creato con righe offerta                                             | F        |
| 8       | Transizioni stato non consentite       | Offerta draft                  | Tentare salto draft → sent                                                         | Bloccato; solo transizioni valide consentite                            | T        |

---

## Note d'uso

- I test case sono baseline. **Adattare wording, pre-requisite ed expected
  result al contesto cliente** (versione Odoo, configurazioni specifiche,
  dati di test reali).
- L'**Audience F/T** suggerita è un default. L'utente può sempre
  riclassificare in fase di intake.
- Per scenari custom o integrazioni (SAP, Tagetik, FINA Croazia, EDI/SDI),
  produrre test case **ad hoc** mantenendo la stessa struttura
  (descrizione processo + tabella con Audience).
- Le descrizioni di processo (intro) devono essere **specifiche del cliente**:
  non copiare letteralmente dal manuale Odoo. Estrarle dall'Analisi
  Funzionale del progetto.
