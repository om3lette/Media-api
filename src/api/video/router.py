import copy
from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, File, HTTPException
from pydantic import ValidationError

from src.api.common.queue_request import queue_request
from src.api.common.schemas.MediaRequest import MediaRequestDTO
from src.api.video.enums import VideoRequestType
from src.api.video.schemas import VideoRequests

video_router: APIRouter = APIRouter()

@video_router.post("/compress/")
async def compress_video(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(VideoRequestType.COMPRESS, VideoRequests.compress, data, file)


@video_router.post("/extract-audio/")
async def compress_video(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(VideoRequestType.EXTRACT_AUDIO, VideoRequests.extract_audio, data, file)

@video_router.post("/transcribe/")
async def compress_video(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(VideoRequestType.TRANSCRIBE, VideoRequests.transcribe, data, file)

@video_router.post("/summarize/")
async def compress_video(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(VideoRequestType.SUMMARIZE, VideoRequests.summarize, data, file)
