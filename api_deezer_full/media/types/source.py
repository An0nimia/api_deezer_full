from pydantic import BaseModel


class Source(BaseModel):
	url: str
	provider: str