# https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/

from __future__ import annotations

from urllib.parse import urlparse

from functools import update_wrapper

from requests import get as req_get

from typing import (
	Any, TYPE_CHECKING
)

from ..exceptions.track_404 import Error_404

if TYPE_CHECKING:
	from ..api import API_PIPE


VALID_DOMAINS = (
	'deezer.page.link', 'deezer.com', 'api.deezer.com',
	'www.deezer.com',
)

NOT_VERIFY = VALID_DOMAINS[1:]

# https://book.pythontips.com/en/latest/decorators.html#decorators-with-arguments


def __check_errors(
	params: dict[str, Any],
	json_data: dict[str, Any],
	id_media: str,
	type_media: str,
	link: str
) -> None:

	#print(json_data)
	is_error: list[dict[str, Any]] | None = json_data.get('errors')

	if is_error:
		is_type: str | None = is_error[0].get('type')

		match is_type:
			case 'TrackNotFoundError':
				raise Error_404(
					params = params,
					resp = json_data,
					id_media = id_media,
					type_media = type_media,
					link = link
				)
			case 'AlbumNotFoundError':
				raise Error_404(
					params = params,
					resp = json_data,
					id_media = id_media,
					type_media = type_media,
					link = link
				)
			case _:
				if 'The query exceeds' in is_error[0]['message']:
					raise Exception('To add')
				raise Exception(
					f'Error type \'{is_type}\' error is unknown. Link \'{link}\' for media type \'{type_media}\'. Message \'{is_error[0]['message']}\'. Report this kindly :)')


def __get_id_media(link: str, type_media: str) -> str:
	url_parsed = urlparse(link)

	if 'deezer.page.link' == url_parsed.netloc:
		url = req_get(link).url
		url_parsed_new = urlparse(url)
		path = url_parsed_new.path
	elif url_parsed.netloc in NOT_VERIFY:
		path = url_parsed.path
	else:
		raise Exception(link, type_media)

	if not type_media in path:
		raise Exception(link, type_media)

	id_media = path.split('/')[-1]

	if not id_media.isdigit():
		raise Exception(link, type_media)

	return id_media


def check_link(type_media: str):
	def decorator(func: Any):
		def inner(self: API_PIPE, link: str) -> dict[str, Any]:
			if not link.isdigit():
				id_media = __get_id_media(link, type_media)
			else:
				id_media = link

			params = func(self, id_media)
			json_data = self.pipe_make_req(params)

			__check_errors(
				params = params,
				json_data = json_data,
				id_media = id_media,
				type_media = type_media,
				link = link
			)

			return json_data

		update_wrapper(inner, func) # https://docs.python.org/3/library/functools.html#functools.wraps

		return inner

	return decorator