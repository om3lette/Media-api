from pathlib import Path
from pydantic import HttpUrl

from yadisk import AsyncClient
from yadisk.exceptions import NotFoundError

from src.api.common.file_helpers.BaseFileHelper import BaseFileHelper
from src.api.common.enums import FileRetrievalCodes
from src.config.ConfigParser import ConfigParser


class YaDiskHelper(BaseFileHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("yadisk")

    async def init(self, app_config: ConfigParser):
        self.client = AsyncClient()

    async def retrieve_file(self, url: HttpUrl, out_path: Path) -> FileRetrievalCodes:
        try:
            await self.client.download_public(str(url), str(out_path))
            return FileRetrievalCodes.OK
        except NotFoundError:
            return FileRetrievalCodes.NOT_FOUND
