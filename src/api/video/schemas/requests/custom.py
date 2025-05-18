from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.compress import CompressConfig
from src.api.video.schemas.requests.extract_audio import ExtractAudioConfig
from src.api.video.schemas.requests.summarize import SummarizeConfig
from src.api.video.schemas.requests.transcribe import TranscribeConfig


class CustomConfig(ExtractAudioConfig, SummarizeConfig, TranscribeConfig):
    ffmpeg: CompressConfig = Field(default_factory=CompressConfig)


class CustomSchema(MediaRequestSchema):
    config: CustomConfig = Field(default_factory=CustomConfig)
    actions: list[VideoRequestType]
