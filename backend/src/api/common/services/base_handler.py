from pathlib import Path

from backend.src.api.common.enums import FileType, RequestProcessCodes
from backend.src.api.common.io_handlers import progress_handler
from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.api.common.schemas import MediaRequestSchema
from backend.src.api.common.types.request import GeneralRequestType
from backend.src.pipeline.render import Renderer
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


class BaseHandler:
    event_type: GeneralRequestType
    file_types: list[FileType]

    def __init__(self, event_type: GeneralRequestType, file_types: list[FileType]):
        self.event_type = event_type
        self.file_types = file_types

    def _build_renderer(self, actions: list, raw_file_path: Path) -> Renderer:
        raise NotImplementedError("No implementation provided for _build_renderer")

    async def handle(
        self,
        request_id: str,
        request: MediaRequestSchema,
        helpers: HelpersHandler,
        paths: PathsSchema,
    ) -> RequestProcessCodes:
        logger.info("Building renderer for %s request", self.event_type)

        actions: list[GeneralRequestType] = []
        if "actions" in request.model_fields:
            actions = request.actions

        renderer: Renderer = self._build_renderer(actions, paths.raw_path)
        if renderer is None:
            logger.error("Unable to create renderer, exiting")
            return RequestProcessCodes.UNKNOWN_ERROR

        await progress_handler.init_progress(request_id, renderer.stages)

        async def update_progress_wrapper(percentage: int = -1) -> None:
            await progress_handler.update_progress(request_id, percentage)

        async def update_stage_wrapper(stage: int) -> None:
            await progress_handler.update_stage(request_id, stage)

        logger.info("Starting the renderer")
        await renderer.run(
            request.config,
            helpers,
            paths,
            update_stage_wrapper,
            update_progress_wrapper,
        )

        return RequestProcessCodes.OK
