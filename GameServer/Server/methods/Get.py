if __name__=='__main__':
    exit()


from typing import List

from server.Host import Host
from utils.StatusCode import StatusCode


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
		pass