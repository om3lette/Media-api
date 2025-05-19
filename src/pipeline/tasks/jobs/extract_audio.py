import ffmpeg

from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.types.request import CustomRequestActions, GeneralRequestType
from src.api.common.schemas.requests import ExtractAudioConfig
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.jobs.base_job import BaseJob
from src.pipeline.tasks.utils import extract_config_by_field_name, ffmpeg_run
from src.pipeline.types import RenderConfig


class ExtractAudioTask(BaseJob):
    request_type: CustomRequestActions = GeneralRequestType.EXTRACT_AUDIO

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
        output = ffmpeg.output(
            streams.audio,
            filename=str(paths.audio_path),
            vn=None,
            acodec=config.audio.codec,
            audio_bitrate=f"{config.audio.bitrate}k",
            ar=config.audio.sample_rate,
            y=None,
        )
        await ffmpeg_run(paths.raw_path, output)
