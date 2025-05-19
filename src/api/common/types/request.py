from enum import StrEnum
from typing import Union

from src.api.tasks_handlers.enums import VideoRequestType, AudioRequestType


class GeneralRequestType(StrEnum):
    COMPRESS = "compress"
    TRANSCRIBE = "transcribe"
    EXTRACT_AUDIO = "extract_audio"
    SUMMARIZE = "summarize"
    CUSTOM = "custom"


RequestType = Union[VideoRequestType, AudioRequestType]
