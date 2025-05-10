from typing import Self
from pathlib import Path

from src.constants import DATA_FOLDER
from src.pipeline.types import Job, Preprocessor, Postprocessor
from src.pipeline.render import Renderer


class RendererBuilder:
    def __init__(self):
        self._renderer: Renderer = Renderer(Path(), [], [], [])

    def use_file(self, file_name: str) -> Self:
        self._renderer.file_path = DATA_FOLDER / file_name
        return self

    def add_preprocessor(self, preprocessor: Preprocessor) -> Self:
        self._renderer.preprocessors.append(preprocessor)
        return self

    def add_job(self, job: Job) -> Self:
        self._renderer.jobs.append(job)
        return self

    def add_postprocessor(self, postprocessor: Postprocessor) -> Self:
        self._renderer.postprocessors.append(postprocessor)
        return self

    def build(self) -> Renderer:
        if (
            len(self._renderer.jobs)
            + len(self._renderer.preprocessors)
            + len(self._renderer.postprocessors)
            == 0
        ):
            raise RuntimeError("No jobs were registered for renderer")
        return self._renderer
