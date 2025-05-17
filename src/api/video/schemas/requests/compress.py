from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.app_config import app_config
from src.config.schemas.ffmpeg import FFMPEGProperties


class CompressConfig(FFMPEGProperties):
    pass


class CompressSchema(MediaRequestSchema):
    # extract_config() of BaseTask runs isinstance and expects CompressConfig
    # Without explicit convertion isinstance for default value will output FFMPEGProperties instead
    config: CompressConfig = Field(
        default=CompressConfig.model_validate(app_config.ffmpeg.model_dump())
    )
