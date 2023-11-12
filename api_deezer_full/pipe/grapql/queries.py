from typing import Any

from .types import (
	get_track, get_album,
	get_lyric, get_track_edges, get_playlist
)


def get_track_query(id_track: str) -> dict[str, Any]:
	params = {
		'operationName': 'get_track',
		'variables': {
			'id_track': id_track,
		},
		'query': (
			f'''
				query get_track($id_track: String!) {{
					track(trackId: $id_track) {{
						{
							get_track()
						}
					}}
				}}
			'''
		)
	}

	return params


def get_album_query(id_album: str) -> dict[str, Any]:
	params = {
		'operationName': 'get_album',
		'variables': {
			'id_album': id_album,
		},
		'query': (
			f'''
				query get_album($id_album: String!) {{
					album(albumId: $id_album) {{
						{
							get_album()
						}
					}}
				}}
			'''
		)
	}

	return params


def get_track_lyric_query(id_track: str) -> dict[str, Any]:
	params = {
		'operationName': 'get_track_lyric',
		'variables': {
			'id_track': id_track,
		},
		'query': (
			f'''
				query get_track_lyric($id_track: String!) {{
					track(trackId: $id_track) {{
						lyrics {{
							{
								get_lyric()
							}
						}}
					}}
				}}
			'''
		)
	}

	return params


def get_tracks_query(id_tracks: list[str]) -> dict[str, Any]:
	params = {
		'operationName': 'get_tracks',
		'variables': {
			'id_tracks': id_tracks,
		},
		'query': (
			f'''
				query get_tracks($id_tracks: [String!]) {{
					tracks(trackIds: $id_tracks) {{
						{
							get_track_edges()
						}
					}}
				}}
			'''
		)
	}

	return params


def get_playlist_query(id_playlist: str) -> dict[str, Any]:
	params = {
		'operationName': 'get_playlist',
		'variables': {
			'id_playlist': id_playlist,
		},
		'query': (
			f'''
				query get_playlist($id_playlist: String!) {{
					playlist(playlistId: $id_playlist) {{
						{
							get_playlist()
						}
					}}
				}}
			'''
		)
	}

	return params


def get_lyric_query(id_lyric: str) -> dict[str, Any]:
	params = {
		'operationName': 'get_lyric',
		'variables': {
			'id_lyric': id_lyric,
		},
		'query': (
			f'''
				query get_lyric($id_lyric: String!) {{
					lyrics(lyricsId: $id_lyric) {{
						{
							get_lyric()
						}
					}}
				}}
			'''
		)
	}

	return params