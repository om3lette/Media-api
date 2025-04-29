from typing import Union
from pathlib import Path

from src.api.video.constants import OUT_FILE_EXTENSION, INPUT_FILENAME, OUT_FILENAME
from src.constants import DATA_FOLDER, OUT_FOLDER

def file_path_from_name(base_path: Union[DATA_FOLDER, OUT_FOLDER], request_id: str, filename: str) -> Path:
    return base_path / request_id / (filename + "." + OUT_FILE_EXTENSION)

def input_path_from_name(request_id: str, filename: str = INPUT_FILENAME) -> Path:
    return file_path_from_name(DATA_FOLDER, request_id, filename)

def out_path_from_name(request_id: str, filename: str = OUT_FILENAME) -> Path:
    return file_path_from_name(OUT_FOLDER, request_id, filename)
