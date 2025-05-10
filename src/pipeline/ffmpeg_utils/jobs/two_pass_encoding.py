import ffmpeg

from src.app_config import app_config
from src.pipeline.types import VideoStream, AudioStream, OutputFilePath
from src.constants import NULL_PATH, PASSLOG_PATH


async def two_pass_encoding(video_stream: VideoStream, audio_stream: AudioStream, out_path: OutputFilePath) -> None:
    first_pass_params = {
        "vcodec": app_config.ffmpeg.codecs.video,
        "preset": app_config.ffmpeg.preset,
        "video_bitrate": f"{app_config.ffmpeg.quality.video_bitrate}k",
        "pass": 1,
        "passlogfile": PASSLOG_PATH,
        "f": "mp4",
        "an": None,
        "y": None
    }
    ffmpeg \
        .output(video_stream, str(NULL_PATH), **first_pass_params) \
        .run()

    second_pass_params = {
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
        .output(video_stream, audio_stream, str(out_path), **second_pass_params) \
        .run()