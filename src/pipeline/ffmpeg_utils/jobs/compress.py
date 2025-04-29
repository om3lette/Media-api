import ffmpeg
from src.pipeline.types import VideoStream, AudioStream, OutputFilePath

def compress(video_stream: VideoStream, audio_stream: AudioStream, out_path: OutputFilePath) -> bool:
    ffmpeg \
        .output(
            video_stream,
            audio_stream,
            str(out_path),
            vcodec='libx265',
            preset='medium',
            video_bitrate='2500k',
            acodec='aac',
            audio_bitrate='330k'
        ) \
        .global_args('-x265-params', 'pass=2') \
        .run(overwrite_output=True)
    return True
