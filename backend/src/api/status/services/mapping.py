from backend.src.api.status.schemas.status import EventType
from backend.src.api.status.services.event_handlers import (
    handle_sub,
    handle_unsub,
    handle_sync,
)
from backend.src.api.status.services.validators import (
    validate_sub,
    validate_unsub,
    validate_sync,
)
from backend.src.api.status.types import EventValidator, EventHandler

event_type_to_handlers: dict[EventType, tuple[EventValidator, EventHandler]] = {
    "sub": (validate_sub, handle_sub),
    "unsub": (validate_unsub, handle_unsub),
    "sync": (validate_sync, handle_sync),
}
