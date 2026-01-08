from pydantic import Field

from backend.src.config.schemas.base_enum_model import BaseEnumModel
from backend.src.pipeline.enums import WhisperModelType


class TranscriptionSchema(BaseEnumModel):
    model: WhisperModelType = Field(default=WhisperModelType.SMALL)
