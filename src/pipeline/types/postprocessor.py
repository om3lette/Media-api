from typing import Callable, Awaitable

from src.api.common.request_helpers import HelpersHandler
from src.pipeline.schemas.Paths import PathsSchema
from src.pipeline.schemas.Streams import StreamsSchema
from src.pipeline.types.render_config import RenderConfig


Postprocessor = Callable[
    [RenderConfig, HelpersHandler, StreamsSchema, PathsSchema], Awaitable[None]
]
