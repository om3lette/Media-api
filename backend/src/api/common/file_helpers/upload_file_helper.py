from pathlib import Path

import aiofiles
from fastapi import UploadFile
from yadisk import AsyncClient

from backend.src.api.common.enums import FileRetrievalCodes
from backend.src.api.common.file_helpers.base_file_helper import BaseFileHelper
from backend.src.api.common.file_helpers.utils import get_adjusted_save_path
from backend.src.app_config import app_config
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


class UploadFileHelper(BaseFileHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("upload_file")

    async def retrieve_file(
        self, source: UploadFile, save_path: Path
    ) -> tuple[FileRetrievalCodes, Path]:
        file_size_mb: float = round(source.size / 2**20, 2)
        file_size_str: str = (
            f"{file_size_mb}mb"
            if file_size_mb < 1024
            else f"{round(file_size_mb / 2**10, 2)}gb"
        )
        correct_save_path: Path = get_adjusted_save_path(save_path, source.filename)
        logger.info("Saving %s | %s", source.filename, file_size_str)
        async with aiofiles.open(correct_save_path, "wb") as out_file:
            while chunk := await source.read(app_config.file_read_chunk_size):
                await out_file.write(chunk)
        await source.seek(0)
        logger.info("File saved to %s", correct_save_path)
        return FileRetrievalCodes.OK, correct_save_path
