import ffmpeg

from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.types.request import CustomRequestActions, GeneralRequestType
from src.api.common.schemas.requests.compress import CompressConfig
from src.pipeline.base_task import BaseTask
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks import preprocessors
from src.pipeline.tasks.jobs.base_job import BaseJob
from src.constants import NULL_PATH, PASSLOG_PATH
from src.pipeline.tasks.utils import extract_config_by_field_name, ffmpeg_run
from src.pipeline.types import RenderConfig


class TwoPassEncodingTask(BaseJob):
    request_type: CustomRequestActions = GeneralRequestType.COMPRESS
    dependencies: list[BaseTask] = [preprocessors.NormalizeTask()]

    @staticmethod
    def extract_config(full_config: RenderConfig) -> CompressConfig:
        return extract_config_by_field_name(full_config, "ffmpeg", CompressConfig)

    async def execute(
        self,
        config: CompressConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
    ):
        first_pass_params = {
            "vcodec": config.codecs.video,
            "preset": config.preset,
            "video_bitrate": f"{config.video.video_bitrate}k",
            "pass": 1,
            "passlogfile": PASSLOG_PATH,
            "f": "mp4",
            "an": None,
            "y": None,
        }
        output = ffmpeg.output(streams.video, str(NULL_PATH), **first_pass_params)
        await ffmpeg_run(paths.raw_path, output)

        second_pass_params = {
            "vcodec": config.codecs.video,
            "preset": config.preset,
            "video_bitrate": f"{config.video.video_bitrate}k",
            "acodec": config.codecs.audio,
            "audio_bitrate": f"{config.video.audio_bitrate}k",
            "ar": config.video.audio_sample_rate,
            "pass": 2,
            "passlogfile": PASSLOG_PATH,
            "y": None,
        }
        output = ffmpeg.output(
            streams.video, streams.audio, str(paths.out_path), **second_pass_params
        )
        await ffmpeg_run(paths.raw_path, output)
