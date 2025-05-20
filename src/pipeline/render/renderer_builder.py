from pathlib import Path
from typing import Self

from src.constants import DATA_FOLDER
from src.pipeline.base_task import BaseTask
from src.pipeline.enums import TaskType
from src.pipeline.render.renderer import Renderer
from src.pipeline.schemas.task_wrapper import TaskWrapper
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


class RendererBuilder:
    def __init__(self):
        self.__renderer: Renderer = Renderer(Path(), [], [], [])
        self.__seen_tasks: set[BaseTask] = set()

    def __register_task(self, task: BaseTask):
        container: list = self.__renderer.preprocessors
        if task.type == TaskType.JOB:
            container = self.__renderer.jobs
        elif task.type == TaskType.POSTPROCESSOR:
            container = self.__renderer.postprocessors
        elif task.type != TaskType.PREPROCESSOR:
            raise NotImplementedError(f"Task type {task.type} is not supported")
        container.append(
            TaskWrapper(execute=task.execute, extract_config=task.extract_config)
        )

    def add_task(self, task: BaseTask) -> Self:
        def collect(to_collect: BaseTask):
            if to_collect in self.__seen_tasks:
                return
            logger.info("Added task: %s to Renderer", to_collect.__class__.__name__)
            self.__seen_tasks.add(to_collect)

            for d in to_collect.dependencies:
                collect(d)

            self.__register_task(to_collect)

        collect(task)
        return self

    def use_file(self, file_name: str) -> Self:
        self.__renderer.file_path = DATA_FOLDER / file_name
        return self

    def build(self) -> Renderer:
        if (
            len(self.__renderer.jobs)
            + len(self.__renderer.preprocessors)
            + len(self.__renderer.postprocessors)
            == 0
        ):
            raise RuntimeError("No jobs were registered for renderer")
        return self.__renderer
