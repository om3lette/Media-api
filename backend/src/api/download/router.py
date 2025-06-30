from fastapi import APIRouter

from backend.src.api.common.utils import (
    request_archive_path_from_id,
    transcription_path_from_request_id,
    audio_path_from_request_id,
    video_path_from_request_id,
    summary_path_from_request_id,
)
from backend.src.api.download.utils import (
    download_request_wrapper,
    file_response_builder,
    json_response_builder,
)

download_router: APIRouter = APIRouter()


@download_router.get("/{request_id}/")
async def download_archive(request_id: str):
    return download_request_wrapper(
        request_id, request_archive_path_from_id, file_response_builder
    )


@download_router.get("/{request_id}/video/")
async def download_video(request_id: str):
    return download_request_wrapper(
        request_id, video_path_from_request_id, file_response_builder
    )


@download_router.get("/{request_id}/audio/")
async def download_audio(request_id: str):
    return download_request_wrapper(
        request_id, audio_path_from_request_id, file_response_builder
    )


@download_router.get("/{request_id}/text/")
async def get_text(request_id: str):
    return download_request_wrapper(
        request_id, transcription_path_from_request_id, json_response_builder
    )


@download_router.get("/{request_id}/summary/")
async def get_summary(request_id: str):
    return download_request_wrapper(
        request_id, summary_path_from_request_id, json_response_builder
    )
