import ffmpeg

from src.api.common.request_helpers import HelpersHandler
from src.api.common.types.request import RequestType
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.ExtractAudio import ExtractAudioConfig
from src.pipeline.schemas.Paths import PathsSchema
from src.pipeline.schemas.Streams import StreamsSchema
from src.pipeline.tasks.jobs.BaseJob import BaseJob
from src.pipeline.types import RenderConfig


class ExtractAudioTask(BaseJob):
    request_type: RequestType = VideoRequestType.EXTRACT_AUDIO

    @staticmethod
    def extract_config(full_config: RenderConfig) -> ExtractAudioConfig:
        if isinstance(full_config, ExtractAudioConfig):
            return full_config
        if "audio" in full_config.model_fields:
            return full_config.audio
        return ExtractAudioConfig()

    async def execute(
        self,
        config: ExtractAudioConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
    ):
        ffmpeg.output(
            streams.audio,
            filename=paths.audio_path,
            vn=None,
            acodec=config.audio.codec,
            loglevel="quiet",
            stats=None,
            y=None,
        ).run()
