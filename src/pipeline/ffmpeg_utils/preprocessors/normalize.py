from src.app_config import app_config
from src.pipeline.types import VideoStream, AudioStream


async def normalize(
    video_stream: VideoStream, audio_stream: AudioStream
) -> tuple[VideoStream, AudioStream]:
    filtered_video: VideoStream = video_stream.filter(
        "scale",
        app_config.ffmpeg.quality.width,
        app_config.ffmpeg.quality.height,
        flags="lanczos",
    ).filter("fps", app_config.ffmpeg.fps)
    normalized_audio: AudioStream = audio_stream.filter(
        "loudnorm", i="-16", lra="11", tp="-1.5"
    )

    return filtered_video, normalized_audio
