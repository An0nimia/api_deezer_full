from typing import Any


class Error_404(Exception):
	def __init__(
		self,
		params: dict[str, Any],
		resp: dict[str, Any],
		id_media: str,
		type_media: str,
		link: str | None = None
	) -> None:

		self.query = params
		self.resp = resp
		self.id_media = id_media
		self.type_media = type_media
		self.link = link
		self.message = f'No Data found for type \'{self.type_media}\' with link \'{self.id_media}\''

		super().__init__(self.message)