if __name__=='__main__':
    exit()


from typing import List

from server.Host import Host
from utils.StatusCode import StatusCode


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
		pass