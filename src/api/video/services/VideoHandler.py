import os
import logging
import shutil
from pathlib import Path
from typing import Optional

from src.api.video.enums import VideoRequestType, VideoProcessCodes, FileRetrievalCodes
from src.api.video.services.YaDiskHelper import YaDiskHelper
from src.api.video.utils import out_path_from_request_id, input_path_from_request_id, audio_path_from_request_id, \
    transcription_path_from_request_id
from src.app_config import app_config
from src.pipeline.render import RendererBuilder, Renderer
from src.pipeline.ffmpeg_utils import jobs, preprocessors, postprocessors

from src.api.video.schemas import VideoRequest
from src.api.video.services.RequestQueue import RequestQueue
from src.pipeline.transcription.Transcriber import Transcriber

logger = logging.getLogger(os.path.basename(__file__))

class VideoRequestsHandler:
    current_request_id: str = ""
    def __init__(self, ya_disk_helper: YaDiskHelper, audio_helper: Transcriber):
        self.queue: RequestQueue = RequestQueue()
        self.ya_disk_helper = ya_disk_helper
        self.audio_helper = audio_helper

    async def add_request(self, request: VideoRequest, request_type: VideoRequestType) -> VideoProcessCodes:
        if self.queue.exists(request.get_video_id()):
            return VideoProcessCodes.ALREADY_QUEUED
        request_id: str = request.get_video_id()
        out_path: Path = out_path_from_request_id(request_id)

        if app_config.dev_mode and out_path.parent.is_dir():
            shutil.rmtree(out_path.parent)

        if request_type == VideoRequestType.COMPRESS and out_path.is_file():
            return VideoProcessCodes.ALREADY_PROCESSED

        audio_path: Path = audio_path_from_request_id(request_id)
        transcription_path: Path = transcription_path_from_request_id(request_id)
        if request_type == VideoRequestType.COMPRESS_AND_TRANSCRIBE and \
                out_path.is_file() and \
                audio_path.is_file() and \
                transcription_path.is_file():
            return VideoProcessCodes.ALREADY_PROCESSED
        logger.info(f"Queued request: {request.get_video_id()}")
        success = await self.queue.push(request, request_type, request.get_video_id())
        return VideoProcessCodes.OK if success else VideoProcessCodes.QUEUE_FULL

    async def start(self):
        logger.info(f"Startup completed")
        while True:
            req, req_type, req_id = await self.queue.pop()
            self.current_request_id = req_id
            try:
                await self._process_video(req, req_type)
            except Exception as e:
                logger.error(f"Error occurred when processing video:\n{e}")
            self.current_request_id = ""
            self.queue.task_done()

    def _build_renderer(self, request_id: str, request_type: VideoRequestType, file_path: Path) -> Optional[Renderer]:
        # TODO: Rewrite as a chain of responsibility
        if request_type == VideoRequestType.COMPRESS:
            return (
                RendererBuilder().use_file(str(file_path))
                    .add_job(jobs.preflight)
                    .add_job(jobs.compress)
                    .build()
            )
        if request_type == VideoRequestType.COMPRESS_AND_TRANSCRIBE:
            return (
                RendererBuilder().use_file(str(file_path))
                    .add_preprocessor(preprocessors.normalize)
                    .add_job(jobs.preflight)
                    .add_job(jobs.compress)
                    .add_postprocessor(postprocessors.extract_audio)
                    .add_postprocessor(
                        lambda x: self.audio_helper.transcribe(
                            audio_path_from_request_id(request_id)
                        )
                    )
                    .build()
            )
        return None

    async def _process_video(self, request: VideoRequest, request_type: VideoRequestType) -> VideoProcessCodes:
        request_id: str = request.get_video_id()
        logger.info(f"Starting to process request: {request_id}")
        raw_file_path: Path = input_path_from_request_id(request_id)

        os.makedirs(raw_file_path.parent, exist_ok=True)
        # Recreate the request folder
        out_dir: Path = out_path_from_request_id(request_id).parent
        if out_dir.is_dir():
            shutil.rmtree(out_dir)
        os.makedirs(out_dir)

        if not raw_file_path.is_file():
            return_code: FileRetrievalCodes = await self.ya_disk_helper.get_file_by_url(request.video_url, raw_file_path)
            if return_code == FileRetrievalCodes.NOT_FOUND:
               return VideoProcessCodes.FILE_NOT_FOUND
        logger.info(f"Raw file retrieved")
        renderer: Renderer = self._build_renderer(request_id, request_type, raw_file_path)
        logger.info(f"Renderer created")
        if renderer is None:
            return VideoProcessCodes.UNKNOWN_ERROR

        logger.info(f"Starting the renderer")
        renderer.run(out_path_from_request_id(request_id))
        logger.info(f"Task done: {request_id}")
        return VideoProcessCodes.OK
