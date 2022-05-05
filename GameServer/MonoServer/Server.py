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




import os
import sys
import json
import socket
import sqlite3
from pathlib import Path
from sqlite3 import Error
from threading import Thread
from datetime import datetime
from typing import Dict, List, Union




class DataBase: ...
class StatusCode: ...
class Host: ...
class Get: ...
class Set: ...
class SignUp: ...
class SignIn: ...
class SignOut: ...
class Check: ...
class Server: ...




class DataBase:
	""""""
	VERSION = '0.1'
	PATH = Path('sql', 'database.db').absolute().__str__()

	@staticmethod
	def query(query:str) -> Union[List, False]:
		try:
			with sqlite3.connect(DataBase.PATH) as db:
				cursor = db.execute(query)
				values = cursor.fetchall()
				db.commit()
				return values
		except Error as e:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] DataBase.query({query}) Error')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')
			return False
	
	@staticmethod
	def check() -> Dict[str, str]:
		return {
			'name': sqlite3.__name__,
			'version': sqlite3.version,
			'sql_version': sqlite3.sqlite_version,
			'api_level': sqlite3.apilevel,
			'parameter_style': sqlite3.paramstyle,
			'class_version': DataBase.VERSION
		}


class StatusCode:
	CODES = {
		200: 'Ok',
		400: 'Bad Request',
		401: 'Unauthorized',
		403: 'Forbidden',
		404: 'Not Found',
		410: 'Gone',
		450: 'Alredy Used',
		500: 'Internal Server Error',
		501: 'Not Implemented',
		503: 'Server Unavailable',
		510: 'Server Host Limit',
		511: 'Server Capience Limit'
	}
	OK = 200
	BAD_REQUEST = 400
	UNAUTHORIZED = 401
	FORBIDDEN = 403
	NOT_FOUND = 404
	GONE = 410
	ALREDY_USED = 450
	INTERNAL_SERVER_ERROR = 500
	NOT_IMPLEMENTED = 501
	SERVER_UNAVAILABLE = 503
	SERVER_HOST_LIMIT = 510
	SERVER_CAPIENCE_LIMIT = 511

	@staticmethod
	def codeToString(code:int) -> str:
		return StatusCode.CODES[code]

	@staticmethod
	def isValid(code:int) -> bool:
		if code==StatusCode.OK:
			return True
		return False


class Host:
	ALL_KEYS = ['id', 'username', 'email', 'rank', 'team', 'bitcoins', 'available_data']

	def __init__(self, server:Server, index:int, conn:socket.socket, addr:tuple) -> None:
		self.server = server
		self.index = index
		self.conn = conn
		self.addr = addr[0]
		self.username = 'Ste' #None
		self.email = 'ste@gmail.com' #None
		self.password = 'ste' #None
		self.isAuthorized = True #False
	
	def run(self):
		try:
			while True:
				cmd = self.conn.recv(4096).decode('utf-8')
				print(f'[{datetime.now()}] {self.addr} {cmd}')
				if cmd.startswith('GET '):
					Get.parse(self, cmd[4:])
				elif cmd.startswith('SET '):
					Set.parse(self, cmd[4:])
				elif cmd.startswith('SIGNUP '):
					SignUp.parse(self, cmd[7:])
				elif cmd.startswith('SIGNIN '):
					SignIn.parse(self, cmd[7:])
				elif cmd.startswith('SIGNOUT '):
					SignOut.parse(self, cmd[8:])
				elif cmd.startswith('CHECK '):
					Check.parse(self, cmd[6:])
				else:
					self.send(StatusCode.BAD_REQUEST)
		except ConnectionError:
			print(f'[{datetime.now()}] {self.addr} ConnectionError')
		except TimeoutError:
			print(f'[{datetime.now()}] {self.addr} TimeoutError')
		except:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] {self.addr} Exception')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')
		finally:
			try:
				self.conn.close()
				self.server.remove(self.index)
			except:
				pass
			print(f'[{datetime.now()}] {self.addr} EXITED')
	
	def send(self, status:int, *args, **kwargs) -> None:
		responce = {}
		responce['status_code'] = status
		responce['status_message'] = StatusCode.codeToString(status)
		if len(args)>0:
			responce['args'] = list(args)
		for k, v in kwargs.items():
			responce[k] = v
		responce = json.dumps(responce)
		print(responce) # <-------------------------------- DEBUG -------------
		self.conn.send(responce.encode('UTF-8'))


