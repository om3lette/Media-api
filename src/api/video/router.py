from fastapi import APIRouter

from src.api.common.queue_request import queue_request
from src.api.video.enums import VideoRequestType
from src.api.video.schemas import VideoRequestSchema

video_router: APIRouter = APIRouter()


@video_router.post("/compress/")
async def compress_video(request_body: VideoRequestSchema):
    return await queue_request(request_body.get_video_id(), request_body, VideoRequestType.COMPRESS)

@video_router.post("/extract-audio/")
async def compress_video(request_body: VideoRequestSchema):
    return await queue_request(request_body.get_video_id(), request_body, VideoRequestType.EXTRACT_AUDIO)

@video_router.post("/transcribe/")
async def compress_video(request_body: VideoRequestSchema):
    return await queue_request(request_body.get_video_id(), request_body, VideoRequestType.TRANSCRIBE)

@video_router.post("/summarize/")
async def compress_video(request_body: VideoRequestSchema):
    return await queue_request(request_body.get_video_id(), request_body, VideoRequestType.SUMMARIZE)

