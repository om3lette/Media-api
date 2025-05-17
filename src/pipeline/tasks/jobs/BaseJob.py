from src.pipeline.BaseTask import BaseTask
from src.pipeline.enums import TaskType


class BaseJob(BaseTask):
    type: TaskType = TaskType.JOB
