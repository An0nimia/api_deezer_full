from typing import TypedDict


class Format(TypedDict):
	cipher: str
	format: str


class Media_Format(TypedDict):
	type: str
	formats: list[Format]


type Media_Formats =  list[Media_Format]