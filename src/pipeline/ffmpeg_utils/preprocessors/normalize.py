from src.pipeline.types import VideoStream, AudioStream

def normalize(video_stream: VideoStream, audio_stream: AudioStream) -> tuple[VideoStream, AudioStream]:
    filtered_video: VideoStream = (
        video_stream
        .filter('scale', 1920, 1080, flags='lanczos')
        .filter('fps', 24)
    )
    normalized_audio: AudioStream = (
        audio_stream
        .filter('loudnorm', i='-16', lra='11', tp='-1.5')
    )

    return filtered_video, normalized_audio