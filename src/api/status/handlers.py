from src.api.common.io_handlers import redis_client
from src.api.status.services.StatusSubscriber import StatusSubscriber

status_subscriber: StatusSubscriber = StatusSubscriber(redis_client)
