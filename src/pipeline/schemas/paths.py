from pathlib import Path
from dataclasses import dataclass

from src.api.common.utils import (
    input_path_from_request_id,
    out_path_from_request_id,
    request_data_dir_from_id,
    request_out_dir_from_id,
    transcription_path_from_request_id,
    summary_path_from_request_id,
    audio_path_from_request_id,
)
from src.api.video.constants import OUT_FILE_EXTENSION, OUT_AUDIO_FILE_EXTENSION


@dataclass
class PathsSchema:
    raw_path: Path

    out_path: Path
    audio_path: Path
    transcription_path: Path
    summary_path: Path

    data_dir: Path
    out_dir: Path

    def __init__(
        self,
        raw_suffix: str,
        request_id: str,
        out_suffix=OUT_FILE_EXTENSION,
        audio_suffix=OUT_AUDIO_FILE_EXTENSION,
    ):
        self.raw_path = input_path_from_request_id(request_id, extension=raw_suffix)

        self.out_path = out_path_from_request_id(request_id, extension=out_suffix)
        self.audio_path = audio_path_from_request_id(request_id, extension=audio_suffix)

        self.transcription_path = transcription_path_from_request_id(request_id)
        self.summary_path = summary_path_from_request_id(request_id)

        self.data_dir = request_data_dir_from_id(request_id)
        self.out_dir = request_out_dir_from_id(request_id)
