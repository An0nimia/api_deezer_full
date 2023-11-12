from pydantic import BaseModel


class Cover(BaseModel):
	url: list[str]