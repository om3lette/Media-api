import json
import sqlite3

import threading
from datetime import datetime
from typing import Any

from backend.src.api.common.io.request_type_to_schema import request_type_to_schema
from backend.src.api.common.schemas.media_request import MediaRequestDTO
from backend.src.api.common.types.request import GeneralRequestType


class RequestsRepository:
    # Status constants
    QUEUED = 0
    PROCESSING = 1
    FINISHED = 2
    DONE_PARTIALLY = 3
    CANCELED = 4
    DELETED = 5

    _SCHEMA = """
        CREATE TABLE IF NOT EXISTS requests (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            ext_id        TEXT    UNIQUE NOT NULL,
            start_time    TEXT    NULL,
            end_time      TEXT    NULL,
            status        INTEGER NOT NULL DEFAULT 0,
            request_type  TEXT    NOT NULL,
            config        TEXT    NOT NULL CHECK(json_valid(config)),
            input_type    TEXT    NOT NULL CHECK(input_type IN ('path','url','blob')),
            input_value   TEXT    NOT NULL
        );
    """

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self._lock = threading.Lock()
        self._initialize()

    def _initialize(self) -> None:
        with self._lock:
            self.conn.executescript(self._SCHEMA)
            self.conn.commit()

    def is_subscribable(self, request_id: str) -> bool:
        status = self.get_request_status(request_id)
        if status is None:
            return False
        return status["end_time"] is None

    def add_request(self, request_id: str, request_type, dto: MediaRequestDTO) -> int:
        sql = """
            INSERT OR REPLACE INTO requests (ext_id, request_type, input_type, input_value, config)
            VALUES (?, ?, ?, ?, ?);
        """
        input_type: str = "path"
        input_value: str = str(dto.request.path)
        if dto.file:
            input_type = "blob"
            input_value = ""
        elif dto.request.url:
            input_type = "url"
            input_value = str(dto.request.url)
        with self._lock:
            cur = self.conn.execute(
                sql,
                (
                    request_id,
                    request_type,
                    input_type,
                    input_value,
                    dto.request.config.model_dump_json(),
                ),
            )
            self.conn.commit()
            return cur.lastrowid

    def get_request_status(self, request_id: str) -> dict | None:
        sql = "SELECT status, start_time, end_time FROM requests WHERE ext_id = ?"
        with self._lock:
            row = self.conn.execute(sql, (request_id,)).fetchone()
        if not row:
            return None
        fmt = "%Y-%m-%d %H:%M:%S"
        start_time = datetime.strptime(row[1], fmt) if row[1] else None
        end_time = datetime.strptime(row[2], fmt) if row[2] else None

        return {"status": int(row[0]), "start_time": start_time, "end_time": end_time}

    def processing_started(self, request_id: str):
        sql = "UPDATE requests SET status = ?, start_time = datetime('now', 'localtime') WHERE ext_id = ?"
        with self._lock:
            self.conn.execute(sql, (self.PROCESSING, request_id))
            self.conn.commit()

    def update_status(self, request_id: str, status: int) -> None:
        parts = ["status = ?"]
        params: list[Any] = [status]
        if status in (self.FINISHED, self.DONE_PARTIALLY, self.CANCELED):
            parts.append("end_time = datetime('now')")
        params.append(request_id)
        sql = f"UPDATE requests SET {', '.join(parts)} WHERE ext_id = ?;"
        with self._lock:
            self.conn.execute(sql, params)
            self.conn.commit()

    def get_pending_requests(self) -> list[tuple[str, str, MediaRequestDTO]]:
        sql = """
            SELECT * FROM requests
            WHERE status = ?
            ORDER BY start_time ASC;
        """
        with self._lock:
            rows = self.conn.execute(sql, (self.QUEUED,)).fetchall()
        return [
            (
                row["ext_id"],
                row["request_type"],
                MediaRequestDTO(
                    request=request_type_to_schema(
                        GeneralRequestType(row["request_type"])
                    ).model_validate(
                        {
                            "url": row["input_value"]
                            if row["input_type"] == "url"
                            else None,
                            "path": row["input_value"]
                            if row["input_type"] == "path"
                            else None,
                            "config": json.loads(row["config"]),
                        },
                        strict=False,
                    ),
                    file="tmp" if row["input_type"] == "blob" else None,
                ),
            )
            for row in map(lambda row: dict(row), rows)
        ]

    def get_expired_requests(self, cutoff_hours: float) -> list[dict[str, Any]]:
        sql = """
            SELECT id, ext_id FROM requests
            WHERE end_time <= datetime('now', ?);
        """
        interval = f"-{cutoff_hours} hours"
        with self._lock:
            return self.conn.execute(sql, (interval,)).fetchall()

    def delete_requests(self, ids: list[str]) -> None:
        if not ids:
            return
        placeholders = ",".join("?" for _ in ids)
        sql = f"DELETE FROM requests WHERE ext_id IN ({placeholders});"
        with self._lock:
            self.conn.execute(sql, ids)
            self.conn.commit()
