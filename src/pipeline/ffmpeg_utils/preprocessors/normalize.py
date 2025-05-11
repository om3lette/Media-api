from src.api.video.schemas.requests.Compress import CompressConfig
from src.pipeline.types import VideoStream, AudioStream


async def normalize(
    config: CompressConfig, video_stream: VideoStream, audio_stream: AudioStream
) -> tuple[VideoStream, AudioStream]:
    filtered_video: VideoStream = video_stream.filter(
        "scale", config.video.width, config.video.height, flags="lanczos"
    ).filter("fps", config.video.fps)
    normalized_audio: AudioStream = audio_stream.filter(
        "loudnorm", i="-16", lra="11", tp="-1.5"
    )

    return filtered_video, normalized_audio
