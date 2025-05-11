from pathlib import Path

from src import Renderer, RendererBuilder
from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers.HelpersHandler import HelpersHandler
from src.api.common.request_helpers import TranscriptionHelper
from src.api.common.services.BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.api.video.schemas.requests.ExtractAudio import ExtractAudioConfig
from src.api.video.schemas.requests.Transcribe import TranscribeConfig
from src.pipeline.ffmpeg_utils import postprocessors
from src.api.common.utils import audio_path_from_request_id, get_audio_filename


class TranscriptionHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.TRANSCRIBE)

    def _build_renderer(
        self, request, helpers: HelpersHandler, request_id: str, raw_file_path: Path
    ) -> Renderer:
        transcription_helper: TranscriptionHelper = helpers.get_helper_by_name(
            RequestHelpersNames.TRANSCRIPTION
        )

        async def transcribe(config: TranscribeConfig, *args):
            transcription_helper.transcribe(
                config, audio_path_from_request_id(request_id)
            )

        async def extract_audio(config: TranscribeConfig, req_data_dir, req_out_dir):
            await postprocessors.extract_audio(
                ExtractAudioConfig(), raw_file_path, req_out_dir / get_audio_filename()
            )

        return (
            RendererBuilder()
            .use_file(str(raw_file_path))
            .add_postprocessor(extract_audio)
            .add_postprocessor(transcribe)
        ).build()
