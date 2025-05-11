import asyncio

from src.api.common import RequestType
from src.api.common.schemas import MediaRequestSchema
from src.api.common.schemas.MediaRequest import MediaRequestDTO
from src.api.video.constants import MAX_REQUESTS_BACKLOG

class RequestQueue:
    def __init__(self, maxsize: int = MAX_REQUESTS_BACKLOG):
        self._queue: asyncio.Queue[tuple[MediaRequestDTO, RequestType, str]] = asyncio.Queue(maxsize)
        # for quick existence checks or de‐duplication
        self._ids: set[str] = set()

    async def join(self):
        await self._queue.join()

    def empty(self) -> bool:
        return self._queue.empty()

    def full(self) -> bool:
        return self._queue.full()

    def task_done(self):
        self._queue.task_done()

    def exists(self, request_id: str) -> bool:
        """Check if a request with this ID is already in the backlog."""
        return request_id in self._ids

    async def push(self, request: MediaRequestDTO, request_type: RequestType, request_id: str) -> bool:
        """
        Try to enqueue.  Returns False if queue is full or duplicate.
        """
        if request_id in self._ids:
            return False

        try:
            self._queue.put_nowait((request, request_type, request_id))
        except asyncio.QueueFull:
            return False

        self._ids.add(request_id)
        return True

    async def pop(self) -> tuple[MediaRequestDTO, RequestType, str]:
        """
        Wait for the next request, remove its ID from the lookup, and return it.
        """
        request, request_type, request_id = await self._queue.get()
        self._ids.discard(request_id)
        return request, request_type, request_id
