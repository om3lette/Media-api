import logging
import os
import shutil
from pathlib import Path

from src.api.common import RequestType
from src.api.common.file_helpers import BaseFileHelper
from src.api.common.schemas import MediaRequestSchema
from src.api.common.request_helpers.HelpersHandler import HelpersHandler
from src.api.common.schemas.MediaRequest import MediaRequestDTO
from src.api.video.enums import VideoRequestType
from src.api.common.enums import RequestProcessCodes, FileRetrievalCodes, FileHelperNames
from src.api.common.utils import out_path_from_request_id, input_path_from_request_id

from src.api.common.types import RequestHandler, RequestHelper, FileHelper
from src.api.common.services.RequestQueue import RequestQueue
from src.app_config import app_config
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)

class GlobalRequestsHandler:
    current_request_id: str = ""

    def __init__(self):
        self.queue: RequestQueue = RequestQueue()
        self._handlers: list[RequestHandler] = []
        self._file_helpers: HelpersHandler = HelpersHandler()
        self._helpers: HelpersHandler = HelpersHandler()

    def register_request_handler(self, handler: RequestHandler):
        logger.info(f"Registering {handler.event_type} request handler...")
        self._handlers.append(handler)

    async def register_file_helper(self, file_helper: FileHelper):
        logger.info(f"Initializing {file_helper.name} file helper...")
        await self._file_helpers.register_helper(file_helper)

    async def register_request_helper(self, helper: RequestHelper):
        logger.info(f"Initializing {helper.name} helper...")
        await self._helpers.register_helper(helper)

    async def add_request(self, request_id: str, request: MediaRequestDTO, request_type: RequestType) -> RequestProcessCodes:
        if self.queue.exists(request_id):
            return RequestProcessCodes.ALREADY_QUEUED

        # UploadFile is a only alive while the request is being processed
        # By the time _process_request is called UploadFile is destroyed
        # To fix that file needs to be saved during add_request
        self._request_folders_setup(request_id)
        if request.file:
            await self._retrieve_file(request, input_path_from_request_id(request_id))

        logger.info(f"Queued request: {request_id}")
        success = await self.queue.push(request, request_type, request_id)
        return RequestProcessCodes.OK if success else RequestProcessCodes.QUEUE_FULL

    async def start(self):
        logger.info(f"Startup completed")
        while True:
            req, req_type, req_id = await self.queue.pop()
            self.current_request_id = req_id
            try:
                await self._process_request(req, req_id, req_type)
            except Exception as e:
                logger.error(f"Error occurred when processing video:\n{e}")
            self.current_request_id = ""
            self.queue.task_done()

    def _get_request_handler(self, request_type: VideoRequestType) -> RequestHandler:
        for handler in self._handlers:
            if handler.event_type == request_type:
                return handler
        raise NameError(f"Handler not found for request type: {request_type}")

    @staticmethod
    def _request_folders_setup(request_id: str):
        os.makedirs(input_path_from_request_id(request_id).parent, exist_ok=True)
        out_dir: Path = out_path_from_request_id(request_id).parent
        # TODO: Reconsider
        if out_dir.is_dir():
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)

    async def _process_request(self, dto: MediaRequestDTO, request_id: str, request_type: VideoRequestType) -> RequestProcessCodes:
        logger.info(f"Starting to process request: {request_id}")
        input_file_path: Path = input_path_from_request_id(request_id)

        return_code: FileRetrievalCodes = await self._retrieve_file(dto, input_file_path)
        if return_code == FileRetrievalCodes.NOT_FOUND:
            logger.info(f"Failed to retrieve input file")
            return RequestProcessCodes.FILE_NOT_FOUND
        logger.info(f"Input file retrieved")

        request_handler = self._get_request_handler(request_type)
        await request_handler.handle(self._helpers, request_id, input_file_path)
        logger.info("Render complete")

        # Cleanup input files
        # Save files retrieved from url in dev move
        if not app_config.dev_mode or dto.file:
            logging.info("Deleting input file")
            shutil.rmtree(input_file_path.parent)

        logger.info(f"Task done: {request_id}")
        return RequestProcessCodes.OK

    async def _retrieve_file(self, request_body: MediaRequestDTO, save_path: Path) -> FileRetrievalCodes:
        if save_path.is_file():
            return FileRetrievalCodes.OK
        helper_name: FileHelperNames = FileHelperNames.UPLOAD_FILE
        if request_body.request.url:
            helper_name = FileHelperNames.YADISK
        helper: BaseFileHelper = self._file_helpers.get_helper_by_name(helper_name)

        return await helper.retrieve_file(
            request_body.request.url or request_body.file,
            save_path
        )
