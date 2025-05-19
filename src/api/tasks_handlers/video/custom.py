from pathlib import Path

from src.api.common.enums import FileType
from src.api.common.types.request import GeneralRequestType
from src.pipeline.render import RendererBuilder, Renderer
from src.api.common.services.base_handler import BaseHandler
from src.api.tasks_handlers.enums import VideoActions

from src.pipeline.tasks import jobs, postprocessors


class CustomVideoHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.CUSTOM, [FileType.VIDEO])

    def _build_renderer(
        self, actions: list[VideoActions], raw_file_path: Path
    ) -> Renderer:
        render_builder: RendererBuilder = RendererBuilder().use_file(str(raw_file_path))

        if VideoActions.SUMMARIZE in actions:
            render_builder.add_task(postprocessors.SummarizeTask())

        if VideoActions.TRANSCRIBE in actions:
            render_builder.add_task(jobs.TranscribeTask())

        if VideoActions.EXTRACT_AUDIO in actions:
            render_builder.add_task(jobs.ExtractAudioTask())

        if VideoActions.COMPRESS in actions:
            render_builder.add_task(jobs.TwoPassEncodingTask())

        return render_builder.build()
