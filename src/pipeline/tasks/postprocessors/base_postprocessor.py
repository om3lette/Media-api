from src.pipeline.base_task import BaseTask
from src.pipeline.enums import TaskType


class BasePostprocessor(BaseTask):
    type: TaskType = TaskType.POSTPROCESSOR
