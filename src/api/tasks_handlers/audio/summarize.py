from pathlib import Path

from src.api.common.enums import FileType
from src.api.common.services.base_handler import BaseHandler
from src.api.common.types.request import CustomRequestActions, GeneralRequestType
from src.api.tasks_handlers.audio.adjusted_tasks import audio_summarize_task
from src.pipeline.render import Renderer, RendererBuilder


class SummarizeAudioHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.SUMMARIZE, [FileType.AUDIO])

    def _build_renderer(
        self, actions: list[CustomRequestActions], raw_file_path: Path
    ) -> Renderer:
        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_task(audio_summarize_task)
        ).build()
