from pathlib import Path
from typing import Callable
from ffmpeg.nodes import FilterableStream

VideoStream = FilterableStream
AudioStream = FilterableStream
OutputFilePath = Path

RawVideoFilePath = Path

FfmpegPreprocessor = Callable[[VideoStream, AudioStream], tuple[VideoStream, AudioStream]]
FfmpegJob = Callable[[VideoStream, AudioStream, OutputFilePath], bool]
