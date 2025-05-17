from src.pipeline.BaseTask import BaseTask
from src.pipeline.enums import TaskType


class BasePostprocessor(BaseTask):
    type: TaskType = TaskType.POSTPROCESSOR
