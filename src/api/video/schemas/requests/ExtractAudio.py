from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.app_config import app_config
from src.config.enums import AudioCodecs
from src.config.schemas.BaseEnumModel import BaseEnumModel

class AudioSettings(BaseEnumModel):
    codec: AudioCodecs = Field(default=app_config.ffmpeg.codecs.audio)
    bitrate: int = Field(default=app_config.ffmpeg.quality.audio_bitrate)
    sample_rate: int = Field(default=app_config.ffmpeg.quality.audio_sample_rate)

class ExtractAudioConfig(BaseEnumModel):
    audio: AudioSettings

class ExtractAudioSchema(MediaRequestSchema):
    config: ExtractAudioConfig
