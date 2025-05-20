import uuid
from dataclasses import dataclass
from pathlib import Path

from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl, field_validator


class MediaRequestSchema(BaseModel):
    url: HttpUrl | Path | None = Field(default=None)
    config: dict[str, BaseModel]

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: HttpUrl | Path | None) -> HttpUrl | Path | None:
        if value is None or isinstance(value, Path):
            return value
        split_path: list[str] = value.path.split("/")
        if (
            value.host != "disk.yandex.ru"
            or len(split_path) != 3
            or not split_path[-2].isalpha()
            or len(split_path[-1]) != 14
        ):
            raise ValueError("Invalid Yandex Disk URL format")
        return value

    def get_request_id(self) -> str:
        """
        Extracts id from url if present, otherwise generates it using uuid4
        """
        if not self.url or isinstance(self.url, Path):
            return uuid.uuid4().hex
        # pylint: disable=no-member
        return self.url.path.split("/")[-1]
        # pylint: enable=no-member


@dataclass
class MediaRequestDTO:
    request: MediaRequestSchema
    file: UploadFile | None
