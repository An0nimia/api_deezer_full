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
	__ARL = 'af1bd8c14439541ed722aaee9b98f213632ca9a74ad93d379afe47711f7452dcbde84079d07bac961596e193e8aaae13e7b0f1c1ec9634c4e0b87f29e10e186acaef9ee7e4189f8ac93176648391313ea3ca60b1df07895fbfbe6f6bb963212e'
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
								format = 'MP3_128'
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


	def test_pipe_get_track_lyric(self):
		id_tracks = ('2326670385', '157596012', '424438852')
		results = (None, None, True)

		for i, id_track in enumerate(id_tracks):
			lyric = self.__api_pipe.pipe_get_track_lyric(id_track)

			assert lyric == results[i] if results[i] is None else lyric is not None
