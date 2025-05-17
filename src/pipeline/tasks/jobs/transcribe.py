from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers import HelpersHandler, TranscriptionHelper
from src.api.common.types.request import RequestType
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.transcribe import TranscribeConfig
from src.pipeline.base_task import BaseTask
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.jobs.extract_audio import ExtractAudioTask
from src.pipeline.tasks.jobs.base_job import BaseJob
from src.pipeline.tasks.utils import extract_config_by_field_name
from src.pipeline.types import RenderConfig


class TranscribeTask(BaseJob):
    request_type: RequestType = VideoRequestType.TRANSCRIBE
    dependencies: list[BaseTask] = [ExtractAudioTask()]

    @staticmethod
    def extract_config(full_config: RenderConfig) -> TranscribeConfig:
        return extract_config_by_field_name(full_config, "transcribe", TranscribeConfig)

    async def execute(
        self,
        config: TranscribeConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
    ):
        transcription_helper: TranscriptionHelper = helpers.get_helper_by_name(
            RequestHelpersNames.TRANSCRIPTION
        )
        transcription_helper.transcribe(config, paths.audio_path)
