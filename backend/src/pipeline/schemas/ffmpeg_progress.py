from datetime import timedelta
from typing import Callable

from pydantic import BaseModel, field_validator


class FFMPEGProgressSchema(BaseModel):
    bitrate: float = 0
    total_size: int = 0
    out_time_us: int = 0
    out_time_ms: int = 0
    out_time: timedelta = timedelta(0)
    dup_frames: int = 0
    drop_frames: int = 0
    speed: float = 0.0
    fps: float = 0.0
    progress: str = "continue"

    @staticmethod
    def __handle_na(
        v: str,
        default_value: int | float | timedelta,
        converter: Callable[[str], int | float | timedelta],
    ):
        if v == "N/A":
            return default_value
        return converter(v)

    @field_validator("bitrate", mode="before")
    @classmethod
    def parse_bitrate(cls, v):
        return cls.__handle_na(v, 0.0, lambda x: float(v.replace("kbits/s", "")))

    @field_validator("speed", mode="before")
    @classmethod
    def parse_speed(cls, v):
        return cls.__handle_na(v, 0.0, lambda x: float(v.replace("x", "")))

    @field_validator("out_time", mode="before")
    @classmethod
    def parse_out_time(cls, v):
        # Remove milliseconds and parse
        def str_to_timedelta(v: str):
            h, m, s = map(int, v[:-7].split(":"))
            return timedelta(hours=h, minutes=m, seconds=s)

        return cls.__handle_na(v, timedelta(0), str_to_timedelta)

    @field_validator("out_time_ms", "out_time_us", mode="before")
    @classmethod
    def parse_out_time_ms(cls, v):
        return cls.__handle_na(v, 0, int)
