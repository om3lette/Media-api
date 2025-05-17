from pathlib import Path

from src.api.common.types.request import RequestType
from src.pipeline.render import RendererBuilder, Renderer
from src.api.common.services.BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType

from src.pipeline.tasks import jobs, postprocessors


class CustomHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.CUSTOM)

    def _build_renderer(
        self, actions: list[RequestType], raw_file_path: Path
    ) -> Renderer:
        render_builder: RendererBuilder = RendererBuilder().use_file(str(raw_file_path))

        if VideoRequestType.SUMMARIZE in actions:
            render_builder.add_task(postprocessors.SummarizeTask())

        if VideoRequestType.TRANSCRIBE in actions:
            render_builder.add_task(jobs.TranscribeTask())

        if VideoRequestType.EXTRACT_AUDIO in actions:
            render_builder.add_task(jobs.ExtractAudioTask())

        if VideoRequestType.COMPRESS in actions:
            render_builder.add_task(jobs.TwoPassEncodingTask())

        return render_builder.build()
