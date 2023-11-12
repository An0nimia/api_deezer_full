from typing import Any

from requests import post as req_post

from .types.medias import Medias
from .types.aliases import Media_Formats

from .exceptions import Insufficient_Rights


class API_Media:
	__API_MEDIA_URL = 'https://media.deezer.com/v1/get_url'

	@classmethod
	def get_medias_json(
		cls,
		license_token: str,
		media_formats: Media_Formats,
		track_tokens: list[str]
	) -> dict[str, Any]:

		json_data = {
			'license_token': license_token,
			'media': [
				media
				for media in media_formats
			],
			'track_tokens': track_tokens
		}


		res: dict[str, Any] = req_post(
			url = cls.__API_MEDIA_URL,
			json = json_data
		).json()

		errors = res.get('errors')

		if not errors is None:
			if errors[0]['code'] == 1002:
				raise Insufficient_Rights(
					msg = errors[0]['message'],
					resp = res,
					license_token = license_token
				)

		return res


	@classmethod
	def get_medias(
		cls,
		license_token: str, 
		media_formats: Media_Formats,
		track_tokens: list[str]
	) -> Medias:

		res = cls.get_medias_json(
			license_token, media_formats, track_tokens
		)

		return Medias.model_validate(res)