from fastapi import APIRouter
from starlette.responses import Response

from src.api.common.handlers import global_requests_handler
from src.api.common.utils import request_archive_from_id

request_status_router: APIRouter = APIRouter()


@request_status_router.get("/status/")
async def get_request_status(request_id: str):
    if global_requests_handler.queue.exists(request_id):
        return Response(status_code=202, content="Queued")
    if global_requests_handler.current_request_id == request_id:
        return Response(status_code=204)
    if not request_archive_from_id(request_id).is_file():
        return Response(status_code=404, content="Request not found")
    return Response(status_code=200, content="Ready to be downloaded")
