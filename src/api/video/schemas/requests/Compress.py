from pydantic import Field, BaseModel

from src.api.common.schemas import MediaRequestSchema
from src.app_config import app_config
from src.config.schemas.quality import QualitySchema


class CompressConfig(BaseModel):
    quality: QualitySchema = Field(default=app_config.ffmpeg.quality)

class CompressSchema(MediaRequestSchema):
    config: CompressConfig

