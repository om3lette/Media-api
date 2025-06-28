import uuid

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from starlette.responses import Response

from backend.src.api.common.enums import RequestProcessCodes
from backend.src.api.common.handlers import global_requests_handler
from backend.src.api.common.io_handlers import requests_repository
from backend.src.api.common.schemas.media_request import MediaRequestDTO, MediaRequestSchema
from backend.src.api.common.types.request import GeneralRequestType
from backend.src.app_config import app_config
from backend.src.constants import DEV_MOD_RID


async def queue_request(
    request_type: GeneralRequestType,
    data_schema: type[MediaRequestSchema],
    data: str,
    file: UploadFile | None,
):
    try:
        parsed_data: MediaRequestSchema = data_schema.model_validate_json(
            data, by_alias=True
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e.errors())) from e

    input_sources = [parsed_data.path, parsed_data.url, file]
    provided_sources: int = sum(x is not None for x in input_sources)

    if provided_sources == 0:
        raise HTTPException(
            status_code=400, detail="Either a file or a url must be provided"
        )

    if provided_sources != 1:
        raise HTTPException(
            status_code=400,
            detail=f"Only one of the following: url/file/path should be provided, received {provided_sources} options",
        )

    if parsed_data.path and not app_config.allow_local_files:
        raise HTTPException(
            status_code=400, detail="Local files are disabled on this server"
        )

    dto: MediaRequestDTO = MediaRequestDTO(parsed_data, file)
    request_id: str = uuid.uuid4().hex if not app_config.dev_mode else DEV_MOD_RID
    return_code: RequestProcessCodes = await global_requests_handler.add_request(
        request_id, request_type, dto
    )

    if return_code == RequestProcessCodes.ALREADY_QUEUED:
        raise HTTPException(status_code=409, detail="Already queued")
    if return_code == RequestProcessCodes.QUEUE_FULL:
        raise HTTPException(
            status_code=503, detail="Queue limit has been reached. Try again later"
        )
    requests_repository.add_request(request_id, request_type, dto)
    return Response(status_code=202, content=request_id)
