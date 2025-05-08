from pathlib import Path
from typing import Callable
from ffmpeg.nodes import FilterableStream

VideoStream = FilterableStream
AudioStream = FilterableStream

OutputFilePath = Path

Preprocessor = Callable[[VideoStream, AudioStream], tuple[VideoStream, AudioStream]]
Job = Callable[[VideoStream, AudioStream, OutputFilePath], bool]
Postprocessor = Callable[[OutputFilePath], any]
