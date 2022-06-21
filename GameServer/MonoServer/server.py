"""
SERVER 0.3

La struttura del server è orientata ad oggetti:
Un oggetto centrale "server" gestisce le riechiesta di connessione dai vari client.
Per ogni client connesso al server, viene creata un oggetto "host" che itera con il metodo "run".
I metodi utilizzabili sono gestiti da classi specifiche, con metodo statici predefiniti:

class MethodName:
	METHOD = 'METHODNAME'
	VERSION = '0.0'
	COMMAND_VERSION = '0'
	COMMAND_SYNTAX = 'METHODNAME args'

	@staticmethod
	def parse(host:Host, args:str) -> None: ...

	@staticmethod
	def execute(host:Host [, ...]) -> None: ...

	@staticmethod
	def check() -> str: ...

	@staticmethod
	def help() -> str: ...

Dove "host" è l'oggetto che richiama il metodo in questione (self); args è il restante della stringa del comando richiesto dal client.
"execute" viene riciamato da "parse" una volta che esso ha effettuato i dovuti controlli e ha suddiviso i vari parametri del comando richiesto.

Ad ogni comando richiesto dal client, si provvede ad inviare il codice di stato, questi codici sono forniti dalla classe "utils.StatusCode"
che permette di convertire un codice in testo (es: 200 -> "ok" o 500 -> "Internal Error Server") e di valutare se un codice è "valido" o meno,
ovvero, se un codice è considerato "di successo" o "d'errore".

Le risposte alle richieste del client sono sempre inviate sottoforma di file json.
"""




#TODO utilizza la classe "serversocket" per il server.
#TODO [0.2] fai si che il metodo "host.run" non debba modificare la stringa "args", ma che la ritaglino su midura i singoli metodi "*.parse". Sistema poi la documentazione.
#TODO [0.3] gestione degli errori tramite "ERROR_MANUAL".
#TODO [1.0] aggiungi il metodo "check" e "help" alle classi dei comandi.
#TODO [2.0] Aggiorna le funzioni ai comandi v2.
#TODO [2.1] Aggiungi il metodo help nei vari comandi
#TODO [2.2] Aggiungi variabili standard dei metodi

#FIXME aggiungere il limite di host connessi.
#FIXME aggiungere metodo "status" che ritorna le condizioni del server.
#FIXME r.277, r.227 username -> id
#FIXME i metodi Help e Check non funzionano



import os
import sys
import json
import socket
import sqlite3
from pathlib import Path
from sqlite3 import Error
from threading import Thread
from datetime import datetime
#from Crypto.Cipher import AES
from passlib.hash import sha512_crypt
from typing import Any, Dict, List, Union




class DataBase: ...
class StatusCode: ...
class Host: ...
class Get: ...
class Set: ...
class SignUp: ...
class SignIn: ...
class SignOut: ...
class Check: ...
class Help: ...
class Server: ...




class DataBase:
	VERSION = '0.1'
	PATH = Path('sql', 'database.db').absolute().__str__()
	AES_KEY = 'hT.1dok903kaas:-21e23a'

	@staticmethod
	def selectQuery(query:str) -> Union[List, bool]:
		try:
			with sqlite3.connect(DataBase.PATH) as db:
				cursor = db.execute(query)
				values = cursor.fetchall()
				db.commit()
				return values
		except Error:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] DataBase.query({query}) Error')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')
			return False
	
	@staticmethod
	def updateQuery(query:str) -> bool:
		try:
			with sqlite3.connect(DataBase.PATH) as db:
				db.execute(query)
				db.commit()
				return True
		except Error:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] DataBase.query({query}) Error')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')
			return False

	@staticmethod
	def insertQuery(query:str) -> Union[int, bool]:
		try:
			with sqlite3.connect(DataBase.PATH) as db:
				cursor = db.execute(query)
				db.commit()
				return cursor.lastrowid
		except Error as e:
			print(e)
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
	ALL_KEYS = ['id', 'created_at', 'username', 'email', 'rank', 'team', 'bitcoins']

	def __init__(self, server:Server, index:int, conn:socket.socket, addr:tuple) -> None:
		self.server = server
		self.index = index
		self.conn = conn
		self.addr = addr[0]

		self.id = None
		self.username = None
		self.email = None
		self.isLogged = False
		self.isAuthorized = False
	
	def run(self):
		try:
			while True:
				cmd = self.conn.recv(4096).decode('utf-8')
				print(f'[{datetime.now()}] {self.addr} {cmd}')
				if cmd.startswith('GET'):
					Get.parse(self, cmd)
				elif cmd.startswith('SET'):
					Set.parse(self, cmd)
				elif cmd.startswith('SIGNUP'):
					SignUp.parse(self, cmd)
				elif cmd.startswith('SIGNIN'):
					SignIn.parse(self, cmd)
				elif cmd.startswith('SIGNOUT'):
					SignOut.parse(self, cmd)
				elif cmd.startswith('CHECK'):
					Check.parse(self, cmd)
				elif cmd.startswith('HELP'):
					Help.parse(self, cmd)
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
		print(responce) #<-------------------------------- DEBUG -------------
		self.conn.send(responce.encode('UTF-8'))

	@staticmethod
	def check() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)


