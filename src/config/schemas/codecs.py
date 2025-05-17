from pydantic import Field

from src.config.enums import AudioCodecs, VideoCodecs
from src.config.schemas.base_enum_model import BaseEnumModel


class CodecsSchema(BaseEnumModel):
    video: VideoCodecs = Field(default=VideoCodecs.H264)
    audio: AudioCodecs = Field(default=AudioCodecs.MP3)
