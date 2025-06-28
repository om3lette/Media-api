from enum import StrEnum
from typing import Union

from backend.src.api.tasks_handlers.enums import (
    AudioActions,
    ImageActions,
    TextActions,
    VideoActions,
)


class GeneralRequestType(StrEnum):
    COMPRESS = "compress"
    TRANSCRIBE = "transcribe"
    EXTRACT_AUDIO = "extract_audio"
    SUMMARIZE = "summarize"
    CUSTOM = "custom"
    FILE_TO_TEXT = "extract_text"


CustomRequestActions = Union[VideoActions, AudioActions, ImageActions, TextActions]
