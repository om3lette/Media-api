from collections.abc import Callable

from pydantic import BaseModel

from src.pipeline.types import RenderConfig, ExecuteMethod


class TaskWrapper(BaseModel):
    execute: ExecuteMethod
    extract_config: Callable[[RenderConfig], RenderConfig]

    class Config:
        arbitrary_types_allowed = True
