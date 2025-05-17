import ffmpeg

from src.api.common.request_helpers import HelpersHandler
from src.api.common.types.request import RequestType
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.Compress import CompressConfig
from src.pipeline.BaseTask import BaseTask
from src.pipeline.schemas.Paths import PathsSchema
from src.pipeline.schemas.Streams import StreamsSchema
from src.pipeline.tasks import preprocessors
from src.pipeline.tasks.jobs.BaseJob import BaseJob
from src.constants import NULL_PATH, PASSLOG_PATH
from src.pipeline.types import RenderConfig


class TwoPassEncodingTask(BaseJob):
    request_type: RequestType = VideoRequestType.COMPRESS
    dependencies: list[BaseTask] = [preprocessors.NormalizeTask()]

    @staticmethod
    def extract_config(full_config: RenderConfig) -> CompressConfig:
        if isinstance(full_config, CompressConfig):
            return full_config
        if "ffmpeg" in full_config.model_fields:
            return full_config.ffmpeg
        return CompressConfig()

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
        ffmpeg.output(streams.video, str(NULL_PATH), **first_pass_params).run()

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
        ffmpeg.output(
            streams.video, streams.audio, str(paths.out_path), **second_pass_params
        ).run()
