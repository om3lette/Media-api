from pathlib import Path

from src.api.common.types.request import RequestType
from src.pipeline.render import RendererBuilder, Renderer
from src.api.common.services.BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.pipeline.tasks import jobs


class CompressHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.COMPRESS)

    def _build_renderer(
        self, actions: list[RequestType], raw_file_path: Path
    ) -> Renderer:
        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_task(jobs.TwoPassEncodingTask())
            .build()
        )
