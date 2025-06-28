from pydantic import Field

from backend.src.config.enums import AudioCodecs, VideoCodecs
from backend.src.config.schemas.base_enum_model import BaseEnumModel


class CodecsSchema(BaseEnumModel):
    video: VideoCodecs = Field(default=VideoCodecs.H264)
    audio: AudioCodecs = Field(default=AudioCodecs.MP3)
