from typing import Any

from requests import post as req_post

from .types.medias import Medias
from .types.aliases import Media_Formats

from .exceptions import Insufficient_Rights


class API_Media:
	__API_MEDIA_URL = 'https://media.deezer.com/v1/get_url'
	__DEFAULT_MAX_X_MEDIA = 250


	@classmethod
	def __get_medias(
		cls,
		license_token: str,
		media_formats: Media_Formats,
		track_tokens: list[str]
	) -> dict[str, Any]:

		json_data = {
			'license_token': license_token,
			'media': media_formats,
			'track_tokens': track_tokens
		}

		res: dict[str, Any] = req_post(
			url = cls.__API_MEDIA_URL,
			json = json_data
		).json()

		return res


	@classmethod
	def __get_medias_all(
		cls,
		license_token: str,
		tracks_token: list[str],
		media_formats: Media_Formats,
		n_tracks: int,
		medias: dict[str, Any]
	) -> dict[str, Any]:

		for a in range(0, n_tracks, cls.__DEFAULT_MAX_X_MEDIA):
			medias += cls.__get_medias(
				license_token = license_token,
				media_formats = media_formats[a:a + cls.__DEFAULT_MAX_X_MEDIA],
				track_tokens = tracks_token[a:a + cls.__DEFAULT_MAX_X_MEDIA]
			)['data']		

		return medias


	@classmethod
	def get_medias_json(
		cls,
		license_token: str,
		media_formats: Media_Formats,
		track_tokens: list[str],
		saiyan: bool = True
	) -> dict[str, Any]:

		n_tracks = len(track_tokens)

		if n_tracks <= cls.__DEFAULT_MAX_X_MEDIA:
			i = n_tracks
		else:
			i = cls.__DEFAULT_MAX_X_MEDIA

		res = cls.__get_medias(
			license_token = license_token,
			media_formats = media_formats[:i],
			track_tokens = track_tokens[:i]
		)

		errors = res.get('errors')

		if not errors is None:
			if errors[0]['code'] == 1002:
				raise Insufficient_Rights(
					msg = errors[0]['message'],
					resp = res,
					license_token = license_token
				)

		if saiyan and n_tracks > cls.__DEFAULT_MAX_X_MEDIA:
			cls.__get_medias_all(
				license_token = license_token,
				tracks_token = track_tokens[cls.__DEFAULT_MAX_X_MEDIA:],
				media_formats = media_formats[cls.__DEFAULT_MAX_X_MEDIA:],
				n_tracks = (n_tracks - cls.__DEFAULT_MAX_X_MEDIA),
				medias = res['data']
			)

		return res


	@classmethod
	def get_medias(
		cls,
		license_token: str, 
		media_formats: Media_Formats,
		track_tokens: list[str],
		saiyan: bool = True
	) -> Medias:

		res = cls.get_medias_json(
			license_token = license_token,
			media_formats = media_formats,
			track_tokens = track_tokens,
			saiyan = saiyan
		)

		return Medias.model_validate(res)