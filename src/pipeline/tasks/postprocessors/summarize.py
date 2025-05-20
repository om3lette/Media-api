from pathlib import Path

from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers.gigachat_helper import GigachatHelper
from src.api.common.request_helpers.helpers_handler import HelpersHandler
from src.api.common.schemas.requests.summarize import SummarizeConfig
from src.api.common.types.request import CustomRequestActions, GeneralRequestType
from src.pipeline.base_task import BaseTask
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.jobs import TranscribeTask
from src.pipeline.tasks.postprocessors.base_postprocessor import BasePostprocessor
from src.pipeline.tasks.utils import extract_config_by_field_name
from src.pipeline.types import RenderConfig


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
