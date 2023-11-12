from typing import Any

from requests import Session

from json import dump as JSON_dump

from .exceptions import Arl_Invalid

from .types import (
	Track, Album, User, Playlist
)

from .decorators import (
	check_link, check_login
)


# https://e-cdn-files.dzcdn.net/cache/js/app-web.bb0399eb33362d783b36.js


class API_GW:
	__API_URL = 'https://www.deezer.com/ajax/gw-light.php' #?method=deezer.getUserData&input=3&api_version=1.0&api_token=&cid=465385533


	def __init__(self, arl: str) -> None:
		self.__arl = arl
		self._session = Session()
		self._session.cookies['arl'] = self.__arl
		self.refresh()


	def write_log(
		self,
		json: dict[str, Any], 
		path: str = 'out.json'
	) -> None:

		with open(path, 'w') as f:
			JSON_dump(json, f)


	@check_login
	def gw_make_req(
		self,
		method: str,
		json_data: dict[str, Any] | None = None
	) -> dict[str, Any]:

		match method:
			case 'deezer.getUserData':
				api_token = 'null'
			case _:
				api_token = self.token

		params = {
			'api_version': '1.0',
			'input': 3,
			'method': method,
			'api_token': api_token
		}

		resp = self._session.post(
			url = self.__API_URL,
			params = params,
			json = json_data
		).json()

		return resp


	@check_link(method = 'deezer.getUserData')
	def gw_get_user_data_JSON(self) -> dict[str, Any]:
		...


	def gw_get_user_data(self) -> User:
		raise NotImplementedError('Sorry obj serialization at the moment sucks')
		res = self.gw_get_user_data_JSON()


	def refresh(self) -> None:
		self.check_expire = False
		self.__set_tokens()
		self.check_expire = True


	def __set_tokens(self) -> None:
		user_data_json = self.gw_get_user_data_JSON()['results']
		self.id_user = user_data_json['USER']['USER_ID']

		if self.id_user == 0:
			raise Arl_Invalid(self.__arl)

		self.token: str = user_data_json['checkForm']
		self.license_token: str = user_data_json['USER']['OPTIONS']['license_token']
		self.exp_license_token: str = user_data_json['USER']['OPTIONS']['expiration_timestamp']


	def gw_get_track_lyric(self, id_track: int) -> dict[str, Any]:
		method = 'song.getLyrics'

		params = {
			'SNG_ID': id_track
		}

		return self.gw_make_req(method, params)


	@check_link(method = 'song.getData', type_media = 'track')
	def gw_get_track_JSON(self, id_track: str) -> dict[str, Any]:
		params = {
			'SNG_ID': id_track
		}

		return params


	def gw_get_track(self, link: str) -> Track:
		res = self.gw_get_track_JSON(link)

		return Track.model_validate(res['results'])


	def gw_get_tracks(self, id_tracks: list[int]) -> dict[str, Any]:
		method = 'song.getListData'

		params = {
			'sng_ids': id_tracks
		}

		return self.gw_make_req(method, params)


	@check_link(method = 'song.getListByAlbum', type_media = 'album')
	def gw_get_album_JSON(
		self,
		id_album: str,
		nb: int = -1,
		start: int = 0
	) -> dict[str, Any]:

		params = {
			'alb_id': id_album,
			'nb': nb,
			'start': start
		}

		return params


	def gw_get_album(
		self,
		id_album: str,
		nb: int = -1,
		start: int = 0
	) -> Album:
		res = self.gw_get_album_JSON(id_album, nb, start)

		return Album.model_validate(res['results'])


	@check_link(method = 'playlist.getSongs', type_media = 'playlist')
	def gw_get_playlist_JSON(
		self,
		id_playlist: str,
		nb: int = -1,
		start: int = 0
	) -> dict[str, Any]:

		params = {
			'playlist_id': id_playlist,
			'nb': nb,
			'start': start
		}

		return params


	def gw_get_playlist(
		self,
		id_playlist: str,
		nb: int = -1,
		start: int = 0
	) -> Playlist:

		res = self.gw_get_playlist_JSON(id_playlist, nb, start)

		return Playlist.model_validate(res['results'])


	@check_link(method = 'deezer.pageAlbum', type_media = 'album')
	def gw_get_page_album(
		self,
		id_album: int,
		lang: str = 'en'
	) -> dict[str, Any]:

		params = {
			'alb_id': id_album,
			'lang': lang
		}

		return params


	@check_link(method = 'deezer.pageSearch')
	def gw_search_JSON(
		self,
		query: str,
		start: int = 0,
		artist_suggest: bool = True,
		nb: int = 40,
		suggest: bool = True,
		top_tracks: bool = True
	) -> dict[str, Any]:

		params = {
			'query': query,
			'start': start,
			'nb': nb,
			'suggest' :suggest,
			'artist_suggest': artist_suggest,
			'top_tracks': top_tracks
		}

		return params