from pydantic import (
	BaseModel, Field, ConfigDict
)

from .track import Base_Track


class Playlist(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	tracks: list[Base_Track] = Field(validation_alias = 'data')
	id: str
	count: int
	total: int
	checksum: str
	filtered_count: int