from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ProgressSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True, alias_generator=to_camel
    )

    cur_stage: int
    total_stages: int
    elapsed_time: int
    status: int
    pct: int
