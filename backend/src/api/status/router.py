import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from backend.src.api.common.io_handlers import requests_repository
from backend.src.api.status.handlers import status_subscriber
from backend.src.api.status.schemas.status import StatusEventSchema
from backend.src.api.status.services.mapping import event_type_to_handlers
from backend.src.api.status.utils import build_request_status

request_status_router: APIRouter = APIRouter()


@request_status_router.websocket("/status/ws/")
async def websocket_status(websocket: WebSocket):
    await websocket.accept()
    subscribed: set[str] = set()

    async def listen_for_subscriptions():
        while True:
            message = await websocket.receive_json()
            try:
                payload: StatusEventSchema = StatusEventSchema.model_validate(message)
            except ValidationError as e:
                await websocket.send_json(
                    json.dumps({"type": "error", "detail": e, "isValidation": True})
                )
                continue

            validator, handler = event_type_to_handlers[payload.type]
            error_code, is_missing = validator(payload, subscribed, requests_repository)
            if error_code:
                err_payload: dict[str, int | str | bool] = {
                    "type": "error",
                    "rid": payload.rid,
                    "code": error_code,
                }
                if is_missing:
                    err_payload["isMissing"] = True
                await websocket.send_json(err_payload)
                continue

            await handler(websocket, subscribed, payload, status_subscriber)

    try:
        await listen_for_subscriptions()
    except WebSocketDisconnect:
        pass

    for rid in subscribed:
        status_subscriber.unsubscribe(websocket, rid)


@request_status_router.get("/status/")
async def rest_status(request_id: str):
    return await build_request_status(request_id)
