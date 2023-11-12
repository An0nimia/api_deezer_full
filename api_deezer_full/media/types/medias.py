from pydantic import (
	BaseModel, Field
)

from .media import Media


class Medias(BaseModel):
	medias: list[Media] = Field(validation_alias = 'data')