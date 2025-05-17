from pydantic import BaseModel

from src.config.schemas.base_enum_model import BaseEnumModel

RenderConfig = BaseModel | BaseEnumModel
