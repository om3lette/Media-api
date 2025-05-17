from pathlib import Path

from src.api.common.request_helpers import HelpersHandler

from src.api.common.enums import RequestProcessCodes
from src.api.common.schemas import MediaRequestSchema
from src.api.common.types.request import RequestType
from src.pipeline.render import Renderer
from src.pipeline.schemas.paths import PathsSchema

from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class BaseHandler:
    event_type: RequestType

    def __init__(self, event_type: RequestType):
        self.event_type = event_type

    def _build_renderer(
        self, actions: list[RequestType], raw_file_path: Path
    ) -> Renderer:
        raise NotImplementedError("No implementation provided for _build_renderer")

    async def handle(
        self, request: MediaRequestSchema, helpers: HelpersHandler, paths: PathsSchema
    ) -> RequestProcessCodes:
        logger.info("Building renderer for %s request", self.event_type)

        actions: list[RequestType] = []
        if "actions" in request.model_fields:
            actions = request.actions

        renderer: Renderer = self._build_renderer(actions, paths.raw_path)
        if renderer is None:
            logger.error("Unable to create renderer, exiting")
            return RequestProcessCodes.UNKNOWN_ERROR

        logger.info("Starting the renderer")
        await renderer.run(request.config, helpers, paths)

        return RequestProcessCodes.OK
