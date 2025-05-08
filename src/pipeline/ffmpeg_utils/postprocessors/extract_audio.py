from pathlib import Path

import ffmpeg

from src.app_config import app_config
from src.api.video.utils import get_audio_filename
from src.pipeline.ffmpeg_utils.utils import get_streams_from_file
from src.pipeline.types import OutputFilePath

def extract_audio(out_path: OutputFilePath) -> bool:
    video_stream, audio_stream = get_streams_from_file(out_path)
    ffmpeg \
        .output(
            audio_stream,
            str(out_path.parent / get_audio_filename()),
            vn=None,
            acodec='copy',
            y=None
        ) \
        .run()
    return True
