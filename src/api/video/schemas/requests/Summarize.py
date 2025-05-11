from pydantic import Field

from src.api.common.schemas import MediaRequestSchema
from src.app_config import app_config
from src.config.enums import GigachatModels
from src.config.schemas.BaseEnumModel import BaseEnumModel


class SummarizeSettings(BaseEnumModel):
    model: GigachatModels = Field(default=app_config.summary.model)


class SummarizeConfig(BaseEnumModel):
    summary: SummarizeSettings = Field(default_factory=SummarizeSettings)


class SummarizeSchema(MediaRequestSchema):
    config: SummarizeConfig = Field(default_factory=SummarizeConfig)
