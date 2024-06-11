from typing import Any

from .exceptions import Error_404


def check_errors(
	params: dict[str, Any],
	json_data: dict[str, Any] | None,
) -> None:

	if not json_data:
		return

	is_error: list[dict[str, Any]] | None = json_data.get('errors')

	if is_error:
		is_type: str | None = is_error[0].get('type')

		match is_type:
			case 'TrackNotFoundError':
				raise Error_404(
					params = params,
					resp = json_data
				)
			case 'AlbumNotFoundError':
				raise Error_404(
					params = params,
					resp = json_data
				)
			case _:
				if 'The query exceeds' in is_error[0]['message']:
					raise Exception('To add')
				raise Exception(
					f'Error type \'{is_type}\' error is unknown. Message \'{is_error[0]['message']}\'. Report this kindly :)'
				)
