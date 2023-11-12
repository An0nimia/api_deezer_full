from __future__ import annotations

from datetime import datetime

from pydantic import (
	BaseModel, Field
)

from .cover import Cover
from .media import Media
from .lyrics import Lyrics
from .disk_info import Disk_Info
from .contributor import Contributors


class Base_Album(BaseModel):
	id: str
	title: str = Field(validation_alias = 'displayTitle')
	cover: Cover | None
	label: str | None
	producer: str | None = Field(validation_alias = 'producerLine')
	copyright: str | None
	duration: int
	contributors: Contributors
	release_date: datetime = Field(validation_alias = 'releaseDate')
	fans_count: int = Field(validation_alias = 'fansCount')
	is_explicit: bool | None = Field(validation_alias = 'isExplicit')
	is_taken_down: bool = Field(validation_alias = 'isTakenDown')
	fallback: Base_Album | None
	disks_count: int = Field(validation_alias = 'discsCount')
	tracks_count: int = Field(validation_alias = 'tracksCount')


class Base_Track(BaseModel):
	id: str
	title: str
	ISRC: str | None
	disk_info: Disk_Info = Field(validation_alias = 'diskInfo')
	duration: int
	gain: float | None
	bpm: float | None
	popularity: float
	release_date: datetime = Field(validation_alias = 'releaseDate')
	contributors: Contributors
	is_explicit: bool | None = Field(validation_alias = 'isExplicit')
	lyrics: Lyrics | None
	media: Media | None
	is_favorite: bool | None = Field(validation_alias = 'isFavorite')
	is_banned_from_recommendation: bool | None = Field(validation_alias = 'isBannedFromRecommendation')