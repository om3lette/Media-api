import os
import shutil
from pathlib import Path

from src.api.request_helpers.HelpersHandler import HelpersHandler
from src.api.video.enums import VideoRequestType
from src.api.common.enums import RequestProcessCodes, FileRetrievalCodes
from src.api.video.schemas.requests.types import RequestHelper
from src.api.common.utils import out_path_from_request_id, input_path_from_request_id, audio_path_from_request_id, \
    transcription_path_from_request_id
from src.app_config import app_config

from src.api.video.schemas import VideoRequest, RequestHandler
from src.api.common.services.RequestQueue import RequestQueue
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)

class GlobalRequestsHandler:
    current_request_id: str = ""

    def __init__(self, helpers_handler: HelpersHandler):
        self.queue: RequestQueue = RequestQueue()
        self._handlers: list[RequestHandler] = []
        self._helpers: HelpersHandler = helpers_handler

    def register_request_handler(self, handler: RequestHandler):
        logger.info(f"Registering {handler.event_type} request handler...")
        self._handlers.append(handler)

    async def register_request_helper(self, helper: RequestHelper):
        logger.info(f"Initializing {helper.name} helper...")
        await self._helpers.register_helper(helper)

    async def add_request(self, request_id: str, request: VideoRequest, request_type: VideoRequestType) -> RequestProcessCodes:
        if self.queue.exists(request.get_video_id()):
            return RequestProcessCodes.ALREADY_QUEUED
        out_path: Path = out_path_from_request_id(request_id)

        # Force reprocessing requests in dev mode
        if app_config.dev_mode and out_path.parent.is_dir():
            shutil.rmtree(out_path.parent)

        if request_type == VideoRequestType.COMPRESS and out_path.is_file():
            return RequestProcessCodes.ALREADY_PROCESSED

        audio_path: Path = audio_path_from_request_id(request_id)
        transcription_path: Path = transcription_path_from_request_id(request_id)
#        if request_type == VideoRequestType.COMPRESS_AND_TRANSCRIBE and \
#                out_path.is_file() and \
#                audio_path.is_file() and \
#                transcription_path.is_file():
#            return RequestProcessCodes.ALREADY_PROCESSED
        logger.info(f"Queued request: {request.get_video_id()}")
        success = await self.queue.push(request, request_type, request.get_video_id())
        return RequestProcessCodes.OK if success else RequestProcessCodes.QUEUE_FULL

    async def start(self):
        logger.info(f"Startup completed")
        while True:
            req, req_type, req_id = await self.queue.pop()
            self.current_request_id = req_id
            try:
                await self._process_video(req, req.get_video_id(), req_type)
            except Exception as e:
                logger.error(f"Error occurred when processing video:\n{e}")
            self.current_request_id = ""
            self.queue.task_done()

    def _get_request_handler(self, request_type: VideoRequestType) -> RequestHandler:
        for handler in self._handlers:
            if handler.event_type == request_type:
                return handler
        raise NameError(f"Handler not found for request type: {request_type}")

    async def _process_video(self, request: VideoRequest, request_id: str, request_type: VideoRequestType) -> RequestProcessCodes:
        logger.info(f"Starting to process request: {request_id}")
        raw_file_path: Path = input_path_from_request_id(request_id)

        os.makedirs(raw_file_path.parent, exist_ok=True)
        out_dir: Path = out_path_from_request_id(request_id).parent
        if out_dir.is_dir():
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)

        if not raw_file_path.is_file():
            return_code: FileRetrievalCodes = await self._helpers.get_helper_by_name("yadisk").get_file_by_url(request.video_url, raw_file_path)
            if return_code == FileRetrievalCodes.NOT_FOUND:
               return RequestProcessCodes.FILE_NOT_FOUND
        logger.info(f"Raw file retrieved")

        request_handler = self._get_request_handler(request_type)
        await request_handler.handle(self._helpers, request_id, raw_file_path)

        logger.info(f"Task done: {request_id}")
        return RequestProcessCodes.OK
