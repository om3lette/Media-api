from pydantic import Field, field_validator

from backend.src.config.enums import FfmpegPresets
from backend.src.config.schemas.base_enum_model import BaseEnumModel
from backend.src.config.schemas.codecs import CodecsSchema
from backend.src.config.schemas.video import VideoSchema


class FFMPEGProperties(BaseEnumModel):
    preset: FfmpegPresets = Field(default=FfmpegPresets.VERYFAST)
    video: VideoSchema = Field(default_factory=VideoSchema)
    codecs: CodecsSchema = Field(default_factory=CodecsSchema)

    @field_validator("preset", mode="before")
    @classmethod
    def to_lower(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value
