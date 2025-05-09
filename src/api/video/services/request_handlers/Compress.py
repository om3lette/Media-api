from pathlib import Path

from src import Renderer, RendererBuilder
from src.api.request_helpers.HelpersHandler import HelpersHandler
from .BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.pipeline.ffmpeg_utils import jobs, preprocessors, postprocessors


class CompressHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.COMPRESS)

    def _build_renderer(self, helpers: HelpersHandler, request_id: str, raw_file_path: Path) -> Renderer:
        return (
            RendererBuilder().use_file(str(raw_file_path))
            .add_job(jobs.preflight)
            .add_job(jobs.compress)
            .build()
        )
