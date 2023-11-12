from pydantic import (
	BaseModel, Field
)


class Synchronized_Line(BaseModel):
	lrcTimestamp: str
	line: str
	milliseconds: int
	duration: int


class Lyrics(BaseModel):
	id: str
	synchronized_lines: list[Synchronized_Line] | None = Field(validation_alias = 'synchronizedLines')
	text: str
	copyright: str | None
	writers: str | None