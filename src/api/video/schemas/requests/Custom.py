from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.Compress import CompressConfig
from src.api.video.schemas.requests.ExtractAudio import AudioSettings
from src.api.video.schemas.requests.Summarize import SummarizeConfig
from src.api.video.schemas.requests.Transcribe import TranscribeConfig


class CustomConfig(AudioSettings, SummarizeConfig, TranscribeConfig):
    ffmpeg: CompressConfig = Field(default_factory=CompressConfig)


class CustomSchema(MediaRequestSchema):
    config: CustomConfig = Field(default_factory=CustomConfig)
    actions: list[VideoRequestType]
