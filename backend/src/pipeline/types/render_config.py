from pydantic import BaseModel

from backend.src.config.schemas.base_enum_model import BaseEnumModel

RenderConfig = BaseModel | BaseEnumModel
