from pathlib import Path

from src.api.common.services.base_handler import BaseHandler
from src.api.common.types.request import RequestType
from src.api.video.enums import VideoRequestType
from src.pipeline.render import Renderer, RendererBuilder
from src.pipeline.tasks import postprocessors


class SummarizeHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.SUMMARIZE)

    def _build_renderer(
        self, actions: list[RequestType], raw_file_path: Path
    ) -> Renderer:
        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_task(postprocessors.SummarizeTask())
        ).build()
