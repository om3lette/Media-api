from pathlib import Path

from backend.src.api.common.enums import FileRetrievalCodes
from backend.src.api.common.request_helpers.base_helper import BaseHelper


class BaseFileHelper(BaseHelper):
    async def retrieve_file(
        self, source, save_path: Path
    ) -> tuple[FileRetrievalCodes, Path | None]:
        return FileRetrievalCodes.NOT_FOUND, None
