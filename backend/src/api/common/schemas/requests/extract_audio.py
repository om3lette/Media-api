from pydantic import Field

from backend.src.api.common.schemas import MediaRequestSchema
from backend.src.app_config import app_config
from backend.src.config.enums import AudioCodecs
from backend.src.config.schemas.base_enum_model import BaseEnumModel


class AudioSettings(BaseEnumModel):
    codec: AudioCodecs = Field(default=app_config.ffmpeg.codecs.audio)
    bitrate: int = Field(default=app_config.ffmpeg.video.audio_bitrate)
    sample_rate: int = Field(default=app_config.ffmpeg.video.audio_sample_rate)


class ExtractAudioConfig(BaseEnumModel):
    audio: AudioSettings = Field(default_factory=AudioSettings)


class ExtractAudioSchema(MediaRequestSchema):
    config: ExtractAudioConfig = Field(default_factory=ExtractAudioConfig)
