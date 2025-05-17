from pathlib import Path

from src.api.common.enums import FileRetrievalCodes
from src.api.common.request_helpers.BaseHelper import BaseHelper


class BaseFileHelper(BaseHelper):
    async def retrieve_file(self, source, out_path: Path) -> FileRetrievalCodes:
        return FileRetrievalCodes.NOT_FOUND
