from pathlib import Path
from typing import Callable, Awaitable
from ffmpeg.nodes import FilterableStream

VideoStream = FilterableStream
AudioStream = FilterableStream

OutputFilePath = Path

RequestDataDir = Path
RequestOutDir = Path

Preprocessor = Callable[[VideoStream, AudioStream], Awaitable[tuple[VideoStream, AudioStream]]]
Job = Callable[[VideoStream, AudioStream, OutputFilePath], Awaitable[None]]
Postprocessor = Callable[[RequestDataDir, RequestOutDir], Awaitable[None]]
