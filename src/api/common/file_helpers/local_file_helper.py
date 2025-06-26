from pathlib import Path

from yadisk import AsyncClient

from src.api.common.enums import FileRetrievalCodes
from src.api.common.file_helpers.base_file_helper import BaseFileHelper
from src.constants import NULL_PATH
from src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


class LocalFileHelper(BaseFileHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("local_file")

    async def retrieve_file(
        self, source: Path, save_path: Path
    ) -> tuple[FileRetrievalCodes, Path]:
        if not source.is_file():
            return FileRetrievalCodes.NOT_FOUND, NULL_PATH
        logger.info("Using local file: %s", source)
        return FileRetrievalCodes.OK, source
