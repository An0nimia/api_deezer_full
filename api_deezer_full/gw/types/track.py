from __future__ import annotations

from typing import Annotated

from datetime import (
	date, datetime
)

from pydantic import (
	BaseModel, ValidationInfo,
	BeforeValidator, ConfigDict,
	Field, field_validator
)

from .artist import Artists
from .contributor import Contributors


int_2_str = Annotated[
	str, BeforeValidator(
		lambda data: str(data)
	)
]


DEFAULT_DATE = datetime(1, 1, 1)
NO_DATE = '0000-00-00'

class Base_Track(BaseModel):
	model_config = ConfigDict(populate_by_name = True) # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.populate_by_name

	id_album: str = Field(validation_alias = 'ALB_ID')
	album_picture_md5: str = Field(validation_alias = 'ALB_PICTURE')
	album_title: str = Field(validation_alias = 'ALB_TITLE')
	artists: Artists = Field(validation_alias = 'ARTISTS')
	duration: int = Field(validation_alias = 'DURATION')
	hierarchical_title: str = Field(validation_alias = 'HIERARCHICAL_TITLE')
	ISRC: str
	id_lyric: int_2_str = Field(validation_alias = 'LYRICS_ID')

	rank: int | None = Field(
		default = None,
		validation_alias = 'RANK'
	)

	contributors: Contributors = Field(validation_alias = 'SNG_CONTRIBUTORS')
	id: str = Field(validation_alias = 'SNG_ID')
	title: str = Field(validation_alias = 'SNG_TITLE')
	track_number: int = Field(validation_alias = 'TRACK_NUMBER')

	version: str = Field(
		default = '',
		validation_alias = 'VERSION'
	)

	md5_origin: str = Field(validation_alias = 'MD5_ORIGIN')
	AAC_64: int = Field(validation_alias = 'FILESIZE_AAC_64')
	MP3_64: int = Field(validation_alias = 'FILESIZE_MP3_64')
	MP3_128: int = Field(validation_alias = 'FILESIZE_MP3_128')
	MP3_256: int = Field(validation_alias = 'FILESIZE_MP3_256')
	MP3_320: int = Field(validation_alias = 'FILESIZE_MP3_320')
	FLAC: int = Field(validation_alias = 'FILESIZE_FLAC')

	gain: float | None = Field(
		default = None,
		validation_alias = 'GAIN'
	)

	media_version: str = Field(validation_alias = 'MEDIA_VERSION')
	track_token: str = Field(validation_alias = 'TRACK_TOKEN')
	track_token_expire: datetime = Field(validation_alias = 'TRACK_TOKEN_EXPIRE')

	fallback: Base_Track | None = Field(
		default = None,
		validation_alias = 'FALLBACK'
	)


class Track(Base_Track):
	digital_release_date: date = Field(validation_alias = 'DIGITAL_RELEASE_DATE')
	disk_number: int = Field(validation_alias = 'DISK_NUMBER')
	id_genre: str = Field(validation_alias = 'GENRE_ID')
	physical_release_date: date = Field(validation_alias = 'PHYSICAL_RELEASE_DATE')
	status: int = Field(validation_alias = 'STATUS')

	fallback: Track | None = Field( # pyright: ignore [reportIncompatibleVariableOverride]
		default = None,
		validation_alias = 'FALLBACK'
	)


	@field_validator(
		'digital_release_date',
		'physical_release_date',
		mode = 'before'
	)
	@classmethod
	def check_dates(cls, date: date, info: ValidationInfo) -> date:
		if date == NO_DATE:
			date = DEFAULT_DATE

		return date