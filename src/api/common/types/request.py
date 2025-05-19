from enum import StrEnum
from typing import Union

from src.api.audio.enums import AudioRequestType
from src.api.video.enums import VideoRequestType


class GeneralRequestType(StrEnum):
    COMPRESS = "compress"
    TRANSCRIBE = "transcribe"
    EXTRACT_AUDIO = "extract_audio"
    SUMMARIZE = "summarize"
    CUSTOM = "custom"

RequestType = Union[VideoRequestType, AudioRequestType]
