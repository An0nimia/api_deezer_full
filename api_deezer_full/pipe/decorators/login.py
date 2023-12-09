from __future__ import annotations

from datetime import datetime

from collections.abc import Callable

from functools import update_wrapper

from typing import (
	Any, TYPE_CHECKING
)


if TYPE_CHECKING:
	from ..api import API_PIPE


def check_login(
	func: Callable[
		..., dict[str, Any]
	]
):
	def inner(self: API_PIPE, *args: ...) -> dict[str, Any]:
		d_time = datetime.fromtimestamp(self.exp_jwt)
		c_time = datetime.now()

		if c_time >= d_time:
			self.refresh_jwt()

		return func(self, *args)

	update_wrapper(inner, func)

	return inner