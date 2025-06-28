from dataclasses import dataclass
from pathlib import Path

from backend.src.api.common.request_helpers.helpers_handler import HelpersHandler
from backend.src.pipeline.schemas.paths import PathsSchema
from backend.src.pipeline.schemas.streams import StreamsSchema
from backend.src.pipeline.schemas.task_wrapper import TaskWrapper
from backend.src.pipeline.tasks.utils import get_streams_from_file
from backend.src.pipeline.types import RenderConfig
from backend.src.pipeline.types.state_callbacks import UpdateStageCb, UpdateProgressCb
from backend.src.utils import get_logger_by_filepath

logger = get_logger_by_filepath(__file__)


@dataclass
class Renderer:
    file_path: Path
    preprocessors: list[TaskWrapper]
    jobs: list[TaskWrapper]
    postprocessors: list[TaskWrapper]

    @property
    def stages(self) -> int:
        # Preprocessors are not considered stages
        # as they are filters and don't produce output (files)
        return len(self.jobs) + len(self.postprocessors)

    @staticmethod
    def __get_task_name(task: TaskWrapper) -> str:
        return task.execute.__qualname__.split(".")[0]

    async def run(
        self,
        config: RenderConfig,
        helpers: HelpersHandler,
        paths: PathsSchema,
        update_stage: UpdateStageCb,
        update_progress: UpdateProgressCb,
    ) -> bool:
        current_stage = 0

        async def new_stage():
            nonlocal current_stage
            current_stage += 1
            await update_stage(current_stage)

        if not self.file_path.is_file():
            raise RuntimeError(
                f"Incorrect file path provided for renderer: {self.file_path}"
            )
        streams: StreamsSchema = get_streams_from_file(self.file_path)

        for p in self.preprocessors:
            logger.info("Running preprocessor: %s", self.__get_task_name(p))
            streams: StreamsSchema = await p.execute(
                p.extract_config(config), helpers, streams, paths, update_progress
            )

        for j in self.jobs:
            await new_stage()
            logger.info("Running job: %s", self.__get_task_name(j))
            await j.execute(
                j.extract_config(config), helpers, streams, paths, update_progress
            )

        for p in self.postprocessors:
            await new_stage()
            logger.info("Running postprocessor: %s", self.__get_task_name(p))
            await p.execute(
                p.extract_config(config), helpers, streams, paths, update_progress
            )

        return True
