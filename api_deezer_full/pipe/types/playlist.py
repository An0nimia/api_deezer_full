from typing import Annotated

from datetime import datetime

from pydantic import (
	BaseModel, BeforeValidator, Field
)

from .track import Track
from .cover import Cover
from .artist import Artist


type Playlist_Track = Annotated[
	Track, BeforeValidator(
		lambda data: data['node']
	)
]


type Playlist_Tracks = Annotated[
	list[Playlist_Track], BeforeValidator(
		lambda data: data['edges']
	)
]


class Playlist(BaseModel):
	id: str
	title: str
	description: str | None
	is_private: bool = Field(validation_alias = 'isPrivate')
	is_collaborative: bool = Field(validation_alias = 'isCollaborative')
	is_charts: bool = Field(validation_alias = 'isCharts')
	is_blind_testable: bool = Field(validation_alias = 'isBlindTestable')
	is_from_favorite_tracks: bool = Field(validation_alias = 'isFromFavoriteTracks')
	is_editorialized: bool = Field(validation_alias = 'isEditorialized')
	artist: Artist | None = Field(validation_alias = 'linkedArtist')
	picture: Cover | None
	estimated_tracks_count: int = Field(validation_alias = 'estimatedTracksCount')
	estimated_duration: int = Field(validation_alias = 'estimatedDuration')
	creation_date: datetime = Field(validation_alias = 'creationDate')
	last_modification_date: datetime = Field(validation_alias = 'lastModificationDate')
	fans_count: int = Field(validation_alias = 'fansCount')
	tracks: Playlist_Tracks