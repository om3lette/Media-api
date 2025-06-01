import shutil
from pathlib import Path

from src.api.tasks_handlers.constants import (
    AUDIO_FILENAME,
    INPUT_FILENAME,
    OUT_AUDIO_FILE_EXTENSION,
    OUT_FILE_EXTENSION,
    OUT_FILENAME,
    OUT_SUMMARY_FILE_EXTENSION,
    OUT_TRANSCRIPTION_FILE_EXTENSION,
    SUMMARY_FILENAME,
    TRANSCRIPTION_FILENAME,
)
from src.constants import ARCHIVE_FORMAT, DATA_FOLDER, OUT_FOLDER


def request_archive_from_id(request_id: str):
    return OUT_FOLDER / (str(request_id) + "." + ARCHIVE_FORMAT)


def archive_request_output(request_id: str, remove_folder: bool = False):
    shutil.make_archive(
        str(request_archive_from_id(request_id).with_suffix("")),
        ARCHIVE_FORMAT,
        request_out_dir_from_id(request_id),
    )
    if remove_folder:
        delete_request_data(request_id, delete_input=False)


def delete_request_data(
    request_id: str, delete_input: bool = True, delete_output: bool = True
):
    if delete_input:
        shutil.rmtree(request_data_dir_from_id(request_id))
    if delete_output:
        shutil.rmtree(request_out_dir_from_id(request_id))


def file_path_from_name(
    base_path: Path, request_id: str, filename: str, file_extension: str
) -> Path:
    return base_path / request_id / (filename + "." + file_extension)


def request_data_dir_from_id(request_id: str):
    return DATA_FOLDER / request_id


def request_out_dir_from_id(request_id: str):
    return OUT_FOLDER / request_id


def input_path_from_request_id(
    request_id: str, filename: str = INPUT_FILENAME, extension: str = OUT_FILE_EXTENSION
) -> Path:
    return file_path_from_name(DATA_FOLDER, request_id, filename, extension)


def out_path_from_request_id(
    request_id: str, filename: str = OUT_FILENAME, extension: str = OUT_FILE_EXTENSION
) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename, extension)


def audio_path_from_request_id(
    request_id: str, filename: str = AUDIO_FILENAME, extension=OUT_AUDIO_FILE_EXTENSION
) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename, extension)


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


def summary_path_from_request_id(request_id: str, filename: str = SUMMARY_FILENAME):
    return file_path_from_name(
        OUT_FOLDER, request_id, filename, OUT_SUMMARY_FILE_EXTENSION
    )
