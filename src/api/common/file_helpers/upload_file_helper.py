from pathlib import Path

import aiofiles
from fastapi import UploadFile

from yadisk import AsyncClient

from src.api.common.file_helpers.base_file_helper import BaseFileHelper
from src.api.common.enums import FileRetrievalCodes
from src.app_config import app_config
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class UploadFileHelper(BaseFileHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("upload_file")

    async def retrieve_file(
        self, source: UploadFile, out_path: Path
    ) -> FileRetrievalCodes:
        file_size_mb: float = round(source.size / 2**20, 2)
        file_size_str: str = (
            f"{file_size_mb}mb"
            if file_size_mb < 1024
            else f"{round(file_size_mb / 2**10, 2)}gb"
        )
        logger.info("Saving %s | %s", source.filename, file_size_str)
        async with aiofiles.open(out_path, "wb") as out_file:
            while chunk := await source.read(app_config.file_read_chunk_size):
                await out_file.write(chunk)
        await source.seek(0)
        logger.info("File saved to %s", out_path)
        return FileRetrievalCodes.OK
