from .compress import CompressSchema, CompressConfig
from .file_to_text import FileToTextConfig, FileToTextSchema
from .transcribe import TranscribeSchema, TranscribeConfig
from .summarize import SummarizeSchema, SummarizeConfig
from .extract_audio import ExtractAudioSchema, ExtractAudioConfig
from .custom import CustomSchema, CustomConfig


class RequestsMapping:
    summarize = SummarizeSchema
    compress = CompressSchema
    transcribe = TranscribeSchema
    extract_audio = ExtractAudioSchema
    file_to_text = FileToTextSchema
    custom = CustomSchema
