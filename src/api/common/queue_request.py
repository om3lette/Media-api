
from fastapi import HTTPException, UploadFile
from pydantic import ValidationError
from starlette.responses import Response

from src.api.common.types.request import RequestType, GeneralRequestType
from src.api.common.handlers import global_requests_handler
from src.api.common.enums import RequestProcessCodes
from src.api.common.schemas.media_request import MediaRequestDTO, MediaRequestSchema


async def queue_request(
    request_type: GeneralRequestType,
    data_schema: type[MediaRequestSchema],
    data: str,
    file: UploadFile | None,
):
    try:
        parsed_data: MediaRequestSchema = data_schema.model_validate_json(data)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e.errors())
        ) from e

    if (not parsed_data.url and file is None) or (parsed_data.url and file):
        raise HTTPException(
            status_code=400, detail="Either a file or a url must be provided"
        )
    dto: MediaRequestDTO = MediaRequestDTO(parsed_data, file)
    request_id: str = dto.request.get_request_id()
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
