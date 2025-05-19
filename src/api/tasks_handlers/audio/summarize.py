from pathlib import Path

from src.api.common.enums import FileType
from src.api.common.services.base_handler import BaseHandler
from src.api.common.types.request import RequestType, GeneralRequestType
from src.pipeline.render import Renderer, RendererBuilder
from src.pipeline.tasks import postprocessors, jobs


class SummarizeAudioHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.SUMMARIZE, [FileType.AUDIO])

    def _build_renderer(
        self, actions: list[RequestType], raw_file_path: Path
    ) -> Renderer:
        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_task(
                postprocessors.SummarizeTask(
                    dependencies=[jobs.TranscribeTask(dependencies=[])]
                )
            )
        ).build()
