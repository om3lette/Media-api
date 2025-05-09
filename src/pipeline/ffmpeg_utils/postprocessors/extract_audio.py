import ffmpeg

from src.api.video.utils import get_audio_filename
from src.app_config import app_config
from src.pipeline.ffmpeg_utils.utils import get_streams_from_file
from src.pipeline.types import OutputFilePath

async def extract_audio(out_path: OutputFilePath) -> None:
    video_stream, audio_stream = get_streams_from_file(out_path)
    ffmpeg \
        .output(
            audio_stream,
            str(out_path.parent / get_audio_filename()),
            vn=None,
            acodec=app_config.ffmpeg.codecs.audio,
            y=None
        ) \
        .run()
