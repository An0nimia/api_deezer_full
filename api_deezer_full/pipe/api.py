from jwt import decode #pyright: ignore [reportUnknownVariableType]
from typing import Any
from requests import Session

from ..gw import API_GW

from .grapql import queries
from .grapql.types import get_introspection

from .decorators import check_login

from .types import (
	Track, Album,
	Lyrics, Playlist
)


class API_PIPE(API_GW):
	__API_AUTH = 'https://auth.deezer.com/login/arl?jo=p&rto=c&i=c'
	__API_PIPE = 'https://pipe.deezer.com/api'


	def __init__(self, arl: str) -> None:
		super().__init__(arl)
		self.__session = Session()
		self.refresh_jwt()


	def refresh_jwt(self) -> None:
		self.refresh()
		resp = self._session.post(self.__API_AUTH).json()

		self.exp_jwt: int = decode(
			resp['jwt'],
			options = {
				'verify_signature': False
			}
		)['exp']

		self.jwt = resp['jwt']
		self.__session.headers['authorization'] = f'Bearer {self.jwt}'


	@check_login
	def pipe_make_req(self, params: dict[str, Any]) -> dict[str, Any]:
		resp = self.__session.post(
			url = self.__API_PIPE,
			json = params
		).json()

		return resp


	def dump_introspection(self) -> None:
		params = {
			'query': get_introspection()
		}

		res = self.pipe_make_req(params)

		self.write_log(res, 'introspection.json')


	def pipe_get_track_JSON(self, id_track: int | str) -> dict[str, Any]:
		"""

		Function for getting Track's infos in JSON format

		"""

		params = queries.get_track_query(id_track)

		return self.pipe_make_req(params)


	def pipe_get_track(self, id_track: int | str) -> Track:
		res = self.pipe_get_track_JSON(id_track)

		return Track.model_validate(res['data']['track'])


	def pipe_get_album_JSON(self, id_album: int | str) -> dict[str, Any]:
		"""

		Function for getting Album's infos in JSON format

		"""

		params = queries.get_album_query(id_album)

		return self.pipe_make_req(params)


	def pipe_get_album(self, id_album: int | str) -> Album:
		res = self.pipe_get_album_JSON(id_album)

		return Album.model_validate(res['data']['album'])


	def pipe_get_playlist_JSON(self, id_playlist: int | str) -> dict[str, Any]:
		"""

		Function for getting Playlist's infos in JSON format

		"""

		params = queries.get_playlist_query(id_playlist)

		return self.pipe_make_req(params)


	def pipe_get_playlist(self, id_playlist: int | str) -> Playlist:
		res = self.pipe_get_playlist_JSON(id_playlist)
		
		return Playlist.model_validate(res['data']['playlist'])


	def pipe_get_track_lyric_JSON(self, id_track: int | str) -> dict[str, Any]:
		params = queries.get_track_lyric_query(id_track)

		return self.pipe_make_req(params)


	def pipe_get_track_lyric(self, id_track: int | str) -> Lyrics | None:
		res = self.pipe_get_track_lyric_JSON(id_track)

		if not res['data']['track']['lyrics']:
			return

		return Lyrics.model_validate(res['data']['track']['lyrics'])


	def pipe_get_lyric_JSON(self, id_lyric: int | str) -> dict[str, Any]:
		params = queries.get_lyric_query(id_lyric)

		return self.pipe_make_req(params)


	def pipe_get_lyric(self, id_lyric: str) -> Lyrics:
		res = self.pipe_get_lyric_JSON(id_lyric)

		return Lyrics.model_validate(res['data']['lyrics'])


	def pipe_get_tracks(
		self,
		id_tracks: list[int | str],
		obj: bool = True
	) -> list[Track] | dict[str, Any]:

		res = self.pipe_make_req(
			queries.get_tracks_query(id_tracks)
		)

		if obj:
			res = {
				track['node']['id']: Track.model_validate(track['node'])				
				for track in res['data']['tracks']['edges']
			}

		return res
