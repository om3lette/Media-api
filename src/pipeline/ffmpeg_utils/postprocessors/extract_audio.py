import ffmpeg

from pathlib import Path

from src.api.video.schemas.requests.ExtractAudio import ExtractAudioConfig
from src.pipeline.ffmpeg_utils.utils import get_streams_from_file


async def extract_audio(
    config: ExtractAudioConfig, video_path: Path, save_path: Path
) -> None:
    video_stream, audio_stream = get_streams_from_file(video_path)
    ffmpeg.output(
        audio_stream, filename=save_path, vn=None, acodec=config.audio.codec, y=None
    ).run()
