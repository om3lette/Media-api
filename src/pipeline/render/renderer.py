from dataclasses import dataclass
from pathlib import Path

from src.api.common.request_helpers import HelpersHandler
from src.pipeline.schemas.paths import PathsSchema
from src.pipeline.schemas.streams import StreamsSchema
from src.pipeline.schemas.task_wrapper import TaskWrapper
from src.pipeline.tasks.utils import get_streams_from_file
from src.pipeline.types import RenderConfig
from src.utils import get_logger_from_filepath

logger = get_logger_from_filepath(__file__)


@dataclass
class Renderer:
    file_path: Path
    preprocessors: list[TaskWrapper]
    jobs: list[TaskWrapper]
    postprocessors: list[TaskWrapper]

    @staticmethod
    def __get_task_name(task: TaskWrapper) -> str:
        return task.execute.__qualname__.split(".")[0]

    async def run(
        self, config: RenderConfig, helpers: HelpersHandler, paths: PathsSchema
    ) -> bool:
        if not self.file_path.is_file():
            raise RuntimeError(
                f"Incorrect file path provided for renderer: {self.file_path}"
            )
        streams: StreamsSchema = get_streams_from_file(self.file_path)

        for p in self.preprocessors:
            logger.info("Running preprocessor: %s", self.__get_task_name(p))
            streams: StreamsSchema = await p.execute(
                p.extract_config(config), helpers, streams, paths
            )

        for j in self.jobs:
            logger.info("Running job: %s", self.__get_task_name(j))
            await j.execute(j.extract_config(config), helpers, streams, paths)

        for p in self.postprocessors:
            logger.info("Running postprocessor: %s", self.__get_task_name(p))
            await p.execute(p.extract_config(config), helpers, streams, paths)

        return True