class Get:
	METHOD = 'GET'
	VERSION = '1.0'
	COMMAND_VERSION = '1'
	COMMAND_SYNTAX = 'GET {ALL|key [key ...]} FROM {ME|user_id [user_id ...]}'

	@staticmethod
	def parse(host:Host, args:str) -> None:
		if not host.isAuthorized:
			return host.send(StatusCode.FORBIDDEN)
		else:
			try:
				args = args[4:]
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
					users.append(host.id)
				else:
					for element in u.split(' '):
						users.append(element)
				Get.execute(host, keys, users)
			except:
				return host.send(StatusCode.BAD_REQUEST)
	
	@staticmethod
	def execute(host:Host, keys:List[str], users:List[str]) -> None:
		total_result = dict()
		for user in users:
			result = DataBase.selectQuery(f'SELECT {str(keys)[1:-1]} FROM account WHERE id={user}')
			if result:
				if len(result)==1:
					total_result[user] = result
				elif len(result)<0:
					total_result[user] = (StatusCode.BAD_REQUEST, StatusCode.codeToString(StatusCode.BAD_REQUEST))
				else:
					total_result[user] = (StatusCode.BAD_REQUEST, StatusCode.codeToString(StatusCode.BAD_REQUEST))
					break
			else:
				total_result[user] = (StatusCode.NOT_FOUND, StatusCode.codeToString(StatusCode.NOT_FOUND))
		else:
			return host.send(StatusCode.OK, result=total_result)
		return host.send(StatusCode.INTERNAL_SERVER_ERROR, errno=2111)

	@staticmethod
	def check() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def help() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)


class Set:
	METHOD = 'SET'
	VERSION = '0.2'
	COMMAND_VERSION = '1'
	COMMAND_SYNTAX = 'SET key [key ...] TO value [value ...] FROM {ME|user_id [user_id ...]}'

	@staticmethod
	def parse(host:Host, args:str) -> None:
		if not host.isAuthorized:
			host.send(StatusCode.FORBIDDEN)
		else:
			try:
				args = args[4:]
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
					users.append(host.id)
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
	def execute(host:Host, keys:List[str], values:List[Any], users:List[str]) -> None:
		total_result = dict()
		for user in users:
			for k, v in zip(keys, values):
				result = DataBase.updateQuery(f'UPDATE account SET {k}="{v}" WHERE id={user}')
				if result:
					total_result[user] = (StatusCode.OK, StatusCode.codeToString(StatusCode.OK))
				else:
					total_result[user] = (StatusCode.NOT_FOUND, StatusCode.codeToString(StatusCode.NOT_FOUND))
		return host.send(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def check() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def help() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)


