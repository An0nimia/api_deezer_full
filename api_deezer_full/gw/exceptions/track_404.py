from typing import Any


class Error_404(Exception):
	def __init__(
		self,
		params: dict[str, Any],
		resp: dict[str, Any]
	) -> None:

		self.query = params
		self.resp = resp
		self.message = 'No Data found'

		super().__init__(self.message)
