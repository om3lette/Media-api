from pathlib import Path

from backend.src.api.common.enums import FileType
from backend.src.api.common.services.base_handler import BaseHandler
from backend.src.api.common.types.request import (
    CustomRequestActions,
    GeneralRequestType,
)
from backend.src.pipeline.render import Renderer, RendererBuilder
from backend.src.pipeline.tasks import jobs


class CompressVideoHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.COMPRESS, [FileType.VIDEO])

    def _build_renderer(
        self, actions: list[CustomRequestActions], raw_file_path: Path
    ) -> Renderer:
        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_task(jobs.TwoPassEncodingTask())
            .build()
        )
