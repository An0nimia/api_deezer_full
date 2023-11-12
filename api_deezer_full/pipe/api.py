from typing import Any

from requests import Session

from jwt import decode

from ..gw import API_GW

from .decorators import (
	check_link, check_login
)

from .grapql import queries
from .grapql.types import get_introspection

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


	@check_link(type_media = 'track')
	def pipe_get_track_JSON(self, id_track: str) -> dict[str, Any]:
		'''

		Function for getting Track's infos in JSON format

		'''

		return queries.get_track_query(id_track)


	def pipe_get_track(self, link: str) -> Track:
		res = self.pipe_get_track_JSON(link)

		return Track.model_validate(res['data']['track'])


	@check_link(type_media = 'album')
	def pipe_get_album_JSON(self, id_album: str) -> dict[str, Any]:
		'''

		Function for getting Album's infos in JSON format

		'''

		return queries.get_album_query(id_album)


	def pipe_get_album(self, link: str) -> Album:
		res = self.pipe_get_album_JSON(link)

		return Album.model_validate(res['data']['album'])


	@check_link(type_media = 'playlist')
	def pipe_get_playlist_JSON(self, id_playlist: str) -> dict[str, Any]:
		'''

		Function for getting Playlist's infos in JSON format

		'''

		return queries.get_playlist_query(id_playlist)


	def pipe_get_playlist(self, link: str) -> Playlist:
		res = self.pipe_get_playlist_JSON(link)
		
		return Playlist.model_validate(res['data']['playlist'])


	@check_link(type_media = 'track_lyric')
	def pipe_get_track_lyric_JSON(self, id_track: str) -> dict[str, Any]:
		return queries.get_track_lyric_query(id_track)


	def pipe_get_track_lyric(self, id_track: str) -> Lyrics:
		res = self.pipe_get_track_lyric_JSON(id_track)

		return Lyrics.model_validate(res['data']['track']['lyrics'])


	def pipe_get_lyric_JSON(self, id_lyric: str) -> dict[str, Any]:
		params = queries.get_lyric_query(id_lyric)

		return self.pipe_make_req(params)


	def pipe_get_lyric(self, id_lyric: str) -> Lyrics:
		res = self.pipe_get_lyric_JSON(id_lyric)

		return Lyrics.model_validate(res['data']['lyrics'])


	def pipe_get_tracks(
		self,
		id_tracks: list[str],
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