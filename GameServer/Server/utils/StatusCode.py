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