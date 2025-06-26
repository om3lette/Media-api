import asyncio

from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.request_helpers.transcription_helper import TranscriptionHelper
from src.api.common.schemas.requests.transcribe import TranscribeConfig
from src.api.common.types.request import CustomRequestActions, GeneralRequestType
from src.pipeline.base_task import BaseTask
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.jobs.base_job import BaseJob
from src.pipeline.tasks.jobs.extract_audio import ExtractAudioTask
from src.pipeline.tasks.utils import extract_config_by_field_name
from src.pipeline.types import RenderConfig
from src.pipeline.types.state_callbacks import UpdateProgressCb


class TranscribeTask(BaseJob):
    request_type: CustomRequestActions = GeneralRequestType.TRANSCRIBE
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
        update_progress: UpdateProgressCb,
    ):
        transcription_helper: TranscriptionHelper = helpers.get_helper_by_name(
            RequestHelpersNames.TRANSCRIPTION
        )
        await asyncio.to_thread(
            lambda: transcription_helper.transcribe(
                config,
                paths.audio_path if paths.audio_path.is_file() else paths.raw_path,
                paths.transcription_path,
            )
        )
