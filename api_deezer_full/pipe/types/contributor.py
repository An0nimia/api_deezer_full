from typing import Annotated


from pydantic import (
	BaseModel, Field, BeforeValidator
)

from .artist import Artist


class Contributor(BaseModel):
	roles: list[str]
	artist: Artist = Field(validation_alias = 'node')


type Contributors = Annotated[
	list[Contributor], BeforeValidator(
		lambda data: data['edges']
	)
]