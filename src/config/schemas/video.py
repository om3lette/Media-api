from pydantic import Field

from src.config.schemas.base_enum_model import BaseEnumModel


class VideoSchema(BaseEnumModel):
    width: int = Field(default=1920)
    height: int = Field(default=1080)
    video_bitrate: int = Field(default=2500)
    audio_bitrate: int = Field(default=320)
    audio_sample_rate: int = Field(default=48000)
    fps: int = Field(default=24)
