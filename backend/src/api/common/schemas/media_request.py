from dataclasses import dataclass
from pathlib import Path

from camel_converter import to_camel
from fastapi import UploadFile
from pydantic import BaseModel, Field, HttpUrl, field_validator, ConfigDict


class MediaRequestSchema(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True, validate_by_alias=True, alias_generator=to_camel
    )

    url: HttpUrl | None = Field(default=None)
    path: Path | None = Field(default=None)
    config: dict[str, BaseModel]

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: HttpUrl | None) -> HttpUrl | None:
        if not value:
            return value

        split_path: list[str] = value.path.split("/")
        if (
            value.host not in ["disk.yandex.ru", "disk.360.yandex.ru"]
            or len(split_path) != 3
            or not split_path[-2].isalpha()
            or len(split_path[-1]) != 14
        ):
            raise ValueError("Invalid Yandex Disk URL format")
        return value


@dataclass
class MediaRequestDTO:
    request: MediaRequestSchema
    file: UploadFile | None
