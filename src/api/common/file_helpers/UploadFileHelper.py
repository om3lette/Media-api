from pathlib import Path

import aiofiles
from fastapi import UploadFile

from yadisk import AsyncClient

from src.api.common.file_helpers.BaseFileHelper import BaseFileHelper
from src.api.common.enums import FileRetrievalCodes
from src.app_config import app_config
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class UploadFileHelper(BaseFileHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("upload_file")

    async def retrieve_file(
        self, file: UploadFile, save_path: Path
    ) -> FileRetrievalCodes:
        file_size_mb: float = round(file.size / 2**20, 2)
        file_size_str: str = (
            f"{file_size_mb}mb"
            if file_size_mb < 1024
            else f"{round(file_size_mb / 2**10, 2)}gb"
        )
        logger.info(f"Saving {file.filename} | {file_size_str}")
        async with aiofiles.open(save_path, "wb") as out_file:
            while chunk := await file.read(app_config.file_read_chunk_size):
                await out_file.write(chunk)
        await file.seek(0)
        logger.info(f"File saved to {save_path}")
        return FileRetrievalCodes.OK
