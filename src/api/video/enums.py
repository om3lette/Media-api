from enum import StrEnum


class VideoRequestType(StrEnum):
    COMPRESS = "video_compress"
    TRANSCRIBE = "video_transcribe"
    EXTRACT_AUDIO = "video_extract_audio"
    SUMMARIZE = "video_summarize"
    CUSTOM = "video_custom"
    UTILITY = "video_util" # Used for preprocessors which can only be called as a dependency of another task
