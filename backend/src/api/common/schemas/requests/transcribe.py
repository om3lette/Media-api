from pydantic import BaseModel, Field

from backend.src.api.common.enums import TranscribeLanguages
from backend.src.api.common.schemas import MediaRequestSchema


class TranscribeSettings(BaseModel):
    language: TranscribeLanguages = Field(default=TranscribeLanguages.AUTO)


class TranscribeConfig(BaseModel):
    transcribe: TranscribeSettings = Field(default_factory=TranscribeSettings)


class TranscribeSchema(MediaRequestSchema):
    config: TranscribeConfig = Field(default_factory=TranscribeConfig)
