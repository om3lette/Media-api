from pydantic import Field

from backend.src.api.common.schemas import MediaRequestSchema
from backend.src.api.common.schemas.requests.compress import CompressConfig
from backend.src.api.common.schemas.requests.extract_audio import ExtractAudioConfig
from backend.src.api.common.schemas.requests.summarize import SummarizeConfig
from backend.src.api.common.schemas.requests.transcribe import TranscribeConfig
from backend.src.api.common.types.request import CustomRequestActions


class CustomConfig(ExtractAudioConfig, SummarizeConfig, TranscribeConfig):
    ffmpeg: CompressConfig = Field(default_factory=CompressConfig)


class CustomSchema(MediaRequestSchema):
    config: CustomConfig = Field(default_factory=CustomConfig)
    actions: list[CustomRequestActions]
