from dataclasses import dataclass
from pathlib import Path

from backend.src.api.common.utils import (
    audio_path_from_request_id,
    out_path_from_request_id,
    request_data_dir_from_id,
    request_out_dir_from_id,
    summary_path_from_request_id,
    transcription_path_from_request_id,
)
from backend.src.config.enums import AudioCodecs, VideoCodecs
from backend.src.pipeline.suffix_utils import (
    get_suffix_by_audio_codec,
    get_suffix_by_video_codec,
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