class SignUp:
	METHOD = 'SIGNUP'
	VERSION = '2.1'
	COMMAND_VERSION = '2'
	COMMAND_SYNTAX = 'SIGNUP username email password'

	@staticmethod
	def parse(host:Host, args:str) -> None:
		try:
			if host.isLogged:
				return host.send(StatusCode.FORBIDDEN)
			else:
				args = args[7:]
				username, email, password = args.split(' ')
				if username and email and password:
					SignUp.execute(host, username, email, password)
				else:
					return host.send(StatusCode.BAD_REQUEST)
		except:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, username:str, email:str, password:str) -> None:
		try:
			result = DataBase.selectQuery(f'SELECT * FROM account WHERE username="{username}" OR email="{email}"')
			if result!=False:
				if len(result)==0:
					password = sha512_crypt.using().hash(password)
					id = DataBase.insertQuery(f'INSERT INTO account (id, created_at, username, email, password, rank, bitcoins) VALUES ("1", "{datetime.now()}", "{username}", "{email}", "{password}", "1", "0.0")')
					if id!=False:
						host.id = id
						host.username = username
						host.email = email
						host.isLogged = True
						host.isAuthorized = True
						return host.send(StatusCode.OK)
					else:
						return host.send(StatusCode.INTERNAL_SERVER_ERROR, errno=3111)
				else:
					return host.send(StatusCode.ALREDY_USED)
			else:
				return host.send(StatusCode.INTERNAL_SERVER_ERROR, errno=3111)
		except:
			exc_type, _, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(f'[{datetime.now()}] {host.addr} Exception')
			print('\t{', f'{exc_type}, {fname}, {exc_tb.tb_lineno}', '}')
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def check() -> str:
		check_str = f'method: {SignUp.METHOD}\n'
		check_str += f'version: {SignUp.VERSION}\n'
		check_str += f'command version: {SignUp.COMMAND_VERSION}'
		return check_str

	@staticmethod
	def help() -> str:
		help_str = f'method: {SignUp.METHOD}\n'
		help_str = f'command version: {SignUp.COMMAND_VERSION}\n'
		help_str += f'sintax: {SignUp.COMMAND_SYNTAX}'
		return help_str


class SignIn:
	METHOD = 'SIGNIN'
	VERSION = '0.0'
	COMMAND_VERSION = '2'
	COMMAND_SYNTAX = 'SIGNIN email password'

	@staticmethod
	def parse(host:Host, args) -> None:
		return host.send(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def execute(host:Host, id:str, password:str) -> None:
		try:
			result = DataBase.selectQuery(f'SELECT username, email, password FROM account WHERE id="{id}"')
			if result:
				if len(result)==1:
					#FIXME controlla la correttezza della struttura della variabile
					username = result[0]['username']
					email = result[0]['email']
					hash_password = result[0]['password']
					if sha512_crypt.verify(password, hash_password):
						host.username = username
						host.email = email
						host.isLogged = True
						host.isAuthorized = True
					else:
						return host.send(StatusCode.NOT_FOUND)
				elif len(result)<1:
					return host.send(StatusCode.NOT_FOUND)
				else:
					return host.send(StatusCode.INTERNAL_SERVER_ERROR, errno=3211)
		except:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def check() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)

	@staticmethod
	def help() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)


class SignOut:
	METHOD = 'SIGNOUT'
	VERSION = '2.1'
	COMMAND_VERSION = '2'
	COMMAND_SYNTAX = 'SIGNOUT'

	@staticmethod
	def parse(host:Host, args:str) -> None:
		try:
			if host.isLogged:
				if args==SignOut.METHOD:
					SignOut.execute(host)
				else:
					return host.send(StatusCode.BAD_REQUEST)
			else:
				return host.send(StatusCode.FORBIDDEN)
		except:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host) -> None:
		try:
			host.id = None
			host.email = None
			host.username = None
			host.isLogged = False
			host.isAuthorized = False
		except:
			return host.send(StatusCode.BAD_REQUEST)
		else:
			return host.send(StatusCode.OK)

	@staticmethod
	def check() -> str:
		check_str = f'method: {SignOut.METHOD}\n'
		check_str += f'version: {SignOut.VERSION}\n'
		check_str += f'command version: {SignOut.COMMAND_VERSION}'
		return check_str

	@staticmethod
	def help() -> str:
		help_str = f'method: {SignOut.METHOD}\n'
		help_str = f'command version: {SignOut.COMMAND_VERSION}\n'
		help_str += f'sintax: {SignOut.COMMAND_SYNTAX}'
		return help_str


