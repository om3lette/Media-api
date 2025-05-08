import ffmpeg
from pathlib import Path

from src.pipeline.types import VideoStream, AudioStream


def get_streams_from_file(file_path: Path) -> tuple[VideoStream, AudioStream]:
    ffmpeg_input = ffmpeg.input(file_path)
    return ffmpeg_input.video, ffmpeg_input.audio
