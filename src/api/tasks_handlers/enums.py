from enum import StrEnum


class VideoActions(StrEnum):
    COMPRESS = "compress"
    TRANSCRIBE = "transcribe"
    EXTRACT_AUDIO = "extract_audio"
    SUMMARIZE = "summarize"


class AudioActions(StrEnum):
    TRANSCRIBE = "transcribe"
    SUMMARIZE = "summarize"
    EXTRACT_AUDIO = "extract_audio"


class ImageActions(StrEnum):
    TO_TEXT = "to_text"


class VideoRequestType(StrEnum):
    COMPRESS = "video_compress"
    TRANSCRIBE = "video_transcribe"
    EXTRACT_AUDIO = "video_extract_audio"
    SUMMARIZE = "video_summarize"
    CUSTOM = "video_custom"
    # Used for preprocessors which can only be called as a dependency of another task
    UTILITY = "video_util"
