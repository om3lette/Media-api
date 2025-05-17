from pydantic import Field

from src.config.schemas.base_enum_model import BaseEnumModel
from src.pipeline.enums import WhisperModelType


class TranscriptionSchema(BaseEnumModel):
    model: WhisperModelType = Field(default=WhisperModelType.TURBO)
