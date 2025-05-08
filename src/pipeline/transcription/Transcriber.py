import whisper
import logging
import os
from pathlib import Path

from src.api.video.utils import get_transcription_filename

logger = logging.getLogger(os.path.basename(__file__))

class Transcriber:
    _model: whisper.Whisper

    def load_model(self, model_name: str):
        """Preloads the given model into memory"""
        logger.info(f"Loading {model_name} model...")
        self._model = whisper.load_model(model_name, in_memory=True)
        logger.info(f"{model_name} model loaded!")

    def transcribe(self, file_path: Path) -> Path:
        if self._model is None:
            raise RuntimeError("Model was not loaded when 'transcribe' was called. Use 'load_model' first")
        result = self._model.transcribe(str(file_path))
        out_path: Path = file_path.parent / get_transcription_filename()
        with open(out_path, "w") as f:
            f.write(result["text"] or "No words detected")
        return out_path
