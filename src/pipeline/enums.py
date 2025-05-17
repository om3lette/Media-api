from enum import StrEnum


class WhisperModelType(StrEnum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    TURBO = "turbo"


class TaskType:
    PREPROCESSOR = 0
    JOB = 1
    POSTPROCESSOR = 2
