from typing import Annotated

from pydantic import BeforeValidator

from .bases import (
	Base_Track, Base_Album
)


type Album_Track = Annotated[
	Base_Track, BeforeValidator(
		lambda data: data['node']
	)
]


type Album_Tracks = Annotated[
	list[Album_Track], BeforeValidator(
		lambda data: data['edges']
	)
]


class Album(Base_Album):
	tracks: Album_Tracks