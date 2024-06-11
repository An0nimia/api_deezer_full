from pydantic import (
	BaseModel, Field, ConfigDict
)

from ..artist import Artists


class Album(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	id: str = Field(validation_alias = 'ALB_ID')
	title: str = Field(validation_alias = 'ALB_TITLE')
	picture_md5: str = Field(validation_alias = 'ALB_PICTURE')
	artists: Artists = Field(validation_alias = 'ARTISTS')
