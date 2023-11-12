from pydantic import (
	BaseModel, Field, ConfigDict
)


class Artist(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	id: str = Field(validation_alias = 'ART_ID')
	id_role: str = Field(validation_alias = 'ROLE_ID')
	name: str = Field(validation_alias = 'ART_NAME')
	picture_md5: str = Field(validation_alias = 'ART_PICTURE')
	rank: int = Field(validation_alias = 'RANK')


type Artists = list[Artist]