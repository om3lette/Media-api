from pydantic import Field

from backend.src.api.common.enums import FileToTextLanguages, FileToTextModels
from backend.src.api.common.schemas import MediaRequestSchema
from backend.src.config.schemas.base_enum_model import BaseEnumModel


class FileToTextSettings(BaseEnumModel):
    image_model: FileToTextModels = Field(default=FileToTextModels.TESSERACT)
    language: FileToTextLanguages = Field(default=FileToTextLanguages.RU)
    min_confidence: int = Field(default=60)


class FileToTextConfig(BaseEnumModel):
    file_to_text: FileToTextSettings = Field(default_factory=FileToTextSettings)


class FileToTextSchema(MediaRequestSchema):
    config: FileToTextConfig = Field(default_factory=FileToTextConfig)
