from pydantic import Field, BaseModel

from src.api.common.schemas import MediaRequestSchema


class TranscribeConfig(BaseModel):
    pass


class TranscribeSchema(MediaRequestSchema):
    config: TranscribeConfig = Field(default_factory=TranscribeConfig)
