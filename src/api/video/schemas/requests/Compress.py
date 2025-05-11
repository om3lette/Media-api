from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.app_config import app_config
from src.config.schemas.ffmpeg import FFMPEGProperties


class CompressConfig(FFMPEGProperties):
    pass


class CompressSchema(MediaRequestSchema):
    config: CompressConfig = Field(default=app_config.ffmpeg)
