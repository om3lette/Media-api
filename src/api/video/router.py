from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException
from starlette.responses import Response, FileResponse, RedirectResponse

from src.api.video.enums import VideoRequestType, VideoProcessCodes
from src.api.video.schemas import CompressRequestSchema
from src.api.video.handlers import video_requests_handler
from src.api.video.utils import out_path_from_request_id

video_router: APIRouter = APIRouter()


@video_router.get("/status/")
async def get_request_status(request_id: str):
    if video_requests_handler.queue.exists(request_id):
        return Response(status_code=202, content="Queued")
    if video_requests_handler.current_request_id == request_id:
        return Response(status_code=204)
    if not out_path_from_request_id(request_id).is_file():
        return Response(status_code=404, content="Request not found")
    return Response(status_code=200, content="Ready to be downloaded")

@video_router.post("/compress/")
async def compress_video(request_body: CompressRequestSchema):
    # return_code: VideoProcessCodes = await video_requests_handler.add_request(request_body, VideoRequestType.COMPRESS)
    return_code: VideoProcessCodes = await video_requests_handler.add_request(request_body, VideoRequestType.COMPRESS_AND_TRANSCRIBE)
    if return_code == VideoProcessCodes.ALREADY_QUEUED:
        return HTTPException(status_code=400, detail="Already queued")
    if return_code == VideoProcessCodes.QUEUE_FULL:
        return HTTPException(status_code=503, detail="Queue limit has been reached. Try again later")
    return Response(status_code=200, content=request_body.get_video_id())
