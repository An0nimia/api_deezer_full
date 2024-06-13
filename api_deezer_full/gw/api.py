from typing import Any

from requests import Session

from datetime import datetime

from logging import getLogger

from json import dump as JSON_dump

from .utils import check_errors
from .decorators import check_login
from .exceptions import Arl_Invalid

from .types import (
	Track, Album, User,
	Playlist, Search
)


# https://e-cdn-files.dzcdn.net/cache/js/app-web.bb0399eb33362d783b36.js


class API_GW:
	__API_URL = 'https://www.deezer.com/ajax/gw-light.php' #?method=deezer.getUserData&input=3&api_version=1.0&api_token=&cid=465385533
	logger = getLogger('API_DEEZER_FULL_GW')

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
				# trunk-ignore(bandit/B105)
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

		check_errors(params, json_data)
		self.logger.debug(resp)

		return resp


	def gw_get_user_data_JSON(self) -> dict[str, Any]:
		method = 'deezer.getUserData'

		return self.gw_make_req(method)


	def gw_get_user_data(self) -> User:
		raise NotImplementedError('Sorry obj serialization at the moment sucks')


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
		self.exp_token = datetime.now()
		self.license_token: str = user_data_json['USER']['OPTIONS']['license_token']

		self.exp_license_token: datetime = datetime.fromtimestamp(
			int(
				user_data_json['USER']['OPTIONS']['expiration_timestamp']
			)
		)


	def gw_get_track_lyric(self, id_track: int | str) -> dict[str, Any]:
		method = 'song.getLyrics'

		params = {
			'SNG_ID': id_track
		}

		return self.gw_make_req(method, params)


	def gw_get_track_JSON(self, id_track: int | str) -> dict[str, Any]:
		method = 'song.getData'

		params = {
			'SNG_ID': id_track
		}

		return self.gw_make_req(method, params)


	def gw_get_track(self, id_track: int | str) -> Track:
		res = self.gw_get_track_JSON(id_track)

		return Track.model_validate(res['results'])


	def gw_get_tracks(self, id_tracks: list[int | str]) -> dict[str, Any]:
		method = 'song.getListData'

		params = {
			'sng_ids': id_tracks
		}

		return self.gw_make_req(method, params)


	def gw_get_album_JSON(
		self,
		id_album: int | str,
		nb: int = -1,
		start: int = 0
	) -> dict[str, Any]:

		method = 'song.getListByAlbum'

		params = {
			'alb_id': id_album,
			'nb': nb,
			'start': start
		}

		return self.gw_make_req(method, params)


	def gw_get_album(
		self,
		id_album: int | str,
		nb: int = -1,
		start: int = 0
	) -> Album:
		res = self.gw_get_album_JSON(id_album, nb, start)

		return Album.model_validate(res['results'])


	def gw_get_playlist_JSON(
		self,
		id_playlist: int | str,
		nb: int = -1,
		start: int = 0
	) -> dict[str, Any]:

		method = 'playlist.getSongs'

		params = {
			'playlist_id': id_playlist,
			'nb': nb,
			'start': start
		}

		return self.gw_make_req(method, params)


	def gw_get_playlist(
		self,
		id_playlist: int | str,
		nb: int = -1,
		start: int = 0
	) -> Playlist:

		res = self.gw_get_playlist_JSON(id_playlist, nb, start)

		return Playlist.model_validate(res['results'])


	def gw_get_page_album_JSON(
		self,
		id_album: int | str,
		lang: str = 'en'
	) -> dict[str, Any]:

		method = 'deezer.pageAlbum'

		params = {
			'alb_id': id_album,
			'lang': lang
		}

		return self.gw_make_req(method, params)


	def gw_search_JSON(
		self,
		query: str,
		start: int = 0,
		artist_suggest: bool = True,
		nb: int = 40,
		suggest: bool = True,
		top_tracks: bool = True
	) -> dict[str, Any]:

		method = 'deezer.pageSearch'

		params = {
			'query': query,
			'start': start,
			'nb': nb,
			'suggest' :suggest,
			'artist_suggest': artist_suggest,
			'top_tracks': top_tracks
		}

		return self.gw_make_req(method, params)


	def gw_search(
		self,
		query: str,
		start: int = 0,
		artist_suggest: bool = True,
		nb: int = 25,
		suggest: bool = True,
		top_tracks: bool = True
	) -> Search:

		res = self.gw_search_JSON(
			query, start, artist_suggest,
			nb, suggest, top_tracks
		)

		return Search.model_validate(res['results'])
