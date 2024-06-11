from pydantic import (
	BaseModel, Field, ConfigDict
)


class Artist(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	id: str = Field(validation_alias = 'ART_ID')
	name: str = Field(validation_alias = 'ART_NAME')
	picture_md5: str = Field(validation_alias = 'ART_PICTURE')
	fans_count: int = Field(validation_alias = 'NB_FAN')
