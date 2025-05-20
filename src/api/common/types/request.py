from enum import StrEnum
from typing import Union

from src.api.tasks_handlers.enums import AudioActions, ImageActions, VideoActions


class GeneralRequestType(StrEnum):
    COMPRESS = "compress"
    TRANSCRIBE = "transcribe"
    EXTRACT_AUDIO = "extract_audio"
    SUMMARIZE = "summarize"
    CUSTOM = "custom"
    FILE_TO_TEXT = "extract_text"


CustomRequestActions = Union[VideoActions, AudioActions, ImageActions]
