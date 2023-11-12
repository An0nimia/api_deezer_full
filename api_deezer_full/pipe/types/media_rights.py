from datetime import datetime

from pydantic import (
	BaseModel, Field
)


class Ads_Rights(BaseModel):
	available: bool
	available_after: datetime = Field(validation_alias = 'availableAfter')


class Sub_Rights(BaseModel):
	available: bool
	available_after: datetime = Field(validation_alias = 'availableAfter')


class Upload_Rights(BaseModel):
	available: bool


class Media_Rights(BaseModel):
	ads: Ads_Rights
	sub: Sub_Rights
	upload: Upload_Rights