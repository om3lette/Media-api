from pathlib import Path

import pytesseract
from PIL import Image

from src.api.common.enums import FileToTextLanguages, RequestHelpersNames
from src.api.common.request_helpers.base_helper import BaseHelper
from src.api.common.schemas.requests import FileToTextConfig
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class TesseractHelper(BaseHelper):
    def __init__(self):
        super().__init__(RequestHelpersNames.TESSERACT)

    @staticmethod
    def image_to_text(
        config: FileToTextConfig, image_path: Path, save_path: Path
    ) -> None:
        language: str| None = (
            config.file_to_text.language
            if config.file_to_text.language != FileToTextLanguages.AUTO
            else None
        )
        with open(save_path, "w", encoding="UTF-8") as f:
            output: str = pytesseract.image_to_string(
                Image.open(image_path), lang=language
            )
            f.write(output)
