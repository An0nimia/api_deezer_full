from typing import Any


class Insufficient_Rights(Exception):
	def __init__(
		self,
		msg: str,
		resp: dict[str, Any],
		license_token: str
	) -> None:

		self.msg = msg
		self.license_token = license_token
		self.resp = resp
		self.message = f'Sorry the \'{self.license_token[:10]}...\' looks that isn\'t enought for the media requested it could depend on the quality you asked'

		super().__init__(self.message)