from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ProgressSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True, alias_generator=to_camel
    )

    rid: str
    cur_stage: int = Field(default=-1)
    total_stages: int = Field(default=-1)
    elapsed_time: int
    status: int
    pct: int = Field(default=0)
