from pydantic import Field

from src.config.enums import GigachatModels, GigachatModelScopes
from src.config.schemas.base_enum_model import BaseEnumModel


class SummarySchema(BaseEnumModel):
    gigachat_api_token: str = Field(default="<YOUR_TOKEN>")
    model: GigachatModels = Field(default=GigachatModels.PRO)
    scope: GigachatModelScopes = Field(default=GigachatModelScopes.PERS)
