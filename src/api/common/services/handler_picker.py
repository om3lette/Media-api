from pathlib import Path

import magic

from src.api.common.enums import FileType
from src.api.common.types.request import GeneralRequestType
from src.api.common.types.request_handler import RequestHandler
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class HandlerPicker:
    def __init__(self):
        self.__handlers: list[RequestHandler] = []

    def add_handler(self, handler: RequestHandler):
        self.__handlers.append(handler)

    @staticmethod
    def __deduce_file_type(file_path: Path) -> None | FileType:
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            mime_type: str = m.id_filename(str(file_path))
            if not mime_type:
                return FileType.OTHER
            _type, subtype = mime_type.split("/")

            if _type == "video":
                # .m4a is recognised as video/mp4 (m4a is a mp4 container with no video stream)
                if file_path.suffix == ".m4a":
                    return FileType.AUDIO
                return FileType.VIDEO
            if _type == "audio":
                return FileType.AUDIO
            if _type == "image":
                return FileType.IMAGE
            if _type == "text":
                return FileType.TEXT
            if _type == "application":
                if subtype == "octet-stream":
                    return FileType.EXECUTABLE
                return FileType.DOCUMENT
            return FileType.OTHER

    def pick_handler(
        self, file_path: Path, request_type: GeneralRequestType
    ) -> RequestHandler | None:
        file_type: FileType = self.__deduce_file_type(file_path)
        if file_type == FileType.EXECUTABLE:
            logger.warning("Found executable file. Aborting request")
            return None
        if file_type == FileType.OTHER:
            # Unknown file type -> not supported
            return None

        for handler in self.__handlers:
            if handler.event_type == request_type and file_type in handler.file_types:
                return handler
        logger.info(
            "No handler found for request_type: %s and file_type: %s",
            request_type,
            file_type,
        )
        return None
