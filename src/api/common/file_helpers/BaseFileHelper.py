from pathlib import Path

from src.api.common.enums import FileRetrievalCodes
from src.api.common.request_helpers.BaseHelper import BaseHelper


class BaseFileHelper(BaseHelper):
    def __init__(self, name: str):
        super().__init__(name)

    async def retrieve_file(self, source, out_path: Path) -> FileRetrievalCodes:
        return FileRetrievalCodes.NOT_FOUND
