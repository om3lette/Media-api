import ffmpeg

from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.api.common.schemas.requests.compress import CompressConfig
from backend.src.api.common.types.request import CustomRequestActions, GeneralRequestType
from backend.src.constants import NULL_PATH, PASSLOG_PATH
from backend.src.pipeline.base_task import BaseTask
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.tasks import preprocessors
from backend.src.pipeline.tasks.jobs.base_job import BaseJob
from backend.src.pipeline.tasks.utils import extract_config_by_field_name, ffmpeg_run
from backend.src.pipeline.types import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb


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
        update_progress: UpdateProgressCb,
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
        await ffmpeg_run(paths.raw_path, output, update_progress)

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
        await ffmpeg_run(paths.raw_path, output, update_progress)
