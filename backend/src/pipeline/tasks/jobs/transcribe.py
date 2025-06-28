import asyncio

from backend.src.api.common.enums import RequestHelpersNames
from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.api.common.request_helpers.transcription_helper import TranscriptionHelper
from backend.src.api.common.schemas.requests.transcribe import TranscribeConfig
from backend.src.api.common.types.request import CustomRequestActions, GeneralRequestType
from backend.src.pipeline.base_task import BaseTask
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.tasks.jobs.base_job import BaseJob
from backend.src.pipeline.tasks.jobs.extract_audio import ExtractAudioTask
from backend.src.pipeline.tasks.utils import extract_config_by_field_name
from backend.src.pipeline.types import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb


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
