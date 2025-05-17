from dataclasses import dataclass

from ffmpeg.nodes import FilterableStream


@dataclass
class StreamsSchema:
    video: FilterableStream
    audio: FilterableStream
