from enum import StrEnum


class FfmpegPresets(StrEnum):
    ULTRAFAST = "ultrafast"
    SUPERFAST = "superfast"
    VERYFAST = "veryfast"
    FASTER = "faster"
    MEDIUM = "medium"
    SLOW = "slow"
    SLOWER = "slower"
    VERYSLOW = "veryslow"


class VideoCodecs(StrEnum):
    H264 = "libx264"
    H265 = "libx265"


class AudioCodecs(StrEnum):
    MP3 = "libmp3lame"
    AAC = "aac"


class GigachatModels(StrEnum):
    LITE = "GigaChat-2"
    PRO = "GigaChat-2-Pro"
    MAX = "GigaChat-2-Max"


class GigachatModelScopes(StrEnum):
    PERS = "GIGACHAT_API_PERS"
    B2B = "GIGACHAT_API_B2B"
    CORP = "GIGACHAT_API_CORP"
