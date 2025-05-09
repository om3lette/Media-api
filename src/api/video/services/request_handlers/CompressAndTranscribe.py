import logging
from pathlib import Path

from src import Renderer, RendererBuilder
from src.api.request_helpers.GigachatHelper import GigachatHelper
from src.api.request_helpers.HelpersHandler import HelpersHandler
from src.api.request_helpers.TranscriptionHelper import TranscriptionHelper
from .BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.pipeline.ffmpeg_utils import jobs, preprocessors, postprocessors
from src.api.video.utils import audio_path_from_request_id, transcription_path_from_request_id


class CompressAndTranscribeHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.COMPRESS_AND_TRANSCRIBE)

    def _build_renderer(self, helpers: HelpersHandler, request_id: str, raw_file_path: Path) -> Renderer:
        transcription_helper: TranscriptionHelper = helpers.get_helper_by_name("transcriber")
        gigachat_helper: GigachatHelper = helpers.get_helper_by_name("gigachat")
        async def transcribe(*args):
            transcription_helper.transcribe(
                audio_path_from_request_id(request_id)
            )
        async def summarize(*args):
            await gigachat_helper.summarize(transcription_path_from_request_id(request_id))
        return (
            RendererBuilder()
                .use_file(str(raw_file_path))
                .add_preprocessor(preprocessors.normalize)
                .add_job(jobs.preflight)
                .add_job(jobs.compress)
                .add_postprocessor(postprocessors.extract_audio)
                .add_postprocessor(transcribe)
                .add_postprocessor(summarize)
        ).build()