class Get:
	@staticmethod
	def parse(host:Host, args:str) -> None:
		if not host.isAuthorized:
			return host.send(StatusCode.FORBIDDEN)
		else:
			try:
				keys = list()
				users = list()
				k, u = args.split(' FROM ')
				if k=='ALL':
					for element in Host.ALL_KEYS:
						keys.append(element)
				else:
					for element in k.split(' '):
						if element in Host.ALL_KEYS:
							keys.append(element)
						else:
							return host.send(StatusCode.NOT_FOUND)
				if u=='ME':
					users.append(host.username)
				else:
					for element in u.split(' '):
						users.append(element)
				Get.execute(host, keys, users)
			except:
				return host.send(StatusCode.BAD_REQUEST)
	
	@staticmethod
	def execute(host:Host, keys:List[str], users:List[str]) -> None:
		#FIXME assicurati di controllare che gli utenti richiesti esistano nel database (else: NOT_FOUND)
		print(f'GET\n\tkeys: {keys}\n\tusers: {users}')
		return host.send(StatusCode.NOT_IMPLEMENTED)


class Set:
	@staticmethod
	def parse(host:Host, args) -> None:
		if not host.isAuthorized:
			host.send(StatusCode.FORBIDDEN)
		else:
			try:
				keys = list()
				values = list()
				users = list()
				k, v = args.split(' TO ')
				v, u = v.split(' FROM ')
				for element in k.split(' '):
					if element in Host.ALL_KEYS:
						keys.append(element)
					else:
						return host.send(StatusCode.NOT_FOUND)
				for element in v.split(' '):
					values.append(element)
				if u=='ME':
					users.append(host.username)
				else:
					for element in u.split(' '):
						users.append(element)
				if len(keys)==len(values):
					Set.execute(host, keys, values, users)
				else:
					host.send(StatusCode.BAD_REQUEST)
			except:
				return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, keys:List[str], values:list, users:List[str]) -> None:
		#FIXME assicurati di controllare che gli utenti richiesti esistano nel database (else: NOT_FOUND)
		print(f'SET\n\tkeys: {keys}\n\tvaleus: {values}\n\tusers: {users}')
		return host.send(StatusCode.NOT_IMPLEMENTED)


class SignUp:
	@staticmethod
	def parse(host:Host, args) -> None:
		return host.send(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def execute(host:Host) -> None: #FIXME aggiungi le specifiche per il comando
		return host.send(StatusCode.NOT_IMPLEMENTED)


class SignIn:
	@staticmethod
	def parse(host:Host, args) -> None:
		return host.send(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def execute(host:Host) -> None: #FIXME aggiungi le specifiche per il comando
		return host.send(StatusCode.NOT_IMPLEMENTED)


class SignOut:
	@staticmethod
	def parse(host:Host, args) -> None:
		return host.send(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def execute(host:Host) -> None: #FIXME aggiungi le specifiche per il comando
		return host.send(StatusCode.NOT_IMPLEMENTED)


class Check:
	@staticmethod
	def parse(host:Host, args) -> None:
		return host.send(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def execute(host:Host) -> None: #FIXME aggiungi le specifiche per il comando
		return host.send(StatusCode.NOT_IMPLEMENTED)


class Server:
	"""v: 0.2
	* Risolto errori in "remove()"
	* Aggiunto try-except
	* Aggioranto metodologia di stampa degli errori #TODO fallo su tutte le classi
	"""

	VERSION = '0.2'
	MAX_HOST = 250

	def __init__(self, ip:str, port:int) -> None:
		try:
			self.ip = ip
			self.port = port
			self.hosts = list()
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((self.ip, self.port))
			print(f'[{datetime.now()}] SERVER STARTED')
			self.sock.listen()
		except:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] Server.__init__({ip}, {port}) -> Exception')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')
			input()
			exit()

		while True:
			try:
				conn, addr = self.sock.accept()
				print(f'[{datetime.now()}] {addr} ENTERED')
				host = Host(self, len(self.hosts), conn, addr)
				Thread(target=host.run).start()
				self.hosts.append(host)
			except:
				exc_type, _, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(f'[{datetime.now()}] Server.__init__({ip}, {port}).while -> Exception')
				print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')

	def remove(self, index:int) -> None:
		try:
			del self.hosts[index]
		except IndexError:
			print(f'[{datetime.now()}] Server.remove({index}) -> IndexError')
		except:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] Server.remove({index}) -> Exception')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')


if __name__=='__main__':
	Server('127.0.0.1', 54321)
