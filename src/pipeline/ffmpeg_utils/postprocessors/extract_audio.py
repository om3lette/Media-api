import ffmpeg

from pathlib import Path

from src.app_config import app_config
from src.pipeline.ffmpeg_utils.utils import get_streams_from_file

async def extract_audio(video_path: Path, save_path: Path) -> None:
    video_stream, audio_stream = get_streams_from_file(video_path)
    ffmpeg \
        .output(
            audio_stream,
            filename=save_path,
            vn=None,
            acodec=app_config.ffmpeg.codecs.audio,
            y=None
        ) \
        .run()
