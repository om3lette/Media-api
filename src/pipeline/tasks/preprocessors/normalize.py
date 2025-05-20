from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.schemas.requests.compress import CompressConfig
from src.api.common.types.request import CustomRequestActions
from src.api.tasks_handlers.enums import VideoRequestType
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.preprocessors.base_preprocessor import BasePreprocessor
from src.pipeline.tasks.utils import extract_config_by_field_name
from src.pipeline.types import AudioStream, RenderConfig, VideoStream


class NormalizeTask(BasePreprocessor):
    request_type: CustomRequestActions = VideoRequestType.UTILITY

    @staticmethod
    def extract_config(full_config: RenderConfig) -> CompressConfig:
        return extract_config_by_field_name(full_config, "ffmpeg", CompressConfig)

    async def execute(
        self,
        config: CompressConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
    ) -> StreamsSchema:
        filtered_video: VideoStream = streams.video.filter(
            "scale", config.video.width, config.video.height, flags="lanczos"
        ).filter("fps", config.video.fps)
        normalized_audio: AudioStream = streams.audio.filter(
            "loudnorm", i="-16", lra="11", tp="-1.5"
        )
        return StreamsSchema(video=filtered_video, audio=normalized_audio)
