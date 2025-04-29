import ffmpeg

from dataclasses import dataclass
from pathlib import Path

from src.constants import OUT_FOLDER
from src.pipeline.types import FfmpegJob, FfmpegPreprocessor

@dataclass
class Renderer:
    file_path: Path
    preprocessors: list[FfmpegPreprocessor]
    jobs: list[FfmpegJob]

    def run(self, save_path: Path) -> bool:
        if not self.file_path.is_file():
            raise RuntimeError(f"Incorrect file path provided for renderer: {self.file_path}")
        ffmpeg_input = ffmpeg.input(self.file_path)
        video_stream, audio_stream = ffmpeg_input.video, ffmpeg_input.audio

        for preprocessor in self.preprocessors:
            preprocessor(video_stream, audio_stream)

        for job in self.jobs:
            job(video_stream, audio_stream, save_path)
        return True