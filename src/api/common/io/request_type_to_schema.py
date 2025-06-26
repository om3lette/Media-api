from src.api.common.schemas.requests import (
    CustomSchema,
    FileToTextSchema,
    CompressSchema,
    SummarizeSchema,
    TranscribeSchema,
    ExtractAudioSchema,
)
from src.api.common.types.request import GeneralRequestType


def request_type_to_schema(request_type: GeneralRequestType):
    if request_type == GeneralRequestType.CUSTOM:
        return CustomSchema
    if request_type == GeneralRequestType.FILE_TO_TEXT:
        return FileToTextSchema
    if request_type == GeneralRequestType.COMPRESS:
        return CompressSchema
    if request_type == GeneralRequestType.SUMMARIZE:
        return SummarizeSchema
    if request_type == GeneralRequestType.TRANSCRIBE:
        return TranscribeSchema
    if request_type == GeneralRequestType.EXTRACT_AUDIO:
        return ExtractAudioSchema
    raise NameError(f"No schema found for request_type: {request_type}")
