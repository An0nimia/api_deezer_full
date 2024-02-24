from typing import Any


class Bad_Credentials(Exception):
	def __init__(
		self,
		res: dict[str, Any],
		username: str,
		msg: str = 'Sorry the credentials for {} are wrong'
	) -> None:

		self.res = res

		for error, msg_error in self.res['error'].items():
			self.error = error
			self.msg_error = msg_error

		super().__init__(
			msg.format(username)
		)