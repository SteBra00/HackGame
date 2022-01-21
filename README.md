# HackGame

## Elenco di cose da fare

### Front-end
- [ ] [Creare sito web](#info-sito-web)
- [ ] [Creare schermata iniziale](#info-schermata-iniziale)
- [ ] [Creare interfaccia creazione avatar](#info-interfaccia-creazione-avatar)
- [ ] [Creare interfaccia creazione pagina web](#info-interfaccia-creazione-pagina-web)
- [x] [Creare interfaccia ***Shell***](#info-interfaccia-shell)
- [x] [Creare interfaccia ***Room***](#info-interfaccia-room)
- [ ] [Creare interfaccia ***Web***](#info-interfaccia-web)
- [ ] [Creare interfaccia ***Group***](#info-interfaccia-group)
- [ ] [Creare interfaccia ***Option***](#info-interfaccia-option)

### Back-end
- [ ] Aquisto serve fisico
- [ ] Creare server
- [ ] Creare database
- [ ] Creare template per pagine web
- [ ] Creare rete virtuale

## Informazioni
### Linguaggi
- Python3 (Back-end, Front-end)
- SQL (Back-end)
- HTML5+CSS3 (Front-end)
- JavaScript (Front-end)

### Requisiti di sistema
- PyQt5
`python3 -m pip install PyQt5`

- PyQtWebEngine
`python3 -m pip install PyQtWebEngine`

- Qt_Matetial
`python3 -m pip install qt_matetial`


## Specifiche di progettazione
### Info Sito Web
#### Descrizione
Il sito è il principale mezzo di comunicazione con gli utenti non ancora presenti nel gioco;
E' fondamentale far si che gli utenti non possano inserire foto personali o template html propri, questo per il semplice motivo che un utente può camuffare un malware di qualsiasi tipo;
Per qualsiasi comunicazione, l'email sarà una remota possibilità: le email non sono un mezzo molto sicuro, pertanto sarebbe meglio evitare.

#### Operazioni possibili
- [ ] SignUp
- [ ] SignIn
- [ ] SignOut
- [ ] Collegamento al server discord
- [ ] Collegamento alla pagina social (Instagram, Facebook, ...)
- [ ] Visualizza e modifica i dati del profilo
- [ ] Visualizza i gruppi e gli altri utenti
- [ ] Visualizza condizioni del server
- [ ] Controlla/Scarica aggiornamenti
- [ ] Fornire un Feedback
- [ ] Segnala Bug
- [ ] [Crea avatar](#info-interfaccia-creazione-avatar)
- [ ] [Crea pagina web](#info-interfaccia-creazione-pagina-web)

### Info Schermata Iniziale
#### Descrizione
Semplice schermata per l'inizializzazione del gioco;
Il SignUp (registrazione nuovo utente) sarà possibile SOLO attraverso l'interfaccia web.

#### Operazioni possibili
- [ ] SignUp (Apri pagina web)
- [ ] SignIn

### Info Interfaccia Creazione Avatar
#### Descrizione
L'avatar è l'immagine profilo di ogni utente, quindi un maggiorn numero di elementi fornirà una personalizzazione più completa.

#### Operazioni possibili
- [ ] Scegli colore sfondo
- [ ] Scegli genere dell'avatar
- [ ] Scegli tipo di abbigliamento
- [ ] Scegli colore abbigliamento
- [ ] Scegli accessori capo
- [ ] Scegli accessori occhi
- [ ] Scegli accessori bocca
- [ ] Scegli accessori collo
- [ ] Scegli accessori schiena
- [ ] Salva Immagine

### Info interfaccia Creazione Pagina Web
#### Descrizione
La pagina web è il sito ufficiale appartenete all'utente in fase di gioco, se esso decide utilizzare uno dei suoi dispositivi digitali per fornire (simulazione) un servizio web.

#### Operazioni possibili
- [ ] Scegli template da usare
- [ ] Scegli titolo pagina
- [ ] Scegli sottotitolo pagina
- [ ] Scegli colore primario
- [ ] Scegli colore secondario
- [ ] Scegli colore di sfondo
- [ ] Salva template

### Info Interfaccia ***Shell***
#### Descrizione
L'interfaccia ***shell*** è la schemata principale del gioco, qui è possibile fare la maggiorparte delle operazioni del gioco, es. attacchi, attivazione/modifica/disattivazione servizi forniti agli utenti virtuali (simulazione), implementazioni malware/firewall/protocolli di criptazione o difesa, ...;

#### Operazioni possibili
- [x] Inserisci comandi
- [x] Visualizza l'output dei comandi lanciati
- [ ] Visualizza lista comandi possibili/non possibili/tutti
- [ ] Visualizza cronologia comandi eseguiti
- [ ] Visualizza comandi salvati

### Info Interfaccia ***Room***
#### Descrizione
Interfaccia dove sono posizionati i dispositivi digitali dell'utente.

#### Operazioni possibili
- [ ] Aggiungi/rimuovi dispositivo
- [ ] Modifica le caratteristiche hardware dei dispositivi
- [ ] Visualizza caratteristiche del dispositivo (durata, potenza, consumi, ...)

### Info Interfaccia ***Web***
#### Descrizione
Permette di interagire con gli altri utenti e con i lori servizi (simulazione).

#### Operazioni possibili
- [ ] Visualizza propria pagina web, se disponibile
- [ ] Visualizza locazione (simulazione) degli indirizzi IP (virtuali)
- [ ] Scegli persagli perl'hacking
- [ ] Visualizza targhet privilegiati
- [ ] Visualizza eventi
- [ ] Visualizza richieste pubbliche di soccordo (sia attaccanti che difensori)
- [ ] Visualizza sedi pubbliche di azziende o gruppi (quest'ultimi solo se aperti)

### Info Interfaccia ***Group***
#### Descrizione
Area di interazione con il proprio gruppo di appartenenza; un gruppo è come un clan o una gilda, con cui è possibile collaborare e/o interagire con i vari membri.

#### Operazioni possibili
- [ ] Visualizza lista globale dei gruppi aperti
- [ ] Crea un gruppo
- [ ] Pertecipa ad un gruppo
- [ ] Gestione e Modifica gruppo
- [ ] Chatta con i membri del gruppo
- [ ] Visualizza dati dei membri del gruppo
- [ ] Richiedi supporto d'attacco
- [ ] Richiedi supporto di difesa

### Info Interfaccia ***Option***
#### Descrizione
Gestione primaria del gioco, es. tema, SignOut, ...

#### Operazioni possibili
- [ ] Visualizza dati di diagnosi (durata sessione, stato server, IP reale, IPv4 virtuale, IPv6 virtuale, ...)
- [ ] Cambia tema e colorazione interfaccia utente
- [ ] Cancella cronologia web
- [ ] Cancella cronologia comandi
- [ ] SignOut
