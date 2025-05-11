from pathlib import Path

from src import Renderer, RendererBuilder
from src.api.common.request_helpers.HelpersHandler import HelpersHandler
from src.api.common.services.BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.pipeline.ffmpeg_utils import jobs, preprocessors


class CompressHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.COMPRESS)

    def _build_renderer(
        self, request, helpers: HelpersHandler, request_id: str, raw_file_path: Path
    ) -> Renderer:
        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_preprocessor(preprocessors.normalize)
            .add_job(jobs.two_pass_encoding)
            .build()
        )
