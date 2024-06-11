from unittest import TestCase

from api_deezer_full.media.types.aliases import (
	Media_Format, Format
)

from api_deezer_full import (
	API_GW, API_Media, API_PIPE
)

from api_deezer_full.gw.types import (
	Track, Album
)


class GW_Test(TestCase):
	__ARL = "d1b59217b86abb231097b0fdd2b0e2e03304af8b9d25d9408c9c0cb9fb65a9536b131094fb65a27a5fb52658c518f865119bf6e7dc5a573ad0ac364feca3513c7b7dd332d59e2edc72b3711b306c39f5ac4cd8422ce33828009f50cf418af99b"
	__api = API_GW(__ARL)
	__api_pipe = API_PIPE(__ARL)
	__TRACKS = ('2825782592', '374251471')
	__ALBUMS = ('43274571',)

	def test_token_expire(self):
		self.__api.gw_search('eminem')
		self.__api.refresh()
		self.__api.gw_search('valeria stoica')


	def test_gw_track(self):
		for track in self.__TRACKS:
			res = self.__api.gw_get_track(track)
			Track.model_validate(res.model_dump())


	def test_gw_album(self):
		for album in self.__ALBUMS:
			res = self.__api.gw_get_album(album)
			Album.model_validate(res.model_dump())


	def test_get_media(self):
		for track in self.__TRACKS:
			gw_info = self.__api.gw_get_track(track)

			track_token = gw_info.track_token

			if gw_info.fallback:
				track_token = gw_info.fallback.track_token

			media_infos = API_Media.get_medias(
				license_token = self.__api.license_token,
				media_formats = [
					Media_Format(
						type = 'FULL',
						formats = [
							Format(
								cipher = 'BF_CBC_STRIPE',
								format = 'MP3_320'
							)
						]
					)
				],
				track_tokens = [track_token]
			)

			print(media_infos)


	def test_track_pipe(self):
		for track in self.__TRACKS:
			pipe_info = self.__api_pipe.pipe_get_track(track)
			print(pipe_info)


	def test_album_pipe(self):
		for album in self.__ALBUMS:
			pipe_info = self.__api_pipe.pipe_get_album(album)
			print(pipe_info)


	def test_dump_introspection(self):
		self.__api_pipe.dump_introspection()