import os
import logging
from pathlib import Path
from typing import Optional

from src.api.video.enums import VideoRequestType, VideoProcessCodes, FileRetrievalCodes
from src.api.video.services.YaDiskHelper import YaDiskHelper
from src.api.video.utils import out_path_from_name, input_path_from_name
from src.pipeline.render import RendererBuilder, Renderer
from src.pipeline.ffmpeg_utils import preflight, compress, normalize

from src.api.video.schemas import VideoRequest
from src.api.video.services.RequestQueue import RequestQueue

logger = logging.getLogger(os.path.basename(__file__))

class VideoRequestsHandler:
    current_request_id: str = ""
    def __init__(self, ya_disk_helper: YaDiskHelper):
        self.queue: RequestQueue = RequestQueue()
        self.ya_disk_helper = ya_disk_helper

    async def add_request(self, request: VideoRequest, request_type: VideoRequestType) -> VideoProcessCodes:
        if self.queue.exists(request.get_video_id()):
            return VideoProcessCodes.ALREADY_QUEUED
        if out_path_from_name(request.get_video_id()).is_file():
            return VideoProcessCodes.ALREADY_PROCESSED
        logger.info(f"Queued request: {request.get_video_id()}")
        success = await self.queue.push(request, request_type, request.get_video_id())
        return VideoProcessCodes.OK if success else VideoProcessCodes.QUEUE_FULL

    async def start(self):
        logger.info(f"Startup completed")
        while True:
            req, req_type, req_id = await self.queue.pop()
            self.current_request_id = req_id
            await self._process_video(req, req_type)
            self.current_request_id = ""
            self.queue.task_done()

    @staticmethod
    def _build_renderer(request_type: VideoRequestType, file_path: Path) -> Optional[Renderer]:
        if request_type == VideoRequestType.COMPRESS:
            return (
                RendererBuilder().use_file(str(file_path))
                    .add_preprocessor(normalize)
                    .add_job(preflight)
                    .add_job(compress)
                    .build()
            )
        return None

    async def _process_video(self, request: VideoRequest, request_type: VideoRequestType) -> VideoProcessCodes:
        request_id: str = request.get_video_id()
        logger.info(f"Starting to process request: {request_id}")
        raw_file_path: Path = input_path_from_name(request_id)

        os.makedirs(raw_file_path.parent, exist_ok=True)
        os.makedirs(out_path_from_name(request_id).parent, exist_ok=True)

        if not raw_file_path.is_file():
            return_code: FileRetrievalCodes = await self.ya_disk_helper.get_file_by_url(request.video_url, raw_file_path)
            if return_code == FileRetrievalCodes.NOT_FOUND:
               return VideoProcessCodes.FILE_NOT_FOUND
        logger.info(f"Raw file retrieved")
        renderer: Renderer = self._build_renderer(request_type, raw_file_path)
        logger.info(f"Renderer created")
        if renderer is None:
            return VideoProcessCodes.UNKNOWN_ERROR

        logger.info(f"Starting the renderer")
        renderer.run(out_path_from_name(request_id))
        logger.info(f"Task done: {request_id}")
        return VideoProcessCodes.OK
