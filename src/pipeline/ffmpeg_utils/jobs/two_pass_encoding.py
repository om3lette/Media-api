import ffmpeg

from src.api.video.schemas.requests.Compress import CompressConfig
from src.pipeline.types import VideoStream, AudioStream, OutputFilePath
from src.constants import NULL_PATH, PASSLOG_PATH


async def two_pass_encoding(
    config: CompressConfig,
    video_stream: VideoStream,
    audio_stream: AudioStream,
    out_path: OutputFilePath,
) -> None:
    first_pass_params = {
        "vcodec": config.codecs.video,
        "preset": config.preset,
        "video_bitrate": f"{config.quality.video_bitrate}k",
        "pass": 1,
        "passlogfile": PASSLOG_PATH,
        "f": "mp4",
        "an": None,
        "y": None,
    }
    ffmpeg.output(video_stream, str(NULL_PATH), **first_pass_params).run()

    second_pass_params = {
        "vcodec": config.codecs.video,
        "preset": config.preset,
        "video_bitrate": f"{config.quality.video_bitrate}k",
        "acodec": config.codecs.audio,
        "audio_bitrate": f"{config.quality.audio_bitrate}k",
        "ar": config.quality.audio_sample_rate,
        "pass": 2,
        "passlogfile": PASSLOG_PATH,
        "y": None,
    }
    ffmpeg.output(video_stream, audio_stream, str(out_path), **second_pass_params).run()
