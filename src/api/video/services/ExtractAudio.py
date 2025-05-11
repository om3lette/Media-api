from pathlib import Path

from src import Renderer, RendererBuilder
from src.api.common.utils import get_audio_filename
from src.api.common.request_helpers.HelpersHandler import HelpersHandler
from src.api.common.services.BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.ExtractAudio import ExtractAudioConfig
from src.pipeline.ffmpeg_utils import postprocessors


class ExtractAudioHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.EXTRACT_AUDIO)

    def _build_renderer(
        self, helpers: HelpersHandler, request_id: str, raw_file_path: Path
    ) -> Renderer:
        async def extract_audio(config: ExtractAudioConfig, req_data_dir, req_out_dir):
            await postprocessors.extract_audio(
                config, raw_file_path, req_out_dir / get_audio_filename()
            )

        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_postprocessor(extract_audio)
        ).build()
