from typing import (
	Annotated, Any
)

from pydantic import (
	BaseModel, BeforeValidator
)

from .cipher import Cipher
from .source import Source


class _Media(BaseModel):
	media_type: str
	cipher: Cipher
	format: str
	sources: list[Source]
	nbf: float
	exp: float


def media_exist(media: dict[str, Any]) -> dict[str, Any] | None:
	is_media = media.get('media')

	if not is_media is None:
		is_media = is_media[0]

	return is_media


type Media = Annotated[
	_Media | None, BeforeValidator(
		media_exist
	)
]