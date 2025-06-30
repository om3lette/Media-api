from pydantic import Field

from backend.src.config.schemas.base_enum_model import BaseEnumModel


class WebsocketsSchema(BaseEnumModel):
    no_progress_updates: bool = Field(default=False)
