import ffmpeg

from src.app_config import app_config
from src.pipeline.types import VideoStream, AudioStream, OutputFilePath
from src.constants import NULL_PATH, PASSLOG_PATH


def preflight(video_stream: VideoStream, audio_stream: AudioStream, out_path: OutputFilePath) -> bool:
    params = {
        "vcodec":  app_config.ffmpeg.codecs.video,
        "preset": app_config.ffmpeg.preset,
        "video_bitrate": f"{app_config.ffmpeg.quality.video_bitrate}k",
        "pass": 1,
        "passlogfile": PASSLOG_PATH,
        "f": "mp4",
        "an": None,
        "y": None
    }
    ffmpeg \
        .output(video_stream, str(NULL_PATH), **params) \
        .run()
    return True