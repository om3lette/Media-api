import json

from redis.asyncio import Redis


class ProgressHandler:
    def __init__(self, redis_client: Redis, ttl_seconds):
        self.redis = redis_client
        self.status_ttl = ttl_seconds

    @staticmethod
    def __get_key_by_id(request_id: str):
        return f"progress:{request_id}"

    @staticmethod
    def get_status_key_by_id(request_id: str):
        return f"status:{request_id}"

    async def init_progress(self, request_id: str, total_stages: int) -> None:
        await self.redis.hset(
            self.__get_key_by_id(request_id),
            mapping={"total_stages": total_stages, "cur_stage": 0, "pct": 0},
        )

    async def update_stage(self, request_id, new_stage: int) -> None:
        key: str = self.__get_key_by_id(request_id)
        payload = {"cur_stage": new_stage}

        pipe = self.redis.pipeline()
        pipe.hset(key, mapping=payload)
        pipe.expire(key, self.status_ttl)
        pipe.publish(self.get_status_key_by_id(request_id), json.dumps(payload))

        await pipe.execute()

    async def update_progress(self, request_id, percentage: int) -> None:
        key: str = self.__get_key_by_id(request_id)
        payload = {"pct": percentage}

        pipe = self.redis.pipeline()
        pipe.hset(key, mapping=payload)
        pipe.expire(key, self.status_ttl)
        pipe.publish(
            self.get_status_key_by_id(request_id), json.dumps(payload)
        )
        await pipe.execute()

    async def request_finished(self, request_id: str, status_code: int) -> None:
        payload = {"status": status_code}
        await self.redis.publish(
            self.get_status_key_by_id(request_id), json.dumps(payload)
        )

    async def get_progress_data(self, request_id: str) -> dict[str, int]:
        raw = await self.redis.hgetall(self.__get_key_by_id(request_id))
        if raw is None:
            return {}
        return {
            "cur_stage": int(raw.get("cur_stage", -1)),
            "total_stages": int(raw.get("total_stages", -1)),
            "pct": int(raw.get("pct", 0)),
        }
