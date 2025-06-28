from pydantic import Field

from backend.src.api.common.schemas import MediaRequestSchema
from backend.src.app_config import app_config
from backend.src.config.schemas.ffmpeg import FFMPEGProperties


class CompressConfig(FFMPEGProperties):
    pass


class CompressSchema(MediaRequestSchema):
    # extract_config() of BaseTask runs isinstance and expects CompressConfig
    # Without explicit convertion isinstance for default value will output FFMPEGProperties instead
    config: CompressConfig = Field(
        default=CompressConfig.model_validate(app_config.ffmpeg.model_dump())
    )
