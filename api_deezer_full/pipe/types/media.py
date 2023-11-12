from __future__ import annotations

from typing import Any

from pydantic import (
	BaseModel, model_validator, Field
)


class Estimated_Sizes(BaseModel):
	SBC_256: int | None
	AAC_64: int | None
	AAC_96: int | None
	MP3_MISC: int | None
	MP3_32: int | None
	MP3_64: int | None
	MP3_128: int | None
	MP3_192: int | None
	MP3_256: int | None
	MP3_320: int | None
	FLAC: int | None
	MP4_RA1: int | None
	MP4_RA2: int | None
	MP4_RA3: int | None
	DD_JOC: int | None
	AC4_IMS: int | None
	media_formats: list[str]


	@model_validator(mode = 'before')
	@classmethod
	def add_available_formats(cls, data: dict[str, Any]) -> dict[str, Any]:
		media_formats: list[str] = []

		for media_format, size in data.items():
			if size and size > 0:
				media_formats.append(media_format)			

		media_formats = ['MP3_128']
		data['media_formats'] = media_formats

		return data


class Token(BaseModel):
	payload: str
	expires_at: str = Field(validation_alias = 'expiresAt')


class Media(BaseModel):
	id: str
	version: str
	token: Token
	estimated_sizes: Estimated_Sizes = Field(validation_alias = 'estimatedSizes')