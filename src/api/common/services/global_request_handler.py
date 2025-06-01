import os
from pathlib import Path

from src.api.common.enums import (
    FileHelperNames,
    FileRetrievalCodes,
    RequestProcessCodes,
)
from src.api.common.file_helpers import BaseFileHelper
from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.schemas.media_request import MediaRequestDTO
from src.api.common.services.handler_picker import HandlerPicker
from src.api.common.services.request_queue import RequestQueue
from src.api.common.types.file_helper import FileHelper
from src.api.common.types.request import GeneralRequestType
from src.api.common.types.request_handler import RequestHandler
from src.api.common.types.request_helper import RequestHelper
from src.api.common.utils import (
    archive_request_output,
    delete_request_data,
    input_path_from_request_id,
    out_path_from_request_id,
)
from src.api.tasks_handlers.constants import INPUT_FILENAME
from src.app_config import app_config
from src.config.enums import AudioCodecs, VideoCodecs
from src.constants import NULL_PATH
from src.pipeline.schemas.paths import PathsSchema
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class GlobalRequestsHandler:
    current_request_id: str = ""

    def __init__(self):
        self.queue: RequestQueue = RequestQueue()
        self.__handler_picker: HandlerPicker = HandlerPicker()
        self._file_helpers: HelpersHandler = HelpersHandler()
        self._helpers: HelpersHandler = HelpersHandler()

    def register_request_handler(self, handler: RequestHandler):
        logger.info(
            "Registering %s handler with file_types=[%s]...",
            handler.event_type,
            ", ".join(map(str, handler.file_types)),
        )
        self.__handler_picker.add_handler(handler)

    async def register_file_helper(self, file_helper: FileHelper):
        logger.info("Initializing %s helper...", file_helper.name)
        await self._file_helpers.register_helper(file_helper)

    async def register_request_helper(self, helper: RequestHelper):
        logger.info("Initializing %s helper...", helper.name)
        await self._helpers.register_helper(helper)

    async def add_request(
        self,
        request_id: str,
        request: MediaRequestDTO,
        request_type: GeneralRequestType,
    ) -> RequestProcessCodes:
        if self.queue.exists(request_id):
            return RequestProcessCodes.ALREADY_QUEUED

        # UploadFile is a only alive while the request is being processed
        # By the time _process_request is called UploadFile is destroyed
        # To fix that file needs to be saved during add_request
        self._request_folders_setup(request_id)
        if request.file:
            return_code, _ = await self._retrieve_file(
                request, input_path_from_request_id(request_id)
            )

            if return_code != FileRetrievalCodes.OK:
                delete_request_data(request_id)
                logger.info("Failed to retrieve input file")
                return RequestProcessCodes.FILE_NOT_FOUND

        logger.info("Queued request: %s", request_id)
        success = await self.queue.push(request, request_type, request_id)
        return RequestProcessCodes.OK if success else RequestProcessCodes.QUEUE_FULL

    async def start(self):
        logger.info("Startup completed")
        while True:
            req, req_type, req_id = await self.queue.pop()
            self.current_request_id = req_id
            try:
                await self._process_request(req, req_id, req_type)
            # pylint: disable=broad-exception-caught
            except Exception as e:
                delete_request_data(req_id)
                logger.error(
                    "Error occurred when processing request %s:\n%s", req_type, e
                )
            # pylint: enable=broad-exception-caught
            self.current_request_id = ""
            self.queue.task_done()

    @staticmethod
    def _request_folders_setup(request_id: str):
        os.makedirs(input_path_from_request_id(request_id).parent, exist_ok=True)
        out_dir: Path = out_path_from_request_id(request_id).parent
        # TODO: Reconsider
        if out_dir.is_dir():
            delete_request_data(request_id, delete_input=False)
        os.makedirs(out_dir)

    async def _process_request(
        self, dto: MediaRequestDTO, request_id: str, request_type: GeneralRequestType
    ) -> RequestProcessCodes:
        logger.info("Starting to process request: %s", request_id)

        return_code, input_file_path = await self._retrieve_file(
            dto, input_path_from_request_id(request_id)
        )

        if return_code != FileRetrievalCodes.OK:
            delete_request_data(request_id)
            logger.info("Failed to download input file")
            return RequestProcessCodes.FILE_NOT_FOUND
        logger.info("Input file retrieved")

        request_handler = self.__handler_picker.pick_handler(
            input_file_path, request_type
        )
        if request_handler is None:
            # TODO: More descriptive error
            delete_request_data(request_id)
            return RequestProcessCodes.UNKNOWN_ERROR

        video_codec: VideoCodecs = app_config.ffmpeg.codecs.video
        if "codecs" in dto.request.config.model_fields:
            video_codec = dto.request.config.codecs.video
        elif "ffmpeg" in dto.request.config:
            video_codec = dto.request.config.ffmpeg.codecs.video

        audio_codec: AudioCodecs = app_config.ffmpeg.codecs.audio
        if "audio" in dto.request.config.model_fields:
            audio_codec = dto.request.config.audio.codec

        await request_handler.handle(
            dto.request,
            self._helpers,
            PathsSchema(input_file_path, request_id, video_codec, audio_codec),
        )
        logger.info("Render complete")

        # Cleanup input files
        # Save files retrieved from url in dev move
        if not app_config.dev_mode or dto.file:
            logger.info("Deleting input file")
            delete_request_data(request_id, delete_output=False)

        logger.info("Archiving request output...")
        archive_request_output(request_id)

        logger.info("Task done: %s", request_id)
        return RequestProcessCodes.OK

    async def _retrieve_file(
        self, request_body: MediaRequestDTO, save_path: Path
    ) -> tuple[FileRetrievalCodes, Path]:
        """
        :param request_body:
        :param save_path:
        :return: Path where file was saved. save_path with correct suffix
        """
        # Check if input file is present in directory
        for f in save_path.parent.iterdir():
            if not f.is_file():
                continue
            if f.name.startswith(INPUT_FILENAME):
                return FileRetrievalCodes.OK, save_path.parent / f.name

        helper_name: FileHelperNames | None = FileHelperNames.UPLOAD_FILE
        if request_body.request.url:
            helper_name = FileHelperNames.YADISK
        elif request_body.request.path and app_config.allow_local_files:
            helper_name = FileHelperNames.LOCAL
        elif request_body.request.path:
            helper_name = None

        if not helper_name:
            return FileRetrievalCodes.UNSUPPORTED_METHOD, NULL_PATH

        helper: BaseFileHelper = self._file_helpers.get_helper_by_name(helper_name)
        return await helper.retrieve_file(
            request_body.request.url or request_body.file or request_body.request.path,
            save_path,
        )
