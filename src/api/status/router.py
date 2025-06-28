import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.common.io_handlers import requests_repository
from src.api.status.handlers import status_subscriber
from src.api.status.utils import build_request_status

request_status_router: APIRouter = APIRouter()

ALLOWED_WS_EVENT_TYPES: tuple[str, str, str] = ("sub", "unsub", "sync")


@request_status_router.websocket("/status/ws/")
async def websocket_status(websocket: WebSocket):
    await websocket.accept()
    subscribed: set[str] = set()

    async def listen_for_subscriptions():
        while True:
            message = await websocket.receive_json()
            msg_type: str | None = message.get("type")
            request_id: str | None = message.get("rid")

            error_message: str = ""
            invalid_rid: bool = False
            if not msg_type or not request_id:
                error_message = "'type' and 'rid' fields must be of type str"
            elif msg_type not in ALLOWED_WS_EVENT_TYPES:
                error_message = (
                    f"'type' should be one of: {', '.join(ALLOWED_WS_EVENT_TYPES)}"
                )
            elif msg_type == "sub" and request_id in subscribed:
                error_message = "Already subscribed"
            elif not requests_repository.is_subscribable(request_id):
                error_message = "Request does not exist"
                invalid_rid = True

            if error_message:
                await websocket.send_json(
                    {"type": "error", "invalidId": invalid_rid, "rid": request_id, "detail": error_message}
                )
                continue

            if msg_type == "sub":
                subscribed.add(request_id)
                status_subscriber.subscribe(websocket, request_id)
            elif msg_type == "unsub":
                subscribed.remove(request_id)
                status_subscriber.unsubscribe(websocket, request_id)
            elif msg_type == "sync":
                sync_data = await build_request_status(request_id)
                sync_data["type"] = "sync"
                await websocket.send_json(sync_data)

    try:
        await listen_for_subscriptions()
    except WebSocketDisconnect:
        pass

    for rid in subscribed:
        status_subscriber.unsubscribe(websocket, rid)


@request_status_router.get("/status/")
async def rest_status(request_id: str):
    return await build_request_status(request_id)
