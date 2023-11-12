from pydantic import (
	BaseModel, Field
)


class Disk_Info(BaseModel):
	disk_number: int = Field(validation_alias = 'diskNumber')
	track_number: int = Field(validation_alias = 'trackNumber')