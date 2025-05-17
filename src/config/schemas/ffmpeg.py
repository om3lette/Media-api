from pydantic import Field

from src.config.enums import FfmpegPresets
from src.config.schemas.base_enum_model import BaseEnumModel
from src.config.schemas.codecs import CodecsSchema
from src.config.schemas.video import VideoSchema


class FFMPEGProperties(BaseEnumModel):
    preset: FfmpegPresets = Field(default=FfmpegPresets.VERYFAST)
    video: VideoSchema = Field(default_factory=VideoSchema)
    codecs: CodecsSchema = Field(default_factory=CodecsSchema)
