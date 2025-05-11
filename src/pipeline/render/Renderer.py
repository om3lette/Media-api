from dataclasses import dataclass
from pathlib import Path

from src.pipeline.ffmpeg_utils.utils import get_streams_from_file
from src.pipeline.types import (
    Job,
    Preprocessor,
    Postprocessor,
    RequestDataDir,
    RequestOutDir,
    RenderConfig,
)
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


@dataclass
class Renderer:
    file_path: Path
    preprocessors: list[Preprocessor]
    jobs: list[Job]
    postprocessors: list[Postprocessor]

    async def run(
        self,
        config: RenderConfig,
        data_dir: RequestDataDir,
        out_dir: RequestOutDir,
        save_path: Path,
    ) -> bool:
        if not self.file_path.is_file():
            raise RuntimeError(
                f"Incorrect file path provided for renderer: {self.file_path}"
            )
        video_stream, audio_stream = get_streams_from_file(self.file_path)

        for preprocessor in self.preprocessors:
            logger.info(f"Running preprocessor: {preprocessor.__name__}")
            video_stream, audio_stream = await preprocessor(
                config, video_stream, audio_stream
            )

        for job in self.jobs:
            logger.info(f"Running job: {job.__name__}")
            await job(config, video_stream, audio_stream, save_path)

        for postprocessor in self.postprocessors:
            logger.info(f"Running postprocessor: {postprocessor.__name__}")
            await postprocessor(config, data_dir, out_dir)

        return True
