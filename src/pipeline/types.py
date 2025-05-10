from pathlib import Path
from typing import Callable, Awaitable
from ffmpeg.nodes import FilterableStream
from pydantic import BaseModel

from src.config.schemas.BaseEnumModel import BaseEnumModel

VideoStream = FilterableStream
AudioStream = FilterableStream
RenderConfig = BaseModel | BaseEnumModel

OutputFilePath = Path

RequestDataDir = Path
RequestOutDir = Path

Preprocessor = Callable[
    [RenderConfig, VideoStream, AudioStream], Awaitable[tuple[VideoStream, AudioStream]]
]
Job = Callable[
    [RenderConfig, VideoStream, AudioStream, OutputFilePath], Awaitable[None]
]
Postprocessor = Callable[[RenderConfig, RequestDataDir, RequestOutDir], Awaitable[None]]
