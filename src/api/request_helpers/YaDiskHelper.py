from pathlib import Path
from pydantic import HttpUrl

from yadisk import AsyncClient
from yadisk.exceptions import NotFoundError

from src.api.request_helpers.BaseHelper import BaseHelper
from src.api.common.enums import FileRetrievalCodes


class YaDiskHelper(BaseHelper):
    client: AsyncClient

    def __init__(self):
        super().__init__("yadisk")
        self.client = AsyncClient()

    async def get_file_by_url(self, url: HttpUrl, out_path: Path) -> FileRetrievalCodes:
        try:
            await self.client.download_public(str(url), str(out_path))
            return FileRetrievalCodes.OK
        except NotFoundError:
            return FileRetrievalCodes.NOT_FOUND