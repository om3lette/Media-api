from enum import IntEnum, StrEnum


class FileType(IntEnum):
    TEXT = 0
    DOCUMENT = 1
    VIDEO = 2
    AUDIO = 3
    IMAGE = 4
    EXECUTABLE = 5
    OTHER = 6


class RequestProcessCodes(IntEnum):
    OK = 0
    QUEUE_FULL = 1
    ALREADY_QUEUED = 2
    UNKNOWN_ERROR = 3
    FILE_NOT_FOUND = 4


class FileRetrievalCodes(IntEnum):
    OK = 0
    NOT_FOUND = 1


class FileHelperNames(StrEnum):
    YADISK = "yadisk"
    UPLOAD_FILE = "upload_file"


class RequestHelpersNames(StrEnum):
    GIGACHAT = "gigachat"
    TRANSCRIPTION = "transcriber"
    TESSERACT = "tesseract"


class FileToTextModels(StrEnum):
    TESSERACT = "tesseract"


class FileToTextLanguages(StrEnum):
    RU = "rus"
    ENG = "eng"
    AUTO = "auto"
