from fastapi import HTTPException
from starlette.responses import Response

from src.api.common.handlers import global_requests_handler
from src.api.common.enums import RequestProcessCodes


async def queue_request(request_id: str, request_body, request_type):
    return_code: RequestProcessCodes = await global_requests_handler.add_request(
        request_id,
        request_body,
        request_type
    )
    if return_code == RequestProcessCodes.ALREADY_QUEUED:
        return HTTPException(status_code=400, detail="Already queued")
    if return_code == RequestProcessCodes.QUEUE_FULL:
        return HTTPException(status_code=503, detail="Queue limit has been reached. Try again later")
    return Response(status_code=200, content=request_id)
