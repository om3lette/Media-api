from starlette.websockets import WebSocket

from backend.src.api.status.schemas.status import StatusEventSchema
from backend.src.api.status.services.StatusSubscriber import StatusSubscriber
from backend.src.api.status.types import SubChannels
from backend.src.api.status.utils import build_request_status


async def handle_sub(
    ws: WebSocket,
    subs: SubChannels,
    payload: StatusEventSchema,
    status_sub: StatusSubscriber,
) -> None:
    subs.add(payload.rid)
    status_sub.subscribe(ws, payload.rid)


async def handle_unsub(
    ws: WebSocket,
    subs: SubChannels,
    payload: StatusEventSchema,
    status_sub: StatusSubscriber,
) -> None:
    subs.remove(payload.rid)
    status_sub.unsubscribe(ws, payload.rid)


async def handle_sync(
    ws: WebSocket,
    subs: SubChannels,
    payload: StatusEventSchema,
    status_sub: StatusSubscriber,
) -> None:
    sync_data: dict = await build_request_status(payload.rid)
    sync_data["type"] = "sync"
    await ws.send_json(sync_data)
