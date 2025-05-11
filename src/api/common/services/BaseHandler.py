from pathlib import Path

from src.api.audio.enums import AudioRequestType
from src.api.common.schemas import MediaRequest

from src.api.common.enums import RequestProcessCodes
from src.api.common.utils import (
    out_path_from_request_id,
    request_data_dir_from_id,
    request_out_dir_from_id,
)
from src.api.video.enums import VideoRequestType
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


# TODO: Use RequestType - partially initialized module
class BaseHandler:
    event_type: VideoRequestType | AudioRequestType

    def __init__(self, event_type: VideoRequestType | AudioRequestType):
        self.event_type = event_type

    # FIXME Solve partially initialized module
    def _build_renderer(
        self,
        request: MediaRequest,
        helpers: "HelpersHandler",
        request_id: str,
        raw_file_path: Path,
    ) -> "Renderer":
        pass

    async def handle(
        self,
        request: MediaRequest,
        helpers: "HelpersHandler",
        request_id: str,
        raw_file_path: Path,
    ) -> RequestProcessCodes:
        logger.info(f"Building renderer for {self.event_type} request")
        renderer: "Renderer" = self._build_renderer(
            request, helpers, request_id, raw_file_path
        )
        if renderer is None:
            logger.error("Unable to create renderer, exiting")
            return RequestProcessCodes.UNKNOWN_ERROR

        logger.info("Starting the renderer")
        await renderer.run(
            request.config,
            request_data_dir_from_id(request_id),
            request_out_dir_from_id(request_id),
            out_path_from_request_id(request_id),
        )

        return RequestProcessCodes.OK
