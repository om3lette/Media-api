from pathlib import Path

from src import Renderer, RendererBuilder
from src.api.common.enums import RequestHelpersNames
from src.api.common.request_helpers.GigachatHelper import GigachatHelper
from src.api.common.request_helpers.HelpersHandler import HelpersHandler
from src.api.common.request_helpers import TranscriptionHelper
from src.api.common.services.BaseHandler import BaseHandler
from src.api.video.enums import VideoRequestType
from src.api.video.schemas import CustomSchema
from src.api.video.schemas.requests.Custom import CustomConfig
from src.api.video.schemas.requests.ExtractAudio import ExtractAudioConfig
from src.api.video.schemas.requests.Summarize import SummarizeConfig

from src.pipeline.ffmpeg_utils import jobs, preprocessors, postprocessors
from src.api.common.utils import (
    audio_path_from_request_id,
    transcription_path_from_request_id,
    get_audio_filename,
)


class CustomHandler(BaseHandler):
    def __init__(self):
        super().__init__(VideoRequestType.CUSTOM)

    def _build_renderer(
        self,
        request: CustomSchema,
        helpers: HelpersHandler,
        request_id: str,
        raw_file_path: Path,
    ) -> Renderer:
        transcription_helper: TranscriptionHelper = helpers.get_helper_by_name(
            RequestHelpersNames.TRANSCRIPTION
        )
        gigachat_helper: GigachatHelper = helpers.get_helper_by_name(
            RequestHelpersNames.GIGACHAT
        )

        async def transcribe(config: CustomConfig, *args):
            transcription_helper.transcribe(
                config.transcribe, audio_path_from_request_id(request_id)
            )

        async def summarize(config: CustomConfig, *args):
            await gigachat_helper.summarize(
                SummarizeConfig(summary=config.summary),
                transcription_path_from_request_id(request_id),
            )

        async def extract_audio(config: CustomConfig, req_data_dir, req_out_dir):
            # TODO: Remove hardcode out.mp4
            await postprocessors.extract_audio(
                ExtractAudioConfig(audio=config.audio),
                req_data_dir / "raw.mp4",
                req_out_dir / get_audio_filename(),
            )

        async def normalize(config: CustomConfig, *args):
            return await preprocessors.normalize(config.ffmpeg, *args)

        async def two_pass_encoding(config: CustomConfig, *args):
            return await jobs.two_pass_encoding(config.ffmpeg, *args)

        render_builder: RendererBuilder = RendererBuilder().use_file(str(raw_file_path))

        # TODO: Build a proper dependency system?
        if VideoRequestType.COMPRESS in request.actions:
            render_builder.add_preprocessor(normalize).add_job(two_pass_encoding)

        if VideoRequestType.EXTRACT_AUDIO in request.actions:
            render_builder.add_postprocessor(extract_audio)

        if VideoRequestType.TRANSCRIBE in request.actions:
            render_builder.add_postprocessor(extract_audio).add_postprocessor(
                transcribe
            )

        if VideoRequestType.SUMMARIZE in request.actions:
            render_builder.add_postprocessor(extract_audio).add_postprocessor(
                transcribe
            ).add_postprocessor(summarize)

        return render_builder.build()
