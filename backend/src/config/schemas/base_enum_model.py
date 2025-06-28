from camel_converter import to_camel
from pydantic import BaseModel, ConfigDict


class BaseEnumModel(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        alias_generator=to_camel,
        validate_default=True,
        use_enum_values=True,
    )
