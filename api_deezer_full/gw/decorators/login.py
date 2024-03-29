from __future__ import annotations

from datetime import datetime

from collections.abc import Callable

from functools import update_wrapper

from typing import (
	Any, TYPE_CHECKING
)


if TYPE_CHECKING:
	from ..api import API_GW


def check_login(
	func: Callable[
		..., dict[str, Any]
	]
):
	def inner(self: API_GW, *args: ...) -> dict[str, Any]:
		if self.check_expire:
			c_time = datetime.now()

			if c_time >= self.exp_license_token:
				self.refresh()

		return func(self, *args)

	update_wrapper(inner, func)

	return inner