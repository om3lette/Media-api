import ffmpeg

from src.app_config import app_config
from src.constants import PASSLOG_PATH
from src.pipeline.types import VideoStream, AudioStream, OutputFilePath

async def compress(video_stream: VideoStream, audio_stream: AudioStream, out_path: OutputFilePath) -> None:
    params = {
        "vcodec": app_config.ffmpeg.codecs.video,
        "preset": app_config.ffmpeg.preset,
        "video_bitrate": f"{app_config.ffmpeg.quality.video_bitrate}k",
        "acodec": app_config.ffmpeg.codecs.audio,
        "audio_bitrate": f"{app_config.ffmpeg.quality.audio_bitrate}k",
        "ar": app_config.ffmpeg.quality.audio_sample_rate,
        "pass": 2,
        "passlogfile": PASSLOG_PATH,
        "y": None
    }
    ffmpeg \
        .output(video_stream, audio_stream, str(out_path), **params) \
        .run()
