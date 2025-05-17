from pydantic import BaseModel

from src.config.schemas.BaseEnumModel import BaseEnumModel

RenderConfig = BaseModel | BaseEnumModel
