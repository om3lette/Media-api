from pathlib import Path
import ffmpeg

from src.pipeline.schemas.Streams import StreamsSchema


def get_streams_from_file(file_path: Path) -> StreamsSchema:
    ffmpeg_input = ffmpeg.input(file_path)
    return StreamsSchema(video=ffmpeg_input.video, audio=ffmpeg_input.audio)
