import ffmpeg

from src.api.common.request_helpers import HelpersHandler
from src.api.common.types.request import RequestType
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.ExtractAudio import ExtractAudioConfig
from src.pipeline.schemas.Paths import PathsSchema
from src.pipeline.schemas.Streams import StreamsSchema
from src.pipeline.tasks.jobs.BaseJob import BaseJob
from src.pipeline.tasks.utils import extract_config_by_field_name
from src.pipeline.types import RenderConfig


class ExtractAudioTask(BaseJob):
    request_type: RequestType = VideoRequestType.EXTRACT_AUDIO

    @staticmethod
    def extract_config(full_config: RenderConfig) -> ExtractAudioConfig:
        return extract_config_by_field_name(full_config, "audio", ExtractAudioConfig)

    async def execute(
        self,
        config: ExtractAudioConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
    ):
        # TODO: Construct audio path according to codec
        ffmpeg.output(
            streams.audio,
            filename=paths.audio_path,
            vn=None,
            acodec=config.audio.codec,
            audio_bitrate=f"{config.audio.bitrate}k",
            ar=config.audio.sample_rate,
            loglevel="warning",
            stats=None,
            y=None,
        ).run()
