import asyncio

from backend.src.api.common.schemas.media_request import MediaRequestDTO
from backend.src.api.common.types.request import GeneralRequestType
from backend.src.api.tasks_handlers.constants import MAX_REQUESTS_BACKLOG


class RequestQueue:
    def __init__(self, maxsize: int = MAX_REQUESTS_BACKLOG):
        self._queue: asyncio.Queue[tuple[MediaRequestDTO, GeneralRequestType, str]] = (
            asyncio.Queue(maxsize)
        )
        # for quick existence checks or de‐duplication
        self._ids: set[str] = set()

    def to_list(self) -> list[tuple[MediaRequestDTO, GeneralRequestType, str]]:
        """
        Returns a list representation of the queue.\n
        Queue is cleared as a result
        """
        entries: list[tuple[MediaRequestDTO, GeneralRequestType, str]] = []
        while not self._queue.empty():
            entries.append(self._queue.get_nowait())
            self._queue.task_done()
        return entries

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

    async def push(
        self,
        request: MediaRequestDTO,
        request_type: GeneralRequestType,
        request_id: str,
    ) -> bool:
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

    async def pop(self) -> tuple[MediaRequestDTO, GeneralRequestType, str]:
        """
        Wait for the next request, remove its ID from the lookup, and return it.
        """
        request, request_type, request_id = await self._queue.get()
        self._ids.discard(request_id)
        return request, request_type, request_id
