from pydantic import Field

from src.config.enums import FfmpegPresets
from src.config.schemas.BaseEnumModel import BaseEnumModel
from src.config.schemas.codecs import CodecsSchema
from src.config.schemas.quality import QualitySchema


class FFMPEGProperties(BaseEnumModel):
    preset: FfmpegPresets = Field(default=FfmpegPresets.VERYFAST)
    quality: QualitySchema = Field(default_factory=QualitySchema)
    codecs: CodecsSchema = Field(default_factory=CodecsSchema)
    fps: int = Field(default=24)
