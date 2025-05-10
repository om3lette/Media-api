from typing import Union
from pathlib import Path

from src.api.video.constants import (
    OUT_FILE_EXTENSION,
    INPUT_FILENAME,
    OUT_FILENAME,
    AUDIO_FILENAME,
    OUT_AUDIO_FILE_EXTENSION,
    OUT_TRANSCRIPTION_FILE_EXTENSION,
    TRANSCRIPTION_FILENAME,
    SUMMARY_FILENAME,
    OUT_SUMMARY_FILE_EXTENSION,
)
from src.constants import DATA_FOLDER, OUT_FOLDER


def file_path_from_name(
    base_path: Union[DATA_FOLDER, OUT_FOLDER],
    request_id: str,
    filename: str,
    file_extension: str,
) -> Path:
    return base_path / request_id / (filename + "." + file_extension)


def request_data_dir_from_id(request_id: str):
    return DATA_FOLDER / request_id


def request_out_dir_from_id(request_id: str):
    return OUT_FOLDER / request_id


def input_path_from_request_id(request_id: str, filename: str = INPUT_FILENAME) -> Path:
    return file_path_from_name(DATA_FOLDER, request_id, filename, OUT_FILE_EXTENSION)


def out_path_from_request_id(request_id: str, filename: str = OUT_FILENAME) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename, OUT_FILE_EXTENSION)


def audio_path_from_request_id(request_id: str, filename: str = AUDIO_FILENAME) -> Path:
    return file_path_from_name(
        OUT_FOLDER, request_id, filename, OUT_AUDIO_FILE_EXTENSION
    )


def get_audio_filename() -> str:
    return AUDIO_FILENAME + "." + OUT_AUDIO_FILE_EXTENSION


def transcription_path_from_request_id(
    request_id: str, filename: str = TRANSCRIPTION_FILENAME
) -> Path:
    return file_path_from_name(
        OUT_FOLDER, request_id, filename, OUT_TRANSCRIPTION_FILE_EXTENSION
    )


def get_transcription_filename() -> str:
    return TRANSCRIPTION_FILENAME + "." + OUT_TRANSCRIPTION_FILE_EXTENSION


def get_summary_filename() -> str:
    return SUMMARY_FILENAME + "." + OUT_SUMMARY_FILE_EXTENSION
