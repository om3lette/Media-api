from pydantic import BaseModel


class BaseEnumModel(BaseModel):
    class Config:
        validate_default = True
        use_enum_values = True
