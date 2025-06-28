from collections.abc import Awaitable, Callable

from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.types.render_config import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb

Preprocessor = Callable[
    [RenderConfig, HelpersHandler, StreamsSchema, PathsSchema, UpdateProgressCb],
    Awaitable[StreamsSchema],
]
