from pathlib import Path
from dataclasses import dataclass

from src.api.common.utils import (
    out_path_from_request_id,
    request_data_dir_from_id,
    request_out_dir_from_id,
    transcription_path_from_request_id,
    summary_path_from_request_id,
    audio_path_from_request_id,
)
from src.config.enums import VideoCodecs, AudioCodecs
from src.pipeline.suffix_utils import (
    get_suffix_by_video_codec,
    get_suffix_by_audio_codec,
)


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
        input_path: Path,
        request_id: str,
        video_codec: VideoCodecs,
        audio_codec: AudioCodecs,
    ):
        self.raw_path = input_path
        self.out_path = out_path_from_request_id(
            request_id, extension=get_suffix_by_video_codec(video_codec)
        )
        self.audio_path = audio_path_from_request_id(
            request_id, extension=get_suffix_by_audio_codec(audio_codec)
        )

        self.transcription_path = transcription_path_from_request_id(request_id)
        self.summary_path = summary_path_from_request_id(request_id)

        self.data_dir = request_data_dir_from_id(request_id)
        self.out_dir = request_out_dir_from_id(request_id)
