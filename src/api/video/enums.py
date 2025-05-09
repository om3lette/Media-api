from enum import IntEnum, StrEnum

class VideoRequestType(StrEnum):
    COMPRESS = "compress"
    COMPRESS_AND_TRANSCRIBE = "compress&transcribe"

class VideoProcessCodes(IntEnum):
    OK = 0
    QUEUE_FULL = 1
    ALREADY_QUEUED = 2
    ALREADY_PROCESSED = 3
    UNKNOWN_ERROR = 4
    FILE_NOT_FOUND = 5

class FileRetrievalCodes(IntEnum):
    OK = 0
    NOT_FOUND = 1