import json
import socket
from datetime import datetime

from .Server import Server

from utils.StatusCode import StatusCode

from methods.Get import Get
from methods.Set import Set
from methods.SignUp import SignUp
from methods.SignIn import SignIn
from methods.SignOut import SignOut
from methods.Check import Check


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