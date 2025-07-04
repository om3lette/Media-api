from pathlib import Path

import whisper

from backend.src.api.common.enums import RequestHelpersNames, TranscribeLanguages
from backend.src.api.common.request_helpers.base_helper import BaseHelper
from backend.src.api.common.schemas.requests.transcribe import TranscribeConfig
from backend.src.config.config_parser import ConfigParser
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


class TranscriptionHelper(BaseHelper):
    _model: whisper.Whisper

    def __init__(self):
        super().__init__(RequestHelpersNames.TRANSCRIPTION)

    async def init(self, app_config: ConfigParser):
        """Preloads the given model into memory"""
        logger.info("Loading %s model...", app_config.transcription.model)
        self._model = whisper.load_model(app_config.transcription.model, in_memory=True)
        logger.info("%s model loaded!", app_config.transcription.model.capitalize())

    def transcribe(
        self, config: TranscribeConfig, file_path: Path, save_path: Path
    ) -> None:
        if self._model is None:
            raise RuntimeError(
                "Model was not loaded when 'transcribe' was called. Use 'load_model' first"
            )
        selected_language: str | None = (
            config.transcribe.language
            if config.transcribe.language != TranscribeLanguages.AUTO
            else None
        )
        result = self._model.transcribe(
            str(file_path), verbose=False, language=selected_language
        )
        with open(save_path, "w", encoding="UTF-8") as f:
            f.write(result["text"] or "No words detected")
