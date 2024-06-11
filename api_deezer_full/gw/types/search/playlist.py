from datetime import datetime

from pydantic import (
	BaseModel, Field, ConfigDict
)


type Playlist_Artists = list[Playlist_Artist]

class Playlist_Artist(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name
	id: str = Field(validation_alias = 'ART_ID')
	name: str = Field(validation_alias = 'ART_NAME')
	picture_md5: str = Field(validation_alias = 'ART_PICTURE')
	

class Playlist(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	id: str = Field(validation_alias = 'PLAYLIST_ID')
	id_parent: str = Field(validation_alias = 'PARENT_PLAYLIST_ID')
	title: str = Field(validation_alias = 'TITLE')
	id_user_parent: str = Field(validation_alias = 'PARENT_USER_ID')
	username_parent: str = Field(validation_alias = 'PARENT_USERNAME')
	username_picture_parent_md5: str = Field(validation_alias = 'PARENT_USER_PICTURE')
	picture_md5: str = Field(validation_alias = 'PLAYLIST_PICTURE')
	count: int = Field(validation_alias = 'NB_SONG')
	created: datetime = Field(validation_alias = 'DATE_ADD')
	modified: datetime = Field(validation_alias = 'DATE_MOD')

	artists: Playlist_Artists | None = Field(
		default = None,
		validation_alias = 'PLAYLIST_LINKED_ARTIST'
	)
