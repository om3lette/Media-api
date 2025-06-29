from enum import IntEnum


class ValidationStatusCode(IntEnum):
    OK = 0
    REQUEST_NOT_FOUND = 1
    SUB_NOT_ACCEPTED = 2
    ALREADY_SUBSCRIBED = 3
    NOT_SUBSCRIBED = 4
