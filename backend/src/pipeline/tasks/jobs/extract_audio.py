import ffmpeg

from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.api.common.schemas.requests import ExtractAudioConfig
from backend.src.api.common.types.request import (
    CustomRequestActions,
    GeneralRequestType,
)
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.tasks.jobs.base_job import BaseJob
from backend.src.pipeline.tasks.utils import extract_config_by_field_name, ffmpeg_run
from backend.src.pipeline.types import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb


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
        update_progress: UpdateProgressCb,
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
        await ffmpeg_run(paths.raw_path, output, update_progress)
