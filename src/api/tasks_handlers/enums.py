from enum import StrEnum


class VideoActions(StrEnum):
    COMPRESS = "compress"
    TRANSCRIBE = "transcribe"
    EXTRACT_AUDIO = "extract_audio"
    SUMMARIZE = "summarize"


class VideoRequestType(StrEnum):
    COMPRESS = "video_compress"
    TRANSCRIBE = "video_transcribe"
    EXTRACT_AUDIO = "video_extract_audio"
    SUMMARIZE = "video_summarize"
    CUSTOM = "video_custom"
    # Used for preprocessors which can only be called as a dependency of another task
    UTILITY = "video_util"


class AudioRequestType(StrEnum):
    COMPRESS = "audio_compress"
    TRANSCRIBE = "audio_transcribe"
    SUMMARIZE = "audio_summarize"
    CUSTOM = "audio_custom"
