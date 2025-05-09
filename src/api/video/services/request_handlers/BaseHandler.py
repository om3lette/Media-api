import logging
import os

from pathlib import Path

from src import Renderer
from src.api.video.enums import VideoRequestType, VideoProcessCodes
from src.api.video.utils import out_path_from_request_id

logger = logging.getLogger(os.path.basename(__file__))

class BaseHandler:
    event_type: VideoRequestType

    def __init__(self, event_type: VideoRequestType):
        self.event_type = event_type

    # FIXME Solve partially initialized module
    def _build_renderer(self, helpers: "HelpersHandler", request_id: str, raw_file_path: Path) -> Renderer:
        pass

    async def handle(self, helpers: "HelpersHandler", request_id: str, raw_file_path: Path) -> VideoProcessCodes:
        logger.info(f"Building renderer for {self.event_type} request")
        renderer: Renderer = self._build_renderer(helpers, request_id, raw_file_path)
        if renderer is None:
            logger.error("Unable to create renderer, exiting")
            return VideoProcessCodes.UNKNOWN_ERROR

        logger.info(f"Starting the renderer")
        renderer.run(out_path_from_request_id(request_id))

        return VideoProcessCodes.OK
