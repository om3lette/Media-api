from src.pipeline.base_task import BaseTask
from src.pipeline.enums import TaskType


class BaseJob(BaseTask):
    type: TaskType = TaskType.JOB
