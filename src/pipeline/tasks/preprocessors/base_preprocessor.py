from src.pipeline.base_task import BaseTask
from src.pipeline.enums import TaskType


class BasePreprocessor(BaseTask):
    type: TaskType = TaskType.PREPROCESSOR
