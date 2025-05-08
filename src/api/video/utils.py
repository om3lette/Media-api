from typing import Union
from pathlib import Path

from src.api.video.constants import OUT_FILE_EXTENSION, INPUT_FILENAME, OUT_FILENAME, AUDIO_FILENAME, \
    OUT_AUDIO_FILE_EXTENSION, OUT_TRANSCRIPTION_FILE_EXTENSION, TRANSCRIPTION_FILENAME
from src.constants import DATA_FOLDER, OUT_FOLDER

def file_path_from_name(
        base_path: Union[DATA_FOLDER, OUT_FOLDER],
        request_id: str,
        filename: str,
        file_extension: str
    ) -> Path:
    return base_path / request_id / (filename + "." + file_extension)

def input_path_from_request_id(request_id: str, filename: str = INPUT_FILENAME) -> Path:
    return file_path_from_name(DATA_FOLDER, request_id, filename, OUT_FILE_EXTENSION)

def out_path_from_request_id(request_id: str, filename: str = OUT_FILENAME) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename, OUT_FILE_EXTENSION)

def audio_path_from_request_id(request_id: str, filename: str = AUDIO_FILENAME) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename, OUT_AUDIO_FILE_EXTENSION)

def get_audio_filename() -> str:
    return AUDIO_FILENAME + "." + OUT_AUDIO_FILE_EXTENSION

def transcription_path_from_request_id(request_id: str, filename: str = TRANSCRIPTION_FILENAME) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename, OUT_TRANSCRIPTION_FILE_EXTENSION)

def get_transcription_filename() -> str:
    return TRANSCRIPTION_FILENAME + "." + OUT_TRANSCRIPTION_FILE_EXTENSION
