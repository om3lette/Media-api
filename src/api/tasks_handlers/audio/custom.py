from pathlib import Path

from src.api.common.enums import FileType
from src.api.common.services.base_handler import BaseHandler
from src.api.common.types.request import GeneralRequestType
from src.api.tasks_handlers.audio.adjusted_tasks import (
    audio_summarize_task,
    audio_transcribe_task,
)
from src.api.tasks_handlers.enums import AudioActions
from src.pipeline.render import Renderer, RendererBuilder
from src.pipeline.tasks import jobs


class CustomAudioHandler(BaseHandler):
    def __init__(self):
        super().__init__(GeneralRequestType.CUSTOM, [FileType.AUDIO])

    def _build_renderer(
        self, actions: list[AudioActions], raw_file_path: Path
    ) -> Renderer:
        render_builder: RendererBuilder = RendererBuilder().use_file(str(raw_file_path))

        if AudioActions.SUMMARIZE in actions:
            render_builder.add_task(audio_summarize_task)

        if AudioActions.TRANSCRIBE in actions:
            render_builder.add_task(audio_transcribe_task)

        if AudioActions.EXTRACT_AUDIO in actions:
            render_builder.add_task(jobs.ExtractAudioTask())

        return render_builder.build()
