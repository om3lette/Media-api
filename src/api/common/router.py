from typing import Annotated

from fastapi import APIRouter, UploadFile, Form, File

from src.api.common.queue_request import queue_request
from src.api.common.types.request import GeneralRequestType
from src.api.video.schemas import VideoRequests

requests_router: APIRouter = APIRouter()


@requests_router.post("/compress/")
async def compress(
    data: Annotated[str, Form()], file: UploadFile | None = File(None)
):
    return await queue_request(
        GeneralRequestType.COMPRESS, VideoRequests.compress, data, file
    )


@requests_router.post("/extract-audio/")
async def extract(
    data: Annotated[str, Form()], file: UploadFile | None = File(None)
):
    return await queue_request(
        GeneralRequestType.EXTRACT_AUDIO, VideoRequests.extract_audio, data, file
    )


@requests_router.post("/transcribe/")
async def transcribe(
    data: Annotated[str, Form()], file: UploadFile | None = File(None)
):
    return await queue_request(
        GeneralRequestType.TRANSCRIBE, VideoRequests.transcribe, data, file
    )


@requests_router.post("/summarize/")
async def summarize(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(
        GeneralRequestType.SUMMARIZE, VideoRequests.summarize, data, file
    )


@requests_router.post("/custom/")
async def custom(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(
        GeneralRequestType.CUSTOM, VideoRequests.custom, data, file
    )