class Check:
	METHOD = 'CHECK'
	VERSION = '2.1'
	COMMAND_VERSION = '2'
	COMMAND_SYNTAX = 'CHECK {ALL|SERVER|DATABASE|GET|SET|SIGNUP|SIGNIN|SIGNOUT|CHECK}'

	@staticmethod
	def parse(host:Host, args:str) -> None:
		try:
			args = args.split(' ')
			if len(args)==2:
				Check.execute(host, args[1])
			else:
				return host.send(StatusCode.BAD_REQUEST)
		except:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, arg) -> None:
		if arg=='ALL':
			result = Server.check()+'\n'
			result += DataBase.check()+'\n'
			result += Get.check()+'\n'
			result += Set.check()+'\n'
			result += SignUp.check()+'\n'
			result += SignUp.check()+'\n'
			result += SignOut.check()+'\n'
			result += Check.check()+'\n'
			result += Help.check()
			return host.send(StatusCode.OK, result=result)
		elif arg=='SERVER':
			return host.send(Server.check())
		elif arg=='DATABASE':
			return host.send(DataBase.check())
		elif arg==Get.METHOD:
			return host.send(Get.check())
		elif arg==Set.METHOD:
			return host.send(Set.check())
		elif arg==SignUp.METHOD:
			return host.send(SignUp.check())
		elif arg==SignIn.METHOD:
			return host.send(SignUp.check())
		elif arg==SignOut.METHOD:
			return host.send(SignOut.check())
		elif arg==Check.METHOD:
			return host.send(Check.check())
		elif arg==Help.METHOD:
			return host.send(Help.check())
		else:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def check() -> str:
		check_str = f'method: {Check.METHOD}\n'
		check_str += f'version: {Check.VERSION}\n'
		check_str += f'command version: {Check.COMMAND_VERSION}'
		return check_str

	@staticmethod
	def help() -> str:
		help_str = f'method: {Check.METHOD}\n'
		help_str = f'command version: {Check.COMMAND_VERSION}\n'
		help_str += f'sintax: {Check.COMMAND_SYNTAX}'
		return help_str


class Help:
	METHOD = 'HELP'
	VERSION = '0.0'
	COMMAND_VERSION = '2'
	COMMAND_SYNTAX = 'HELP [{GET|SET|SIGNUP|SIGNIN|SIGNOUT|CHECK}]'

	@staticmethod
	def parse(host:Host, args:str) -> None:
		try:
			args = args.split(' ')
			if len(args)==2:
				Help.execute(host, args[1])
			else:
				return host.send(StatusCode.BAD_REQUEST)
		except:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, arg) -> None:
		if arg=='ALL':
			result = Get.help()+'\n'
			result += Set.help()+'\n'
			result += SignUp.help()+'\n'
			result += SignUp.help()+'\n'
			result += SignOut.help()+'\n'
			result += Check.help()+'\n'
			result += Help.help()
			return host.send(StatusCode.OK, result=result)
		elif arg==Get.METHOD:
			return host.send(Get.help())
		elif arg==Set.METHOD:
			return host.send(Set.help())
		elif arg==SignUp.METHOD:
			return host.send(SignUp.help())
		elif arg==SignIn.METHOD:
			return host.send(SignUp.help())
		elif arg==SignOut.METHOD:
			return host.send(SignOut.help())
		elif arg==Check.METHOD:
			return host.send(Check.help())
		elif arg==Help.METHOD:
			return host.send(Help.help())
		else:
			return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def check() -> str:
		check_str = f'method: {Help.METHOD}\n'
		check_str += f'version: {Help.VERSION}\n'
		check_str += f'command version: {Help.COMMAND_VERSION}'
		return check_str

	@staticmethod
	def help() -> str:
		help_str = f'method: {Help.METHOD}\n'
		help_str = f'command version: {Help.COMMAND_VERSION}\n'
		help_str += f'sintax: {Check.COMMAND_SYNTAX}'
		return help_str


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
	
	@staticmethod
	def check() -> str:
		return StatusCode.codeToString(StatusCode.NOT_IMPLEMENTED)


if __name__=='__main__':
	Server('127.0.0.1', 54321)