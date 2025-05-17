from pathlib import Path
from typing import Type

import ffmpeg

from src.pipeline.schemas.Streams import StreamsSchema
from src.pipeline.types import RenderConfig


def get_streams_from_file(file_path: Path) -> StreamsSchema:
    ffmpeg_input = ffmpeg.input(file_path)
    return StreamsSchema(video=ffmpeg_input.video, audio=ffmpeg_input.audio)


def extract_config_by_field_name(
    extract_from: RenderConfig, field_name: str, config_type: Type[RenderConfig]
) -> RenderConfig:
    if isinstance(extract_from, config_type):
        return extract_from
    if field_name in extract_from.model_fields:
        return getattr(extract_from, field_name)
    return config_type()
