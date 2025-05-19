from collections.abc import Callable, Awaitable

from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.types.render_config import RenderConfig


Job = Callable[
    [RenderConfig, HelpersHandler, StreamsSchema, PathsSchema], Awaitable[None]
]
