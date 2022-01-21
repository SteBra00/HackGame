import json
import socket
from threading import Thread
from datetime import datetime
from typing import List



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

	def __init__(self, server, index:int, conn:socket.socket, addr:tuple) -> None:
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
				elif cmd.startswith('SIGNOUT'):
					SignOut.parse(self, cmd[6:])
				elif cmd.startswith('CHECK'):
					Check.parse(self, cmd[5:])
				elif cmd.startswith('ME'):
					Me.parse(self, cmd[2:])
				else:
					self.send(StatusCode.BAD_REQUEST)
		except ConnectionError:
			print(f'[{datetime.now()}] {self.addr} ConnectionError')
		except TimeoutError:
			print(f'[{datetime.now()}] {self.addr} TimeoutError')
		except Exception as e:
			print(f'[{datetime.now()}] {self.addr} {repr(e)}')
		finally:
			try:
				self.conn.close()
				self.server.remove(self.index)
			except Exception:
				pass
			print(f'[{datetime.now()}] {self.addr} EXITED')
			self.server.remove(self)
	
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
			except Exception:
				return host.send(StatusCode.BAD_REQUEST)
	
	@staticmethod
	def execute(host:Host, keys:List[str], users:List[str]) -> None:
		#FIXME assicurati di controllare che gli utenti richiesti esistano nel database (else: NOT_FOUND)
		print(f'GET\n\tkeys: {keys}\n\tusers: {users}')
		host.send(StatusCode.NOT_IMPLEMENTED)



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
			except Exception:
				return host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, keys:List[str], values:list, users:List[str]) -> None:
		#FIXME assicurati di controllare che gli utenti richiesti esistano nel database (else: NOT_FOUND)
		print(f'SET\n\tkeys: {keys}\n\tvaleus: {values}\n\tusers: {users}')
		host.send(StatusCode.NOT_IMPLEMENTED)


class SignUp:
	@staticmethod
	def parse(host:Host, args) -> None:
		try:
			args = args.split(' ')
			if len(args)==3:
				username, email, password = args
				SignUp.execute(host, username, email, password)
			else:
				host.send(StatusCode.BAD_REQUEST)
		except Exception:
			host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, username:str, email:str, password:str) -> None:
		print(f'username: {username}\nemail: {email}\npassword: {password}')
		host.send(StatusCode.NOT_IMPLEMENTED)
		#TODO Hash password
		#TODO verifica l'username e l'email
		#TODO Salva i dati nel database


class SignIn:
	@staticmethod
	def parse(host:Host, args) -> None:
		try:
			args = args.split(' ')
			if len(args)==2:
				username, password = args
				SignIn.execute(host, username, password)
			else:
				host.send(StatusCode.BAD_REQUEST)
		except Exception:
			host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host, username:str, password:str) -> None:
		print(f'username: {username}\npassword: {password}')
		host.send(StatusCode.NOT_IMPLEMENTED)
		#TODO Hash password
		#TODO Validate user
		#TODO edit host with relative authorizations


class SignOut:
	@staticmethod
	def parse(host:Host, args) -> None:
		try:
			if len(args)>1:
				host.send(StatusCode.BAD_REQUEST)
			else:
				SignOut.execute(host)
		except Exception:
			host.send(StatusCode.BAD_REQUEST)
		
	@staticmethod
	def execute(host:Host) -> None:
		host.send(StatusCode.NOT_IMPLEMENTED)
		#TODO remove authorizations from host
		#TODO close connection from server


class Check:
	@staticmethod
	def parse(host:Host, args) -> None:
		try:
			if len(args)>1:
				host.send(StatusCode.BAD_REQUEST)
			else:
				Check.execute(host)
		except Exception:
			host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host) -> None:
		host.send(StatusCode.NOT_IMPLEMENTED)


class Me:
	@staticmethod
	def parse(host:Host, args) -> None:
		try:
			if len(args)>1:
				host.send(StatusCode.BAD_REQUEST)
			else:
				Me.execute(host)
		except Exception:
			host.send(StatusCode.BAD_REQUEST)

	@staticmethod
	def execute(host:Host) -> None:
		host.send(StatusCode.NOT_IMPLEMENTED)



#TODO aggiungere il limite di host connessi
#FIXME aggiungere metodo "status"
class Server:
	def __init__(self, ip:str, port:int) -> None:
		self.name = 'HackerGameServer1'
		self.maxhost = 50
		self.numhost = 0

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

	def status(self, recipient:Host) -> None:
		try:
			data = {
				'name': self.name,
				'maxhost': self.maxhost,
				'numhost': self.numhost
			}
			recipient.send(StatusCode.OK, **data)
		except Exception:
			recipient.send(StatusCode.BAD_REQUEST)


	def remove(self, index:int) -> None:
		try:
			del self.hosts[index]
		except IndexError:
			print(f'[{datetime.now()}] Server.remove({index}) -> IndexError')


Server('127.0.0.1', 54321)
