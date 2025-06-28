import asyncio
import os
import shutil
from pathlib import Path
from typing import Coroutine

from backend.src.api.common.io_handlers import requests_repository
from backend.src.api.common.utils import (
    request_data_dir_from_id,
    request_out_dir_from_id,
    request_archive_path_from_id,
)
from backend.src.app_config import app_config
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


async def disk_cleanup():
    def delete_request_data(request_id: str):
        # Input should be deleted automatically when the request is finished
        # Extra safety measure
        shutil.rmtree(request_data_dir_from_id(request_id), ignore_errors=True)
        shutil.rmtree(request_out_dir_from_id(request_id), ignore_errors=True)

        archive_path: Path = request_archive_path_from_id(request_id)
        if archive_path.is_file():
            os.remove(archive_path)

    tasks: list[Coroutine] = []
    ids: list[str] = []
    requests_data = requests_repository.get_expired_requests(
        app_config.cleanup.request_files_ttl / 3600
    )
    logger.info("Deleting %d entries", len(requests_data))

    for _, request_id in requests_data:
        tasks.append(asyncio.to_thread(delete_request_data, request_id))
        ids.append(request_id)

    await asyncio.gather(*tasks)
    requests_repository.delete_requests(ids)
