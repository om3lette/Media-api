from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers import HelpersHandler, GigachatHelper
from src.api.common.types.request import RequestType
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.summarize import SummarizeConfig
from src.pipeline.base_task import BaseTask
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.tasks.jobs import TranscribeTask
from src.pipeline.tasks.postprocessors.base_postprocessor import BasePostprocessor
from src.pipeline.tasks.utils import extract_config_by_field_name
from src.pipeline.types import RenderConfig


class SummarizeTask(BasePostprocessor):
    request_type: RequestType = VideoRequestType.SUMMARIZE
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
        await gigachat_helper.summarize(config, paths.transcription_path)
