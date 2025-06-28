from backend.src.pipeline.base_task import BaseTask
from backend.src.pipeline.enums import TaskType


class BaseJob(BaseTask):
    type: TaskType = TaskType.JOB
