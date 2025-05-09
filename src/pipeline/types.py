from pathlib import Path
from typing import Callable, Awaitable
from ffmpeg.nodes import FilterableStream

VideoStream = FilterableStream
AudioStream = FilterableStream

OutputFilePath = Path

Preprocessor = Callable[[VideoStream, AudioStream], Awaitable[tuple[VideoStream, AudioStream]]]
Job = Callable[[VideoStream, AudioStream, OutputFilePath], Awaitable[None]]
Postprocessor = Callable[[OutputFilePath], Awaitable[None]]
