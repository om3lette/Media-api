from ...common.types import RequestHandler
from .requests import (
    SummarizeSchema,
    CompressSchema,
    TranscribeSchema,
    ExtractAudioSchema,
)

class VideoRequests:
    summarize = SummarizeSchema
    compress = CompressSchema
    transcribe = TranscribeSchema
    extract_audio = ExtractAudioSchema
