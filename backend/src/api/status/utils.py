from datetime import datetime

from backend.src.api.common.io_handlers import requests_repository, progress_handler
from backend.src.api.common.schemas.progress.progress_schema import ProgressSchema


async def build_request_status(request_id: str):
    request_status: dict = requests_repository.get_request_status(request_id)
    if not request_status:
        return {"status": requests_repository.DELETED}

    request_progress: dict = await progress_handler.get_progress_data(request_id)
    end_time = (
        request_status["end_time"]
        if request_status["end_time"] is not None
        else datetime.now()
    )

    return ProgressSchema(
        **{
            "rid": request_id,
            "status": request_status["status"],
            "elapsed_time": int(
                (end_time - request_status["start_time"]).total_seconds()
            ),
            **request_progress,
        }
    ).model_dump(by_alias=True)
