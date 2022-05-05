"""
SERVER

La struttura del server è orientata ad oggetti:
Un oggetto centrale "server" gestisce le riechiesta di connessione dai vari client.
Per ogni client connesso al server, viene creata un oggetto "host" che itera con il metodo "run".
I metodi utilizzabili sono gestiti da classi specifiche, con metodo statici predefiniti:

class MethodName:
	@staticmethod
	def parse(host:Host, args:str) -> None: ...

	@staticmethod
	def execute(host:Host [, ...]) -> None: ...

Dove "host" è l'oggetto che richiama il metodo in questione (self); args è il restante della stringa del comando richiesto dal client.
"execute" viene riciamato da "parse" una volta che esso ha effettuato i dovuti controlli e ha suddiviso i vari parametri del comando richiesto.

Ad ogni comando richiesto dal client, si provvede ad inviare il codice di stato, questi codici sono forniti dalla classe "utils.StatusCode"
che permette di convertire un codice in testo (es: 200 -> "ok" o 500 -> "Internal Error Server") e di valutare se un codice è "valido" o meno,
ovvero, se un codice è considerato "di successo" o "d'errore".

Le risposte alle richieste del client sono sempre inviate sottoforma di file json.
"""

#TODO utilizza la classe "serversocket" per il server
#TODO fai si che il metodo "host.run" non debba modificare la stringa "args", ma che la ritaglino su midura i singoli metodi "*.parse". Sistema poi la documentazione.

#FIXME aggiungere il limite di host connessi
#FIXME aggiungere metodo "status" che ritorna le condizioni del server


import socket
from threading import Thread
from datetime import datetime

from .Host import Host


class Server:
	def __init__(self, ip:str, port:int) -> None:
		self.ip = ip
		self.port = port
		self.hosts = list()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.ip, self.port))
		print(f'[{datetime.now()}] SERVER STARTED')
		self.sock.listen()
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f'[{datetime.now()}] {addr} ENTERED')
				host = Host(self, len(self.hosts), conn, addr)
				Thread(target=host.run).start()
				self.hosts.append(host)
			except Exception as e:
				print(repr(e))

	def remove(self, index:int) -> None:
		try:
			del self.hosts[index]
		except IndexError:
			print(f'[{datetime.now()}] Server.remove({index}) -> IndexError')