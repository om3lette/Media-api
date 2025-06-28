from pydantic import Field

from backend.src.config.enums import GigachatModels, GigachatModelScopes
from backend.src.config.schemas.base_enum_model import BaseEnumModel


class SummarySchema(BaseEnumModel):
    gigachat_api_token: str = Field(default="<YOUR_TOKEN>")
    model: GigachatModels = Field(default=GigachatModels.PRO)
    scope: GigachatModelScopes = Field(default=GigachatModelScopes.PERS)
