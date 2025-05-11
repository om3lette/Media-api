import uuid
from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, field_validator, HttpUrl, Field

from dataclasses import dataclass

class MediaRequestSchema(BaseModel):
    url: Optional[HttpUrl] = Field(default=None)
    config: dict[str, dict]

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: Optional[HttpUrl]) -> Optional[HttpUrl]:
        if value is None:
            return value
        """Checks url for the following pattern: https://disk.yandex.ru/[a-zA-Z]/<ID>"""
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
        if not self.url:
            return uuid.uuid4().hex
        return self.url.path.split("/")[-1]

@dataclass
class MediaRequestDTO:
    request: MediaRequestSchema
    file: Optional[UploadFile]
