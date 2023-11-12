from pydantic import (
	BaseModel, Field
)

from .cover import Cover


class Artist(BaseModel):
	id: str
	name: str
	fans_count: int = Field(validation_alias = 'fansCount')
	on_tour: bool = Field(validation_alias = 'onTour')
	status: str | None
	picture: Cover