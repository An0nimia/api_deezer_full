from pydantic import (
	BaseModel, Field, ConfigDict
)

from .track import Track


class Album(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	tracks: list[Track] = Field(validation_alias = 'data')
	id: str
	count: int
	total: int
	filtered_count: int