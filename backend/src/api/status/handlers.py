from backend.src.api.common.io_handlers import redis_client
from backend.src.api.status.services.status_subscriber import StatusSubscriber

status_subscriber: StatusSubscriber = StatusSubscriber(redis_client)
