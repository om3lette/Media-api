from pydantic import Field

from backend.src.api.common.schemas import MediaRequestSchema
from backend.src.app_config import app_config
from backend.src.config.enums import GigachatModels
from backend.src.config.schemas.base_enum_model import BaseEnumModel


class SummarizeSettings(BaseEnumModel):
    model: GigachatModels = Field(default=app_config.summary.model)


class SummarizeConfig(BaseEnumModel):
    summary: SummarizeSettings = Field(default_factory=SummarizeSettings)


class SummarizeSchema(MediaRequestSchema):
    config: SummarizeConfig = Field(default_factory=SummarizeConfig)
