import asyncio

from backend.src.api.common.enums import RequestHelpersNames
from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.api.common.request_helpers.tesseract_helper import TesseractHelper
from backend.src.api.common.schemas.requests import FileToTextConfig
from backend.src.api.common.types.request import CustomRequestActions, GeneralRequestType
from backend.src.pipeline.base_task import BaseTask
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.tasks.jobs.base_job import BaseJob
from backend.src.pipeline.tasks.utils import extract_config_by_field_name
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb


class ImageToTextTask(BaseJob):
    request_type: CustomRequestActions = GeneralRequestType.TRANSCRIBE
    dependencies: list[BaseTask] = []

    @staticmethod
    def extract_config(full_config: FileToTextConfig) -> FileToTextConfig:
        return extract_config_by_field_name(
            full_config, "file_to_text", FileToTextConfig
        )

    async def execute(
        self,
        config: FileToTextConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
        update_progress: UpdateProgressCb,
    ):
        tesseract_helper: TesseractHelper = helpers.get_helper_by_name(
            RequestHelpersNames.TESSERACT
        )
        await asyncio.to_thread(
            lambda: tesseract_helper.image_to_text(
                config, paths.raw_path, paths.transcription_path
            )
        )
