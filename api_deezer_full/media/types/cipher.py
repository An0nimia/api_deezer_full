from pydantic import BaseModel


class Cipher(BaseModel):
	type: str