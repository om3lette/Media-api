from pathlib import Path

import ffmpeg

from src.api.video.utils import get_audio_filename
from src.pipeline.ffmpeg_utils.utils import get_streams_from_file
from src.pipeline.types import OutputFilePath

def extract_audio(out_path: OutputFilePath) -> bool:
    video_stream, audio_stream = get_streams_from_file(out_path)
    ffmpeg \
        .output(
            audio_stream,
            str(out_path.parent / get_audio_filename()),
            acodec='libmp3lame',
            audio_bitrate='330k',
            ar="44100"
        ) \
        .run(overwrite_output=True)
    return True
