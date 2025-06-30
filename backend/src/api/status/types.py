from typing import Callable, Awaitable

from starlette.websockets import WebSocket

from backend.src.api.common.io.requests_repository import RequestsRepository
from backend.src.api.status.schemas.status import StatusEventSchema
from backend.src.api.status.services.status_subscriber import StatusSubscriber
from backend.src.api.status.constants import ValidationStatusCode

SubChannels = set[str]
EventValidator = Callable[
    [StatusEventSchema, SubChannels, RequestsRepository],
    tuple[ValidationStatusCode, bool],
]
EventHandler = Callable[
    [WebSocket, SubChannels, StatusEventSchema, StatusSubscriber], Awaitable[None]
]
