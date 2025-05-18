from datetime import timedelta

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

    @field_validator("bitrate", mode="before")
    @classmethod
    def parse_bitrate(cls, v):
        if v == "N/A":
            return 0
        return float(v.replace("kbits/s", ""))

    @field_validator("speed", mode="before")
    @classmethod
    def parse_speed(cls, v):
        if v == "N/A":
            return 0
        return float(v.replace("x", ""))

    @field_validator("out_time", mode="before")
    @classmethod
    def parse_out_time(cls, v):
        # Remove milliseconds and parse
        h, m, s = map(int, v[:-7].split(":"))
        return timedelta(hours=h, minutes=m, seconds=s)
