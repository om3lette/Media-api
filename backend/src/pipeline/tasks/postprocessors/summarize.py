from pathlib import Path

from backend.src.api.common.enums import RequestHelpersNames
from backend.src.api.common.request_helpers.gigachat_helper import GigachatHelper
from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.api.common.schemas.requests.summarize import SummarizeConfig
from backend.src.api.common.types.request import (
    CustomRequestActions,
    GeneralRequestType,
)
from backend.src.pipeline.base_task import BaseTask
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.tasks.jobs import TranscribeTask
from backend.src.pipeline.tasks.postprocessors.base_postprocessor import (
    BasePostprocessor,
)
from backend.src.pipeline.tasks.utils import extract_config_by_field_name
from backend.src.pipeline.types import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateProgressCb


class SummarizeTask(BasePostprocessor):
    request_type: CustomRequestActions = GeneralRequestType.SUMMARIZE
    dependencies: list[BaseTask] = [TranscribeTask()]

    @staticmethod
    def extract_config(full_config: RenderConfig) -> SummarizeConfig:
        return extract_config_by_field_name(full_config, "summary", SummarizeConfig)

    async def execute(
        self,
        config: SummarizeConfig,
        helpers: HelpersHandler,
        streams: StreamsSchema,
        paths: PathsSchema,
        update_progress: UpdateProgressCb,
    ):
        gigachat_helper: GigachatHelper = helpers.get_helper_by_name(
            RequestHelpersNames.GIGACHAT
        )
        transcription_path: Path = (
            paths.transcription_path
            if paths.transcription_path.is_file()
            else paths.raw_path
        )
        await gigachat_helper.summarize(config, transcription_path, paths.summary_path)
