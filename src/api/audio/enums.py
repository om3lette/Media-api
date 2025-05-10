from enum import StrEnum

class AudioRequestType(StrEnum):
    COMPRESS   = "audio_compress"
    TRANSCRIBE = "audio_transcribe"
    SUMMARIZE  = "audio_summarize"
    CUSTOM     = "audio_custom"
