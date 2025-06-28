from pathlib import Path

from pydantic import HttpUrl
from yadisk import AsyncClient
from yadisk.exceptions import NotFoundError

from backend.src.api.common.enums import FileRetrievalCodes
from backend.src.api.common.file_helpers.base_file_helper import BaseFileHelper
from backend.src.api.common.file_helpers.utils import get_adjusted_save_path
from backend.src.config.config_parser import ConfigParser


class YaDiskHelper(BaseFileHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("yadisk")

    async def init(self, app_config: ConfigParser):
        self.client = AsyncClient()

    async def retrieve_file(
        self, source: HttpUrl, save_path: Path
    ) -> tuple[FileRetrievalCodes, Path | None]:
        try:
            filename: str = (await self.client.get_public_meta(str(source))).name
            correct_save_path: Path = get_adjusted_save_path(save_path, filename)
            await self.client.download_public(str(source), str(correct_save_path))
            return FileRetrievalCodes.OK, correct_save_path
        except NotFoundError:
            return FileRetrievalCodes.NOT_FOUND, None
