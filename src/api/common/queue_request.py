from typing import Optional, Type

from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from starlette.responses import Response

from src.api.common import RequestType
from src.api.common.handlers import global_requests_handler
from src.api.common.enums import RequestProcessCodes
from src.api.common.schemas.MediaRequest import MediaRequestDTO, MediaRequestSchema


async def queue_request(
    request_type: RequestType,
    data_schema: Type[MediaRequestSchema],
    data: str,
    file: Optional[UploadFile],
):
    try:
        parsed_data: MediaRequestSchema = data_schema.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    dto: MediaRequestDTO = MediaRequestDTO(parsed_data, file)
    request_id: str = dto.request.get_request_id()
    if dto.request.url and dto.file:
        raise HTTPException(
            status_code=400, detail="File and url cannot be specified at the same time"
        )
    return_code: RequestProcessCodes = await global_requests_handler.add_request(
        request_id, dto, request_type
    )

    if return_code == RequestProcessCodes.ALREADY_QUEUED:
        raise HTTPException(status_code=400, detail="Already queued")
    if return_code == RequestProcessCodes.QUEUE_FULL:
        raise HTTPException(
            status_code=503, detail="Queue limit has been reached. Try again later"
        )
    return Response(status_code=200, content=request_id)
