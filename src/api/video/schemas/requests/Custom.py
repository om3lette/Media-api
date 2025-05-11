from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.Compress import CompressConfig
from src.api.video.schemas.requests.ExtractAudio import AudioSettings
from src.api.video.schemas.requests.Summarize import SummarizeSettings
from src.api.video.schemas.requests.Transcribe import TranscribeConfig
from src.config.schemas.BaseEnumModel import BaseEnumModel


class CustomConfig(BaseEnumModel):
    ffmpeg: CompressConfig = Field(default_factory=CompressConfig)
    audio: AudioSettings = Field(default_factory=AudioSettings)
    summary: SummarizeSettings = Field(default_factory=SummarizeSettings)
    transcribe: TranscribeConfig = Field(default_factory=TranscribeConfig)


class CustomSchema(MediaRequestSchema):
    config: CustomConfig = Field(default_factory=CustomConfig)
    actions: list[VideoRequestType]
