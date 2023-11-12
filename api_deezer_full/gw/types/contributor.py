from typing import Annotated


from pydantic import (
	BaseModel, BeforeValidator
)


class Contributor(BaseModel):
	role: str
	name: str


def __create_contributors(data: dict[
	str, list[str]
]) -> list[Contributor]:

	contributors: list[Contributor] = []

	if data and type(data) is dict:
		for role, names in data.items():
			for name in names:
				contributors.append(
					Contributor(
						role = role,
						name = name
					)
				)
	else:
		for contributor in data:
			contributors.append(
				Contributor.model_validate(contributor)
			)

	return contributors

type Contributors = Annotated[
	list[Contributor], BeforeValidator(
		__create_contributors
	)
]