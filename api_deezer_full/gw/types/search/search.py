from typing import Annotated

from pydantic import (
	BaseModel, Field,
	ConfigDict, BeforeValidator
)

from ..track import Base_Track

from .album import Album
from .artist import Artist
from .playlist import Playlist


type Artists = Annotated[
	list[Artist], BeforeValidator(
		lambda data: data['data']
	)
]

type Albums = Annotated[
	list[Album], BeforeValidator(
		lambda data: data['data']
	)
]

type Tracks = Annotated[
	list[Base_Track], BeforeValidator(
		lambda data: data['data']
	)
]

type Playlists = Annotated[
	list[Playlist], BeforeValidator(
		lambda data: data['data']
	)
]


class Search(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name
	albums: Albums = Field(validation_alias = 'ALBUM')
	tracks: Tracks = Field(validation_alias = 'TRACK')
	artists: Artists = Field(validation_alias = 'ARTIST')
	playlists: Playlists = Field(validation_alias = 'PLAYLIST')
