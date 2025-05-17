from pathlib import Path

import whisper

from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers.base_helper import BaseHelper
from src.api.common.utils import get_transcription_filename
from src.api.video.schemas.requests.transcribe import TranscribeConfig
from src.config.config_parser import ConfigParser
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class TranscriptionHelper(BaseHelper):
    _model: whisper.Whisper

    def __init__(self):
        super().__init__(RequestHelpersNames.TRANSCRIPTION)

    async def init(self, app_config: ConfigParser):
        """Preloads the given model into memory"""
        logger.info("Loading %s model...", app_config.transcription.model)
        self._model = whisper.load_model(app_config.transcription.model, in_memory=True)
        logger.info("%s model loaded!", app_config.transcription.model.capitalize())

    def transcribe(self, config: TranscribeConfig, file_path: Path) -> Path:
        if self._model is None:
            raise RuntimeError(
                "Model was not loaded when 'transcribe' was called. Use 'load_model' first"
            )
        result = self._model.transcribe(str(file_path))
        out_path: Path = file_path.parent / get_transcription_filename()
        with open(out_path, "w", encoding="UTF-8") as f:
            f.write(result["text"] or "No words detected")
        return out_path
