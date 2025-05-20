from pathlib import Path

from src.api.common.enums import FileType
from src.api.common.services.base_handler import BaseHandler
from src.api.common.types.request import GeneralRequestType
from src.api.tasks_handlers.enums import ImageActions
from src.pipeline.render import Renderer, RendererBuilder
from src.pipeline.tasks import jobs


class CustomImageHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.CUSTOM, [FileType.IMAGE])

    def _build_renderer(
        self, actions: list[ImageActions], raw_file_path: Path
    ) -> Renderer:
        render_builder: RendererBuilder = RendererBuilder().use_file(str(raw_file_path))

        if ImageActions.TO_TEXT in actions:
            render_builder.add_task(jobs.ImageToTextTask())

        return render_builder.build()
