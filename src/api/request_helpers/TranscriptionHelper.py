import whisper
from pathlib import Path

from src.api.request_helpers.BaseHelper import BaseHelper
from src.api.video.utils import get_transcription_filename
from src.config.ConfigParser import ConfigParser
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)

class TranscriptionHelper(BaseHelper):
    _model: whisper.Whisper

    def __init__(self):
        super().__init__("transcriber")

    async def init(self, app_config: ConfigParser):
        """Preloads the given model into memory"""
        logger.info(f"Loading {app_config.transcription.model} model...")
        self._model = whisper.load_model(app_config.transcription.model, in_memory=True)
        logger.info(f"{app_config.transcription.model.capitalize()} model loaded!")

    def transcribe(self, file_path: Path) -> Path:
        if self._model is None:
            raise RuntimeError("Model was not loaded when 'transcribe' was called. Use 'load_model' first")
        result = self._model.transcribe(str(file_path))
        out_path: Path = file_path.parent / get_transcription_filename()
        with open(out_path, "w") as f:
            f.write(result["text"] or "No words detected")
        return out_path
