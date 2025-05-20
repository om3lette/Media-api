from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from src.api.common.queue_request import queue_request
from src.api.common.schemas.requests import RequestsMapping
from src.api.common.types.request import GeneralRequestType

requests_router: APIRouter = APIRouter()


@requests_router.post("/compress/")
async def compress(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(
        GeneralRequestType.COMPRESS, RequestsMapping.compress, data, file
    )


@requests_router.post("/extract-audio/")
async def extract(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(
        GeneralRequestType.EXTRACT_AUDIO, RequestsMapping.extract_audio, data, file
    )


@requests_router.post("/transcribe/")
async def transcribe(
    data: Annotated[str, Form()], file: UploadFile | None = File(None)
):
    return await queue_request(
        GeneralRequestType.TRANSCRIBE, RequestsMapping.transcribe, data, file
    )


@requests_router.post("/summarize/")
async def summarize(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(
        GeneralRequestType.SUMMARIZE, RequestsMapping.summarize, data, file
    )


@requests_router.post("/custom/")
async def custom(data: Annotated[str, Form()], file: UploadFile | None = File(None)):
    return await queue_request(
        GeneralRequestType.CUSTOM, RequestsMapping.custom, data, file
    )


@requests_router.post("/file-to-text/")
async def image_to_text(
    data: Annotated[str, Form()], file: UploadFile | None = File(None)
):
    return await queue_request(
        GeneralRequestType.FILE_TO_TEXT, RequestsMapping.file_to_text, data, file
    )
