from .requests import (
    SummarizeSchema,
    CompressSchema,
    TranscribeSchema,
    ExtractAudioSchema,
    CustomSchema,
)


class VideoRequests:
    summarize = SummarizeSchema
    compress = CompressSchema
    transcribe = TranscribeSchema
    extract_audio = ExtractAudioSchema
    custom = CustomSchema
