from pathlib import Path

from src.api.common.enums import FileType
from src.api.common.services.base_handler import BaseHandler
from src.api.common.types.request import GeneralRequestType
from src.api.tasks_handlers.enums import TextActions
from src.pipeline.render import Renderer, RendererBuilder
from src.pipeline.tasks.postprocessors import SummarizeTask


class CustomTextHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.CUSTOM, [FileType.TEXT])

    def _build_renderer(
        self, actions: list[TextActions], raw_file_path: Path
    ) -> Renderer:
        render_builder: RendererBuilder = RendererBuilder().use_file(str(raw_file_path))

        if TextActions.SUMMARIZE in actions:
            render_builder.add_task(SummarizeTask(dependencies=[]))

        return render_builder.build()
