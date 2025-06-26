from collections.abc import Awaitable, Callable

from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.types.render_config import RenderConfig
from src.pipeline.types.state_callbacks import UpdateProgressCb

Postprocessor = Callable[
    [RenderConfig, HelpersHandler, StreamsSchema, PathsSchema, UpdateProgressCb],
    Awaitable[None],
]
