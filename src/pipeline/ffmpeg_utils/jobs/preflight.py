import ffmpeg
from src.pipeline.types import VideoStream, AudioStream, OutputFilePath
from src.constants import NULL_PATH

def preflight(video_stream: VideoStream, audio_stream: AudioStream, out_path: OutputFilePath) -> bool:
    ffmpeg \
        .output(
            video_stream,
            audio_stream,
            str(NULL_PATH),
            vcodec='libx265',
            preset='medium',
            b='2500k',
            an=None,
            f="null",
        ) \
        .global_args('-x265-params', 'pass=1') \
        .run()
    return True