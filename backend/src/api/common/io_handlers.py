import os
import sqlite3

from dotenv import load_dotenv
from redis.asyncio import Redis

from backend.src.api.common.io.progress_handler import ProgressHandler
from backend.src.api.common.io.requests_repository import RequestsRepository
from backend.src.app_config import app_config
from backend.src.constants import DB_PATH

db_connection = sqlite3.connect(DB_PATH, timeout=5.0, check_same_thread=False)
db_connection.row_factory = sqlite3.Row

requests_repository: RequestsRepository = RequestsRepository(db_connection)

load_dotenv()
redis_connection_string = os.getenv(
    "REDIS_CONNECTION_STRING", "redis://127.0.0.1:6379/0"
)
redis_client: Redis = Redis.from_url(redis_connection_string, decode_responses=True)
progress_handler: ProgressHandler = ProgressHandler(
    redis_client, app_config.cleanup.request_status_ttl
)
